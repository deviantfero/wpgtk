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
    use_vte = settings.getboolean("vte", False)
    is_file = path.isdir(colorscheme) or path.isfile(colorscheme)
    target = colorscheme if is_file else path.join(WALL_DIR, colorscheme)

    set_wall = settings.getboolean("set_wallpaper", True)
    colors = color.get_pywal_dict(target, is_file)
    pywal.sequences.send(colors, WPG_DIR, vte_fix=use_vte)

    if not restore:
        pywal.export.every(colors, FORMAT_DIR)
        color.apply_colorscheme(colors)
        reload.all()
    else:
        reload.xrdb()

    if set_wall:
        filepath = path.join(WALL_DIR, wallpaper)
        set_wall = filepath if path.isfile(filepath) else colors["wallpaper"]
        pywal.wallpaper.change(set_wall)

    files.write_script(wallpaper, colorscheme)
    files.change_current(wallpaper)
    
    Popen(['chmod', '+x', path.join(WPG_DIR, "wp_init.sh")])

    if settings.getboolean('execute_cmd'):
        Popen(['bash', '-c', settings['command']])


def delete_theme(filename):
    remove(path.join(WALL_DIR, filename))
    files.delete_colorschemes(filename)


def get_current():
    image = realpath(path.join(WPG_DIR, '.current')).split('/').pop()
    return image


def reset_theme(theme_name):
    """restore a colorscheme to it's original state by deleting
    and re adding the image"""
    wallpaper = realpath(path.join(WALL_DIR, theme_name))
    delete_theme(theme_name)
    create_theme(wallpaper)


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
