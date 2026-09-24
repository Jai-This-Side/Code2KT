from pathlib import Path

from app.services.detection.detector import ProjectDetector
from app.services.ai.fallback_detector import AIFallbackDetector


class ProjectIntelligence:

    def __init__(self):
        self.detector = ProjectDetector()
        self.ai_detector = AIFallbackDetector()

    def analyze(
        self,
        project_root: Path,
        use_ai_fallback: bool = False,
    ) -> dict:

        result = self.detector.detect(
            project_root
        )

        technologies = result.get(
            "technologies",
            [],
        )

        evidence = result.get(
            "evidence",
            {},
        )

        ai_required = bool(
            result.get(
                "ai_required",
                False,
            )
        )

        ai_used = False

        if (
            use_ai_fallback
            and ai_required
        ):

            try:

                ai_technologies = (
                    self.ai_detector.detect(
                        project_root
                    )
                )

                if ai_technologies:

                    technologies.extend(
                        ai_technologies
                    )

                    ai_used = True

            except Exception as exc:

                evidence[
                    "ai_fallback_error"
                ] = str(exc)

        technologies = (
            self._deduplicate_technologies(
                technologies
            )
        )

        evidence[
            "technology_count"
        ] = len(technologies)

        evidence[
            "high_confidence_count"
        ] = sum(
            1
            for technology in technologies
            if technology.get(
                "confidence",
                0,
            ) >= 0.8
        )

        return {
            "technologies": technologies,
            "evidence": evidence,
            "ai_required": ai_required,
            "ai_used": ai_used,
        }

    @staticmethod
    def _deduplicate_technologies(
        technologies: list[dict],
    ) -> list[dict]:

        seen = set()
        result = []

        for technology in technologies:

            name = technology.get(
                "name"
            )

            if not name:
                continue

            key = name.lower().strip()

            if key in seen:
                continue

            seen.add(key)

            result.append(
                technology
            )

        return result