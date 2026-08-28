from rich.tree import Tree
from axiom.scanner.models import SourceFile, Route


from rich.tree import Tree

from axiom.scanner.models import Route, SourceFile


def build_source_tree(
        source_file: SourceFile,
        routes: list[Route],
) -> Tree:

    tree = Tree(
        f"[bold]{source_file.path}[/bold]"
    )

    imports = tree.add(
        "[cyan]Imports[/cyan]"
    )

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