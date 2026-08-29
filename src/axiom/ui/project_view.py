from pathlib import Path

from rich.tree import Tree

from axiom.scanner.models import Project, Route
from axiom.ui.source_view import build_source_tree


def build_project_tree(project: Project) -> Tree:

    tree = Tree(
        f"[bold]{project.name}[/bold]"
    )

    directories: dict[Path, Tree] = {
        project.root: tree
    }

    for source_file in sorted(
            project.files,
            key=lambda file: file.path,
    ):

        relative_path = (
            source_file.path
            .relative_to(project.root)
        )

        current_path = project.root

        for part in relative_path.parts[:-1]:

            current_path = current_path / part

            if current_path not in directories:

                parent_path = current_path.parent

                parent_tree = directories[parent_path]

                directories[current_path] = parent_tree.add(
                    f"[bold]{part}[/bold]"
                )

        routes = [
            route
            for route in project.routes
            if route.file == source_file.path
        ]

        parent_path = current_path

        file_tree = build_source_tree(
            source_file,
            routes,
            source_file.path.name,
        )

        directories[parent_path].add(
            file_tree
        )

    return tree