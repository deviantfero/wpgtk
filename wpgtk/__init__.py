"""
wpgtk: An easy to use, colorscheme generator and wallpaper manager.
"""
from .data.config import __version__
from . import data
from . import gui

__all__ = [
    "data",
    "gui",
    "__version__",
]
