from os import walk
from . import config
import re


class FileList():
    def __init__(self, path):
        valid = re.compile('^[^\.](.*\.png$|.*\.jpg$|.*\.jpeg$|.*\.jpe$)')
        self.files = []
        self.file_names_only = []
        for(dirpath, dirnames, filenames) in walk(config.WALL_DIR):
            for f in filenames:
                self.files.append(f)
            break
        self.files = [elem for elem in self.files if valid.fullmatch(elem)]
        self.file_names_only = self.files

    def show_list(self):
        for f in self.files:
            print(f)

    def show_files_only(self):
        print(self.file_names_only)
