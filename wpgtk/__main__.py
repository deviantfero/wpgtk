#!/usr/bin/env python3
import sys
import wpgtk.data.config as config
from wpgtk.data import file_list, theme_interface
from wpgtk.data.config import __version__
try:
    from wpgtk.gui import theme_picker
except ModuleNotFoundError as err:
    pass
import argparse
import pywal


def main():
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
        try:
            theme_picker.run()
        except NameError:
            print('ERR:: missing pygobject module, use cli', file=sys.stderr)

    if args.set:
        if len(args.set) == 1:
            try:
                theme_interface.set_theme(args.set[0],
                                          args.set[0],
                                          args.restore)
            except TypeError as e:
                print('ERR:: file ' + args.set[0] + ' not found')
                raise e
        elif len(args.set) == 2:
            try:
                theme_interface.set_theme(args.set[0],
                                          args.set[1],
                                          args.restore)
            except TypeError:
                print('ERR:: file  not found')
        elif len(args.set) > 2:
            print('ERR:: Specify just 2 filenames')

    if args.list:
        files = file_list.FileList(config.WALL_DIR)
        files.show_list()
    if args.tty:
        pywal.reload.colors(True, config.WALL_DIR)
    if args.version:
        print('current version: ' + __version__)
    if args.delete:
        for e in args.delete:
            theme_interface.delete_theme(e)
    if args.current:
        theme_interface.show_current()
    if args.add:
        for e in args.add:
            theme_interface.create_theme(e)
    if args.auto:
        for arg in args.auto:
            theme_interface.auto_adjust_colors(arg)
            print('OK:: Auto-adjusted {}'.format(arg))

    if args.shuffle:
        for arg in args.shuffle:
            theme_interface.shuffle_colors(arg)
            theme_interface.auto_adjust_colors(arg)
            print(f'OK:: shuffled {arg}')


if __name__ == "__main__":
    main()
