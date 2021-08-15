import sys
import random
import pywal
import logging
import argparse
import glob
from os import path
from .data import files
from .data import themer
from .data import color
from .data import util
from .data import sample
from .data.config import OPT_DIR, __version__
from .data.config import settings


def read_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("--version",
                        help="print the current version",
                        action="store_true")

    parser.add_argument("-a",
                        help="add a wallpaper and generate a colorscheme",
                        nargs="+")

    parser.add_argument("-d",
                        help="delete the wallpaper(s) from wallpaper folder",
                        nargs="+")

    parser.add_argument("-t",
                        help="add, remove and list templates instead "
                        "of themes",
                        action="store_true")

    parser.add_argument("-s",
                        help="set the wallpaper and/or colorscheme",
                        nargs="+")

    parser.add_argument('-l',
                        help="see which wallpapers are available",
                        action="store_true")

    parser.add_argument("-n",
                        help="avoid setting a wallpaper",
                        action="store_true")

    parser.add_argument("-m",
                        help="pick a random wallpaper/colorscheme",
                        action="store_true")

    parser.add_argument("-c",
                        help="shows the current wallpaper",
                        action="store_true")

    parser.add_argument("-z",
                        help="shuffles the given colorscheme(s)",
                        nargs="+")

    parser.add_argument("-A",
                        help="auto-adjusts the given colorscheme(s)",
                        nargs="+")

    parser.add_argument("-r",
                        help="restore the wallpaper and colorscheme",
                        action="store_true")

    parser.add_argument("-L", "--light",
                        help="temporarily enable light themes",
                        action="store_true")

    parser.add_argument("--theme",
                        help="list included pywal themes "
                        "or replace your current colorscheme with a "
                        "selection of your own",
                        const="list", nargs="?")

    parser.add_argument("-T",
                        help="assign a pywal theme to a specific wallpaper"
                        " instead of a json file",
                        action="store_true")

    parser.add_argument("-i",
                        help="import a theme in json format and assign "
                        "to a wallpaper [wallpaper, json]",
                        nargs=2)

    parser.add_argument("-o",
                        help="export a theme in json "
                        "format [wallpaper, json]",
                        nargs="+")

    parser.add_argument("-R",
                        help="reset template(s) to their original colors",
                        nargs="+")

    parser.add_argument("--link",
                        help="link config file to template backup "
                        "[.base, config]",
                        nargs=2)

    parser.add_argument("--sat",
                        help="add or substract the saturation of a "
                        "colorscheme [colorscheme, sat] (0, 1)",
                        nargs=2)

    parser.add_argument("--brt",
                        help="add or substract the brightness of a "
                        "colorscheme [colorscheme, brt] (0, 255)",
                        nargs=2)

    parser.add_argument("--backend",
                        help="select a temporary backend",
                        const="list", nargs="?")

    parser.add_argument("--alpha",
                        help="set a one time alpha value",
                        nargs=1)

    parser.add_argument("--preview",
                        help="preview your current colorscheme",
                        action="store_true")

    parser.add_argument("--noreload",
                        help="Skip reloading other software after"
                        "applying colorscheme",
                        action="store_true")

    return parser.parse_args()


def process_arg_errors(args):
    if args.r and not args.s:
        logging.error("invalid combination of flags, use with -s")
        exit(1)

    if args.m and (args.s or args.R):
        logging.error("invalid combination of flags")
        exit(1)

    if args.sat and args.brt:
        logging.error("invalid combination of flags")
        exit(1)

    if args.s and len(args.s) > 2:
        logging.error("specify at most 2 filenames")
        exit(1)

    if args.o and (len(args.o) < 1 or len(args.o) > 2):
        logging.error("specify wallpaper and optionally an output path")
        exit(1)


def process_args(args):
    if args.light:
        settings["light_theme"] = "true"

    if args.n:
        settings["set_wallpaper"] = "false"

    if args.alpha:
        settings["alpha"] = args.alpha[0]

    if args.backend and args.backend != "list":
        if args.backend in pywal.colors.list_backends():
            settings['backend'] = args.backend
        else:
            logging.error("no such backend, please "
                          "choose a valid backend")
            exit(1)

    if args.preview:
        pywal.colors.palette()
        exit(0)

    if args.m:
        file_list = files.get_file_list()
        if len(file_list) > 0:
            filename = random.choice(file_list)
            themer.set_theme(filename, filename, args.r)
            exit(0)
        else:
            logging.error("you have no themes")
            exit(1)

    if args.s:
        if len(args.s) == 1:
            themer.set_theme(args.s[0], args.s[0], args.r)
        elif len(args.s) == 2:
            themer.set_theme(args.s[0], args.s[1], args.r)
        exit(0)

    if args.l:
        if args.t:
            templates = files.get_file_list(OPT_DIR, r".*\.base$")
            any(print(t) for t in templates)
        else:
            print("\n".join(files.get_file_list()))
        exit(0)

    if args.version:
        print("current version: " + __version__)
        exit(0)

    if args.d:
        delete_action = files.delete_template if args.t \
                        else themer.delete_theme
        try:
            any(delete_action(x) for x in args.d)
        except IOError:
            logging.error("file not found")
            exit(1)

        exit(0)

    if args.a:
        add_action = files.add_template if args.t \
                     else themer.create_theme
        for x in args.a:
            if path.isfile(glob.glob(x)[0]):
                add_action(glob.glob(x)[0])
        exit(0)

    if args.c:
        print(themer.get_current())
        exit(0)

    if args.z or args.A:
        alter_action = color.shuffle_colors if args.z \
                       else color.auto_adjust
        arg_list = args.z if args.z else args.A

        for arg in arg_list:
            colors = color.get_color_list(arg)
            colors = alter_action(colors)
            color.write_colors(arg, colors)

            sample.create_sample(colors, files.get_sample_path(arg))
            logging.info("shuffled %s" % arg)
        exit(0)

    if args.link:
        files.add_template(args.link[1], args.link[0])
        exit(0)

    if args.i:
        themer.import_theme(args.i[0], args.i[1], args.T)
        exit(0)

    if args.o:
        themer.export_theme(*args.o)
        exit(0)

    if args.R:
        try:
            any(themer.reset_theme(arg) for arg in args.R)
        except IOError:
            logging.error("file not found")
            exit(1)
        exit(0)

    if args.theme == "list":
        dark = settings['light_theme'] != "true"
        name_dic = pywal.theme.list_themes(dark)
        name_list = [t.name.replace(".json", "") for t in name_dic]
        print("\n".join(name_list))
        exit(0)

    if args.sat:
        cl = color.get_color_list(args.sat[0])
        val = float(args.sat[1])
        cl = [util.alter_brightness(x, 0, val) for x in cl]

        color.write_colors(args.sat[0], cl)
        sample.create_sample(cl, files.get_sample_path(args.sat[0]))
        exit(0)

    if args.brt:
        cl = color.get_color_list(args.brt[0])
        val = float(args.brt[1])
        cl = [util.alter_brightness(x, val, 0) for x in cl]

        color.write_colors(args.brt[0], cl)
        sample.create_sample(cl, files.get_sample_path(args.brt[0]))
        exit(0)

    if args.theme and args.theme != "list":
        light = settings['light_theme'] == "true"
        themer.set_pywal_theme(args.theme, light)
        exit(0)

    if args.backend == "list":
        print("\n".join(pywal.colors.list_backends()))
        exit(0)

    if args.noreload:
        settings["reload"] = "false"


def main():
    util.setup_log()
    args = read_args(sys.argv[1:])
    process_arg_errors(args)
    process_args(args)

    try:
        _gui = __import__("wpgtk.gui.theme_picker", fromlist=['theme_picker'])
        _gui.run(args)
        exit(0)
    except NameError:
        logging.error("missing pygobject module, use cli")
        exit(1)


if __name__ == "__main__":
    main()
