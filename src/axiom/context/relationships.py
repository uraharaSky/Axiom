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
    module: str | None = None

def analyze_relationships(
    unit: RetrievalUnit,
    project:Project,
) -> list[Relationship]:

    source_lines = unit.file.read_text(
        encoding="utf-8"
    ).splitlines()

    unit_source = "\n".join(
        source_lines[unit.start_line - 1:unit.end_line]
    )

    file_source = "\n".join(source_lines)

    unit_tree = ast.parse(unit_source)
    file_tree = ast.parse(file_source)

    relationships: list[Relationship] = []

    for node in ast.walk(unit_tree):

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

    for node in ast.walk(file_tree):

        if isinstance(node, ast.Import):

            for alias in node.names:
                relationships.append(
                    Relationship(
                        kind=RelationshipKind.IMPORT,
                        name=alias.name,
                        source=unit,
                    )
                )

        elif isinstance(node, ast.ImportFrom):

            for alias in node.names:
                relationships.append(
                    Relationship(
                        kind=RelationshipKind.IMPORT,
                        name=alias.name,
                        source=unit,
                    )
                )

    relationships.extend(
        _discover_module_references(
            unit_tree,
            file_tree,
            unit,
        )
    )

    return relationships

def _discover_module_references(
    unit_tree: ast.AST,
    file_tree: ast.AST,
    unit: RetrievalUnit,
) -> list[Relationship]:

    imports: dict[str, str] = {}

    for node in ast.walk(file_tree):

        if isinstance(node, ast.Import):

            for alias in node.names:
                local_name = alias.asname or alias.name.split(".")[0]
                imports[local_name] = alias.name

        elif isinstance(node, ast.ImportFrom):

            # These are symbol imports, not module imports.
            # They are already handled by IMPORT relationships.
            continue

    relationships: list[Relationship] = []

    for node in ast.walk(unit_tree):

        if not isinstance(node, ast.Attribute):
            continue

        if not isinstance(node.value, ast.Name):
            continue

        module_alias = node.value.id

        if module_alias not in imports:
            continue

        relationships.append(
            Relationship(
                kind=RelationshipKind.IMPORT,
                name=node.attr,
                source=unit,
                module=imports[module_alias],
            )
        )

    return relationships
