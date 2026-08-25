import typer

app = typer.Typer(
    name="axiom",
    help="AI-powered autonomous testing engine.",
    no_args_is_help=True,
)


@app.callback()
def main():
    """
    AXIOM — AI-powered autonomous testing engine.
    """
    pass


@app.command()
def version():
    """Show AXIOM version."""
    typer.echo("AXIOM v0.1.0")


if __name__ == "__main__":
    app()