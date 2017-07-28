from getpass import getuser
import configparser

HOME = "/home/" + getuser()
CONFILE = HOME + "/.wallpapers/wpg.conf"


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

    def __init__(self, config_path=CONFILE):
        if not self.instance:
            self.instance = self.__Config(config_path)
            self.options = self.instance.options
        elif config_path != self.instance.config_path:
            self.instance = self.__Config(config_path)
            self.options = self.instance.options

    def reload_conf(self, config_path=CONFILE):
        self.instance = self.__Config(config_path)
        self.options = self.instance.options

    def write_conf(self, config_path=CONFILE):
        with open(config_path, 'w') as config_file:
            self.options.write(config_file)


conf_file = Config(CONFILE)
wpgtk = conf_file.options['wpgtk']
wal = conf_file.options['wal']
