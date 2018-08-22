import os
import shutil
import re
import logging
from . import config
from pywal.colors import cache_fname, list_backends
from os.path import join


def get_file_list(path=config.WALL_DIR, images=True, json=False):
    """gets filenames in a given directory, optional
    parameters for image exclusiveness

    @param path: directory to look for, default wallpaper dir
    @type  :  Optional string

    @param images: wether to show only images or all files
    @type  :  Optional boolean

    @return:  A list with the directories file names
    @rtype :  List
    """
    valid = re.compile('^[^\.](.*\.png$|.*\.jpg$|.*\.jpeg$|.*\.jpe$)')
    files = []
    for(dirpath, dirnames, filenames) in os.walk(path):
        for f in filenames:
            files.append(f)
        break
    files.sort()

    if images:
        return [elem for elem in files if valid.fullmatch(elem)]
    else:
        return files


def get_cache_path(wallpaper, backend=None):
    if not backend:
        backend = config.wpgtk.get('backend', 'wal')
    filepath = join(config.WALL_DIR, wallpaper)
    cache_filename = cache_fname(filepath, backend, False, config.WALL_DIR)
    return join(*cache_filename)


def get_sample_path(wallpaper, backend=None):
    if not backend:
        backend = config.wpgtk.get('backend', 'wal')
    sample_filename = "%s_%s_sample.png" % (wallpaper, backend)
    return join(config.SAMPLE_DIR, sample_filename)


def add_template(cfile, basefile=None):

def add_template(cfile, bfile=None):
    """adds a new base file from a config file to wpgtk
    or re-establishes link with config file for a
    previously generated base file"""
    cfile = os.path.realpath(cfile)

    if bfile:
        template_name = bfile.split('/').pop()
    else:
        template_name = "_".join(cfile.split('/')[-3::]) + ".base"

    try:
        shutil.copy2(cfile, cfile + ".bak")
        src_file = bfile if bfile else cfile
        shutil.copy2(src_file, join(config.OPT_DIR, template_name))
        os.symlink(cfile, join(config.OPT_DIR,
                   template_name.replace(".base", "")))

        logging.info("created backup %s.bak" % cfile)
        logging.info("added %s @ %s" % (template_name, cfile))
    except Exception as e:
        logging.error(str(e.strerror))


def delete_template(basefile):
    """delete a template in wpgtk with the given
    base file name"""
    base_file = join(config.OPT_DIR, basefile)
    conf_file = base_file.replace(".base", "")

    try:
        os.remove(base_file)
        if os.path.islink(conf_file):
            os.remove(conf_file)
    except Exception as e:
        logging.error(str(e.strerror))


def delete_colorschemes(wallpaper):
    """delete all colorschemes related to the given
    wallpaper"""
    for backend in list_backends():
        try:
            os.remove(get_cache_path(wallpaper, backend))
            os.remove(get_sample_path(wallpaper, backend))
        except OSError:
            pass


def change_current(filename):
    os.symlink(join(config.WALL_DIR, filename),
               join(config.WPG_DIR, ".currentTmp"))
    os.rename(join(config.WPG_DIR, ".currentTmp"),
              join(config.WPG_DIR, ".current"))
