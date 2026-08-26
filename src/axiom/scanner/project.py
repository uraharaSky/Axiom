from pathlib import Path
from axiom.scanner.models import SourceFile, Project

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