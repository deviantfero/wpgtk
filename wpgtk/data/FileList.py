import os.path #fetch filenames
from os import walk
from subprocess import Popen, call
import os.path #fetch filenames
from gi.repository import GLib
import re

class FileList():
    def __init__( self, path ):
        valid = re.compile('^[^\.](.*\.png$|.*\.jpg$)')
        self.files = []
        self.file_names_only = []
        number_list = []
        elem_counter = 1
        for( dirpath, dirnames, filenames ) in walk( GLib.get_home_dir() + "/.wallpapers" ):
            self.files.extend( filenames )
        self.files = [ elem for elem in self.files if valid.fullmatch(elem) ]
        self.file_names_only = self.files

    def show_list( self ):
        print( self.files )

    def show_files_only( self ):
        print( self.file_names_only )
