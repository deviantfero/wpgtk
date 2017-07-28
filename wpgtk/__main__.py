#!/usr/bin/env python3
import sys
from getpass import getuser
from subprocess import call
from core.gui import theme_picker
import core.data as data
from core.data import conf_parser
import argparse

HOME = "/home/" + getuser()
WALLDIR = HOME + "/.wallpapers/"
CONFIG = conf_parser.parse_conf()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--set', '-s',
                        help='set the wallpaper and colorscheme, apply \
                        changes system-wide',
                        nargs='*')
    parser.add_argument('--restore', '-r',
                        help='restore the wallpaper and colorscheme',
                        action='store_true')
    parser.add_argument('--add', '-a',
                        help='add images to the wallpaper folder and generate \
                        colorschemes',
                        nargs='*')
    parser.add_argument('--list', '-l',
                        help='see which wallpapers are available',
                        action='store_true')
    parser.add_argument('--version', '-v',
                        help='print the current version',
                        action='store_true')
    parser.add_argument('--delete', '-d',
                        help='delete the wallpaper(s) from wallpaper folder',
                        nargs='*')
    parser.add_argument('--current', '-c',
                        help='shows the current wallpaper',
                        action='store_true')
    parser.add_argument('--auto', '-e',
                        help='auto adjusts the given colorschemes',
                        nargs='*')
    parser.add_argument('--shuffle', '-z',
                        help='shuffles the given colorschemes',
                        nargs='*')
    parser.add_argument('--tty', '-t',
                        help='send sequences to terminal equivalent to wal -r',
                        action='store_true')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        theme_picker.run()

    if args.set:
        if len(args.set) == 1:
            try:
                data.set_theme(args.set[0], args.set[0], CONFIG, args.restore)
            except TypeError as e:
                print('ERR:: file ' + args.set[0] + ' not found')
                raise e
        elif len(args.set) == 2:
            try:
                data.set_theme(args.set[-1], args.set[1], CONFIG, args.restore)
            except TypeError:
                print('ERR:: file  not found')
        elif len(args.set) > 2:
            print('ERR:: Specify just 2 filenames')

    if args.list:
        data.show_wallpapers()
    if args.tty:
        call(['wal', '-r'])
    if args.version:
        print('current version: ' + theme_picker.version)
    if args.delete:
        for e in args.delete:
            data.delete_theme(e)
    if args.current:
        data.show_current()
    if args.add:
        for e in args.add:
            data.create_theme(e)
    if args.auto:
        for arg in args.auto:
            data.auto_adjust_colors(arg, CONFIG)
            print('OK:: Auto-adjusted {}'.format(arg))

    if args.shuffle:
        for arg in args.shuffle:
            data.shuffle_colors(arg)
            data.auto_adjust_colors(arg, CONFIG)
            print('OK:: shuffled {}'.format(arg))
