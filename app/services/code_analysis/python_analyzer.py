import ast
from pathlib import Path


class PythonAnalyzer:

    MAX_FILE_SIZE = 500_000

    def analyze(self, file_path: Path) -> dict:

        if file_path.stat().st_size > self.MAX_FILE_SIZE:
            return {
                "file": str(file_path),
                "language": "Python",
                "functions": [],
                "classes": [],
                "imports": [],
                "routes": [],
                "error": "File too large",
            }

        try:
            source = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(source)

        except (SyntaxError, OSError) as exc:
            return {
                "file": str(file_path),
                "language": "Python",
                "functions": [],
                "classes": [],
                "imports": [],
                "routes": [],
                "error": str(exc),
            }

        return {
            "file": str(file_path),
            "language": "Python",
            "functions": self._extract_functions(tree),
            "classes": self._extract_classes(tree),
            "imports": self._extract_imports(tree),
            "routes": self._extract_routes(tree),
            "error": None,
        }

    @staticmethod
    def _extract_functions(
        tree: ast.AST,
    ) -> list[dict]:

        functions = []

        for node in ast.walk(tree):

            if not isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                continue

            functions.append({
                "name": node.name,
                "line": node.lineno,
                "async": isinstance(
                    node,
                    ast.AsyncFunctionDef,
                ),
                "arguments": [
                    argument.arg
                    for argument in node.args.args
                ],
            })

        return functions

    @staticmethod
    def _extract_classes(
        tree: ast.AST,
    ) -> list[dict]:

        classes = []

        for node in ast.walk(tree):

            if not isinstance(
                node,
                ast.ClassDef,
            ):
                continue

            classes.append({
                "name": node.name,
                "line": node.lineno,
                "bases": [
                    PythonAnalyzer._get_name(base)
                    for base in node.bases
                ],
                "methods": [
                    child.name
                    for child in node.body
                    if isinstance(
                        child,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef,
                        ),
                    )
                ],
            })

        return classes

    @staticmethod
    def _extract_imports(
        tree: ast.AST,
    ) -> list[str]:

        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):

                if node.module:
                    imports.append(node.module)

        return sorted(set(imports))

    @staticmethod
    def _extract_routes(
        tree: ast.AST,
    ) -> list[dict]:

        routes = []

        for node in ast.walk(tree):

            if not isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                continue

            for decorator in node.decorator_list:

                if not isinstance(
                    decorator,
                    ast.Call,
                ):
                    continue

                function = decorator.func

                if not isinstance(
                    function,
                    ast.Attribute,
                ):
                    continue

                if function.attr not in {
                    "get",
                    "post",
                    "put",
                    "patch",
                    "delete",
                }:
                    continue

                if not decorator.args:
                    continue

                path_node = decorator.args[0]

                if not isinstance(
                    path_node,
                    ast.Constant,
                ):
                    continue

                if not isinstance(
                    path_node.value,
                    str,
                ):
                    continue

                routes.append({
                    "method": function.attr.upper(),
                    "path": path_node.value,
                    "function": node.name,
                    "line": node.lineno,
                })

        return routes

    @staticmethod
    def _get_name(node: ast.AST) -> str:

        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Attribute):

            parts = []

            current = node

            while isinstance(
                current,
                ast.Attribute,
            ):
                parts.append(current.attr)
                current = current.value

            if isinstance(
                current,
                ast.Name,
            ):
                parts.append(current.id)

            return ".".join(reversed(parts))

        return "unknown"