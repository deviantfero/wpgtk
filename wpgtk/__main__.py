import sys
import random
import pywal
import logging
import argparse
import glob
from os import path
from subprocess import Popen
from .data import files
from .data import themer
from .data import color
from .data import util
from .data import sample
from .data.config import OPT_DIR, WPG_DIR, __version__
from .data.config import settings


def read_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("-a",
                        help="add a wallpaper and generate a colorscheme",
                        nargs="+")

    parser.add_argument("-d",
                        help="delete the wallpaper(s) from wallpaper folder",
                        nargs="+")

    parser.add_argument("-s",
                        help="set the wallpaper and/or colorscheme",
                        nargs="+")

    parser.add_argument("-m",
                        help="pick a random wallpaper/colorscheme",
                        action="store_true")

    parser.add_argument('-l',
                        help="see which wallpapers are available",
                        action="store_true")

    parser.add_argument("-n",
                        help="don't change wallpaper",
                        action="store_true")

    parser.add_argument("-r",
                        help="restore the wallpaper and colorscheme",
                        action="store_true")

    parser.add_argument("--version",
                        help="print the current version",
                        action="store_true")

    parser.add_argument("-c",
                        help="shows the current wallpaper",
                        action="store_true")

    parser.add_argument("-L", "--light",
                        help="temporarily enable light themes",
                        action="store_true")

    parser.add_argument("-T",
                        help="assign a pywal theme to specific wallpaper"
                        " instead of a json file",
                        action="store_true")

    parser.add_argument("-t",
                        help="send color sequences to all "
                        "terminals (deprecated)",
                        action="store_true")

    parser.add_argument("-x",
                        help="add, remove and list templates instead "
                        "of themes",
                        action="store_true")

    parser.add_argument("-z",
                        help="shuffles the given colorscheme(s)",
                        nargs="+")

    parser.add_argument("-A",
                        help="auto-adjusts the given colorscheme(s)",
                        nargs="+")

    parser.add_argument("-i",
                        help="import a theme in json format and asign "
                        "to wallpaper [wallpaper, json]",
                        nargs=2)
    parser.add_argument("-o",
                        help="export a theme in json "
                        "format [wallpaper, json]",
                        nargs="+")

    parser.add_argument("-y",
                        help="link config file to template backup"
                        "[config, basefile]",
                        nargs="+")

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

    parser.add_argument("--pywal",
                        help="list included pywal themes "
                        "or replace your current colorscheme with a "
                        "selection of your own",
                        const="list", nargs="?")

    return parser.parse_args()


def process_arg_errors(args):
    if args.m and args.s:
        logging.error("invalid combination of flags")
        exit(1)

    if args.sat and args.brt:
        logging.error("invalid combination of flags")
        exit(1)

    if args.s and len(args.s) > 2:
        logging.error("specify at most 2 filenames")
        exit(1)

    if args.y and len(args.y) != 2:
        logging.error("specify a config and a basefile")
        exit(1)

    if args.i and len(args.i) != 2:
        logging.error("specify a wallpaper and a colorscheme json")
        exit(1)

    if args.o and len(args.o) != 2:
        logging.error("specify wallpaper and optionally an output path")
        exit(1)


def process_args(args):
    if args.light:
        settings["light_theme"] = "true"

    if args.n:
        settings["set_wallpaper"] = "false"

    if args.alpha:
        settings["alpha"] = args.alpha[0]

    if args.m:
        filename = random.choice(files.get_file_list())
        themer.set_theme(filename, filename, args.r)
        exit(0)

    if args.s:
        if len(args.s) == 1:
            themer.set_theme(args.s[0], args.s[0], args.r)
        elif len(args.s) == 2:
            themer.set_theme(args.s[0], args.s[1], args.r)
        exit(0)

    if args.l:
        if args.x:
            templates = files.get_file_list(OPT_DIR, False)
            any(print(t) for t in templates if ".base" in t)
        else:
            print("\n".join(files.get_file_list()))
        exit(0)

    if args.t:
        Popen(["cat", path.join(WPG_DIR, "sequences")])
        exit(0)

    if args.version:
        print("current version: " + __version__)
        exit(0)

    if args.d:
        delete_action = files.delete_template if args.x \
                        else themer.delete_theme
        any(delete_action(x) for x in args.d)
        exit(0)

    if args.a:
        add_action = files.add_template if args.x \
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
                       else color.auto_adjust_colors
        arg_list = args.z if args.z else args.A

        for arg in arg_list:
            colors = color.get_color_list(arg)
            colors = alter_action(colors)
            color.write_colors(arg, colors)

            sample.create_sample(colors, files.get_sample_path(arg))
            logging.info("shuffled %s" % arg)
        exit(0)

    if args.y:
        files.add_template(args.y[0], args.y[1])
        exit(0)

    if args.i:
        themer.import_theme(args.i[0], args.i[1], args.T)
        exit(0)

    if args.o:
        themer.export_theme(*args.o)
        exit(0)

    if args.pywal == "list":
        name_dic = pywal.theme.list_themes()
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

    if args.pywal and args.pywal != "list":
        themer.set_pywal_theme(args.pywal)
        exit(0)

    if args.backend == "list":
        print("\n".join(pywal.colors.list_backends()))
        exit(0)

    if args.backend and args.backend != "list":
        if args.backend in pywal.colors.list_backends():
            settings['backend'] = args.backend
        else:
            logging.error("no such backend, please "
                          "choose a valid backend")
            exit(1)


def main():
    util.setup_log()
    args = read_args(sys.argv[1:])
    process_arg_errors(args)
    process_args(args)

    try:
        _gui = __import__("wpgtk.gui.theme_picker", fromlist=['theme_picker'])
        _gui.run(args)
    except NameError:
        logging.error("missing pygobject module, use cli")


if __name__ == "__main__":
    main()
