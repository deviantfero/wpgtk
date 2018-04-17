#!/usr/bin/env python3
import sys
import random
import pywal
import logging
import wpgtk.data.config as config
from os import path
from subprocess import Popen
from wpgtk.data import files, themer, color, util, sample
from wpgtk.data.config import __version__
try:
    from wpgtk.gui import theme_picker
except:
    pass
import argparse


def read_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("-s",
                        help="set the wallpaper and colorscheme, "
                        "apply changes system-wide",
                        nargs="*")

    parser.add_argument("-r",
                        help="restore the wallpaper and colorscheme",
                        action="store_true")

    parser.add_argument("-m",
                        help="pick a random colorscheme and set it, specify "
                        "wallpaper to avoid changing it",
                        const="random_both", nargs="?")

    parser.add_argument("-n",
                        help="Don't set the wallpaper at all when applying "
                        "colorscheme",
                        action="store_true")

    parser.add_argument("-a",
                        help="add a wallpaper and generate a colorscheme",
                        nargs="*")

    parser.add_argument('-l',
                        help="see which wallpapers are available",
                        action="store_true")

    parser.add_argument("--version",
                        help="print the current version",
                        action="store_true")

    parser.add_argument("-d",
                        help="delete the wallpaper(s) from wallpaper folder",
                        nargs="*")

    parser.add_argument("-c",
                        help="shows the current wallpaper",
                        action="store_true")

    parser.add_argument("-z",
                        help="shuffles the given colorscheme(s)",
                        nargs="*")

    parser.add_argument("-i",
                        help="import a theme in json format and asign "
                        "to wallpaper [wallpaper, json]",
                        nargs="*")

    parser.add_argument("-o",
                        help="export a theme in json "
                        "format [wallpaper, json]",
                        nargs="*")

    parser.add_argument("-t",
                        help="send color sequences to all terminals VTE true",
                        action="store_true")

    parser.add_argument("-x",
                        help="add, remove and list templates instead "
                        "of themes",
                        action="store_true")

    parser.add_argument("-y",
                        help="add an existent basefile template "
                        "[config, basefile]",
                        nargs='*')

    parser.add_argument("--backend",
                        help="select a temporary backend",
                        const="list", nargs="?")

    return parser.parse_args()


def process_args(args):
    if args.backend is not None and args.backend != "list":
        if args.backend in pywal.colors.list_backends():
            config.wpgtk['backend'] = args.backend
        else:
            logging.error("no such backend, please "
                          "choose a valid backend")
            exit(1)

    if args.m == "random_both":
        filename = random.choice(files.get_file_list())
        themer.set_theme(filename, filename)
        exit(0)

    if args.m:
        filename = random.choice(files.get_file_list())
        themer.set_theme(args.m, filename)
        exit(0)

    if args.s:
        if len(args.s) == 1:
            themer.set_theme(args.s[0], args.s[0], args.r, not args.n)
        elif len(args.s) == 2:
            themer.set_theme(args.s[0], args.s[1], args.r, not args.n)
        else:
            logging.error("specify just 2 filenames")
            exit(1)
        exit(0)

    if args.l:
        if args.x:
            templates = files.get_file_list(config.OPT_DIR, False)
            [print(t) for t in templates if ".base" in t]
        else:
            files.show_files()
        exit(0)

    if args.t:
        Popen(["cat", path.join(config.WPG_DIR, "sequences")])
        exit(0)

    if args.version:
        print("current version: " + __version__)
        exit(0)

    if args.d:
        for e in args.d:
            if args.x:
                files.delete_template(e)
            else:
                themer.delete_theme(e)
        exit(0)

    if args.c:
        themer.get_current(show=True)
        exit(0)

    if args.a:
        add_function = files.add_template if args.x else themer.create_theme
        for file in args.a:
            add_function(file)
        exit(0)

    if args.z:
        for arg in args.z:
            colors = color.get_color_list(arg)
            colors = color.shuffle_colors(colors)
            color.write_colors(colors)

            sample.create_sample(colors, files.get_sample_path(arg))
            logging.info("shuffled %s" % arg)
        exit(0)

    if args.y:
        if len(args.i) != 2:
            logging.error("specify a config and a basefile")
            exit(1)
        files.add_template(args.y[0], args.y[1])
        exit(0)

    if args.i:
        if len(args.i) != 2:
            logging.error("specify a wallpaper and a colorscheme json")
            exit(1)
        themer.import_theme(args.i[0], args.i[1])
        exit(0)

    if args.o:
        if len(args.o) > 2:
            logging.error("specify wallpaper and optionally an output path")
            exit(1)
        else:
            themer.export_theme(*args.o)
            exit(0)

    if args.backend == "list":
        print("\n".join(pywal.colors.list_backends()))
        exit(0)


def main():
    config.init()
    util.setup_log()
    args = read_args(sys.argv[1:])
    process_args(args)
    try:
        theme_picker.run(args)
    except NameError:
        logging.error("missing pygobject module, use cli")


if __name__ == "__main__":
    main()
