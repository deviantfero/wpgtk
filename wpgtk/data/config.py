import configparser
import os

__version__ = '4.5'

HOME = os.path.expanduser('~')
CONF_FILE = os.path.join(HOME, '.wallpapers/wpg.conf')
WALL_DIR = os.path.join(HOME, '.wallpapers')
SAMPLE_DIR = os.path.join(WALL_DIR, 'sample')
XRES_DIR = os.path.join(WALL_DIR, 'xres')
CSS_DIR = os.path.join(WALL_DIR, 'css')
SHELL_DIR = os.path.join(WALL_DIR, 'shell')
SCHEME_DIR = os.path.join(WALL_DIR, 'schemes')
OPT_DIR = os.path.join(HOME, '.themes/color_other')

FILE_DIC = {'openbox':    os.path.join(HOME, '.themes/colorbamboo/openbox-3/themerc'),
            'openbox-nb': os.path.join(HOME, '.themes/colorbamboo-nb/openbox-3/themerc'),
            'tint2':      os.path.join(HOME, '.config/tint2/tint2rc'),
            'gtk2':       os.path.join(HOME, '.themes/FlatColor/gtk-2.0/gtkrc'),
            'gtk3.0':     os.path.join(HOME, '.themes/FlatColor/gtk-3.0/gtk.css'),
            'gtk3.20':    os.path.join(HOME, '.themes/FlatColor/gtk-3.20/gtk.css'),
            'icon-step1': os.path.join(HOME, '.icons/flattrcolor/scripts/replace_folder_file.sh'),
            'icon-step2': os.path.join(HOME, '.icons/flattrcolor/scripts/replace_script.sh')}


class Config():

    """This class contains the parsed configuration
       File and is to be a singleton for use in all
       other modules and classes"""

    class __Config():
        def __init__(self, config_path):
            self.config_path = config_path
            self.options = configparser.ConfigParser()
            self.options.read(self.config_path)

    options = None
    instance = None

    # Just parse the configuration once, unless reload_config
    # Method is called, the configuration file is never refreshed

    def __init__(self, config_path=CONF_FILE):
        if not self.instance:
            self.instance = self.__Config(config_path)
            self.options = self.instance.options
        elif config_path != self.instance.config_path:
            self.instance = self.__Config(config_path)
            self.options = self.instance.options

    def reload_conf(self, config_path=CONF_FILE):
        self.instance = self.__Config(config_path)
        self.options = self.instance.options

    def write_conf(self, config_path=CONF_FILE):
        with open(config_path, 'w') as config_file:
            self.options.write(config_file)


conf_file = Config(CONF_FILE)
wpgtk = conf_file.options['wpgtk']
wal = conf_file.options['wal']