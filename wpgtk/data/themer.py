import pywal
import shutil
import logging
from os.path import realpath
from os import remove, path
from subprocess import Popen
from . import color, sample, config, files, util


def create_theme(filepath):
    filename = filepath.split("/").pop().replace(" ", "_")
    shutil.copy2(filepath, path.join(config.WALL_DIR, filename))
    auto_adjust_theme(filename)


def set_theme(filename, cs_file, restore=False):
    if(path.join(config.WALL_DIR, filename)):
        if(not restore):
            color.apply_colorscheme(cs_file)
            pywal.reload.gtk()
            pywal.reload.i3()
            pywal.reload.polybar()

        pywal.wallpaper.change(path.join(config.WALL_DIR, filename))
        colors = color.get_pywal_dict(path.join(config.WALL_DIR, cs_file))

        pywal.sequences.send(colors, config.WPG_DIR)

        pywal.export.color(colors, "css",
                           path.join(config.WPG_DIR, "current.css"))
        pywal.export.color(colors, "shell",
                           path.join(config.WPG_DIR, "current.sh"))
        pywal.export.color(colors, "xresources",
                           path.join(config.WPG_DIR, "current.Xres"))

        with open(path.join(config.WPG_DIR), "wp_init.sh", 'w') as script:
            script.writelines(["#!/bin/bash\n",
                               "wpg -rs %s %s" % (filename, cs_file)])

        Popen(['chmod', '+x', path.join(config.WPG_DIR, "wp_init.sh")])
        util.xrdb_merge(path.join(config.XRES_DIR, cs_file + ".Xres"))
        util.xrdb_merge(path.join(config.HOME, ".Xresources"))

        files.change_current(filename)

        if config.wpgtk.getboolean('execute_cmd'):
            Popen(config.wpgtk['command'].split(' '))
    else:
        print("no such file, available files:")
        files.show_files()


def delete_theme(filename):
    remove(path.join(config.WALL_DIR, filename))
    remove(path.join(config.SAMPLE_DIR, (filename + '.sample.png')))
    remove(path.join(config.XRES_DIR, (filename + '.Xres')))
    files.delete_colorschemes(filename)


def get_current(show=False):
    image = realpath(path.join(config.WPG_DIR, '.current')).split('/').pop()
    if show:
        print(image)
    return image


def import_theme(wallpaper, json_file):
    color_list = color.get_color_list(json_file, True)

    color.write_colors(wallpaper, color_list)
    sample.create_sample(color_list,
                         path.join(config.SAMPLE_DIR,
                                   (wallpaper + '.sample.png')))
    logging.info("applied %s to %s" % (json_file, wallpaper))


def export_theme(wallpaper, json_path="."):
    try:
        if(path.isdir(json_path)):
            json_path = path.join(json_path, wallpaper + ".json")
        shutil.copy2(path.join(files.get_cache_filename(wallpaper)), json_path)
        logging.info("theme for %s successfully exported", wallpaper)
    except IOError as e:
        logging.error('file not available')


def auto_adjust_theme(filename):
    try:
        color_list = color.get_color_list(filename)
        color_list = color.auto_adjust_colors(color_list)
        sample.create_sample(color_list,
                             f=path.join(config.SAMPLE_DIR,
                                         (filename + '.sample.png')))
        color.write_colors(filename, color_list)
    except IOError:
        logging.error('file not available')
