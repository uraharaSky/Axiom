import typer

from axiom.ui.welcome import show_welcome


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


if __name__ == "__main__":
    app()