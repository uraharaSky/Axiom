from pathlib import Path

from axiom.context.models import RetrievalUnit
from axiom.context.relationships import (
    Relationship,
    RelationshipKind,
)
from axiom.scanner.models import Project


def _function_to_unit(function) -> RetrievalUnit:
    return RetrievalUnit(
        id=f"{function.file}:{function.line}",
        kind="function",
        name=function.name,
        file=function.file,
        start_line=function.line,
        end_line=function.end_line,
    )


def _class_to_unit(cls) -> RetrievalUnit:
    return RetrievalUnit(
        id=f"{cls.file}:{cls.line}",
        kind="class",
        name=cls.name,
        file=cls.file,
        start_line=cls.line,
        end_line=cls.end_line,
    )


def _module_matches(file: Path, module: str) -> bool:
    module_path = Path(*module.split("."))

    file_without_suffix = file.with_suffix("")

    return (
        file_without_suffix == module_path
        or file_without_suffix.as_posix().endswith(
            module_path.as_posix()
        )
    )


def _resolve_functions(
    name: str,
    project: Project,
    module: str | None = None,
) -> list[RetrievalUnit]:

    candidates = [
        function
        for function in project.functions
        if function.name == name
        and (
            module is None
            or _module_matches(function.file, module)
        )
    ]

    return [
        _function_to_unit(function)
        for function in candidates
    ]


def _resolve_classes(
    name: str,
    project: Project,
    module: str | None = None,
) -> list[RetrievalUnit]:

    candidates = [
        cls
        for cls in project.classes
        if cls.name == name
        and (
            module is None
            or _module_matches(cls.file, module)
        )
    ]

    return [
        _class_to_unit(cls)
        for cls in candidates
    ]


def resolve_relationship(
    relationship: Relationship,
    project: Project,
) -> list[RetrievalUnit]:

    if relationship.kind == RelationshipKind.FUNCTION_CALL:
        return _resolve_functions(
            relationship.name,
            project,
        )

    if relationship.kind == RelationshipKind.CLASS_REFERENCE:
        return _resolve_classes(
            relationship.name,
            project,
        )

    if relationship.kind == RelationshipKind.IMPORT:

        if relationship.module is None:
            return (
                _resolve_functions(
                    relationship.name,
                    project,
                )
                + _resolve_classes(
                    relationship.name,
                    project,
                )
            )

        return (
            _resolve_functions(
                relationship.name,
                project,
                relationship.module,
            )
            + _resolve_classes(
                relationship.name,
                project,
                relationship.module,
            )
        )

    return []