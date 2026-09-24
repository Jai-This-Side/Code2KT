from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".svn",
    ".hg",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".nuxt",
    ".terraform",
    ".idea",
    ".vscode",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


class SourceDetector:

    MAX_FILE_SIZE = 500_000

    SIGNATURES = {
        "fastapi": ("FastAPI", "backend_framework"),
        "django": ("Django", "backend_framework"),
        "flask": ("Flask", "backend_framework"),
        "tensorflow": ("TensorFlow", "machine_learning"),
        "torch": ("PyTorch", "machine_learning"),
        "pandas": ("Pandas", "data_science"),
        "numpy": ("NumPy", "data_science"),
    }

    def detect(self, project_path: Path) -> list[dict]:

        technologies = []
        detected = set()

        extensions = {
            ".py",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
        }

        for path in project_path.rglob("*"):

            if not path.is_file():
                continue

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            if path.suffix.lower() not in extensions:
                continue

            try:
                if path.stat().st_size > self.MAX_FILE_SIZE:
                    continue
            except OSError:
                continue

            try:
                content = path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).lower()
            except OSError:
                continue

            for signature, (
                technology,
                category,
            ) in self.SIGNATURES.items():

                if (
                    signature in content
                    and technology not in detected
                ):
                    detected.add(technology)

                    technologies.append({
                        "name": technology,
                        "category": category,
                        "confidence": 0.90,
                        "source": str(
                            path.relative_to(project_path)
                        ),
                    })

        return technologies