import shutil
import subprocess
import os

from pywal import reload

from . import util
from .config import FORMAT_DIR, HOME


def xrdb():
    """Merges both a user's .Xresources and pywal's."""
    reload.xrdb([
        os.path.join(FORMAT_DIR, "colors.Xresources"),
        os.path.join(HOME, ".Xresources")
    ])


def tint2():
    """Reloads tint2 configuration on the fly."""
    if shutil.which("tint2") and util.get_pid("tint2"):
        subprocess.Popen(["pkill", "-SIGUSR1", "tint2"])


def dunst():
    """Kills dunst so that notify-send reloads it when called."""
    if shutil.which("dunst") and util.get_pid("dunst"):
        subprocess.Popen(["killall", "dunst"])


def openbox():
    """Reloads openbox configuration to reload theme"""
    if shutil.which("openbox") and util.get_pid("openbox"):
        subprocess.Popen(["openbox", "--reconfigure"])


def all():
    """Calls all possible reload methods at once."""
    tint2()
    dunst()
    openbox()
    reload.i3()
    reload.gtk()
    reload.polybar()
    reload.sway()
