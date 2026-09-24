import json

from app.services.ai.gemini_service import (
    GeminiService,
)


class AIFallbackDetector:

    def __init__(self):

        self.llm = GeminiService()

    def detect(
        self,
        context: str,
    ) -> list[dict]:

        if not self.llm.is_available():
            return []

        prompt = f"""
Analyze the following software project evidence.

Return ONLY valid JSON.

Expected format:

[
  {{
    "name": "technology name",
    "category": "technology category",
    "confidence": 0.0,
    "source": "AI analysis"
  }}
]

Use conservative confidence values.

Do not invent technologies without
supporting evidence.

PROJECT EVIDENCE:

{context}
"""

        try:

            response = self.llm.generate(
                prompt
            )

            parsed = json.loads(
                response
            )

            if not isinstance(
                parsed,
                list,
            ):
                return []

            return parsed

        except Exception:

            return []