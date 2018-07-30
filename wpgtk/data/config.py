import configparser
import shutil
import os

import logging

__version__ = '5.5.2'

options = None
wpgtk = None
keywords = None

HOME = os.path.expanduser("~")
WPG_DIR = os.path.join(HOME, ".config/wpg")
CONF_FILE = os.path.join(WPG_DIR, "wpg.conf")
MODULE_DIR = os.path.abspath(os.path.join(__file__, "../../"))
CONF_BACKUP = os.path.join(MODULE_DIR, "misc/wpg.conf")
WALL_DIR = os.path.join(WPG_DIR, "wallpapers")
SAMPLE_DIR = os.path.join(WALL_DIR, "sample")
XRES_DIR = os.path.join(WALL_DIR, "xres")
CSS_DIR = os.path.join(WALL_DIR, "css")
SHELL_DIR = os.path.join(WALL_DIR, "shell")
SCHEME_DIR = os.path.join(WALL_DIR, "schemes")
OPT_DIR = os.path.join(WPG_DIR, "templates")
XREC_DIR = os.path.join(HOME, ".Xresources") # path for xresources (for alpha)
XDEF_DIR = os.path.join(HOME, ".Xdefaults") # path for xdefaults (for alpha)
RCC = []  # random color cache


FILE_DIC = {'templates':  os.path.join(HOME, ".config/wpg/templates"),
            'icon-step1': os.path.join(HOME, ".icons/flattrcolor/scripts"
                                             "/replace_folder_file.sh"),
            'icon-step2': os.path.join(HOME, ".icons/flattrcolor/scripts"
                                             "/replace_script.sh")}


def write_conf(config_path=CONF_FILE):
    global options
    with open(config_path, 'w') as config_file:
        options.write(config_file)


def load_sections():
    global options
    global wpgtk
    global keywords
    options = configparser.ConfigParser()
    options.optionxform = str
    options.read(CONF_FILE)
    wpgtk = options['wpgtk']
    keywords = options['keywords']


def init():
    try:
        if not os.path.isdir(SCHEME_DIR):
            logging.info('creating dirs...')
            os.makedirs(XRES_DIR, exist_ok=True)
            os.makedirs(SAMPLE_DIR, exist_ok=True)
            os.makedirs(SCHEME_DIR, exist_ok=True)
            os.makedirs(OPT_DIR, exist_ok=True)
        load_sections()
        return 0
    except:
        logging.error("not a valid config file")
        logging.info("copying default config file")
        pass

    shutil.copy(CONF_BACKUP, CONF_FILE)
    load_sections()
