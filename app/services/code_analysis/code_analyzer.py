from pathlib import Path

from app.services.code_analysis.python_analyzer import (
    PythonAnalyzer,
)
from app.services.code_analysis.javascript_analyzer import (
    JavaScriptAnalyzer,
)


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


class CodeAnalyzer:

    def __init__(self):
        self.python_analyzer = PythonAnalyzer()
        self.javascript_analyzer = JavaScriptAnalyzer()

    def analyze(
        self,
        project_path: Path,
    ) -> dict:

        results = []

        for path in project_path.rglob("*"):

            if not path.is_file():
                continue

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            suffix = path.suffix.lower()

            if suffix == ".py":

                result = self.python_analyzer.analyze(
                    path
                )

            elif suffix in {
                ".js",
                ".jsx",
                ".ts",
                ".tsx",
            }:

                result = self.javascript_analyzer.analyze(
                    path,
                    project_path,
                )

            else:
                continue

            result["file"] = str(
                path.relative_to(project_path)
            )

            results.append(result)

        return {
            "files_analyzed": len(results),
            "files": results,
        }