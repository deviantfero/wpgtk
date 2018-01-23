import os
import shutil
import sys
import re
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
    files.sort()

    if images:
        return [elem for elem in files if valid.fullmatch(elem)]
    else:
        return files


def show_files(path=config.WALL_DIR, images=True):
    for f in get_file_list(path, images):
        print(f)


def add_template(cfile, basefile=None):

    # we remove dots from possible dotfiles
    if not basefile:
        l = [atom.lstrip('.') for atom in cfile.split('/')
             if atom is not 'home']
        if len(l) > 3:
            l = l[-3::]
        templatename = '.'.join(l) + '.base'
    else:
        templatename = basefile.split('/').pop()
    print('ADD::' + templatename + '@' + cfile)
    try:
        print('::MAKING BACKUP CONFIG')
        shutil.copy2(cfile, cfile + '.bak')
        print('::CREATING BASE')
        if basefile:
            shutil.copy2(basefile, os.path.join(config.OPT_DIR, templatename))
        else:
            shutil.copy2(cfile, os.path.join(config.OPT_DIR, templatename))
        print('::CREATING SYMLINK')
        os.symlink(cfile, os.path.join(config.OPT_DIR,
                   templatename.replace('.base', '')))
    except Exception as e:
        print('ERR::' + str(e.strerror), file=sys.stderr)


def remove_template(basefile):
    basefile_path = os.path.join(config.OPT_DIR, basefile)
    configfile_path = basefile_path.replace('.base', '')

    try:
        os.remove(basefile_path)
        if os.path.islink(configfile_path):
            os.remove(configfile_path)
    except Exception as e:
        print('ERR::' + str(e.strerror), file=sys.stderr)
