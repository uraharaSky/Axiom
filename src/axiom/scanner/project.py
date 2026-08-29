from pathlib import Path
from axiom.scanner.models import SourceFile, Project
from axiom.scanner.python_ast import (
    discover_routes,
    parse_python_file,
    discover_functions,
)

SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".go": "go",
}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".idea",
}

def scan_project(root : Path)-> Project:
    root = root.resolve()

    files: list[SourceFile] = []

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        if any(
            part in IGNORED_DIRECTORIES
            for part in path.parts
        ):
            continue

        language = SUPPORTED_EXTENSIONS.get(path.suffix)

        if language is None:
            continue

        files.append(
            SourceFile(
                path = path,
                language = language,
            )
        )

    return Project(
        root = root,
        name = root.name,
        files = files,
        language = language,
    )

def project_parse(project: Project) -> Project:
    for source_file in project.files:

        if source_file.language != "python":
            continue

        tree = parse_python_file(
            source_file.path
        )

        routes = discover_routes(
            tree,
            source_file.path,
        )

        functions = discover_functions(
            tree,
            source_file.path,
        )

        project.routes.extend(routes)
        project.functions.extend(functions)

    return project