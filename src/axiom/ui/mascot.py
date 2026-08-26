from pathlib import Path

from PIL import Image
from rich.style import Style
from rich.text import Text


# ---------------------------------------------------------
# Byte — AXIOM mascot
# ---------------------------------------------------------

ASSET_PATH = Path(__file__).parent / "assets" / "axiom_cat_mascot.png"

# Byte uses one solid terminal color.
BYTE_COLOR = "#2EDCC6"

# Ignore extremely faint transparent pixels.
ALPHA_THRESHOLD = 40

# Terminal characters are taller than they are wide.
PIXEL_ASPECT_RATIO = 0.95


def render_byte(width: int = 20) -> Text:
    """
    Render Byte as terminal-friendly pixel art.

    The PNG is treated as a binary mask:
        visible pixel     -> AXIOM mint
        transparent pixel -> terminal background

    Two vertical image pixels are represented by one Unicode
    half-block character.
    """

    image = Image.open(ASSET_PATH).convert("RGBA")

    # -----------------------------------------------------
    # Crop transparent padding
    # -----------------------------------------------------

    alpha = image.getchannel("A")
    bbox = alpha.getbbox()

    if bbox:
        image = image.crop(bbox)

    # -----------------------------------------------------
    # Resize for terminal character proportions
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Convert image pixels → Unicode half blocks
    # -----------------------------------------------------

    for y in range(0, height, 2):

        for x in range(width):

            top = image.getpixel((x, y))

            if y + 1 < height:
                bottom = image.getpixel((x, y + 1))
            else:
                bottom = (0, 0, 0, 0)

            top_visible = _is_byte_pixel(top)
            bottom_visible = _is_byte_pixel(bottom)

            if top_visible and bottom_visible:
                result.append(
                    "█",
                    style=Style(color=BYTE_COLOR),
                )

            elif top_visible:
                result.append(
                    "▀",
                    style=Style(color=BYTE_COLOR),
                )

            elif bottom_visible:
                result.append(
                    "▄",
                    style=Style(color=BYTE_COLOR),
                )

            else:
                result.append(" ")

        result.append("\n")

    return result

def _is_byte_pixel(pixel: tuple[int, int, int, int]) -> bool:
    """
    Determine whether a pixel belongs to Byte.

    Byte is a single-color mascot, so dark pixels such as the
    eyes are treated as transparent cutouts.
    """

    r, g, b, a = pixel

    if a <= ALPHA_THRESHOLD:
        return False

    # Ignore black/dark pixels used for Byte's eyes.
    return max(r, g, b) > 80