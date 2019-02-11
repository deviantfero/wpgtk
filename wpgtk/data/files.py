import os
import shutil
import re
import logging
from pywal.colors import cache_fname, list_backends

from .config import settings, WALL_DIR, WPG_DIR, OPT_DIR, SAMPLE_DIR
from os.path import join


def get_file_list(path=WALL_DIR, images=True):
    """gets filenames in a given directory, optional
    parameters for image filter."""
    valid = re.compile(r"^[^\.](.*\.png$|.*\.jpg$|.*\.jpeg$|.*\.jpe$|.*\.gif$)")
    files = []

    for (_, _, filenames) in os.walk(path):
        files.extend(filenames)
        break

    files.sort()

    if images:
        return [elem for elem in files if valid.fullmatch(elem)]
    else:
        return files


def write_script(wallpaper, colorscheme):
    """writes the script that should be called on startup
    to restore the theme."""
    set_wall = settings.getboolean("set_wallpaper", True)
    light_theme = settings.getboolean("light_theme", True)

    flags = "-rs" if set_wall else "-nrs"
    flags += "L" if light_theme else ""

    with open(join(WPG_DIR, "wp_init.sh"), "w") as script:
        command = "wpg %s '%s' '%s'" % (flags, wallpaper, colorscheme)
        script.writelines(["#!/usr/bin/env bash\n", command])


def get_cache_path(wallpaper, backend=None):
    """get a colorscheme cache path using a wallpaper name"""
    if not backend:
        backend = settings.get("backend", "wal")

    filepath = join(WALL_DIR, wallpaper)
    filename = cache_fname(filepath, backend, False, WPG_DIR)

    return join(*filename)


def get_sample_path(wallpaper, backend=None):
    """gets a wallpaper colorscheme sample's path"""
    if not backend:
        backend = settings.get("backend", "wal")

    sample_filename = "%s_%s_sample.png" % (wallpaper, backend)

    return join(SAMPLE_DIR, sample_filename)


def add_template(cfile, bfile=None):
    """adds a new base file from a config file to wpgtk
    or re-establishes link with config file for a
    previously generated base file"""
    cfile = os.path.realpath(cfile)

    if bfile:
        template_name = bfile.split("/").pop()
    else:
        clean_atoms = [atom.lstrip(".") for atom in cfile.split("/")[-3::]]
        template_name = "_".join(clean_atoms) + ".base"

    try:
        shutil.copy2(cfile, cfile + ".bak")
        src_file = bfile if bfile else cfile

        shutil.copy2(src_file, join(OPT_DIR, template_name))
        os.symlink(cfile, join(OPT_DIR,
                   template_name.replace(".base", "")))

        logging.info("created backup %s.bak" % cfile)
        logging.info("added %s @ %s" % (template_name, cfile))
    except Exception as e:
        logging.error(str(e.strerror))


def delete_template(basefile):
    """delete a template in wpgtk with the given
    base file name"""
    base_file = join(OPT_DIR, basefile)
    conf_file = base_file.replace(".base", "")

    try:
        os.remove(base_file)
        if os.path.islink(conf_file):
            os.remove(conf_file)
    except Exception as e:
        logging.error(str(e.strerror))


def delete_colorschemes(wallpaper):
    """delete all colorschemes related to the given wallpaper"""
    for backend in list_backends():
        try:
            os.remove(get_cache_path(wallpaper, backend))
            os.remove(get_sample_path(wallpaper, backend))
        except OSError:
            pass


def update_color(matchobj):
    if matchobj.group(1):
        return "{%s}" % matchobj.group(1).lower()


def update_template(template_path):
    tmp_data = ""

    with open(template_path, "r") as f:
        tmp_data = f.read()

        logging.info("escaping legitimate curly braces {} -> {{}}")
        tmp_data = tmp_data.replace("{", "{{")
        tmp_data = tmp_data.replace("}", "}}")

        logging.info("replacing #<COLORXX> with braces {colorxx}")
        tmp_data = re.sub(r"#<(COLOR[0-9]{1,2})>", update_color, tmp_data)
        tmp_data = tmp_data.replace("#<COLORACT>", "{active}")
        tmp_data = tmp_data.replace("#<COLORIN>", "{inactive}")

    with open(template_path, "w") as f:
        logging.info("writting %s" % template_path)
        f.write(tmp_data)
        logging.info("%s update complete" % template_path)


def change_current(filename):
    """update symlink to point to the current wallpaper"""
    os.symlink(join(WALL_DIR, filename), join(WPG_DIR, ".currentTmp"))
    os.rename(join(WPG_DIR, ".currentTmp"), join(WPG_DIR, ".current"))
