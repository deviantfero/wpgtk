import os
import sys
import re
import shutil
from . import config


def get_file_list(path=config.WALL_DIR, images=True):
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

    if images:
        return [elem for elem in files if valid.fullmatch(elem)]
    else:
        return files


def show_files(path=config.WALL_DIR, images=True):
    for f in get_file_list(path, images):
        print(f)


def connect_conf(filepath):
    l = filepath.split('/', len(filepath))

    # we remove dots from possible dotfiles
    filename = l[-2].lstrip('.') + '.' + l[-1].lstrip('.')
    print('ADD::' + filename + '@' + filepath)
    try:
        shutil.copy2(filepath, filepath + '.bak')
        print('::MAKING BACKUP CONFIG')
        print('::CREATING BASE')
        shutil.copy2(filepath, os.path.join(config.OPT_DIR,
                                            (filename + '.base')))
        shutil.copy2(filepath, os.path.join(config.OPT_DIR, filename))
        os.remove(filepath)
        os.symlink(os.path.join(config.OPT_DIR, filename), filepath)
        print('::CREATING SYMLINK')
    except FileNotFoundError as e:
        print('ERR::' + str(e.__class__), file=sys.stderr)
        os.makedirs(config.OPT_DIR)
        print('INF:: directory created')
