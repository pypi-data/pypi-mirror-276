import sys
from enum import IntEnum
from typing import Literal


class Color(IntEnum):
    black = 0
    red = 1
    green = 2
    yellow = 3
    blue = 4
    purple = 5
    cyan = 6
    white = 7


class FontStyle(IntEnum):
    default = 0
    bold = 1
    dim = 2
    italic = 3
    underline = 4
    blink = 5
    reverse = 7
    hide = 8


def _cprint(text: str, color: Color) -> None:
    sys.stdout.write(basic(text, color, end="\n"))


def basic(
    text: str,
    color: Color = Color.white,
    style: FontStyle = FontStyle.default,
    target: Literal["font", "background"] = "font",
    end="",
) -> str:
    return f"\x1b[{style};{3 if target == 'font' else 4}{color.value}m{text}{end}\x1b[{style.default}m"


def rgb(
    text: str,
    r: int = 255,
    g: int = 255,
    b: int = 255,
    style: FontStyle = FontStyle.default,
    target: Literal["font", "background"] = "font",
    end="",
) -> str:
    return f"\x1b[{style};{3 if target == 'font' else 4}8;2;{r};{g};{b}m{text}{end}\x1b[{FontStyle.default}m"
