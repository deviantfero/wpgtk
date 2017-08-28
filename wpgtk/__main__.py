#!/usr/bin/env python3
import sys
import random
import wpgtk.data.config as config
from wpgtk.data import files, themer
from wpgtk.data.config import __version__
try:
    from wpgtk.gui import theme_picker
except:
    pass
import argparse
import pywal


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s',
                        help='set the wallpaper and colorscheme, apply \
                        changes system-wide',
                        nargs='*')
    parser.add_argument('-r',
                        help='restore the wallpaper and colorscheme',
                        action='store_true')
    parser.add_argument('-m',
                        help='pick a random wallpaper and set it',
                        action='store_true')
    parser.add_argument('-a',
                        help='add images to the wallpaper folder and generate \
                        colorschemes',
                        nargs='*')
    parser.add_argument('-l',
                        help='see which wallpapers are available',
                        action='store_true')
    parser.add_argument('--version', '-v',
                        help='print the current version',
                        action='store_true')
    parser.add_argument('-d',
                        help='delete the wallpaper(s) from wallpaper folder',
                        nargs='*')
    parser.add_argument('-c',
                        help='shows the current wallpaper',
                        action='store_true')
    parser.add_argument('-e',
                        help='auto adjusts the given colorscheme(s)',
                        nargs='*')
    parser.add_argument('-z',
                        help='shuffles the given colorscheme(s)',
                        nargs='*')
    parser.add_argument('-t',
                        help='send color sequences to all terminals',
                        action='store_true')
    parser.add_argument('-x',
                        help='add, remove and list \
                             templates instead of themes',
                        action='store_true')
    parser.add_argument('-y',
                        help='add an existent basefile template',
                        nargs='*')

    config.init()
    args = parser.parse_args()

    if len(sys.argv) < 2:
        try:
            theme_picker.run()
        except NameError:
            print('ERR:: missing pygobject module, use cli', file=sys.stderr)

    if args.s:
        if len(args.s) == 1:
            try:
                themer.set_theme(args.s[0], args.s[0], args.r)
            except TypeError as e:
                print('ERR:: file ' + args.s[0] + ' not found')
                raise e
        elif len(args.s) == 2:
            try:
                themer.set_theme(args.s[0], args.s[1], args.r)
            except TypeError:
                print('ERR:: file  not found')
        elif len(args.s) > 2:
            print('ERR:: Specify just 2 filenames')

    if args.l:
        if args.x:
            templates = files.get_file_list(config.OPT_DIR, False)
            [print(t) for t in templates if '.base' in t]
        else:
            files.show_files()

    if args.t:
        pywal.reload.colors(True, config.WALL_DIR)

    if args.version:
        print('current version: ' + __version__)

    if args.d:
        for e in args.d:
            if args.x:
                files.remove_template(e)
            else:
                themer.delete_theme(e)

    if args.c:
        themer.show_current()

    if args.a:
        if args.x:
            files.add_template(args.a[0])
        else:
            for e in args.a:
                themer.create_theme(e)

    if args.m:
        filename = random.choice(files.get_file_list())
        themer.set_theme(filename, filename)

    if args.e:
        for arg in args.e:
            themer.auto_adjust_colors(arg)
            print('OK:: Auto-adjusted %s' % arg)

    if args.z:
        for arg in args.z:
            themer.shuffle_colors(arg)
            themer.auto_adjust_colors(arg)
            print('OK:: shuffled %s' % arg)

    if args.y:
        files.add_template(arg.y[0], arg.y[1])


if __name__ == "__main__":
    main()
