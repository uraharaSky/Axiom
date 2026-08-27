import ast
from pathlib import Path

from axiom.scanner.models import Route


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

def discover_routes(
        tree: ast.AST,
        file: Path,
) -> list[Route]:
    routes: list[Route] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue

        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue

            if not decorator.args:
                continue

            method = decorator.func.attr.upper()

            path_node = decorator.args[0]

            if not isinstance(path_node, ast.Constant):
                continue

            if not isinstance(path_node.value, str):
                continue

            routes.append(
                Route(
                method = method,
                path = path_node.value,
                function = node.name,
                file = file,
                line = node.lineno,
                )
            )

    return routes
