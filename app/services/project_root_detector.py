from pathlib import Path


class ProjectRootDetector:
    """
    Finds the actual project root inside an extracted ZIP.

    A project root is identified using common project marker files/directories.
    """

    MARKER_FILES = {
        "package.json",
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "Cargo.toml",
        "go.mod",
        "composer.json",
        "manage.py",
        "Dockerfile",
    }

    MARKER_DIRECTORIES = {
        ".github",
        "terraform",
    }

    def find_root(self, extracted_path: Path) -> Path:
        # Case 1: the extraction directory itself is the project
        if self._looks_like_project(extracted_path):
            return extracted_path

        candidates = []

        # Search a few levels deep to avoid walking huge dependency trees.
        for path in extracted_path.iterdir():
            if not path.is_dir():
                continue

            if self._looks_like_project(path):
                candidates.append(path)

        # If exactly one likely project directory exists, use it.
        if len(candidates) == 1:
            return candidates[0]

        # Search recursively up to 3 levels.
        for path in extracted_path.rglob("*"):
            if not path.is_dir():
                continue

            try:
                relative = path.relative_to(extracted_path)
            except ValueError:
                continue

            if len(relative.parts) > 3:
                continue

            if self._looks_like_project(path):
                candidates.append(path)

        if candidates:
            # Prefer the shallowest candidate.
            candidates.sort(key=lambda p: len(p.relative_to(extracted_path).parts))
            return candidates[0]

        # Nothing recognizable — use extraction root.
        return extracted_path

    def _looks_like_project(self, path: Path) -> bool:
        for marker in self.MARKER_FILES:
            if (path / marker).exists():
                return True

        for marker in self.MARKER_DIRECTORIES:
            marker_path = path / marker
            if marker_path.exists() and marker_path.is_dir():
                return True

        return False