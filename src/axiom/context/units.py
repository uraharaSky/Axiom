from axiom.scanner.models import Project
from axiom.context.models import RetrievalUnit

def build_retrieval_units(project: Project) -> list[RetrievalUnit]:
    units = []

    for function in project.functions:
        units.append(
            RetrievalUnit(
                id = f"function:{function.file}:{function.name}",
                kind="function",
                name=function.name,
                file=function.file,
                start_line=function.line,
                end_line=function.end_line,
            )
        )

    return units