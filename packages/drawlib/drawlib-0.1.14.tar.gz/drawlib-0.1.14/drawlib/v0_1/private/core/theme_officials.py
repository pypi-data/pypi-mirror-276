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

    # primary color
    blue1 = _get_rgba_from_hex("#12152B")
    blue2 = _get_rgba_from_hex("#6D7CC5")  # fill

    # secondary color
    green1 = _get_rgba_from_hex("#0C1D1C")
    green2 = _get_rgba_from_hex("#70C2BF")  # fill

    # third color
    pink1 = _get_rgba_from_hex("#1D0C0D")
    pink2 = _get_rgba_from_hex("#C1666B")  # fill

    black1 = _get_rgba_from_hex("#0D1B2A")  # line
    black2 = _get_rgba_from_hex("#1B263B")  # fill

    white = Colors.White

    default_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=black2,
        line_style="solid",
        line_width=2,
        line_color=black2,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1,
        shape_line_color=black2,
        shape_fill_color=blue2,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=black2,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=black2,
    )

    blue_template = default_template.copy()
    blue_template.icon_color = blue2
    blue_template.line_color = blue2
    blue_template.shapetext_color = blue2
    blue_template.text_color = blue2

    green_template = default_template.copy()
    green_template.icon_color = green2
    green_template.line_color = green2
    green_template.shape_fill_color = green2
    green_template.shapetext_color = green2
    green_template.text_color = green2

    pink_template = default_template.copy()
    pink_template.icon_color = pink2
    pink_template.line_color = pink2
    pink_template.shape_fill_color = pink2
    pink_template.shapetext_color = pink2
    pink_template.text_color = pink2

    black_template = default_template.copy()
    black_template.icon_color = black2
    black_template.line_color = black2
    black_template.shape_line_color = black1
    black_template.shape_fill_color = black2
    black_template.shapetext_color = black2
    black_template.text_color = black2

    white_template = default_template.copy()
    white_template.icon_color = white
    white_template.line_color = white
    white_template.shape_line_color = black2
    white_template.shape_fill_color = white
    white_template.shapetext_color = white
    white_template.text_color = white

    return OfficialThemeStyle(
        default_style=_generate_styles(default_template),
        named_styles=[
            ("blue", _generate_styles(blue_template)),
            ("green", _generate_styles(green_template)),
            ("pink", _generate_styles(pink_template)),
            ("black", _generate_styles(black_template)),
            ("white", _generate_styles(white_template)),
        ],
        theme_colors=[
            ("default", blue2),
            ("blue", blue2),
            ("blue1", blue1),
            ("blue2", blue2),
            ("green", green2),
            ("green1", green1),
            ("green2", green2),
            ("pink", pink2),
            ("pink1", pink1),
            ("pink2", pink2),
            ("black", black2),
            ("black1", black1),
            ("black2", black2),
            ("white", white),
        ],
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


def get_flat() -> OfficialThemeStyle:
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

    default_color = peter_river
    default_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=midnight_blue,
        line_style="solid",
        line_width=2,
        line_color=midnight_blue,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1,
        shape_line_color=Colors.White,
        shape_fill_color=default_color,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=clouds,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=midnight_blue,
    )

    named_templates = []
    for name, color in [
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
    ]:
        t = default_template.copy()
        t.icon_color = color
        t.line_color = color
        if name == "clouds":
            t.shape_fill_color = Colors.White
            t.shape_line_color = midnight_blue
        else:
            t.shape_fill_color = color
        t.text_color = color
        named_templates.append((name, t))

    named_styles = []
    for name, template in named_templates:
        named_styles.append((name, _generate_styles(template)))

    return OfficialThemeStyle(
        default_style=_generate_styles(default_template),
        named_styles=named_styles,
        theme_colors=[
            ("default", peter_river),
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
        ],
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

    black_template = default_template.copy()
    black_template.shape_line_width = 0
    black_template.shape_fill_color = black
    black_style = _generate_styles(black_template)

    gray1_template = default_template.copy()
    gray1_template.line_color = gray1
    gray1_template.shape_line_width = 0
    gray1_template.shape_fill_color = gray1
    gray1_template.shapetext_color = gray1
    gray1_template.text_color = gray1
    gray1_style = _generate_styles(gray1_template)

    gray2_template = default_template.copy()
    gray2_template.line_color = gray2
    gray2_template.shape_line_width = 0
    gray2_template.shape_fill_color = gray2
    gray2_template.shapetext_color = gray2
    gray2_template.text_color = gray2
    gray2_style = _generate_styles(gray2_template)

    gray3_template = default_template.copy()
    gray3_template.line_color = gray3
    gray3_template.shape_line_width = 0
    gray3_template.shape_fill_color = gray3
    gray3_template.shapetext_color = gray3
    gray3_template.text_color = gray3
    gray3_style = _generate_styles(gray3_template)

    white_template = default_template.copy()
    white_template.line_color = white
    white_template.shape_line_width = 0
    white_template.shape_fill_color = white
    white_template.shapetext_color = white
    white_template.text_color = white
    white_style = _generate_styles(white_template)

    black_solid_template = default_template.copy()
    black_solid_template.line_color = black
    black_solid_template.shape_line_color = black
    black_solid_template.shape_fill_color = white
    black_solid_style = _generate_styles(black_solid_template)
    black_solid_style.iconstyle = None
    black_solid_style.shapetextstyle = None
    black_solid_style.textstyle = None

    black_dashed_template = default_template.copy()
    black_dashed_template.line_color = black
    black_dashed_template.line_style = "dashed"
    black_dashed_template.shape_line_color = black
    black_dashed_template.shape_fill_color = white
    black_dashed_template.shape_line_style = "dashed"
    black_dashed_style = _generate_styles(black_dashed_template)
    black_dashed_style.iconstyle = None
    black_dashed_style.shapetextstyle = None
    black_dashed_style.textstyle = None

    gray1_solid_template = default_template.copy()
    gray1_solid_template.line_color = gray1
    gray1_solid_template.shape_line_color = gray1
    gray1_solid_template.shape_fill_color = white
    gray1_solid_style = _generate_styles(gray1_solid_template)
    gray1_solid_style.iconstyle = None
    gray1_solid_style.shapetextstyle = None
    gray1_solid_style.textstyle = None

    gray1_dashed_template = default_template.copy()
    gray1_dashed_template.line_color = gray1
    gray1_dashed_template.line_style = "dashed"
    gray1_dashed_template.shape_line_color = gray1
    gray1_dashed_template.shape_fill_color = white
    gray1_dashed_template.shape_line_style = "dashed"
    gray1_dashed_style = _generate_styles(gray1_dashed_template)
    gray1_dashed_style.iconstyle = None
    gray1_dashed_style.shapetextstyle = None
    gray1_dashed_style.textstyle = None

    gray2_solid_template = default_template.copy()
    gray2_solid_template.line_color = gray2
    gray2_solid_template.shape_line_color = gray2
    gray2_solid_template.shape_fill_color = white
    gray2_solid_style = _generate_styles(gray2_solid_template)
    gray2_solid_style.iconstyle = None
    gray2_solid_style.shapetextstyle = None
    gray2_solid_style.textstyle = None

    gray2_dashed_template = default_template.copy()
    gray2_dashed_template.line_color = gray2
    gray2_dashed_template.line_style = "dashed"
    gray2_dashed_template.shape_line_color = gray2
    gray2_dashed_template.shape_fill_color = white
    gray2_dashed_template.shape_line_style = "dashed"
    gray2_dashed_style = _generate_styles(gray2_dashed_template)
    gray2_dashed_style.iconstyle = None
    gray2_dashed_style.shapetextstyle = None
    gray2_dashed_style.textstyle = None

    gray3_solid_template = default_template.copy()
    gray3_solid_template.line_color = gray3
    gray3_solid_template.shape_line_color = gray3
    gray3_solid_template.shape_fill_color = white
    gray3_solid_style = _generate_styles(gray3_solid_template)
    gray3_solid_style.iconstyle = None
    gray3_solid_style.shapetextstyle = None
    gray3_solid_style.textstyle = None

    gray3_dashed_template = default_template.copy()
    gray3_dashed_template.line_color = gray3
    gray3_dashed_template.line_style = "dashed"
    gray3_dashed_template.shape_line_color = gray3
    gray3_dashed_template.shape_fill_color = white
    gray3_dashed_template.shape_line_style = "dashed"
    gray3_dashed_style = _generate_styles(gray3_dashed_template)
    gray3_dashed_style.iconstyle = None
    gray3_dashed_style.shapetextstyle = None
    gray3_dashed_style.textstyle = None

    white_solid_template = default_template.copy()
    white_solid_template.line_color = white
    white_solid_template.shape_line_color = white
    white_solid_template.shape_fill_color = Colors.Transparent
    white_solid_style = _generate_styles(white_solid_template)
    white_solid_style.iconstyle = None
    white_solid_style.shapetextstyle = None
    white_solid_style.textstyle = None

    white_dashed_template = default_template.copy()
    white_dashed_template.line_color = white
    white_dashed_template.line_style = "dashed"
    white_dashed_template.shape_line_color = white
    white_dashed_template.shape_fill_color = Colors.Transparent
    white_dashed_template.shape_line_style = "dashed"
    white_dashed_style = _generate_styles(white_dashed_template)
    white_dashed_style.iconstyle = None
    white_dashed_style.shapetextstyle = None
    white_dashed_style.textstyle = None

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=[
            ("black", black_style),
            ("black_solid", black_solid_style),
            ("black_dashed", black_dashed_style),
            ("gray1", gray1_style),
            ("gray1_solid", gray1_solid_style),
            ("gray1_dashed", gray1_dashed_style),
            ("gray2", gray2_style),
            ("gray2_solid", gray2_solid_style),
            ("gray2_dashed", gray2_dashed_style),
            ("gray3", gray3_style),
            ("gray3_solid", gray3_solid_style),
            ("gray3_dashed", gray3_dashed_style),
            ("white", white_style),
            ("white_solid", white_solid_style),
            ("white_dashed", white_dashed_style),
        ],
        theme_colors=[
            ("default", black),
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
            lwidth=0,
            lstyle=template.shape_line_style,
            lcolor=template.shape_line_color,
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
            color=template.text_color,
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
