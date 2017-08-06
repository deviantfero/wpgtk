import configparser
import pathlib

__version__ = "4.5"

HOME = pathlib.Path.home()
CONF_FILE = HOME / ".wallpapers/wpg.conf"
WALL_DIR = HOME / ".wallpapers"
SAMPLE_DIR = WALL_DIR / "sample"
XRES_DIR = WALL_DIR / "xres"
CSS_DIR = WALL_DIR / "css"
SHELL_DIR = WALL_DIR / "shell"
SCHEME_DIR = WALL_DIR / "schemes"

FILE_DIC = {'openbox':    HOME / '.themes/colorbamboo/openbox-3/themerc',
            'openbox-nb': HOME / '.themes/colorbamboo-nb/openbox-3/themerc',
            'tint2':      HOME / '.config/tint2/tint2rc',
            'gtk2':       HOME / '.themes/FlatColor/gtk-2.0/gtkrc',
            'gtk3.0':     HOME / '.themes/FlatColor/gtk-3.0/gtk.css',
            'gtk3.20':    HOME / '.themes/FlatColor/gtk-3.20/gtk.css',
            'icon-step1': HOME / '.icons/flattrcolor/scripts/replace_folder_file.sh',
            'icon-step2': HOME / '.icons/flattrcolor/scripts/replace_script.sh'}


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
