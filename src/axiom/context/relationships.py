from dataclasses import dataclass

import ast
from  axiom.scanner.models import Project

from enum import Enum

from axiom.context.models import RetrievalUnit

class RelationshipKind(Enum):
    FUNCTION_CALL = "function_call"
    CLASS_REFERENCE = "class_reference"
    IMPORT = "import"

@dataclass
class Relationship:
    kind: RelationshipKind
    name: str
    source: RetrievalUnit

def analyze_relationships(
    unit: RetrievalUnit,
    project,
) -> list[Relationship]:

    source_lines = unit.file.read_text(
        encoding="utf-8"
    ).splitlines()

    source = "\n".join(
        source_lines[unit.start_line - 1:unit.end_line]
    )

    tree = ast.parse(source)

    relationships: list[Relationship] = []

    for node in ast.walk(tree):

        if not isinstance(node, ast.Call):
            continue

        if isinstance(node.func, ast.Name):
            name = node.func.id

            is_class = any(
                cls.name == name
                for cls in project.classes
            )

            kind = (
                RelationshipKind.CLASS_REFERENCE
                if is_class
                else RelationshipKind.FUNCTION_CALL
            )

            relationships.append(
                Relationship(
                    kind=kind,
                    name=name,
                    source=unit,
                )
            )

    return relationships

