import pathlib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Parameter:
    name: str
    type: str | None = None

@dataclass
class Route:
    method: str
    path: str
    function: str
    file: Path
    line: int
    parameters: list[Parameter] = field(default_factory = list)

@dataclass
class SourceFile:
    path: Path
    language: str


@dataclass
class Project:
    root: Path
    name: str
    language: str
    framework: str | None = None
    files: list[SourceFile] = field(default_factory=list)
    routes: list[Route] = field(default_factory=list)