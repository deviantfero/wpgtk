import shutil
import subprocess
import os
import tempfile

from pywal import reload

from . import util
from .config import FORMAT_DIR, HOME, settings


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


def gtk3():
    if shutil.which("xsettingsd") and settings.getboolean("gtk", True):
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w+') as tmp:
                tmp.write('Net/ThemeName "FlatColor"\n')
                tmp.close()
                subprocess.call(
                    ["timeout", "0.2s", "xsettingsd", "-c", path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        finally:
            os.remove(path)


def all():
    """Calls all possible reload methods at once."""
    xrdb()
    tint2()
    dunst()
    openbox()
    reload.i3()
    reload.polybar()
    reload.gtk()
    reload.kitty()
    reload.sway()

    if settings.getboolean("gtk", True):
        gtk3()
