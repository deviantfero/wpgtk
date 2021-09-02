import configparser
import shutil
import os
import logging

__version__ = '6.5.3'


settings = None

HOME = os.getenv("HOME", os.path.expanduser("~"))
CACHE = os.getenv("XDG_CACHE_HOME", os.path.join(HOME, ".cache"))
CONFIG = os.getenv("XDG_CONFIG_HOME", os.path.join(HOME, ".config"))
LOCAL = os.getenv("XDG_DATA_HOME", os.path.join(HOME, ".local", "share"))

WPG_DIR = os.path.join(CONFIG, "wpg")
CONF_FILE = os.path.join(WPG_DIR, "wpg.conf")
KEYWORD_FILE = os.path.join(WPG_DIR, "keywords.conf")
MODULE_DIR = os.path.abspath(os.path.join(__file__, "../../"))
CONF_BACKUP = os.path.join(MODULE_DIR, "misc/wpg.conf")
WALL_DIR = os.path.join(WPG_DIR, "wallpapers")
SAMPLE_DIR = os.path.join(WPG_DIR, "samples")
SCHEME_DIR = os.path.join(WPG_DIR, "schemes")
FORMAT_DIR = os.path.join(CACHE, "wal")
OPT_DIR = os.path.join(WPG_DIR, "templates")
FILE_DIC = {
    'icon-step1': os.path.join(LOCAL, "icons/flattrcolor/scripts"
                               "/replace_folder_file.sh"),
    'icon-step2': os.path.join(LOCAL, "icons/flattrcolor/scripts"
                               "/replace_script.sh")
}


def write_conf(config_path=CONF_FILE):
    global config_parser

    with open(config_path, 'w') as config_file:
        config_parser.write(config_file)


def write_keywords(keywords_path=KEYWORD_FILE):
    global user_keywords

    with open(keywords_path, 'w') as keywords_file:
        user_keywords.write(keywords_file)


def load_settings():
    """reads the sections of the config file"""
    global settings
    global user_keywords
    global config_parser

    config_parser = configparser.ConfigParser()
    config_parser.optionxform = str
    config_parser.read(CONF_FILE)
    settings = config_parser['settings']


def load_keywords():
    global user_keywords

    if not os.path.exists(KEYWORD_FILE):
        open(KEYWORD_FILE, 'a').close()

    user_keywords = configparser.ConfigParser()
    user_keywords.optionxform = str
    user_keywords.read(KEYWORD_FILE)

    if not user_keywords.has_section('default'):
        user_keywords.add_section('default')
        write_keywords()


def init_config():
    os.makedirs(WALL_DIR, exist_ok=True)
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    os.makedirs(SCHEME_DIR, exist_ok=True)
    os.makedirs(FORMAT_DIR, exist_ok=True)
    os.makedirs(OPT_DIR, exist_ok=True)

    try:
        load_settings()
        load_keywords()
    except Exception:
        logging.error("not a valid config file")
        logging.info("copying default config file")

        shutil.copy(CONF_BACKUP, CONF_FILE)
        load_settings()
        load_keywords()


init_config()
