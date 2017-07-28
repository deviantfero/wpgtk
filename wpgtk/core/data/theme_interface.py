import errno
from os.path import expanduser, realpath, isfile
from random import shuffle
from os import symlink, remove
from subprocess import Popen, call
from . import color_parser as cp
from . import make_sample as ms
from .file_list import FileList

WAL_DIR = expanduser('~') + "/.wallpapers/"
SAMPLE_DIR = WAL_DIR + "sample/"
CACHE_DIR = WAL_DIR + "cache/"
XRES_DIR = WAL_DIR + "xres/"
DEFAULT = {'ACT': 0, 'TN2': True, 'GTK': True, 'INV': False}


# TODO: add options to create_theme
def create_theme(filepath):
    # TODO: wal does not support spaces or special characters in file name
    # probably fixed in python version
    call(['wal', '-i', filepath])
    filename = filepath.split("/").pop()
    color_list = cp.read_colors(filename)
    ms.create_sample(color_list, f=SAMPLE_DIR + filename + '.sample.png')


def set_theme(filename, cs_file, opt=DEFAULT, restore=False):
    if(isfile(WAL_DIR + filename)):
        if(not restore):
            cp.execute_gcolorchange(cs_file, opt)
        call('wal -si ' + WAL_DIR + filename, shell=True)
        init_file = open(WAL_DIR + 'wp_init.sh', 'w')
        init_file.writelines(['#!/bin/bash\n', 'wpg -r -s ' +
                              filename + ' ' + cs_file])
        init_file.close()
        Popen(['chmod', '+x', WAL_DIR + 'wp_init.sh'])
        call(['xrdb', '-merge', expanduser('~') + '/.Xresources'])
        call(['xrdb', '-merge', XRES_DIR + cs_file + '.Xres'])
        try:
            symlink(WAL_DIR + filename, WAL_DIR + ".current")
        except OSError as e:
            if e.errno == errno.EEXIST:
                remove(WAL_DIR + ".current")
                symlink(WAL_DIR + filename, WAL_DIR + ".current")
            else:
                raise e
    else:
        print("no such file, available files:")
        show_wallpapers()


def delete_theme(filename):
    remove(WAL_DIR + filename)
    remove(SAMPLE_DIR + filename + ".sample.png")
    remove(CACHE_DIR + filename + ".col")
    remove(XRES_DIR + filename + ".Xres")


def show_wallpapers():
    files = FileList(WAL_DIR)
    files.show_list()


def show_current():
    image = realpath(WAL_DIR + '.current').split('/').pop()
    print(image)
    return image


def shuffle_colors(filename):
    if(isfile(WAL_DIR + filename)):
        colors = cp.read_colors(filename)
        shuffled_colors = colors[1:8]
        shuffle(shuffled_colors)
        colors = colors[:1] + shuffled_colors + colors[8:]
        ms.create_sample(colors, f=SAMPLE_DIR + filename + '.sample.png')
        cp.write_colors(filename, colors)


def auto_adjust_colors(filename, opt=DEFAULT):
    if(isfile(WAL_DIR + filename)):
        color_list = cp.read_colors(filename)
        color8 = color_list[0:1][0]
        if(not opt['INV']):
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
        ms.create_sample(color_list, f=SAMPLE_DIR + filename + '.sample.png')
        cp.write_colors(filename, color_list)
