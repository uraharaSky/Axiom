import ast
from pathlib import Path

from axiom.scanner.python.models import Route, Parameter, Function, Import, Class


def parse_python_file(path: Path) -> ast.AST:
    """
    Parse a Python source file into an Abstract Syntax Tree.
    """

    source = path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(
            source,
            filename=str(path),
        )

    except SyntaxError as error:
        line = error.lineno or 0
        column = error.offset or 0

        raise SyntaxError(
            f"\n"
            f"Parse Error\n"
            f"\n"
            f"File: {path}\n"
            f"Line: {line}, Column: {column}\n"
            f"\n"
            f"{error.msg}"
        ) from error

    return tree

def get_annotation_name(
        annotation: ast.expr | None,
) -> str | None :

        if annotation is None:
            return None

        if isinstance(annotation, ast.Name):
            return annotation.id

        return None


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

            parameters = []

            for argument in node.args.args:
                parameter_type = get_annotation_name(
                    argument.annotation
                )

                parameters.append(
                    Parameter(
                        name=argument.arg,
                        type=parameter_type,
                    )
                )

            routes.append(
                Route(
                method = method,
                path = path_node.value,
                function = node.name,
                file = file,
                line = node.lineno,
                parameters=parameters,
                )
            )

    return routes

def discover_functions(
        tree: ast.AST,
        file: Path,
) -> list[Function]:

    functions: list[Function] = []

    for node in ast.walk(tree):

        if not isinstance(node, ast.FunctionDef):
            continue

        parameters = []

        for argument in node.args.args:

            parameter_type = None

            if isinstance(argument.annotation, ast.Name):
                parameter_type = argument.annotation.id

            parameters.append(
                Parameter(
                    name=argument.arg,
                    type=parameter_type,
                )
            )

        functions.append(
            Function(
                name=node.name,
                file=file,
                line=node.lineno,
                parameters=parameters,
            )
        )

    return functions

def discover_imports(
        tree: ast. AST,
        file: Path,
) -> list[Import]:

    imports: list[Import] = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:
                imports.append(
                    Import(
                        module = alias.name,
                        file = file,
                    )
                )

        elif isinstance(node, ast.ImportFrom):

            names = [
                alias.name
                for alias in node.names
            ]

            imports.append(
                Import(
                    module = node.module or "",
                    file = file,
                    names = names,
                )
            )
    return imports

def discover_classes(
        tree: ast.AST,
        file: Path,
) -> list[Class]:

    classes: list[Class] = []

    for node in ast.walk(tree):

        if not isinstance(node, ast.ClassDef):
            continue

        methods: list[Function] = []

        for child in node.body:

            if not isinstance(child, ast.FunctionDef):
                continue

            parameters = []

            for argument in child.args.args:

                parameter_type = None

                if isinstance(argument.annotation, ast.Name):
                    parameter_type = argument.annotation.id

                parameters.append(
                    Parameter(
                        name=argument.arg,
                        type=parameter_type,
                    )
                )

            methods.append(
                Function(
                    name=child.name,
                    file=file,
                    line=child.lineno,
                    parameters=parameters,
                )
            )

        classes.append(
            Class(
                name=node.name,
                file=file,
                line=node.lineno,
                methods=methods,
            )
        )

    return classes