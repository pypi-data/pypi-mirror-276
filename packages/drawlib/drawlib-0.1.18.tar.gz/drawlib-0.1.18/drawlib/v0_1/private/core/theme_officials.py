from __future__ import annotations
import dataclasses
from typing import Optional, Dict, Tuple, Union, Literal, List
from copy import deepcopy

from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    LineArrowStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
    ThemeStyles,
    OfficialThemeStyle,
)
from drawlib.v0_1.private.core.fonts import (
    FontBase,
    Font,
    FontSourceCode,
)
from drawlib.v0_1.private.core.colors import Colors

#######################
### Official Themes ###
#######################


def get_default() -> OfficialThemeStyle:
    """Change theme to default.

    Returns:
        None

    """

    # blue, green, pink
    # https://coolors.co/6d7cc5-70c2bf-e4dfda-d4b483-c1666b

    # black
    # https://coolors.co/palette/0d1b2a-1b263b-415a77-778da9-e0e1dd

    blue = _get_rgba_from_hex("#6D7CC5")
    green = _get_rgba_from_hex("#70C2BF")
    pink = _get_rgba_from_hex("#C1666B")
    black = _get_rgba_from_hex("#1B263B")  # fill
    white = Colors.White

    default_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=black,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1,
        shape_line_color=black,
        shape_fill_color=blue,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=black,
    )

    blue_style = _get_fill_style(default_template, blue)
    green_style = _get_fill_style(default_template, green)
    pink_style = _get_fill_style(default_template, pink)
    black_style = _get_fill_style(default_template, black, white)
    white_style = _get_fill_style(default_template, white)

    return OfficialThemeStyle(
        default_style=_generate_styles(default_template),
        named_styles=[
            ("blue", blue_style),
            ("green", green_style),
            ("pink", pink_style),
            ("black", black_style),
            ("white", white_style),
        ],
        theme_colors=[
            ("blue", blue),
            ("green", green),
            ("pink", pink),
            ("black", black),
            ("white", white),
        ],
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


def get_simple() -> OfficialThemeStyle:
    """Change theme to default.

    Returns:
        None

    """

    # blue, green, pink
    # https://coolors.co/6d7cc5-70c2bf-e4dfda-d4b483-c1666b

    # black
    # https://coolors.co/palette/0d1b2a-1b263b-415a77-778da9-e0e1dd

    blue = _get_rgba_from_hex("#6D7CC5")
    green = _get_rgba_from_hex("#70C2BF")
    pink = _get_rgba_from_hex("#C1666B")
    black = _get_rgba_from_hex("#1B263B")
    white = Colors.White

    default_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=black,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1,
        shape_line_color=black,
        shape_fill_color=blue,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=black,
    )
    default_style = _generate_styles(default_template)
    default_flat_style = _get_flat_style(default_template, blue)
    default_solid_style = _get_solid_style(default_template, black, has_imagestyle=True)
    default_dashed_style = _get_dashed_style(default_template, black)

    blue_style = _get_fill_style(default_template, blue)
    blue_flat_style = _get_flat_style(default_template, blue)
    blue_solid_style = _get_solid_style(default_template, blue)
    blue_dashed_style = _get_dashed_style(default_template, blue)

    green_style = _get_fill_style(default_template, green)
    green_flat_style = _get_flat_style(default_template, green)
    green_solid_style = _get_solid_style(default_template, green)
    green_dashed_style = _get_dashed_style(default_template, green)

    pink_style = _get_fill_style(default_template, pink)
    pink_flat_style = _get_flat_style(default_template, pink)
    pink_solid_style = _get_solid_style(default_template, pink)
    pink_dashed_style = _get_dashed_style(default_template, pink)

    black_style = _get_fill_style(default_template, black, white)
    black_flat_style = _get_flat_style(default_template, black)
    black_solid_style = _get_solid_style(default_template, black)
    black_dashed_style = _get_dashed_style(default_template, black)

    white_style = _get_fill_style(default_template, white)
    white_flat_style = _get_flat_style(default_template, white)
    white_solid_style = _get_solid_style(default_template, white)
    white_dashed_style = _get_dashed_style(default_template, white)

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=[
            ("flat", default_flat_style),
            ("solid", default_solid_style),
            ("dashed", default_dashed_style),
            # blue
            ("blue", blue_style),
            ("blue_flat", blue_flat_style),
            ("blue_solid", blue_solid_style),
            ("blue_dashed", blue_dashed_style),
            # green
            ("green", green_style),
            ("green_flat", green_flat_style),
            ("green_solid", green_solid_style),
            ("green_dashed", green_dashed_style),
            # pink
            ("pink", pink_style),
            ("pink_flat", pink_flat_style),
            ("pink_solid", pink_solid_style),
            ("pink_dashed", pink_dashed_style),
            # black
            ("black", black_style),
            ("black_flat", black_flat_style),
            ("black_solid", black_solid_style),
            ("black_dashed", black_dashed_style),
            # white
            ("white", white_style),
            ("white_flat", white_flat_style),
            ("white_solid", white_solid_style),
            ("white_dashed", white_dashed_style),
        ],
        theme_colors=[
            ("blue", blue),
            ("green", green),
            ("pink", pink),
            ("black", black),
            ("white", white),
        ],
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


def get_rich() -> OfficialThemeStyle:
    # https://flatuicolors.com/palette/defo
    turquoise = (26, 188, 156)
    green_sea = (22, 160, 133)
    emerald = (46, 204, 113)
    nephritis = (39, 174, 96)
    peter_river = (52, 152, 219)
    belize_hole = (41, 128, 185)
    amethyst = (155, 89, 182)
    wisteria = (142, 68, 173)
    wet_asphalt = (52, 73, 94)
    midnight_blue = (44, 62, 80)
    sun_flower = (241, 196, 15)
    orange = (243, 156, 18)
    carrot = (230, 126, 34)
    pumpkin = (211, 84, 0)
    alizarin = (231, 76, 60)
    pomegranate = (192, 57, 43)
    clouds = (236, 240, 241)
    silver = (189, 195, 199)
    concrete = (149, 165, 166)
    asbestos = (127, 140, 141)
    black = (0, 0, 0)
    white = (255, 255, 255)

    def get_color_pairs():
        return [
            ("turquoise", turquoise),
            ("green_sea", green_sea),
            ("emerald", emerald),
            ("nephritis", nephritis),
            ("peter_river", peter_river),
            ("belize_hole", belize_hole),
            ("amethyst", amethyst),
            ("wisteria", wisteria),
            ("wet_asphalt", wet_asphalt),
            ("midnight_blue", midnight_blue),
            ("sun_flower", sun_flower),
            ("orange", orange),
            ("carrot", carrot),
            ("pumpkin", pumpkin),
            ("alizarin", alizarin),
            ("pomegranate", pomegranate),
            ("clouds", clouds),
            ("silver", silver),
            ("concrete", concrete),
            ("asbestos", asbestos),
            ("black", black),
            ("white", white),
        ]

    default_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=midnight_blue,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=midnight_blue,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1,
        shape_line_color=midnight_blue,
        shape_fill_color=peter_river,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=Colors.White,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=midnight_blue,
    )

    default_flat_style = _get_flat_style(default_template, peter_river)
    default_solid_style = _get_solid_style(default_template, midnight_blue, has_imagestyle=True)
    default_dashed_style = _get_dashed_style(default_template, midnight_blue)

    named_styles = [
        ("flat", default_flat_style),
        ("solid", default_solid_style),
        ("dashed", default_dashed_style),
    ]
    for name, color in get_color_pairs():
        if name in ["midnight_blue", "black"]:
            named_styles.append((name, _get_fill_style(default_template, color, white)))
        else:
            named_styles.append((name, _get_fill_style(default_template, color, midnight_blue)))
        named_styles.append((f"{name}_flat", _get_flat_style(default_template, color)))
        named_styles.append((f"{name}_solid", _get_solid_style(default_template, color)))
        named_styles.append((f"{name}_dashed", _get_dashed_style(default_template, color)))

    return OfficialThemeStyle(
        default_style=_generate_styles(default_template),
        named_styles=named_styles,
        theme_colors=get_color_pairs(),
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


def get_monochrome() -> OfficialThemeStyle:
    black = (0, 0, 0)
    gray1 = (64, 64, 64)
    gray2 = (128, 128, 128)
    gray3 = (192, 192, 192)
    white = (255, 255, 255)

    default_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=black,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1.5,
        shape_line_color=black,
        shape_fill_color=white,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=black,
    )

    default_style = _generate_styles(default_template)
    default_flat_style = _get_flat_style(default_template, black)
    default_solid_style = _get_solid_style(default_template, black, has_imagestyle=True)
    default_dashed_style = _get_dashed_style(default_template, black)

    black_style = _get_fill_style(default_template, black, Colors.White)
    black_flat_style = _get_flat_style(default_template, black)
    black_solid_style = _get_solid_style(default_template, black)
    black_dashed_style = _get_dashed_style(default_template, black)

    gray1_style = _get_fill_style(default_template, gray1)
    gray1_flat_style = _get_flat_style(default_template, gray1)
    gray1_solid_style = _get_solid_style(default_template, gray1)
    gray1_dashed_style = _get_dashed_style(default_template, gray1)

    gray2_style = _get_fill_style(default_template, gray2)
    gray2_flat_style = _get_flat_style(default_template, gray2)
    gray2_solid_style = _get_solid_style(default_template, gray2)
    gray2_dashed_style = _get_dashed_style(default_template, gray2)

    gray3_style = _get_fill_style(default_template, gray3)
    gray3_flat_style = _get_flat_style(default_template, gray3)
    gray3_solid_style = _get_solid_style(default_template, gray3)
    gray3_dashed_style = _get_dashed_style(default_template, gray3)

    white_style = _get_fill_style(default_template, white)
    white_flat_style = _get_flat_style(default_template, white)
    white_solid_style = _get_solid_style(default_template, white)
    white_dashed_style = _get_dashed_style(default_template, white)

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=[
            ("flat", default_flat_style),
            ("solid", default_solid_style),
            ("dashed", default_dashed_style),
            ("black", black_style),
            ("black_flat", black_flat_style),
            ("black_solid", black_solid_style),
            ("black_dashed", black_dashed_style),
            ("gray1", gray1_style),
            ("gray1_flat", gray1_flat_style),
            ("gray1_solid", gray1_solid_style),
            ("gray1_dashed", gray1_dashed_style),
            ("gray2", gray2_style),
            ("gray2_flat", gray2_flat_style),
            ("gray2_solid", gray2_solid_style),
            ("gray2_dashed", gray2_dashed_style),
            ("gray3", gray3_style),
            ("gray3_flat", gray3_flat_style),
            ("gray3_solid", gray3_solid_style),
            ("gray3_dashed", gray3_dashed_style),
            ("white", white_style),
            ("white_flat", white_flat_style),
            ("white_solid", white_solid_style),
            ("white_dashed", white_dashed_style),
        ],
        theme_colors=[
            ("black", black),
            ("gray1", gray1),
            ("gray2", gray2),
            ("gray3", gray3),
            ("white", white),
        ],
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


############
### Data ###
############


@dataclasses.dataclass
class OfficialThemeTemplate:
    """Helper dataclass for defining theme styles"""

    def copy(self) -> OfficialThemeTemplate:
        return deepcopy(self)

    # icon
    icon_style: Literal["thin", "light", "regular", "bold", "fill"]
    icon_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]
    image_line_width: float

    # line
    line_style: Literal["solid", "dashed", "dotted", "dashdot"]
    line_width: float
    line_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]
    arrowhead_style: Literal[
        "->",
        "<-",
        "<->",
        "-|>",
        "<|-",
        "<|-|>",
    ]
    arrowhead_scale: int

    # shape
    shape_line_style: Literal["solid", "dashed", "dotted", "dashdot"]
    shape_line_width: float
    shape_line_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]
    shape_fill_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]

    # shapetext
    shapetext_font: FontBase
    shapetext_size: int
    shapetext_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]

    # text
    text_font: FontBase
    text_size: int
    text_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]


############
### Util ###
############


def _get_rgba_from_hex(hex_color: str) -> Tuple[int, int, int, float]:
    """
    Convert a hexadecimal color code to RGBA values.

    Args:
        hex_color (str): The hexadecimal color code (e.g., "#FF5733" or "#FFF").

    Returns:
        tuple[int, int, int, float]: A tuple containing the RGBA values (0-255 for R, G, B and 0.0-1.0 for A).
    """

    # Remove the '#' prefix if present
    hex_color = hex_color.lstrip("#")

    # Determine the length of the hex color code
    hex_length = len(hex_color)

    # Convert the hex code to RGB values
    if hex_length == 3:  # Short hex format (#RGB)
        r = int(hex_color[0] * 2, 16)
        g = int(hex_color[1] * 2, 16)
        b = int(hex_color[2] * 2, 16)
        a = 1.0
    elif hex_length in (6, 8):  # Full hex format (#RRGGBB)
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        if hex_length == 8:  # With alpha
            a = int(hex_color[6:8], 16)
        else:
            a = 1.0
    else:
        raise ValueError("Invalid hex color code format")

    return (r, g, b, a)


def _get_fill_style(template: OfficialThemeTemplate, color, shape_line_color=None) -> ThemeStyles:
    t = template.copy()
    t.icon_color = color
    t.image_line_width = t.line_width
    t.line_color = color
    if shape_line_color is not None:
        t.shape_line_color = shape_line_color
    t.shape_fill_color = color
    t.shapetext_color = color
    t.text_color = color
    return _generate_styles(t)


def _get_flat_style(template: OfficialThemeTemplate, color, shape_line_color=None) -> ThemeStyles:
    t = template.copy()
    t.icon_color = color
    t.line_color = color
    if shape_line_color is not None:
        t.shape_line_color = shape_line_color
    else:
        t.shape_line_color = Colors.White
    t.shape_fill_color = color
    t.shapetext_color = color
    t.text_color = color
    s = _generate_styles(t)
    s.iconstyle = None
    s.imagestyle = None
    s.linestyle = None
    s.linearrowstyle = None
    s.shapetextstyle = None
    s.textstyle = None
    return s


def _get_solid_style(template: OfficialThemeTemplate, color, has_imagestyle: bool = False) -> ThemeStyles:
    t = template.copy()
    t.image_line_width = t.line_width
    t.line_color = color
    t.shape_line_color = color
    t.shape_fill_color = Colors.Transparent
    s = _generate_styles(t)
    s.iconstyle = None
    if not has_imagestyle:
        s.imagestyle = None
    s.linestyle = None
    s.linearrowstyle = None
    s.shapetextstyle = None
    s.textstyle = None
    return s


def _get_dashed_style(template: OfficialThemeTemplate, color) -> ThemeStyles:
    t = template.copy()
    t.image_line_width = t.line_width
    t.line_color = color
    t.line_style = "dashed"
    t.shape_line_color = color
    t.shape_line_style = "dashed"
    t.shape_fill_color = Colors.Transparent
    s = _generate_styles(t)
    s.iconstyle = None
    s.shapetextstyle = None
    s.textstyle = None
    return s


def _generate_styles(
    template: OfficialThemeTemplate,
) -> ThemeStyles:
    return ThemeStyles(
        iconstyle=IconStyle(
            style=template.icon_style,
            color=template.icon_color,
            halign="center",
            valign="center",
        ),
        imagestyle=ImageStyle(
            lwidth=template.image_line_width,
            lstyle=template.line_style,
            lcolor=template.line_color,
            halign="center",
            valign="center",
        ),
        linestyle=LineStyle(
            style=template.line_style,
            width=template.line_width,
            color=template.line_color,
        ),
        linearrowstyle=LineArrowStyle(
            lstyle=template.line_style,
            lwidth=template.line_width,
            hstyle=template.arrowhead_style,
            hscale=template.arrowhead_scale,
            color=template.line_color,
        ),
        shapestyle=ShapeStyle(
            lwidth=template.shape_line_width,
            lstyle=template.shape_line_style,
            lcolor=template.shape_line_color,
            fcolor=template.shape_fill_color,
            halign="center",
            valign="center",
        ),
        shapetextstyle=ShapeTextStyle(
            font=template.text_font,
            size=template.text_size,
            color=template.shapetext_color,
            halign="center",
            valign="center",
        ),
        textstyle=TextStyle(
            font=template.text_font,
            size=template.text_size,
            color=template.text_color,
            halign="center",
            valign="center",
        ),
    )
