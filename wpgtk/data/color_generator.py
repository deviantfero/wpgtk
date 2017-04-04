from os.path import expanduser
import errno
from os import walk, symlink, remove, getenv
from .color_parser import *
from .make_sample import *

WAL_DIR = expanduser( '~' ) + "/.wallpapers/"
SAMPLE_DIR = WAL_DIR + "sample/"
CACHE_DIR = WAL_DIR + "cache/"
XRES_DIR = WAL_DIR + "xres/"

def create_theme(filepath):
    call( 'wal -i ' + filepath, shell=True )
    filename = filepath.split("/").pop()
    color_list = read_colors(filename)
    create_sample(color_list, f=SAMPLE_DIR + filename + '.sample.png')

def set_theme(filename):
    call( 'wal -si ' + WAL_DIR + filename, shell=True )
    try:
        symlink(WAL_DIR + filename, WAL_DIR + ".current")
    except OSError as e:
        if e.errno == errno.EEXIST:
            remove(WAL_DIR + ".current")
            symlink(WAL_DIR + filename, WAL_DIR + ".current")
        else:
            raise e

def remove_theme(filename):
    remove(WAL_DIR + filename)
    remove(SAMPLE_DIR + filename + ".sample.png")
    remove(CACHE_DIR + filename + ".col")
    remove(XRES_DIR + filename + ".Xres")
