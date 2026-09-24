from pathlib import Path

from app.models.project import (
    APICallInfo,
    ClassInfo,
    CodeFileAnalysis,
    ComponentInfo,
    EvidenceInfo,
    FileInfo,
    FunctionInfo,
    HookInfo,
    ProjectGraph,
    Technology,
)

from app.models.project import DependencyInfo


class ProjectGraphBuilder:

    def build(
        self,
        project_path: Path,
        analysis: dict,
        code_analysis: dict,
        dependency_analysis: dict,
    ) -> ProjectGraph:

        project_name = project_path.name

        technologies = [
            Technology(**technology)
            for technology in analysis[
                "technologies"
            ]
        ]

        files = [
            FileInfo(**file)
            for file in analysis["files"]
        ]

        code_files = []

        for code_file in code_analysis["files"]:

            code_files.append(
                self._build_code_file(
                    code_file
                )
            )

        evidence_data = analysis.get(
            "evidence"
        )

        evidence = None

        if evidence_data:
            evidence = EvidenceInfo(
                **evidence_data
            )

        return ProjectGraph(
            name=project_name,
            root=analysis["project_root"],
            languages=analysis["languages"],
            technologies=technologies,
            files=files,
            code_files=code_files,
            evidence=evidence,
            ai_required=analysis[
                "ai_required"
            ],
            ai_used=analysis[
                "ai_used"
            ],
        )

    def _build_code_file(
        self,
        data: dict,
    ) -> CodeFileAnalysis:

        functions = []

        for function in data.get(
            "functions",
            []
        ):

            functions.append(
                FunctionInfo(
                    name=function["name"],
                    line=function["line"],
                    async_function=function.get(
                        "async",
                        False,
                    ),
                    arguments=function.get(
                        "arguments",
                        [],
                    ),
                    type=function.get(
                        "type"
                    ),
                )
            )

        classes = []

        for cls in data.get(
            "classes",
            []
        ):

            classes.append(
                ClassInfo(
                    name=cls["name"],
                    line=cls["line"],
                    bases=cls.get(
                        "bases",
                        [],
                    ),
                    methods=cls.get(
                        "methods",
                        [],
                    ),
                )
            )

        components = []

        for component in data.get(
            "components",
            []
        ):

            components.append(
                ComponentInfo(
                    name=component["name"],
                    file=data["file"],
                    line=component["line"],
                    component_type=component.get(
                        "type",
                        "react_component",
                    ),
                )
            )

        hooks = []

        for hook in data.get(
            "hooks",
            []
        ):

            hooks.append(
                HookInfo(
                    name=hook["name"],
                    file=data["file"],
                    line=hook["line"],
                )
            )

        api_calls = []

        for api_call in data.get(
            "api_calls",
            []
        ):

            api_calls.append(
                APICallInfo(
                    function=api_call["function"],
                    file=data["file"],
                    line=api_call["line"],
                )
            )

        return CodeFileAnalysis(
            file=data["file"],
            language=data["language"],
            functions=functions,
            classes=classes,
            imports=data.get(
                "imports",
                [],
            ),
            exports=data.get(
                "exports",
                [],
            ),
            components=components,
            hooks=hooks,
            api_calls=api_calls,
            routes=data.get(
                "routes",
                [],
            ),
            error=data.get(
                "error"
            ),
        )