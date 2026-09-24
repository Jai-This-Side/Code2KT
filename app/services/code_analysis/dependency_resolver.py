from pathlib import Path


class DependencyResolver:

    SOURCE_EXTENSIONS = {
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".py",
    }

    INDEX_FILES = {
        "index.js",
        "index.jsx",
        "index.ts",
        "index.tsx",
        "index.py",
    }

    def resolve(
        self,
        project_path: Path,
        code_files: list[dict],
    ) -> dict:

        edges = []
        unresolved = []

        known_files = self._build_file_index(
            project_path
        )

        for code_file in code_files:

            source_file = code_file["file"]

            for import_statement in code_file.get(
                "imports",
                [],
            ):

                import_path = self._extract_import_path(
                    import_statement
                )

                if not import_path:
                    continue

                # External packages such as React,
                # Framer Motion, etc. are not local
                # project dependencies.
                if not import_path.startswith("."):
                    continue

                target = self._resolve_import(
                    project_path,
                    source_file,
                    import_path,
                    known_files,
                )

                if target:

                    edges.append({
                        "source": source_file,
                        "target": target,
                        "type": "local_import",
                    })

                else:

                    unresolved.append({
                        "source": source_file,
                        "import": import_path,
                    })

        return {
            "dependencies": self._deduplicate(
                edges
            ),
            "unresolved": unresolved,
        }

    @staticmethod
    def _build_file_index(
        project_path: Path,
    ) -> set[str]:

        files = set()

        for path in project_path.rglob("*"):

            if not path.is_file():
                continue

            if path.suffix.lower() not in {
                ".js",
                ".jsx",
                ".ts",
                ".tsx",
                ".py",
            }:
                continue

            files.add(
                str(
                    path.relative_to(
                        project_path
                    )
                )
            )

        return files

    @staticmethod
    def _extract_import_path(
        import_statement: str,
    ) -> str | None:

        # Handles:
        #
        # import Foo from "./Foo"
        # import { x } from "../utils"
        # import "./styles.css"

        quote_positions = []

        for index, character in enumerate(
            import_statement
        ):

            if character in {"'", '"'}:
                quote_positions.append(index)

        if len(quote_positions) < 2:
            return None

        start = quote_positions[0]
        end = quote_positions[1]

        return import_statement[
            start + 1:end
        ]

    def _resolve_import(
        self,
        project_path: Path,
        source_file: str,
        import_path: str,
        known_files: set[str],
    ) -> str | None:

        source = (
            project_path / source_file
        ).parent

        candidate = (
            source / import_path
        ).resolve()

        try:
            relative_candidate = str(
                candidate.relative_to(
                    project_path.resolve()
                )
            )

        except ValueError:
            return None

        # Direct file match.
        if relative_candidate in known_files:
            return relative_candidate

        # Try common source extensions.
        for extension in self.SOURCE_EXTENSIONS:

            candidate_file = (
                relative_candidate
                + extension
            )

            if candidate_file in known_files:
                return candidate_file

        # Try directory/index imports.
        for index_file in self.INDEX_FILES:

            candidate_file = str(
                Path(relative_candidate)
                / index_file
            )

            if candidate_file in known_files:
                return candidate_file

        return None

    @staticmethod
    def _deduplicate(
        dependencies: list[dict],
    ) -> list[dict]:

        seen = set()
        result = []

        for dependency in dependencies:

            key = (
                dependency["source"],
                dependency["target"],
                dependency["type"],
            )

            if key in seen:
                continue

            seen.add(key)
            result.append(dependency)

        return result