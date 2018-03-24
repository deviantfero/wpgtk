#!/usr/bin/env python3
import sys
import random
import wpgtk.data.config as config
from os import path
from subprocess import Popen
from wpgtk.data import files, themer, logger, color
from wpgtk.data.config import __version__
try:
    from wpgtk.gui import theme_picker
except:
    pass
import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s",
                        help="set the wallpaper and colorscheme, apply changes system-wide",
                        nargs="*")

    parser.add_argument("-r",
                        help="restore the wallpaper and colorscheme",
                        action="store_true")

    parser.add_argument("-m",
                        help="pick a random colorscheme and set it, specify wallpaper to avoid changing it",
                        const="random_both", nargs="?")

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
                        help="import a theme in json format and asign to wallpaper [wallpaper, json]",
                        nargs="*")

    parser.add_argument("-o",
                        help="export a theme in json format [wallpaper, json path]",
                        nargs="*")

    parser.add_argument("-t",
                        help="send color sequences to all terminals VTE true",
                        action="store_true")

    parser.add_argument("-x",
                        help="add, remove and list templates instead of themes",
                        action="store_true")

    parser.add_argument("-y",
                        help="add an existent basefile template [config, basefile]",
                        nargs='*')

    config.init()
    args = parser.parse_args()

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
            try:
                themer.set_theme(args.s[0], args.s[0], args.r)
            except TypeError as e:
                logger.log.error("file " + args.s[0] + " not found")
                raise e
        elif len(args.s) == 2:
            try:
                themer.set_theme(args.s[0], args.s[1], args.r)
            except TypeError:
                logger.log.error("file  not found")
        elif len(args.s) > 2:
            logger.log.error("specify just 2 filenames")

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
                files.remove_template(e)
            else:
                themer.delete_theme(e)
        exit(0)

    if args.c:
        themer.get_current(show=True)

    if args.a:
        if args.x:
            files.add_template(args.a[0])
        else:
            for e in args.a:
                themer.create_theme(e)
        exit(0)

    if args.z:
        for arg in args.z:
            color.shuffle_colors(arg)
            themer.auto_adjust_theme(arg)
            logger.log.info("shuffled %s" % arg)
        exit(0)

    if args.y:
        files.add_template(args.y[0], args.y[1])
        exit(0)

    if (len(sys.argv) < 2):
        try:
            theme_picker.run(args)
        except NameError:
            logger.log.error("missing pygobject module, use cli")

    if args.i:
        if len(args.i) != 2:
            logger.log.error("specify a wallpaper and a colorscheme json")
            exit(1)
        themer.import_theme(args.i[0], args.i[1])

    if args.o:
        if len(args.o) == 2:
            themer.export_theme(args.o[0], args.o[1])
        elif len(args.o) == 1:
            themer.export_theme(args.o[0])
        else:
            logger.log.error("specify wallpaper and optionally an output path")
            exit(1)


if __name__ == "__main__":
    main()
