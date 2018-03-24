import errno
import pywal
import shutil
from os.path import realpath
from os import symlink, remove, path
from subprocess import Popen, call
from . import color, sample, config, files, logger


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
        image = pywal.image.get(path.join(config.WALL_DIR, cs_file))
        colors = pywal.colors.get(image, config.WALL_DIR)

        pywal.sequences.send(colors, config.WPG_DIR)
        pywal.export.color(colors, 'css',
                           path.join(config.WPG_DIR, 'current.css'))
        pywal.export.color(colors, 'shell',
                           path.join(config.WPG_DIR, 'current.sh'))
        pywal.export.color(colors, 'xresources',
                           path.join(config.WPG_DIR, 'current.Xres'))

        init_file = open(path.join(config.WPG_DIR, 'wp_init.sh'), 'w')
        init_file.writelines(['#!/bin/bash\n', 'wpg -rs ' +
                              filename + ' ' + cs_file])
        init_file.close()

        Popen(['chmod', '+x', path.join(config.WPG_DIR, 'wp_init.sh')])
        call(['xrdb', '-merge', path.join(config.XRES_DIR, cs_file + '.Xres')])
        call(['xrdb', '-merge', path.join(config.HOME, '.Xresources')])
        try:
            if config.wpgtk.getboolean('execute_cmd'):
                Popen(config.wpgtk['command'].split(' '))
            symlink(path.join(config.WALL_DIR, filename),
                    path.join(config.WPG_DIR, ".current"))
        except Exception as e:
            if e.errno == errno.EEXIST:
                remove(path.join(config.WPG_DIR, ".current"))
                symlink(path.join(config.WALL_DIR, filename),
                        path.join(config.WPG_DIR, ".current"))
            else:
                raise e
    else:
        print("no such file, available files:")
        files.show_files()


def delete_theme(filename):
    remove(path.join(config.WALL_DIR, filename))
    remove(path.join(config.SAMPLE_DIR, (filename + '.sample.png')))
    remove(path.join(config.XRES_DIR, (filename + '.Xres')))
    remove(files.get_cache_filename(filename))


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
    logger.log.info("applied %s to %s" % (json_file, wallpaper))


def export_theme(wallpaper, json_path="."):
    try:
        if(path.isdir(json_path)):
            json_path = path.join(json_path, wallpaper + ".json")
        shutil.copy2(path.join(files.get_cache_filename(wallpaper)), json_path)
        logger.log.info("theme for %s successfully exported", wallpaper)
    except IOError as e:
        logger.log.error('file not available')


def auto_adjust_theme(filename):
    try:
        color_list = color.get_color_list(filename)
        color_list = color.auto_adjust_colors(color_list)
        sample.create_sample(color_list,
                             f=path.join(config.SAMPLE_DIR,
                                         (filename + '.sample.png')))
        color.write_colors(filename, color_list)
    except IOError:
        logger.log.error('file not available')
