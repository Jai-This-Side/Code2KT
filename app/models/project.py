from typing import Optional

from pydantic import BaseModel, Field


class Technology(BaseModel):
    name: str
    category: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    source: str


class FunctionInfo(BaseModel):
    name: str
    line: int

    async_function: bool = False

    arguments: list[str] = Field(
        default_factory=list
    )

    type: Optional[str] = None


class ClassInfo(BaseModel):
    name: str
    line: int

    bases: list[str] = Field(
        default_factory=list
    )

    methods: list[str] = Field(
        default_factory=list
    )


class ImportInfo(BaseModel):
    source: str

    imported_names: list[str] = Field(
        default_factory=list
    )


class ExportInfo(BaseModel):
    source: str


class ComponentInfo(BaseModel):
    name: str
    file: str
    line: int

    component_type: str = "react_component"


class HookInfo(BaseModel):
    name: str
    file: str
    line: int


class APICallInfo(BaseModel):
    function: str
    file: str
    line: int


class RouteInfo(BaseModel):
    method: str
    path: str
    function: str
    file: str
    line: int


class FileInfo(BaseModel):
    path: str
    extension: str
    size: int


class CodeFileAnalysis(BaseModel):
    file: str
    language: str

    functions: list[FunctionInfo] = Field(
        default_factory=list
    )

    classes: list[ClassInfo] = Field(
        default_factory=list
    )

    imports: list[str] = Field(
        default_factory=list
    )

    exports: list[str] = Field(
        default_factory=list
    )

    components: list[ComponentInfo] = Field(
        default_factory=list
    )

    hooks: list[HookInfo] = Field(
        default_factory=list
    )

    api_calls: list[APICallInfo] = Field(
        default_factory=list
    )

    routes: list[RouteInfo] = Field(
        default_factory=list
    )

    error: Optional[str] = None


class EvidenceInfo(BaseModel):
    technology_count: int
    high_confidence_count: int
    has_manifest: bool
    ai_required: bool


class DependencyInfo(BaseModel):
    source: str
    target: str

    type: str = "local_import"


class ProjectGraph(BaseModel):
    name: str
    root: str

    languages: list[str] = Field(
        default_factory=list
    )

    technologies: list[Technology] = Field(
        default_factory=list
    )

    files: list[FileInfo] = Field(
        default_factory=list
    )

    code_files: list[CodeFileAnalysis] = Field(
        default_factory=list
    )

    dependencies: list[DependencyInfo] = Field(
        default_factory=list
    )

    unresolved_dependencies: list[dict] = Field(
        default_factory=list
    )

    evidence: Optional[EvidenceInfo] = None

    ai_required: bool = False

    ai_used: bool = False