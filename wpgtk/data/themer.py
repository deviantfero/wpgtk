import pywal
import shutil
import logging
from os.path import realpath
from os import remove, path, symlink
from subprocess import Popen
from . import color
from . import config
from . import files
from . import util
from . import sample


def create_theme(filepath):
    filepath = realpath(filepath)
    filename = filepath.split("/").pop().replace(" ", "_")
    tmplink = path.join(config.WALL_DIR, ".tmp.link")

    symlink(filepath, tmplink)

    shutil.move(tmplink, path.join(config.WALL_DIR, filename))
    return color.get_color_list(filename)


def set_theme(filename, cs_file, restore=False):
    set_wall = config.wpgtk.getboolean("set_wallpaper", True)
    colors = color.get_pywal_dict(path.join(config.WALL_DIR, cs_file))
    pywal.sequences.send(colors, config.WPG_DIR)

    if not restore:
        color.apply_colorscheme(colors)
        pywal.reload.i3()
        pywal.reload.polybar()

    if set_wall:
        pywal.wallpaper.change(path.join(config.WALL_DIR, filename))

    pywal.export.color(colors, "css",
                       path.join(config.WPG_DIR, "current.css"))
    pywal.export.color(colors, "shell",
                       path.join(config.WPG_DIR, "current.sh"))
    pywal.export.color(colors, "xresources",
                       path.join(config.WPG_DIR, "current.Xres"))

    flags = "-rs" if set_wall else "-nrs"
    with open(path.join(config.WPG_DIR, "wp_init.sh"), "w") as script:
        script.writelines(["#!/bin/bash\n",
                           "wpg %s %s %s" % (flags, filename, cs_file)])

    Popen(['chmod', '+x', path.join(config.WPG_DIR, "wp_init.sh")])
    util.xrdb_merge(path.join(config.XRES_DIR, cs_file + ".Xres"))
    util.xrdb_merge(path.join(config.HOME, ".Xresources"))

    files.change_current(filename)

    if config.wpgtk.getboolean('execute_cmd'):
        Popen(config.wpgtk['command'].split(' '))


def delete_theme(filename):
    try:
        remove(path.join(config.WALL_DIR, filename))
        remove(path.join(config.XRES_DIR, (filename + '.Xres')))
        files.delete_colorschemes(filename)
    except IOError as e:
        logging.error("file not available")


def get_current():
    image = realpath(path.join(config.WPG_DIR, '.current')).split('/').pop()
    return image


def import_theme(wallpaper, json_file, theme=False):
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


def set_pywal_theme(theme_name):
    current = get_current()
    theme = pywal.theme.file(theme_name)

    color_list = list(theme["colors"].values())
    color.write_colors(current, color_list)
    sample.create_sample(color_list, files.get_sample_path(current))

    set_theme(current, current)


def export_theme(wallpaper, json_path="."):
    try:
        if(path.isdir(json_path)):
            json_path = path.join(json_path, wallpaper + ".json")
        shutil.copy2(path.join(files.get_cache_path(wallpaper)), json_path)
        logging.info("theme for %s successfully exported", wallpaper)
    except IOError as e:
        logging.error("file not available")
