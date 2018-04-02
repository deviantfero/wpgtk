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


def show_files(path=config.WALL_DIR, images=True):
    print("\n".join(get_file_list(path, images)))


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

    cfile = os.path.realpath(cfile)
    # we remove dots from possible dotfiles
    if not basefile:
        l = [atom.lstrip(".") for atom in cfile.split("/")
             if atom is not 'home']
        if len(l) > 3:
            l = l[-3::]
        templatename = ".".join(l) + ".base"
    else:
        templatename = basefile.split('/').pop()
    logging.info('added ' + templatename + '@' + cfile)
    try:
        logging.info("creating backup %s.bak" % cfile)
        shutil.copy2(cfile, cfile + ".bak")
        logging.info("creating base file")
        if basefile:
            shutil.copy2(basefile, join(config.OPT_DIR, templatename))
        else:
            shutil.copy2(cfile, join(config.OPT_DIR, templatename))
        logging.info("linking template to original file")
        os.symlink(cfile, join(config.OPT_DIR,
                   templatename.replace(".base", "")))
    except Exception as e:
        logging.error(str(e.strerror))


def delete_template(basefile):
    basefile_path = join(config.OPT_DIR, basefile)
    configfile_path = basefile_path.replace(".base", "")
    try:
        os.remove(basefile_path)
        if os.path.islink(configfile_path):
            os.remove(configfile_path)
    except Exception as e:
        logging.error(str(e.strerror))


def delete_colorschemes(wallpaper):
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
