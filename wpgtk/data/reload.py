import shutil
import subprocess
import tempfile
import os
import logging
from pywal import reload
import configparser

from . import util
from .config import FORMAT_DIR, HOME, CONFIG, settings


def xrdb():
    """Merges both a user's .Xresources and pywal's."""
    reload.xrdb(
        [
            os.path.join(FORMAT_DIR, "colors.Xresources"),
            os.path.join(HOME, ".Xresources"),
        ]
    )


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


def xsettingsd(theme):
    """Call xsettingsd with a tempfile to trigger a reload of the GTK3 theme"""
    fd, path = tempfile.mkstemp()

    try:
        with os.fdopen(fd, "w+") as tmp:
            tmp.write('Net/ThemeName "' + theme + '"\n')
            tmp.close()

            util.silent_call(["timeout", "0.2s", "xsettingsd", "-c", path])
            logging.info(
                "reloaded %s from settings.ini using xsettingsd"
                % theme
            )
    finally:
        os.remove(path)


def gtk3():
    settings_ini = os.path.join(CONFIG, "gtk-3.0", "settings.ini")

    refresh_gsettings = (
        "gsettings set org.gnome.desktop.interface "
        "gtk-theme '' && sleep 0.1 && gsettings set "
        "org.gnome.desktop.interface gtk-theme '{}'"
    )

    refresh_xfsettings = (
        "xfconf-query -c xsettings -p /Net/ThemeName -s"
        " '' && sleep 0.1 && xfconf-query -c xsettings -p"
        " /Net/ThemeName -s '{}'"
    )

    if shutil.which("gsettings"):
        cmd = ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"]
        gsettings_theme = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        ).communicate()[0].decode().strip("' \n")

    xfsettings_theme = None
    if shutil.which("xfconf-query"):
        cmd = ["xfconf-query", "-c", "xsettings", "-p", "/Net/ThemeName"]
        xfsettings_theme = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        ).communicate()[0].decode().strip("' \n")

    if util.get_pid("gsd-settings") and gsettings_theme:
        subprocess.Popen(refresh_gsettings.format(gsettings_theme), shell=True)
        logging.info("Reloaded %s theme via gsd-settings" % gsettings_theme)

    elif util.get_pid("xfsettingsd") and xfsettings_theme:
        subprocess.Popen(refresh_xfsettings.format(xfsettings_theme), shell=True)
        logging.info("reloaded %s theme via xfsettingsd" % xfsettings_theme)

    # no settings daemon is running.
    # So GTK is getting theme info from gtkrc file
    # using xsettingd to set the same theme (parsing it from gtkrc)
    elif shutil.which("xsettingsd"):
        if os.path.isfile(settings_ini):
            gtkrc = configparser.ConfigParser()
            gtkrc.read(settings_ini)
            theme = gtkrc["Settings"].get("gtk-theme-name") if "Settings" in gtkrc else "FlatColor"
            xsettingsd(theme)
        else:
            xsettingsd("FlatColor")

    # The system has no known settings daemon installed,
    # but dconf gtk-theme exists, just refreshing its theme
    # Because user might be using unknown settings daemon
    elif shutil.which("gsettings") and gsettings_theme:
        subprocess.Popen(refresh_gsettings.format(gsettings_theme), shell=True)
        logging.warning(
            "No settings daemon found, just refreshing %s theme from gsettings"
            % gsettings_theme
        )


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
