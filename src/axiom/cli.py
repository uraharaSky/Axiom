import typer

from axiom.ui.console import console
from axiom.ui.welcome import show_welcome
from pathlib import Path

from axiom.ui.project_view import build_project_tree
from axiom.scanner.project import (
    scan_project,
    project_parse,
)


app = typer.Typer(
    name="axiom",
    help="AI-powered autonomous testing engine.",
    no_args_is_help=False,
)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    AXIOM — Autonomous Testing Intelligence.
    """

    if ctx.invoked_subcommand is None:
        show_welcome()


@app.command()
def version() -> None:
    """Show AXIOM version."""

    typer.echo("AXIOM v0.1.0")

@app.command()
def scan(path: Path):
    """Discover and analyze an application."""

    if not path.exists():
        console.print(
            f"[red]Path does not exist:[/red] {path}"
        )
        raise typer.Exit(code=1)

    if not path.is_dir():
        console.print(
            f"[red]Path is not a directory:[/red] {path}"
        )
        raise typer.Exit(code=1)

    project = scan_project(path)
    project = project_parse(project)

    tree = build_project_tree(project)

    console.print(tree)


if __name__ == "__main__":
    app()