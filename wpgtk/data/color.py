import sys
import logging
import pywal
import os
from operator import itemgetter
from subprocess import Popen
from random import shuffle, randint

from .config import settings, user_keywords
from .config import WALL_DIR, WPG_DIR, FILE_DIC, OPT_DIR
from . import files
from . import util
from . import sample


def get_pywal_dict(wallpaper):
    """get the color dictionary of a given wallpaper"""
    pywal.util.Color.alpha_num = settings.get("alpha", "100")
    image = pywal.image.get(os.path.join(WALL_DIR, wallpaper))

    return pywal.colors.get(
        image,
        backend=settings.get("backend", "wal"),
        cache_dir=WPG_DIR
    )


def get_color_list(filename, json=False):
    """extract a list with 16 colors from a json or a pywal dict"""
    is_new = not os.path.isfile(files.get_cache_path(filename))

    if json:
        theme = pywal.util.read_file_json(filename)
    else:
        theme = get_pywal_dict(filename)

    if "color" in theme:
        color_list = theme["color"]
    else:
        color_list = list(theme["colors"].values())

    if is_new and not json:
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

    tmp_filename = which + ".base"
    try:
        with open(tmp_filename, "r") as tmp_file:
            first_line = tmp_file.readline()
            tmp_file.seek(0)
            tmp_data = tmp_file.read()

        if "wpgtk-ignore" not in first_line:
            for k, v in user_keywords.items():
                tmp_data = tmp_data.replace(util.build_key(k), v)

            for k, v in {**colors["wpgtk"], **colors["colors"]}.items():
                tmp_data = tmp_data.replace(util.build_key(k.upper()), v.strip("#"))

            if colors["icons"] and opt == "icon-step1":
                for k, v in colors["icons"].items():
                    tmp_data = tmp_data.replace(k, v.strip("#"))

            with open(which, "w") as target_file:
                target_file.write(tmp_data)
                logging.info("wrote: %s" % opt.split("/").pop())

    except IOError:
        logging.error("%s - base file does not exist" % opt)


def smart_sort(colors):
    """automatically set the most look-alike colors to their
    corresponding place in the standar xterm colors"""
    colors = colors[:8]
    sorted_by_color = []
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

    comment = [alter_brightness(clist[0], sign * 20)]
    fg = [alter_brightness(clist[7], sign * 60)]
    clist = clist[:8] + comment \
        + [alter_brightness(x, sign * get_hls_val(x, "light") * 0.3, added_sat)
           for x in clist[1:7]] + fg

    return clist


def add_icon_colors(colors):
    try:
        glyph = util.alter_brightness(colors["wpgtk"]["COLORIN"], -15)
        icon_dic = {}

        with open(FILE_DIC["icon-step1"], "r") as icon_file:
            for line in icon_file:
                if("glyphColorNew=" in line):
                    icon_dic["oldglyph"] = line.split("=")[1].strip("\n")

                if("frontColorNew=" in line):
                    icon_dic["oldfront"] = line.split("=")[1].strip("\n")

                if("backColorNew=" in line):
                    icon_dic["oldback"] = line.split("=")[1].strip("\n")

        icon_dic["newglyph"] = glyph
        icon_dic["newfront"] = colors["wpgtk"]["COLORACT"]
        icon_dic["newback"] = colors["wpgtk"]["COLORIN"]

        return icon_dic

    except IOError:
        logging.error("icons - base file does not exists")
        return


def change_templates(colors):
    """call change_colors on each custom template
    installed or defined by the user"""
    templates = files.get_file_list(OPT_DIR, images=False)
    templates = [x for x in templates if ".base" in x]

    try:
        for template in templates:
            original = template.split(".base").pop(0)
            change_colors(colors, os.path.join(OPT_DIR, original))

    except Exception as e:
        logging.error(str(e))
        logging.error("optional file " + original, file=sys.stderr)


def split_active(hexc, is_dark_theme=True):
    """extract active and inactive colors from a given
    hex color value"""
    brightness = util.get_hls_val(hexc, "light")

    if is_dark_theme:
        return {"COLORACT": util.alter_brightness(hexc, brightness * -0.20),
                "COLORIN": util.alter_brightness(hexc, brightness * -0.45)}
    else:
        return {"COLORACT": util.alter_brightness(hexc, brightness * 0.30),
                "COLORIN": hexc}


def add_wpgtk_colors(cdic):
    """ensamble wpgtk color dictionary"""
    index = settings.getint("active")
    index = index if index > 0 else randint(9, 14)

    base_color = cdic["colors"]["color%s" % index]

    color_list = list(cdic["colors"].values())
    cdic["wpgtk"] = split_active(base_color, is_dark_theme(color_list))
    cdic["icons"] = add_icon_colors(cdic)

    return cdic


def apply_colorscheme(colors):
    colors = add_wpgtk_colors(colors)

    if os.path.isfile(FILE_DIC["icon-step2"]):
        change_colors(colors, "icon-step1")
        Popen(FILE_DIC["icon-step2"])

    change_templates(colors)
