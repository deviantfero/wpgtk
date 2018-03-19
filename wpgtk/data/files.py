import os
import shutil
import re
from . import config, logger
from pywal.settings import __cache_version__
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
    for f in get_file_list(path, images):
        print(f)


def get_cache_filename(img, light=False):
    color_type = 'light' if light else 'dark'
    cache_file = re.sub('[/|\\|.]', '_', join(config.WALL_DIR, img))
    cache_file = join(config.SCHEME_DIR, '%s_%s_%s.json'
                      % (cache_file, color_type, __cache_version__))

    return cache_file


def add_template(cfile, basefile=None):

    cfile = os.path.realpath(cfile)
    # we remove dots from possible dotfiles
    if not basefile:
        l = [atom.lstrip('.') for atom in cfile.split('/')
             if atom is not 'home']
        if len(l) > 3:
            l = l[-3::]
        templatename = '.'.join(l) + '.base'
    else:
        templatename = basefile.split('/').pop()
    logger.log.info('added ' + templatename + '@' + cfile)
    try:
        logger.log.info('MAKING BACKUP CONFIG')
        shutil.copy2(cfile, cfile + '.bak')
        logger.log.info('CREATING BASE')
        if basefile:
            shutil.copy2(basefile, join(config.OPT_DIR, templatename))
        else:
            shutil.copy2(cfile, join(config.OPT_DIR, templatename))
        logger.log.info('CREATING SYMLINK')
        os.symlink(cfile, join(config.OPT_DIR,
                   templatename.replace('.base', '')))
    except Exception as e:
        logger.log.error(str(e.strerror))


def remove_template(basefile):
    basefile_path = join(config.OPT_DIR, basefile)
    configfile_path = basefile_path.replace('.base', '')

    try:
        os.remove(basefile_path)
        if os.path.islink(configfile_path):
            os.remove(configfile_path)
    except Exception as e:
        logger.log.error(str(e.strerror))
