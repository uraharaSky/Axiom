import ast
from pathlib import Path

def parse_python_file(path: Path) -> ast.AST:
    """
    Parse a Python source file into an Abstract Syntax Tree.
    """

    source = path.read_text(encoding="utf-8")

    tree = ast.parse(
        source,
        filename=str(path),
    )

    return tree