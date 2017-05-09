import os.path #fetch filenames
from os import walk
from subprocess import Popen, call
import os.path #fetch filenames
from gi.repository import GLib
import re

class FileList():
    def __init__( self, path ):
        valid = re.compile('^[^\.](.*\.png$|.*\.jpg$|.*\.jpeg$|.*\.jpe$)')
        self.files = []
        self.file_names_only = []
        number_list = []
        elem_counter = 1
        for( dirpath, dirnames, filenames ) in walk( GLib.get_home_dir() + "/.wallpapers" ):
            for f in filenames:
                self.files.append(f)
            break
        self.files = [ elem for elem in self.files if valid.fullmatch(elem) ]
        self.file_names_only = self.files

    def show_list( self ):
        for f in self.files:
            print(f)

    def show_files_only( self ):
        print( self.file_names_only )
