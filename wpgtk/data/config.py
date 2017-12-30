import configparser
import shutil
import os
import sys

__version__ = '4.6.8'

options = None
wpgtk = None
wal = None

HOME = os.path.expanduser('~')
CONF_FILE = os.path.join(HOME, '.wallpapers/wpg.conf')
MODULE_DIR = os.path.abspath(os.path.join(__file__, "../../"))
CONF_BACKUP = os.path.join(MODULE_DIR, 'misc/wpg.conf')
WALL_DIR = os.path.join(HOME, '.wallpapers')
SAMPLE_DIR = os.path.join(WALL_DIR, 'sample')
XRES_DIR = os.path.join(WALL_DIR, 'xres')
CSS_DIR = os.path.join(WALL_DIR, 'css')
SHELL_DIR = os.path.join(WALL_DIR, 'shell')
SCHEME_DIR = os.path.join(WALL_DIR, 'schemes')
OPT_DIR = os.path.join(HOME, '.themes/color_other')
RCC = []  # random color cache


FILE_DIC = {'gtk2':       os.path.join(HOME, '.themes/FlatColor/gtk-2.0/gtkrc'),
            'gtk3.0':     os.path.join(HOME, '.themes/FlatColor/gtk-3.0/gtk.css'),
            'gtk3.20':    os.path.join(HOME, '.themes/FlatColor/gtk-3.20/gtk.css'),
            'icon-step1': os.path.join(HOME, '.icons/flattrcolor/scripts/replace_folder_file.sh'),
            'icon-step2': os.path.join(HOME, '.icons/flattrcolor/scripts/replace_script.sh')}


def write_conf(config_path=CONF_FILE):
    global options
    with open(config_path, 'w') as config_file:
        options.write(config_file)


def load_sections():
    global options
    global wpgtk
    global wal
    options = configparser.ConfigParser()
    options.read(CONF_FILE)
    wpgtk = options['wpgtk']
    wal = options['wal']


def init():
    try:
        if not os.path.isdir(SCHEME_DIR):
            print('INF:: Creating dirs...')
            os.makedirs(XRES_DIR, exist_ok=True)
            os.makedirs(SAMPLE_DIR, exist_ok=True)
            os.makedirs(SCHEME_DIR, exist_ok=True)
            os.makedirs(OPT_DIR, exist_ok=True)
        load_sections()
        return 0
    except:
        print('ERR:: Not a valid config file', file=sys.stderr)
        print('INF:: Copying default config file')
        pass

    shutil.copy(CONF_BACKUP, CONF_FILE)
    load_sections()
