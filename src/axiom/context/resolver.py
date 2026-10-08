from idlelib.debugger_r import close_subprocess_debugger

from axiom.context.models import RetrievalUnit
from axiom.context.relationships import (
    Relationship,
    RelationshipKind,
)
from axiom.scanner.models import Project


def resolve_relationship(
    relationship: Relationship,
    project: Project,
) -> list[RetrievalUnit]:

    if relationship.kind == RelationshipKind.FUNCTION_CALL:

        candidates = [
            function
            for function in project.functions
            if function.name == relationship.name
        ]

        return [
            RetrievalUnit(
                id=f"{function.file}:{function.line}",
                kind="function",
                name=function.name,
                file=function.file,
                start_line=function.line,
                end_line=function.end_line,
            )
            for function in candidates
        ]

    if relationship.kind == RelationshipKind.CLASS_REFERENCE:

        candidates = [
            cls
            for cls in project.classes
            if cls.name == relationship.name
        ]

        return [
            RetrievalUnit(
                id=f"{cls.file}:{cls.line}",
                kind="class",
                name=cls.name,
                file=cls.file,
                start_line=cls.line,
                end_line=cls.end_line,
            )
            for cls in candidates
        ]

    if relationship.kind == RelationshipKind.IMPORT:
        function_candidates = [
            function
            for function in project.functions
            if function.name == relationship.name
        ]

        class_candidates = [
            cls
            for cls in project.classes
            if cls.name == relationship.name
        ]

        return [
            RetrievalUnit(
                id=f"{function.file}:{function.line}",
                kind="function",
                name=function.name,
                file=function.file,
                start_line=function.line,
                end_line=function.end_line,
            )
            for function in function_candidates
        ] + [
            RetrievalUnit(
                id=f"{cls.file}:{cls.line}",
                kind="class",
                name=cls.name,
                file=cls.file,
                start_line=cls.line,
                end_line=cls.end_line,
            )
            for cls in class_candidates
        ]

    return []

