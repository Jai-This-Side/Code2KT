from pathlib import Path

from app.services.detection.manifest_detector import ManifestDetector
from app.services.detection.config_detector import ConfigDetector
from app.services.detection.source_detector import SourceDetector
from app.services.detection.file_detector import FileDetector


class ProjectDetector:

    def __init__(self):
        self.manifest_detector = ManifestDetector()
        self.config_detector = ConfigDetector()
        self.source_detector = SourceDetector()
        self.file_detector = FileDetector()

    def detect(self, project_path: Path) -> dict:

        technologies = []

        technologies.extend(
            self.manifest_detector.detect(project_path)
        )

        technologies.extend(
            self.config_detector.detect(project_path)
        )

        technologies.extend(
            self.file_detector.detect(project_path)
        )

        technologies.extend(
            self.source_detector.detect(project_path)
        )

        technologies = self._deduplicate(technologies)

        evidence = self._calculate_evidence(
            project_path,
            technologies
        )

        return {
            "technologies": technologies,
            "evidence": evidence,
            "ai_required": evidence["ai_required"],
        }

    @staticmethod
    def _deduplicate(
        technologies: list[dict]
    ) -> list[dict]:

        result = {}

        for technology in technologies:

            name = technology["name"]

            if name not in result:
                result[name] = technology
                continue

            existing = result[name]

            if (
                technology["confidence"]
                > existing["confidence"]
            ):
                result[name] = technology

        return list(result.values())

    @staticmethod
    def _calculate_evidence(
        project_path: Path,
        technologies: list[dict]
    ) -> dict:

        technology_count = len(technologies)

        has_manifest = any(
            technology["source"] in {
                "package.json",
                "requirements.txt",
                "pyproject.toml",
                "Pipfile",
                "pom.xml",
                "Cargo.toml",
                "go.mod",
                "composer.json",
            }
            for technology in technologies
        )

        high_confidence_count = sum(
            1
            for technology in technologies
            if technology["confidence"] >= 0.95
        )

        if has_manifest and technology_count >= 2:
            ai_required = False

        elif high_confidence_count >= 3:
            ai_required = False

        elif technology_count == 0:
            ai_required = True

        else:
            ai_required = True

        return {
            "technology_count": technology_count,
            "high_confidence_count": high_confidence_count,
            "has_manifest": has_manifest,
            "ai_required": ai_required,
        }