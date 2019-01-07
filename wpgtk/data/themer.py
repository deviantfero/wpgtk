import pywal
import shutil
import logging
from os.path import realpath
from os import remove, path, symlink
from subprocess import Popen

from .config import WPG_DIR, WALL_DIR, FORMAT_DIR, settings
from . import color
from . import files
from . import sample
from . import reload


def create_theme(filepath):
    """create a colors-scheme from a filepath"""
    filepath = realpath(filepath)
    filename = filepath.split("/").pop().replace(" ", "_")
    tmplink = path.join(WALL_DIR, ".tmp.link")

    symlink(filepath, tmplink)

    shutil.move(tmplink, path.join(WALL_DIR, filename))

    try:
        return color.get_color_list(filename)
    except SystemExit:
        return set_fallback_theme(filename)


def set_theme(wallpaper, colorscheme, restore=False):
    """apply a given wallpaper and a given colorscheme"""
    set_wall = settings.getboolean("set_wallpaper", True)
    colors = color.get_pywal_dict(path.join(WALL_DIR, colorscheme))
    pywal.sequences.send(colors, WPG_DIR)

    if not restore:
        pywal.export.every(colors, FORMAT_DIR)
        color.apply_colorscheme(colors)
        reload.all()

    if set_wall:
        filepath = path.join(WALL_DIR, wallpaper)
        set_wall = filepath if path.isfile(filepath) else colors["wallpaper"]
        pywal.wallpaper.change(set_wall)

    flags = "-rs" if set_wall else "-nrs"
    with open(path.join(WPG_DIR, "wp_init.sh"), "w") as script:
        script.writelines(["#!/usr/bin/env bash\n",
                           "wpg %s '%s' '%s'" %
                           (flags, wallpaper, colorscheme)])

    Popen(['chmod', '+x', path.join(WPG_DIR, "wp_init.sh")])
    reload.xrdb()

    files.change_current(wallpaper)

    if settings.getboolean('execute_cmd'):
        Popen(['bash', '-c', settings['command']])


def delete_theme(filename):
    try:
        remove(path.join(WALL_DIR, filename))
        files.delete_colorschemes(filename)
    except IOError as e:
        logging.error("file not available")
        logging.error(e.message)


def get_current():
    image = realpath(path.join(WPG_DIR, '.current')).split('/').pop()
    return image


def import_theme(wallpaper, json_file, theme=False):
    """import a colorscheme from a JSON file either in
    terminal.sexy or pywal format"""
    json_file = realpath(json_file)
    filename = json_file.split("/").pop()

    if theme:
        theme = pywal.theme.file(filename)
        color_list = list(theme["colors"].values())
    else:
        try:
            color_list = color.get_color_list(json_file, True)
        except IOError:
            logging.error("file does not exist")
            return

    color.write_colors(wallpaper, color_list)
    sample.create_sample(color_list, files.get_sample_path(wallpaper))
    logging.info("applied %s to %s" % (filename, wallpaper))


def set_fallback_theme(wallpaper):
    """fallback theme for when color generation fails"""
    theme = pywal.theme.file("random")

    color_list = list(theme["colors"].values())
    color.write_colors(wallpaper, color_list)
    sample.create_sample(color_list, files.get_sample_path(wallpaper))

    return color_list


def set_pywal_theme(theme_name):
    """set's a pywal theme and applies it to wpgtk"""
    current = get_current()
    theme = pywal.theme.file(theme_name)

    color_list = list(theme["colors"].values())
    color.write_colors(current, color_list)
    sample.create_sample(color_list, files.get_sample_path(current))

    set_theme(current, current)


def export_theme(wallpaper, json_path="."):
    """export a colorscheme to json format"""
    try:
        if(path.isdir(json_path)):
            json_path = path.join(json_path, wallpaper + ".json")

        shutil.copy2(path.join(files.get_cache_path(wallpaper)), json_path)
        logging.info("theme for %s successfully exported", wallpaper)
    except IOError as e:
        logging.error("file not available")
        logging.error(e.message)
