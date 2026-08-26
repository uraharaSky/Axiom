from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from axiom.ui.console import console
from axiom.ui.mascot import render_byte


AXIOM_LOGO = r"""
 █████╗  ██╗  ██╗ ██╗  ██████╗  ███╗   ███╗
██╔══██╗ ╚██╗██╔╝ ██║ ██╔═══██╗ ████╗ ████║
███████║  ╚███╔╝  ██║ ██║   ██║ ██╔████╔██║
██╔══██║  ██╔██╗  ██║ ██║   ██║ ██║╚██╔╝██║
██║  ██║ ██╔╝ ██╗ ██║ ╚██████╔╝ ██║ ╚═╝ ██║
╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝  ╚═════╝  ╚═╝     ╚═╝
"""


def show_welcome() -> None:
    """Render the AXIOM introductory CLI screen."""

    console.clear()

    # ---------------------------------------------------------
    # Welcome message
    # ---------------------------------------------------------

    welcome = Text()
    welcome.append("◆ ", style="bold bright_cyan")
    welcome.append(
        "Welcome to ",
        style="white",
    )
    welcome.append(
        "AXIOM",
        style="bold bright_cyan",
    )
    welcome.append(
        " — Autonomous Testing Intelligence",
        style="white",
    )

    console.print(
        Panel(
            welcome,
            border_style="bright_cyan",
            padding=(0, 1),
        )
    )

    # ---------------------------------------------------------
    # Logo + mascot
    # ---------------------------------------------------------

    logo = Text(
        AXIOM_LOGO,
        style="bold bright_cyan",
    )

    mascot = Align(
        render_byte(width=32),
        vertical="middle",
        # horizontal="left",
        # pad=(3, 0),
    )

    identity = Table.grid(
        padding=(0, 3),
        expand=False,
    )

    identity.add_column(justify="left")
    identity.add_column(justify="left")

    identity.add_row(
        Align(
            logo,
            vertical="middle",
            # horizontal="left",
        ),
        mascot,
    )

    console.print(identity)

    # ---------------------------------------------------------
    # Description
    # ---------------------------------------------------------

    description = Text()

    description.append(
        "◆ AXIOM CLI\n\n",
        style="bold bright_cyan",
    )

    description.append(
        "AI-powered autonomous testing engine that discovers ",
        style="white",
    )

    description.append(
        "application behavior",
        style="bold",
    )

    description.append(
        ", challenges assumptions, and evolves your test suite.",
        style="white",
    )

    console.print(
        Panel(
            description,
            border_style="bright_cyan",
            padding=(1, 2),
        )
    )

    # ---------------------------------------------------------
    # Quick start
    # ---------------------------------------------------------

    quick_start = Table(
        show_header=True,
        header_style="bold bright_cyan",
        box=None,
        padding=(0, 1),
    )

    quick_start.add_column("COMMAND", style="bold")
    quick_start.add_column("DESCRIPTION", style="dim")

    quick_start.add_row(
        "axiom scan <path>",
        "Discover your application",
    )

    quick_start.add_row(
        "axiom --help",
        "Show available commands",
    )

    quick_start.add_row(
        "axiom version",
        "Show AXIOM version",
    )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    status = Text()

    status.append("STATUS\n\n", style="bold bright_cyan")
    status.append("✓ ", style="green")
    status.append("Ready\n", style="white")

    status.append("◆ ", style="bright_cyan")
    status.append("Intelligent\n", style="white")

    status.append("⚡ ", style="yellow")
    status.append("Relentless", style="white")

    lower = Columns(
        [
            Group(
                Text("QUICK START", style="bold bright_cyan"),
                quick_start,
            ),
            status,
        ],
        expand=True,
        equal=True,
    )

    console.print(lower)

    console.print(Rule(style="dim"))

    console.print(
        Text(
            "  axiom › ",
            style="bold bright_cyan",
        )
    )