from pathlib import Path

from tree_sitter import Language, Parser
import tree_sitter_javascript as ts_javascript
import tree_sitter_typescript as ts_typescript


class JavaScriptAnalyzer:

    SUPPORTED_EXTENSIONS = {
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
    }

    HOOKS = {
        "useState",
        "useEffect",
        "useContext",
        "useReducer",
        "useCallback",
        "useMemo",
        "useRef",
        "useLayoutEffect",
        "useImperativeHandle",
        "useId",
        "useTransition",
        "useDeferredValue",
        "useDebugValue",
    }

    API_FUNCTIONS = {
        "fetch",
        "axios",
    }

    def analyze(
        self,
        file_path: Path,
        project_root: Path,
    ) -> dict:

        extension = file_path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            return {}

        try:
            source_bytes = file_path.read_bytes()

            tree = self._parse(
                source_bytes,
                extension,
            )

            relative_file = str(
                file_path.relative_to(
                    project_root
                )
            )

            return {
                "file": relative_file,
                "language": self._language(
                    extension
                ),
                "functions": self._extract_functions(
                    tree.root_node,
                    source_bytes,
                ),
                "classes": self._extract_classes(
                    tree.root_node,
                    source_bytes,
                ),
                "imports": self._extract_imports(
                    tree.root_node,
                    source_bytes,
                ),
                "exports": self._extract_exports(
                    tree.root_node,
                    source_bytes,
                ),
                "components": self._extract_components(
                    tree.root_node,
                    source_bytes,
                ),
                "hooks": self._extract_hooks(
                    tree.root_node,
                    source_bytes,
                    relative_file,
                ),
                "api_calls": self._extract_api_calls(
                    tree.root_node,
                    source_bytes,
                    relative_file,
                ),
                "routes": [],
                "error": None,
            }

        except Exception as exc:
            return {
                "file": str(
                    file_path.relative_to(
                        project_root
                    )
                ),
                "language": self._language(
                    extension
                ),
                "functions": [],
                "classes": [],
                "imports": [],
                "exports": [],
                "components": [],
                "hooks": [],
                "api_calls": [],
                "routes": [],
                "error": str(exc),
            }

    # ==================================================
    # Parser
    # ==================================================

    @staticmethod
    def _parse(
        source_bytes: bytes,
        extension: str,
    ):

        parser = Parser()

        if extension == ".tsx":

            parser.language = Language(
                ts_typescript.language_tsx()
            )

        elif extension == ".ts":

            parser.language = Language(
                ts_typescript.language_typescript()
            )

        else:

            parser.language = Language(
                ts_javascript.language()
            )

        return parser.parse(
            source_bytes
        )

    # ==================================================
    # Language
    # ==================================================

    @staticmethod
    def _language(
        extension: str,
    ) -> str:

        if extension in {
            ".ts",
            ".tsx",
        }:
            return "TypeScript"

        return "JavaScript"

    # ==================================================
    # Node Text
    # ==================================================

    @staticmethod
    def _node_text(
        node,
        source_bytes: bytes,
    ) -> str:

        return source_bytes[
            node.start_byte:node.end_byte
        ].decode(
            "utf-8",
            errors="replace",
        )

    # ==================================================
    # Functions
    # ==================================================

    def _extract_functions(
        self,
        root,
        source_bytes: bytes,
    ) -> list[dict]:

        functions = []

        def visit(node):

            # ------------------------------------------
            # Named function declarations
            # ------------------------------------------

            if node.type in {
                "function_declaration",
                "generator_function_declaration",
            }:

                name_node = node.child_by_field_name(
                    "name"
                )

                if name_node:

                    functions.append({
                        "name": self._node_text(
                            name_node,
                            source_bytes,
                        ),
                        "line": (
                            node.start_point[0] + 1
                        ),
                        "async": self._is_async(
                            node
                        ),
                        "arguments": (
                            self._extract_arguments(
                                node,
                                source_bytes,
                            )
                        ),
                        "type": "function",
                    })

                return

            # ------------------------------------------
            # Named class methods
            # ------------------------------------------

            if node.type in {
                "method_definition",
                "method_signature",
            }:

                name_node = node.child_by_field_name(
                    "name"
                )

                if name_node:

                    functions.append({
                        "name": self._node_text(
                            name_node,
                            source_bytes,
                        ),
                        "line": (
                            node.start_point[0] + 1
                        ),
                        "async": self._is_async(
                            node
                        ),
                        "arguments": (
                            self._extract_arguments(
                                node,
                                source_bytes,
                            )
                        ),
                        "type": "method",
                    })

            # ------------------------------------------
            # Named arrow/function assignments
            #
            # const App = () => {}
            # function-valued variables
            # ------------------------------------------

            if node.type == "variable_declarator":

                name_node = node.child_by_field_name(
                    "name"
                )

                value_node = node.child_by_field_name(
                    "value"
                )

                if (
                    name_node
                    and value_node
                    and value_node.type in {
                        "arrow_function",
                        "function",
                    }
                ):

                    functions.append({
                        "name": self._node_text(
                            name_node,
                            source_bytes,
                        ),
                        "line": (
                            node.start_point[0] + 1
                        ),
                        "async": self._is_async(
                            value_node
                        ),
                        "arguments": (
                            self._extract_arguments(
                                value_node,
                                source_bytes,
                            )
                        ),
                        "type": (
                            "arrow_function"
                            if value_node.type
                            == "arrow_function"
                            else "function"
                        ),
                    })

            for child in node.children:
                visit(child)

        visit(root)

        return self._deduplicate(
            functions
        )

    # ==================================================
    # Classes
    # ==================================================

    def _extract_classes(
        self,
        root,
        source_bytes: bytes,
    ) -> list[dict]:

        classes = []

        def visit(node):

            if node.type == "class_declaration":

                name_node = node.child_by_field_name(
                    "name"
                )

                if name_node:

                    methods = []

                    body = node.child_by_field_name(
                        "body"
                    )

                    if body:

                        for child in body.children:

                            if child.type == "method_definition":

                                method_name = (
                                    child.child_by_field_name(
                                        "name"
                                    )
                                )

                                if method_name:
                                    methods.append(
                                        self._node_text(
                                            method_name,
                                            source_bytes,
                                        )
                                    )

                    classes.append({
                        "name": self._node_text(
                            name_node,
                            source_bytes,
                        ),
                        "line": (
                            node.start_point[0] + 1
                        ),
                        "bases": (
                            self._extract_class_bases(
                                node,
                                source_bytes,
                            )
                        ),
                        "methods": methods,
                    })

            for child in node.children:
                visit(child)

        visit(root)

        return classes

    # ==================================================
    # Imports
    # ==================================================

    def _extract_imports(
        self,
        root,
        source_bytes: bytes,
    ) -> list[str]:

        imports = []

        def visit(node):

            if node.type == "import_statement":

                imports.append(
                    self._node_text(
                        node,
                        source_bytes,
                    )
                )

            for child in node.children:
                visit(child)

        visit(root)

        return self._deduplicate_strings(
            imports
        )

    # ==================================================
    # Exports
    # ==================================================

    def _extract_exports(
        self,
        root,
        source_bytes: bytes,
    ) -> list[str]:

        exports = []

        def visit(node):

            if node.type in {
                "export_statement",
                "export_clause",
            }:

                text = self._node_text(
                    node,
                    source_bytes,
                ).strip()

                if text:
                    exports.append(
                        text
                    )

            for child in node.children:
                visit(child)

        visit(root)

        return self._deduplicate_strings(
            exports
        )

    # ==================================================
    # React Components
    # ==================================================

    def _extract_components(
        self,
        root,
        source_bytes: bytes,
    ) -> list[dict]:

        components = []

        def visit(node):

            # ------------------------------------------
            # function Component() { return <div /> }
            # ------------------------------------------

            if node.type == "function_declaration":

                name_node = node.child_by_field_name(
                    "name"
                )

                if (
                    name_node
                    and self._is_component_name(
                        self._node_text(
                            name_node,
                            source_bytes,
                        )
                    )
                    and self._contains_jsx(node)
                ):

                    components.append({
                        "name": self._node_text(
                            name_node,
                            source_bytes,
                        ),
                        "line": (
                            node.start_point[0] + 1
                        ),
                        "type": "react_component",
                    })

            # ------------------------------------------
            # const Component = () => <div />
            # ------------------------------------------

            if node.type == "variable_declarator":

                name_node = node.child_by_field_name(
                    "name"
                )

                value_node = node.child_by_field_name(
                    "value"
                )

                if (
                    name_node
                    and value_node
                    and self._is_component_name(
                        self._node_text(
                            name_node,
                            source_bytes,
                        )
                    )
                    and value_node.type in {
                        "arrow_function",
                        "function",
                    }
                    and self._contains_jsx(
                        value_node
                    )
                ):

                    components.append({
                        "name": self._node_text(
                            name_node,
                            source_bytes,
                        ),
                        "line": (
                            node.start_point[0] + 1
                        ),
                        "type": "react_component",
                    })

            for child in node.children:
                visit(child)

        visit(root)

        return self._deduplicate_dicts(
            components
        )

    # ==================================================
    # Hooks
    # ==================================================

    def _extract_hooks(
        self,
        root,
        source_bytes: bytes,
        relative_file: str,
    ) -> list[dict]:

        hooks = []

        def visit(node):

            if node.type == "call_expression":

                function_node = (
                    node.child_by_field_name(
                        "function"
                    )
                )

                if function_node:

                    function_name = (
                        self._node_text(
                            function_node,
                            source_bytes,
                        )
                    )

                    if function_name in self.HOOKS:

                        hooks.append({
                            "name": function_name,
                            "file": relative_file,
                            "line": (
                                node.start_point[0]
                                + 1
                            ),
                        })

            for child in node.children:
                visit(child)

        visit(root)

        return self._deduplicate_dicts(
            hooks
        )

    # ==================================================
    # API Calls
    # ==================================================

    def _extract_api_calls(
        self,
        root,
        source_bytes: bytes,
        relative_file: str,
    ) -> list[dict]:

        api_calls = []

        def visit(node):

            if node.type == "call_expression":

                function_node = (
                    node.child_by_field_name(
                        "function"
                    )
                )

                if function_node:

                    function_name = (
                        self._node_text(
                            function_node,
                            source_bytes,
                        )
                    )

                    is_api_call = (
                        function_name in
                        self.API_FUNCTIONS
                        or function_name.startswith(
                            "axios."
                        )
                    )

                    if is_api_call:

                        api_calls.append({
                            "function": function_name,
                            "file": relative_file,
                            "line": (
                                node.start_point[0]
                                + 1
                            ),
                        })

            for child in node.children:
                visit(child)

        visit(root)

        return self._deduplicate_dicts(
            api_calls
        )

    # ==================================================
    # Helpers
    # ==================================================

    @staticmethod
    def _is_async(
        node,
    ) -> bool:

        return any(
            child.type == "async"
            for child in node.children
        )

    def _extract_arguments(
        self,
        node,
        source_bytes: bytes,
    ) -> list[str]:

        parameters = (
            node.child_by_field_name(
                "parameters"
            )
        )

        if not parameters:
            return []

        arguments = []

        for child in parameters.named_children:

            arguments.append(
                self._node_text(
                    child,
                    source_bytes,
                )
            )

        return arguments

    def _extract_class_bases(
        self,
        node,
        source_bytes: bytes,
    ) -> list[str]:

        heritage = (
            node.child_by_field_name(
                "heritage"
            )
        )

        if not heritage:
            return []

        return [
            self._node_text(
                child,
                source_bytes,
            )
            for child in heritage.named_children
        ]

    def _contains_jsx(
        self,
        node,
    ) -> bool:

        jsx_types = {
            "jsx_element",
            "jsx_self_closing_element",
            "jsx_fragment",
        }

        if node.type in jsx_types:
            return True

        for child in node.children:

            if self._contains_jsx(
                child
            ):
                return True

        return False

    @staticmethod
    def _is_component_name(
        name: str,
    ) -> bool:

        if not name:
            return False

        return (
            name[0].isupper()
            and name.replace(
                "_",
                ""
            ).replace(
                "$",
                ""
            ).isalnum()
        )

    @staticmethod
    def _deduplicate(
        items: list[dict],
    ) -> list[dict]:

        seen = set()
        result = []

        for item in items:

            key = (
                item.get("name"),
                item.get("line"),
                item.get("type"),
            )

            if key in seen:
                continue

            seen.add(key)
            result.append(item)

        return result

    @staticmethod
    def _deduplicate_strings(
        items: list[str],
    ) -> list[str]:

        seen = set()
        result = []

        for item in items:

            if item in seen:
                continue

            seen.add(item)
            result.append(item)

        return result

    @staticmethod
    def _deduplicate_dicts(
        items: list[dict],
    ) -> list[dict]:

        seen = set()
        result = []

        for item in items:

            key = tuple(
                sorted(item.items())
            )

            if key in seen:
                continue

            seen.add(key)
            result.append(item)

        return result