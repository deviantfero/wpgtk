import sys
import logging
import pywal
import os
import re
import threading
from operator import itemgetter
from subprocess import Popen
from random import shuffle, randint

from .config import settings, user_keywords
from .config import WALL_DIR, WPG_DIR, FILE_DIC, OPT_DIR
from . import files
from . import util
from . import sample


def get_pywal_dict(wallpaper, is_file=False):
    """get the color dictionary of a given wallpaper"""
    light_theme = settings.getboolean("light_theme", False)
    pywal.util.Color.alpha_num = settings.get("alpha", "100")

    image = pywal.image.get(os.path.join(WALL_DIR, wallpaper))

    return pywal.colors.get(
        image,
        light=(is_file and light_theme),
        backend=settings.get("backend", "wal"),
        cache_dir=WPG_DIR
    )


def get_color_list(filename, json=False):
    """extract a list with 16 colors from a json or a pywal dict"""
    is_new = not os.path.isfile(files.get_cache_path(filename))
    auto_adjust = settings.getboolean("auto_adjust", True)
    light_theme = settings.getboolean("light_theme", False)

    if json:
        theme = pywal.util.read_file_json(filename)
    else:
        theme = get_pywal_dict(filename)

    if "color" in theme:
        color_list = theme["color"]
    else:
        color_list = list(theme["colors"].values())

    if is_new and not json:
        if auto_adjust or light_theme:
            color_list = auto_adjust_colors(color_list)
        sample.create_sample(color_list, files.get_sample_path(filename))
        write_colors(filename, color_list)

    return color_list


def is_dark_theme(color_list):
    """compare brightness values to see if a color-scheme
    is light or dark"""
    fg_brightness = util.get_hls_val(color_list[7], "light")
    bg_brightness = util.get_hls_val(color_list[0], "light")

    return fg_brightness > bg_brightness


def shuffle_colors(colors):
    """shuffle a color list in gorups of 8"""
    color_group = [[colors[i], colors[i + 8]] for i in range(1, 7)]
    shuffle(color_group)

    bg = [colors[0]] + [c[0] for c in color_group] + [colors[7]]
    fg = [colors[8]] + [c[1] for c in color_group] + [colors[15]]

    return bg + fg


def write_colors(img, color_list):
    """write changes to a cache file to persist customizations"""
    full_path = os.path.join(WALL_DIR, img)
    color_dict = pywal.colors.colors_to_dict(color_list, full_path)
    cache_file = files.get_cache_path(img)

    pywal.export.color(color_dict, "json", cache_file)


def change_colors(colors, which):
    opt = which

    if which in FILE_DIC:
        which = FILE_DIC[which]

    try:
        with open("%s.base" % which, "r") as tmp_file:
            first_line = tmp_file.readline()

            if "wpgtk-ignore" not in first_line:
                tmp_file.seek(0)
                tmp_data = tmp_file.read()
                tmp_data = tmp_data.format_map(colors)

                with open(which, "w") as target_file:
                    target_file.write(tmp_data)
                    logging.info("wrote: %s" % opt.split("/").pop())

    except KeyError as e:
        logging.error("%s in %s - key does not exist" % (e, opt))

    except IOError:
        logging.error("%s - base file does not exist" % opt)


def smart_sort(colors):
    """automatically set the most look-alike colors to their
    corresponding place in the standar xterm colors"""
    colors = colors[:8]
    sorted_by_color = list()
    base_colors = ["#000000", "#ff0000", "#00ff00", "#ffff00",
                   "#0000ff", "#ff00ff", "#00ffff", "#ffffff"]

    for y in base_colors:
        cd_tuple = [(x, util.get_distance(x, y)) for i, x in enumerate(colors)]
        cd_tuple.sort(key=itemgetter(1))
        sorted_by_color.append(cd_tuple)

    i = 0
    while i < 8:
        current_cd = sorted_by_color[i][0]
        closest_cds = [sorted_by_color[x][0] for x in range(8)]
        reps = [x for x in range(8) if closest_cds[x][0] == current_cd[0]]

        if len(reps) > 1:
            closest = min([closest_cds[x] for x in reps], key=itemgetter(1))
            reps = [x for x in reps if x != closest_cds.index(closest)]
            any(sorted_by_color[x].pop(0) for x in reps)
            i = 0
        else:
            i += 1

    sorted_colors = [sorted_by_color[x][0][0] for x in range(8)]
    return [*sorted_colors, *sorted_colors]


def auto_adjust_colors(clist):
    """create a clear foreground and background set of colors"""
    light = settings.getboolean("light_theme", False)

    if settings.getboolean("smart_sort", True):
        clist = smart_sort(clist)

    alter_brightness = util.alter_brightness
    get_hls_val = util.get_hls_val

    added_sat = 0.25 if light else 0.1
    sign = -1 if light else 1

    if light == is_dark_theme(clist):
        clist[7], clist[0] = clist[0], clist[7]

    comment = [alter_brightness(clist[0], sign * 25)]
    fg = [alter_brightness(clist[7], sign * 60)]
    clist = clist[:8] + comment \
        + [alter_brightness(x, sign * get_hls_val(x, "light") * 0.3, added_sat)
           for x in clist[1:7]] + fg

    return clist


def change_templates(colors):
    """call change_colors on each custom template
    installed or defined by the user"""
    templates = files.get_file_list(OPT_DIR, images=False)
    templates = [x for x in templates if ".base" in x]

    try:
        for template in templates:
            original = template.split(".base").pop(0)
            args = (colors, os.path.join(OPT_DIR, original))
            t = threading.Thread(target=change_colors, args=args)
            t.start()

    except Exception as e:
        logging.error(str(e))
        logging.error("optional file " + original, file=sys.stderr)


def add_icon_colors(colors):
    try:
        icon_dic = dict()
        entry = re.compile(r"(.*)=(.*)$")

        with open(FILE_DIC["icon-step1"], "r") as icon_file:
            for line in icon_file:
                match = entry.search(line)
                if match:
                    icon_dic[match.group(1)] = match.group(2)

        icon_dic["oldglyph"] = icon_dic["newglyph"]
        icon_dic["oldfront"] = icon_dic["newfront"]
        icon_dic["oldback"] = icon_dic["newback"]

        return icon_dic

    except KeyError:
        logging.error("icons - badly formatted base file for icons")
        return dict()

    except IOError:
        logging.error("icons - base file does not exists")
        return dict()


def wpgtk_colors(hexc, is_dark_theme=True):
    """extract active and inactive colors from a given
    hex color value"""
    brightness = util.get_hls_val(hexc, "light")

    active = util.alter_brightness(hexc, brightness * -0.20) \
        if is_dark_theme else util.alter_brightness(hexc, brightness * 0.30)

    inactive = util.alter_brightness(hexc, brightness * -0.45) \
        if is_dark_theme else hexc

    return {
        "active": active,
        "inactive": inactive,
        "newfront": active,
        "newback": inactive,
        "newglyph": util.alter_brightness(inactive, -15)
    }


def get_color_dict(cdic):
    """ensamble wpgtk color dictionary"""
    index = settings.getint("active")
    index = index if index > 0 else randint(9, 14)

    base_color = cdic["colors"]["color%s" % index]
    color_list = list(cdic["colors"].values())

    all_colors = {
        "wallpaper": cdic["wallpaper"],
        "alpha": cdic["alpha"],
        **cdic["special"],
        **cdic["colors"],
        **add_icon_colors(cdic),
        **wpgtk_colors(base_color, is_dark_theme(color_list))
    }

    try:
        user_words = {k: v.format(**all_colors)
                      for k, v in user_keywords.items()}
        all_colors = {**all_colors, **user_words}

    except KeyError as e:
        logging.error("%s - invalid, use double {{}} "
                      "to escape curly braces" % e)

    return {k: pywal.util.Color(v) for k, v in all_colors.items()}


def apply_colorscheme(colors):
    color_dict = get_color_dict(colors)

    if os.path.isfile(FILE_DIC["icon-step2"]):
        change_colors(color_dict, "icon-step1")
        Popen(FILE_DIC["icon-step2"])

    change_templates(color_dict)
