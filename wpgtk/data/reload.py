import shutil
import subprocess
import os
import tempfile
import logging
from pywal import reload
import configparser

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
    if settings.getboolean("gtk", True):
        gsettings_theme = None
        if shutil.which("gsettings") and subprocess.call(["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],stdout=subprocess.DEVNULL) == 0:
            gsettings_theme = subprocess.Popen(["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],stdout=subprocess.PIPE).communicate()[0].decode().strip("' \n")

        refresh_gsettings = "gsettings set org.gnome.desktop.interface gtk-theme '' && sleep 0.1 && gsettings set org.gnome.desktop.interface gtk-theme '%s'" % gsettings_theme

        # if gnome-settings-daemon is running, no need to use xsettingsd
        if subprocess.call(["pgrep", "gsd-xsettings"],stdout=subprocess.DEVNULL) == 0 and gsettings_theme:
            subprocess.Popen(refresh_gsettings, shell=True)
            logging.info("Reloaded %s theme via gnome-settings-daemon" % gsettings_theme)

        # no settings daemon is running. So GTK is getting theme info from gtkrc file
        # So using xsettingd to set the same theme (parsing it from gtkrc)
        elif shutil.which("xsettingsd") and os.path.isfile(os.path.join(os.environ.get('XDG_CONFIG_HOME'), 'gtk-3.0', 'settings.ini')):
            gtkrc = configparser.ConfigParser()
            gtkrc.read(os.path.join(os.environ.get('XDG_CONFIG_HOME'), 'gtk-3.0', 'settings.ini'))
            if "Settings" in gtkrc and "gtk-theme-name" in gtkrc["Settings"]:
                theme_name = gtkrc["Settings"]["gtk-theme-name"]
                fd, path = tempfile.mkstemp()
                try:
                    with os.fdopen(fd, 'w+') as tmp:
                        tmp.write('Net/ThemeName "'+theme_name+'"\n')
                        tmp.close()
                        subprocess.Popen(
                            ["timeout", "0.2s", "xsettingsd", "-c", path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        ).communicate() # Don't know why I need to communicate. But without calling this, theme dont update
                    logging.info("Reloaded theme %s from gtk-3.0/settings.ini using xsettingsd" % theme_name)
                finally:
                    os.remove(path)
        
        # The system has no known settings daemon installed, but dconf gtk-theme exists, just refreshing its theme
        # Because user might be using unknown settings daemon
        elif gsettings_theme:
            subprocess.Popen(refresh_gsettings, shell=True)
            logging.warning("No settings daemon found, just refreshing %s theme from gsettings" % gsettings_theme)


        elif shutil.which("xsettingsd") and gsettings_theme:
            subprocess.Popen([
                "gsettings", "set",
                "org.gnome.desktop.interface", "gtk-theme", "''"
            ])
            subprocess.Popen([
                "gsettings", "set",
                "org.gnome.desktop.interface", "gtk-theme",
                "'FlatColor'"
            ])
            logging.warning("No gtk theme is set. So falling back to 'FlatColor' Theme")

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
