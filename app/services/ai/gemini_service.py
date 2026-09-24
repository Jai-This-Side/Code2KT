import os
import time
from typing import Callable, Optional

from dotenv import load_dotenv
from google import genai
from openai import OpenAI

from app.services.aws_secrets import load_production_secrets


load_dotenv()


class GeminiService:
    """
    Multi-provider AI service.

    Provider priority:
    1. Gemini
    2. Groq
    3. OpenRouter
    """

    def __init__(self):
        # Production: load credentials from AWS Secrets Manager.
        # Local development: fall back to values from .env.
        production_secrets = load_production_secrets()

        for key, value in production_secrets.items():
            os.environ[key] = value

        # ==================================================
        # GEMINI
        # ==================================================

        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash",
        )

        self.gemini_client = None

        if self.gemini_api_key:
            self.gemini_client = genai.Client(
                api_key=self.gemini_api_key
            )

        # ==================================================
        # GROQ
        # ==================================================

        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b",
        )

        self.groq_client = None

        if self.groq_api_key:
            self.groq_client = OpenAI(
                api_key=self.groq_api_key,
                base_url="https://api.groq.com/openai/v1",
            )

        # ==================================================
        # OPENROUTER
        # ==================================================

        self.openrouter_api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

        self.openrouter_model = os.getenv(
            "OPENROUTER_MODEL",
            "openrouter/free",
        )

        self.openrouter_client = None

        if self.openrouter_api_key:
            self.openrouter_client = OpenAI(
                api_key=self.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1",
            )

        # Provider successfully used by the request.
        self.last_provider: Optional[str] = None

    # ======================================================
    # AVAILABILITY
    # ======================================================

    def is_available(self) -> bool:
        return any(
            [
                self.gemini_client is not None,
                self.groq_client is not None,
                self.openrouter_client is not None,
            ]
        )

    # ======================================================
    # MAIN GENERATION
    # ======================================================

    def generate(
        self,
        prompt: str,
        on_provider_change: Optional[
            Callable[[str], None]
        ] = None,
    ) -> str:

        providers = []

        if self.gemini_client:
            providers.append(
                (
                    "Gemini",
                    self._generate_gemini,
                )
            )

        if self.groq_client:
            providers.append(
                (
                    "Groq",
                    self._generate_groq,
                )
            )

        if self.openrouter_client:
            providers.append(
                (
                    "OpenRouter",
                    self._generate_openrouter,
                )
            )

        if not providers:
            raise RuntimeError(
                "No AI providers are configured."
            )

        errors = []

        self.last_provider = None

        for provider_name, provider_function in providers:

            if on_provider_change:
                on_provider_change(provider_name)

            try:
                print(
                    f"AI provider attempt: {provider_name}"
                )

                result = provider_function(prompt)

                if not result:
                    raise RuntimeError(
                        f"{provider_name} returned an empty response"
                    )

                self.last_provider = provider_name

                print(
                    f"AI provider succeeded: {provider_name}"
                )

                return result

            except Exception as exc:

                error_message = str(exc)

                print(
                    f"{provider_name} failed: "
                    f"{type(exc).__name__}: "
                    f"{error_message}"
                )

                errors.append(
                    f"{provider_name}: {error_message}"
                )

                if not self._is_retryable_error(exc):
                    raise RuntimeError(
                        f"{provider_name} failed: "
                        f"{error_message}"
                    ) from exc

                print(
                    f"{provider_name} temporary failure. "
                    "Trying next provider."
                )

        raise RuntimeError(
            "All AI providers failed.\n"
            + "\n".join(errors)
        )

    # ======================================================
    # GEMINI
    # ======================================================

    def _generate_gemini(
        self,
        prompt: str,
    ) -> str:

        if not self.gemini_client:
            raise RuntimeError(
                "Gemini is not configured."
            )

        last_error = None

        for attempt in range(3):

            try:
                response = (
                    self.gemini_client.models.generate_content(
                        model=self.gemini_model,
                        contents=prompt,
                    )
                )

                result = getattr(
                    response,
                    "text",
                    None,
                )

                if not result:
                    raise RuntimeError(
                        "Gemini returned an empty response"
                    )

                return result

            except Exception as exc:

                last_error = exc

                if not self._is_retryable_error(exc):
                    raise

                if attempt == 2:
                    break

                delay = 2 ** attempt

                print(
                    f"Gemini temporary failure. "
                    f"Retrying in {delay}s..."
                )

                time.sleep(delay)

        raise RuntimeError(
            "Gemini failed after retries: "
            f"{last_error}"
        )

    # ======================================================
    # GROQ
    # ======================================================

    def _generate_groq(
        self,
        prompt: str,
    ) -> str:

        if not self.groq_client:
            raise RuntimeError(
                "Groq is not configured."
            )

        response = (
            self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
        )

        result = (
            response.choices[0].message.content
        )

        if not result:
            raise RuntimeError(
                "Groq returned an empty response"
            )

        return result

    # ======================================================
    # OPENROUTER
    # ======================================================

    def _generate_openrouter(
        self,
        prompt: str,
    ) -> str:

        if not self.openrouter_client:
            raise RuntimeError(
                "OpenRouter is not configured."
            )

        response = (
            self.openrouter_client.chat.completions.create(
                model=self.openrouter_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
        )

        result = (
            response.choices[0].message.content
        )

        if not result:
            raise RuntimeError(
                "OpenRouter returned an empty response"
            )

        return result

    # ======================================================
    # ERROR CLASSIFICATION
    # ======================================================

    @staticmethod
    def _is_retryable_error(
        exc: Exception,
    ) -> bool:

        status_code = getattr(
            exc,
            "status_code",
            None,
        )

        if status_code in {
            429,
            500,
            502,
            503,
            504,
        }:
            return True

        message = str(exc).lower()

        retryable_patterns = [
            "429",
            "500",
            "502",
            "503",
            "504",
            "rate limit",
            "too many requests",
            "timeout",
            "timed out",
            "temporarily unavailable",
            "service unavailable",
            "overloaded",
            "capacity",
            "connection reset",
            "connection refused",
            "connection error",
            "server error",
        ]

        return any(
            pattern in message
            for pattern in retryable_patterns
        )