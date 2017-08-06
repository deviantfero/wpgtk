import errno
import pywal
import shutil
from random import shuffle
from os.path import realpath, isfile
from os import symlink, remove
from subprocess import Popen, call
from . import color_parser as cp
from . import make_sample as ms
from .file_list import FileList
from . import config


def create_theme(filepath):
    filename = filepath.split("/").pop()
    shutil.copy2(filepath, config.WALL_DIR / filename)
    image = pywal.image.get(config.WALL_DIR / filename)
    colors = pywal.colors.get(image, config.WALL_DIR)
    pywal.export.color(colors,
                       "xresources",
                       config.XRES_DIR / (filename + ".Xres"))
    color_list = [val for val in colors['colors'].values()]
    ms.create_sample(color_list,
                     f=config.SAMPLE_DIR / (filename + '.sample.png'))


def set_theme(filename, cs_file, restore=False):
    if(isfile(config.WALL_DIR / filename)):
        if(not restore):
            cp.execute_gcolorchange(cs_file)

        pywal.wallpaper.change(config.WALL_DIR / filename)
        image = pywal.image.get(config.WALL_DIR / cs_file)
        colors = pywal.colors.get(image, config.WALL_DIR)
        pywal.sequences.send(colors, False, config.WALL_DIR)

        init_file = open(config.WALL_DIR / 'wp_init.sh', 'w')
        init_file.writelines(['#!/bin/bash\n', 'wpg -r -s ' +
                              filename + ' ' + cs_file])
        init_file.close()
        Popen(['chmod', '+x', config.WALL_DIR / 'wp_init.sh'])
        call(['xrdb', '-merge', config.HOME / '.Xresources'])
        call(['xrdb', '-merge', config.XRES_DIR / (cs_file + '.Xres')])
        try:
            symlink(config.WALL_DIR / filename, config.WALL_DIR / ".current")
        except OSError as e:
            if e.errno == errno.EEXIST:
                remove(config.WALL_DIR / ".current")
                symlink(config.WALL_DIR / filename,
                        config.WALL_DIR / ".current")
            else:
                raise e
    else:
        print("no such file, available files:")
        show_wallpapers()


def delete_theme(filename):
    cache_file = str(config.WALL_DIR / filename)
    remove(config.WALL_DIR / filename)
    remove(config.SAMPLE_DIR / (filename + '.sample.png'))
    remove(config.XRES_DIR / (filename + '.Xres'))
    remove(config.SCHEME_DIR /
           (cache_file.replace('/', '_').replace('.', '_') + ".json"))


def show_current():
    image = realpath(config.WALL_DIR / '.current').split('/').pop()
    print(image)
    return image


def shuffle_colors(filename):
    if(isfile(config.WALL_DIR + filename)):
        colors = cp.read_colors(filename)
        shuffled_colors = colors[1:8]
        shuffle(shuffled_colors)
        colors = colors[:1] + shuffled_colors + colors[8:]
        ms.create_sample(colors, f=config.SAMPLE_DIR /
                         filename / '.sample.png')
        cp.write_colors(filename, colors)


def auto_adjust_colors(filename):
    try:
        color_list = cp.get_color_list(filename)
        color8 = color_list[0:1][0]
        if not config.wpgtk.getboolean('light_theme'):
            color8 = [cp.add_brightness(color8, 18)]
            color_list = color_list[:8:]
            color_list += color8
            color_list += [cp.add_brightness(x, 50) for x in color_list[1:8:]]
        else:
            color8 = [cp.reduce_brightness(color8, 18)]
            color_list = color_list[:8:]
            color_list += color8
            color_list += [cp.reduce_brightness(x, 50)
                           for x in color_list[1:8:]]
        ms.create_sample(color_list, f=config.SAMPLE_DIR /\
                         (filename + '.sample.png'))
        cp.write_colors(filename, color_list)
    except IOError:
        print(f'ERR:: file not available')
