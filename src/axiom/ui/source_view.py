from rich.tree import Tree

from axiom.scanner.models import (
    Class,
    Function,
    Import,
    Route,
    SourceFile,
)


def build_source_tree(
    source_file: SourceFile,
    functions: list[Function],
    classes: list[Class],
    imports: list[Import],
    routes: list[Route],
    path_label: str | None = None,
) -> Tree:

    path = path_label or source_file.path.as_posix()

    tree = Tree(
        f"[bold]{path}[/bold]"
    )

    if imports:
        imports_tree = tree.add(
            "[cyan]Imports[/cyan]"
        )

        for imported in imports:
            import_tree = imports_tree.add(
                f"[white]{imported.module}[/white]"
            )

            for name in imported.names:
                import_tree.add(
                    f"[dim]{name}[/dim]"
                )

    if classes:
        classes_tree = tree.add(
            "[cyan]Classes[/cyan]"
        )

        for cls in classes:
            class_tree = classes_tree.add(
                f"[white]{cls.name}[/white]"
            )

            if cls.methods:
                methods_tree = class_tree.add(
                    "[cyan]Methods[/cyan]"
                )

                for method in cls.methods:
                    methods_tree.add(
                        f"[white]{method.name}()[/white]"
                    )

    if functions:
        functions_tree = tree.add(
            "[cyan]Functions[/cyan]"
        )

        for function in functions:
            functions_tree.add(
                f"[white]{function.name}()[/white]"
            )

    if routes:
        routes_tree = tree.add(
            "[cyan]Routes[/cyan]"
        )

        for route in routes:

            method_style = {
                "GET": "green",
                "POST": "yellow",
                "PUT": "blue",
                "PATCH": "magenta",
                "DELETE": "red",
            }.get(route.method, "white")

            route_tree = routes_tree.add(
                f"[{method_style}]{route.method}[/{method_style}] "
                f"[white]{route.path}[/white]"
            )

            route_tree.add(
                f"[bright_cyan]Function:[/bright_cyan] "
                f"[white]{route.function}()[/white]"
            )

            if route.parameters:
                parameters = route_tree.add(
                    "[cyan]Parameters[/cyan]"
                )

                for parameter in route.parameters:

                    parameter_type = (
                        parameter.type
                        if parameter.type is not None
                        else "unknown"
                    )

                    parameters.add(
                        f"[white]{parameter.name}[/white]"
                        f": "
                        f"[dim cyan]{parameter_type}[/dim cyan]"
                    )

    return tree