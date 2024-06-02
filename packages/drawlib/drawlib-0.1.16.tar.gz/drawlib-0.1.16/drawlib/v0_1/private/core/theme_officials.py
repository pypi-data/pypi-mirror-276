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

    black1 = _get_rgba_from_hex("#0D1B2A")  # line
    black2 = _get_rgba_from_hex("#1B263B")  # fill

    white = Colors.White

    default_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=black2,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=black2,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1,
        shape_line_color=black2,
        shape_fill_color=blue,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=black2,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=black2,
    )

    solid_template = default_template.copy()
    solid_template.image_line_width = 1
    solid_template.shape_line_width = 1.5
    solid_template.shape_fill_color = Colors.Transparent
    solid_style = _generate_styles(solid_template)
    solid_style.iconstyle = None
    solid_style.linestyle = None
    solid_style.linearrowstyle = None
    solid_style.shapetextstyle = None
    solid_style.textstyle = None

    dashed_template = solid_template.copy()
    dashed_template.line_style = "dashed"
    dashed_template.shape_line_style = "dashed"
    dashed_style = _generate_styles(dashed_template)
    dashed_style.iconstyle = None
    dashed_style.shapetextstyle = None
    dashed_style.textstyle = None

    blue_template = default_template.copy()
    blue_template.icon_color = blue
    blue_template.line_color = blue
    blue_template.shapetext_color = blue
    blue_template.text_color = blue
    blue_style = _generate_styles(blue_template)

    green_template = default_template.copy()
    green_template.icon_color = green
    green_template.line_color = green
    green_template.shape_fill_color = green
    green_template.shapetext_color = green
    green_template.text_color = green
    green_style = _generate_styles(green_template)

    pink_template = default_template.copy()
    pink_template.icon_color = pink
    pink_template.line_color = pink
    pink_template.shape_fill_color = pink
    pink_template.shapetext_color = pink
    pink_template.text_color = pink
    pink_style = _generate_styles(pink_template)

    black_template = default_template.copy()
    black_template.icon_color = black2
    black_template.line_color = black2
    black_template.shape_line_color = black1
    black_template.shape_fill_color = black2
    black_template.shapetext_color = black2
    black_template.text_color = black2
    black_style = _generate_styles(black_template)

    white_template = default_template.copy()
    white_template.icon_color = white
    white_template.line_color = white
    white_template.shape_line_color = black2
    white_template.shape_fill_color = white
    white_template.shapetext_color = white
    white_template.text_color = white
    white_style = _generate_styles(white_template)

    return OfficialThemeStyle(
        default_style=_generate_styles(default_template),
        named_styles=[
            ("solid", solid_style),
            ("dashed", dashed_style),
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
            ("black", black2),
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

    default_color = peter_river
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
        shape_line_color=Colors.White,
        shape_fill_color=default_color,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=Colors.White,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=midnight_blue,
    )

    default_outlined_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=midnight_blue,
        image_line_width=1.5,
        line_style="solid",
        line_width=2,
        line_color=midnight_blue,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1.5,
        shape_line_color=midnight_blue,
        shape_fill_color=Colors.Transparent,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=midnight_blue,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=midnight_blue,
    )

    named_templates = []
    named_templates.append(("solid", default_outlined_template))
    t = default_outlined_template.copy()
    t.line_style = "dashed"
    t.shape_line_style = "dashed"
    named_templates.append(("dashed", t))

    for name, color in get_color_pairs():
        # fill
        t1 = default_template.copy()
        t1.icon_color = color
        t1.line_color = color
        t1.shape_fill_color = color
        t1.shapetext_color = color
        t1.text_color = color
        named_templates.append((name, t1))

        # outline solid
        t2 = default_outlined_template.copy()
        t2.icon_color = color
        t2.line_color = color
        t2.shape_line_color = color
        t2.shapetext_color = color
        t2.text_color = color
        named_templates.append((f"{name}_solid", t2))

        # outline dash
        t3 = t2.copy()
        t3.line_style = "dashed"
        t3.shape_line_style = "dashed"
        named_templates.append((f"{name}_dashed", t3))

    named_styles = []
    for name, template in named_templates:
        style = _generate_styles(template)
        if "solid" in name or "dashed" in name:
            style.iconstyle = None
            style.shapetextstyle = None
            style.textstyle = None
        if "solid" in name:
            style.linestyle = None
            style.linearrowstyle = None
        named_styles.append((name, style))

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

    def get_fill_style(color) -> ThemeStyles:
        t = default_template.copy()
        t.icon_color = color
        t.line_color = color
        t.shape_line_width = 0
        t.shape_fill_color = color
        t.shapetext_color = color
        t.text_color = color
        return _generate_styles(t)

    black_style = get_fill_style(black)
    gray1_style = get_fill_style(gray1)
    gray2_style = get_fill_style(gray2)
    gray3_style = get_fill_style(gray3)
    white_style = get_fill_style(white)

    def get_solid_style(color) -> ThemeStyles:
        t = default_template.copy()
        t.line_color = color
        t.shape_line_color = color
        t.shape_fill_color = Colors.Transparent
        s = _generate_styles(t)
        s.iconstyle = None
        s.linestyle = None
        s.linearrowstyle = None
        s.shapetextstyle = None
        s.textstyle = None
        return s

    black_solid_style = get_solid_style(black)
    gray1_solid_style = get_solid_style(gray1)
    gray2_solid_style = get_solid_style(gray2)
    gray3_solid_style = get_solid_style(gray3)
    white_solid_style = get_solid_style(white)

    def get_dashed_style(color) -> ThemeStyles:
        t = default_template.copy()
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

    black_dashed_style = get_dashed_style(black)
    gray1_dashed_style = get_dashed_style(gray1)
    gray2_dashed_style = get_dashed_style(gray2)
    gray3_dashed_style = get_dashed_style(gray3)
    white_dashed_style = get_dashed_style(white)

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=[
            ("solid", black_solid_style),
            ("dashed", black_dashed_style),
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
