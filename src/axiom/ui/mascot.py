from pathlib import Path

from PIL import Image
from rich.style import Style
from rich.text import Text


# AXIOM mascot asset.
# Place the image at:
# src/axiom/ui/assets/byte.png
ASSET_PATH = Path(__file__).parent / "assets" / "axiom_cat_mascot.png"

# Terminal character cells are taller than they are wide.
# This keeps Byte's proportions visually balanced.
PIXEL_ASPECT_RATIO = 0.95

# Alpha threshold used to decide whether a pixel belongs to Byte.
ALPHA_THRESHOLD = 40


def render_byte(width: int = 32) -> Text:
    """
    Render Byte, the AXIOM mascot, as terminal-friendly pixel art.

    The source image is converted into Unicode half-block characters:
        ▀  top half
        ▄  bottom half

    Two vertical image pixels are represented by one terminal
    character cell while preserving transparency.
    """

    image = Image.open(ASSET_PATH).convert("RGBA")

    # Remove unused transparent space around Byte.
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()

    if bbox:
        image = image.crop(bbox)

    # Compensate for the non-square shape of terminal characters.
    height = max(
        2,
        int(
            image.height
            * width
            / image.width
            * PIXEL_ASPECT_RATIO
        ),
    )

    image = image.resize(
        (width, height),
        Image.Resampling.NEAREST,
    )

    result = Text()

    for y in range(0, height, 2):
        for x in range(width):
            top = image.getpixel((x, y))

            if y + 1 < height:
                bottom = image.getpixel((x, y + 1))
            else:
                bottom = (0, 0, 0, 0)

            top_visible = top[3] > ALPHA_THRESHOLD
            bottom_visible = bottom[3] > ALPHA_THRESHOLD

            if top_visible and bottom_visible:
                result.append(
                    "▀",
                    style=Style(
                        color=_rgb(top),
                        bgcolor=_rgb(bottom),
                    ),
                )

            elif top_visible:
                result.append(
                    "▀",
                    style=Style(color=_rgb(top)),
                )

            elif bottom_visible:
                result.append(
                    "▄",
                    style=Style(color=_rgb(bottom)),
                )

            else:
                result.append(" ")

        result.append("\n")

    return result


def _rgb(pixel: tuple[int, int, int, int]) -> str:
    """Convert an RGBA pixel into a Rich-compatible RGB color."""

    r, g, b, _ = pixel
    return f"#{r:02x}{g:02x}{b:02x}"