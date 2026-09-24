from pathlib import Path

from app.services.project_intelligence import ProjectIntelligence
from app.services.project_root_detector import ProjectRootDetector
from app.services.code_analysis.code_analyzer import CodeAnalyzer
from app.services.code_analysis.dependency_resolver import (
    DependencyResolver,
)
from app.services.project_graph import ProjectGraphBuilder


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


IGNORED_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    "terraform.tfstate",
    "terraform.tfstate.backup",
    ".DS_Store",
    "id_rsa",
    "id_rsa.pub",
}


class ProjectAnalyzer:

    def __init__(self):

        self.intelligence = (
            ProjectIntelligence()
        )

        self.root_detector = (
            ProjectRootDetector()
        )

        self.code_analyzer = (
            CodeAnalyzer()
        )

        self.dependency_resolver = (
            DependencyResolver()
        )

        self.graph_builder = (
            ProjectGraphBuilder()
        )

    def analyze(
        self,
        project_path: Path,
    ) -> dict:

        # =========================================
        # 1. Detect project root
        # =========================================

        project_root = (
            self.root_detector.find_root(
                project_path
            )
        )

        # =========================================
        # 2. Scan files
        # =========================================

        files = []
        directories = set()

        for path in project_root.rglob("*"):

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            if (
                path.is_file()
                and path.name in IGNORED_FILES
            ):
                continue

            if path.is_dir():

                directories.add(
                    str(
                        path.relative_to(
                            project_root
                        )
                    )
                )

            elif path.is_file():

                files.append(
                    {
                        "path": str(
                            path.relative_to(
                                project_root
                            )
                        ),
                        "extension": (
                            path.suffix.lower()
                        ),
                        "size": path.stat().st_size,
                    }
                )

        # =========================================
        # 3. Languages
        # =========================================

        languages = (
            self._detect_languages(
                files
            )
        )

        # =========================================
        # 4. Technology detection
        # =========================================

        technology_detection = (
            self.intelligence.analyze(
                project_root
            )
        )

        # =========================================
        # 5. AST analysis
        # =========================================

        code_analysis = (
            self.code_analyzer.analyze(
                project_root
            )
        )

        # =========================================
        # 6. Base analysis
        # =========================================

        analysis = {
            "project_root": (
                str(
                    project_root.relative_to(
                        project_path
                    )
                )
                if project_root != project_path
                else "."
            ),

            "file_count": len(files),

            "directory_count": len(
                directories
            ),

            "languages": languages,

            "technologies": (
                technology_detection[
                    "technologies"
                ]
            ),

            "evidence": (
                technology_detection[
                    "evidence"
                ]
            ),

            "ai_required": (
                technology_detection[
                    "ai_required"
                ]
            ),

            "ai_used": (
                technology_detection[
                    "ai_used"
                ]
            ),

            "files": files,
        }

        # =========================================
        # 7. Resolve dependencies
        # =========================================

        dependency_analysis = (
            self.dependency_resolver.resolve(
                project_root,
                code_analysis[
                    "files"
                ],
            )
        )

        # =========================================
        # 8. Build graph
        # =========================================

        project_graph = (
            self.graph_builder.build(
                project_root,
                analysis,
                code_analysis,
                dependency_analysis,
            )
        )

        # =========================================
        # 9. Final result
        # =========================================

        return {
            **analysis,

            "code_analysis": (
                code_analysis
            ),

            "dependency_analysis": (
                dependency_analysis
            ),

            "project_graph": (
                project_graph.model_dump()
            ),
        }

    @staticmethod
    def _detect_languages(
        files: list[dict],
    ) -> list[str]:

        extension_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".jsx": "JavaScript",
            ".ts": "TypeScript",
            ".tsx": "TypeScript",
            ".html": "HTML",
            ".css": "CSS",
            ".java": "Java",
            ".cpp": "C++",
            ".cc": "C++",
            ".cxx": "C++",
            ".c": "C",
            ".go": "Go",
            ".php": "PHP",
            ".kt": "Kotlin",
            ".rs": "Rust",
        }

        languages = set()

        for file in files:

            language = extension_map.get(
                file["extension"]
            )

            if language:
                languages.add(language)

        return sorted(languages)