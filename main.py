#!/usr/bin/python
from gi import require_version
require_version( "Gtk", "3.0" )
from os import walk #fetch filenames
from getpass import getuser #findout the username so the route is absolute
#making sure it uses v3.0
from gi.repository import Gtk

class fileList():

    def __init__( self, path ):
        self.files = []
        number_list = []
        elem_counter = 1
        for( dirpath, dirnames, filenames ) in walk( "/home/" + getuser() + "/.wallpapers" ):
            self.files.extend( filenames )
        #self.files = [ elem for elem in self.files if ".Xres" in elem ]
        # filter function goes up there
        for elem in self.files:
            number_list.append( elem_counter )
            elem_counter += 1
        self.files = list( zip( number_list, self.files ) )

    def show_list( self ):
        print( self.files )

#-------------------------------------------------------------------------------------

class mainWindow( Gtk.Window ):

    def __init__( self ):
        Gtk.Window.__init__( self, title = "WP - Wallpaper Manager" )
        
        self.current_walls = fileList( "/home/fernando/.wallpapers" )
        self.current_walls.show_list()

        option_list = Gtk.ListStore( int, str )
        for x in range( 0, len(self.current_walls.files) ):
            option_list.append( list( self.current_walls.files[x] ) )

        option_combo = Gtk.ComboBox.new_with_model_and_entry( option_list )
        option_combo.set_entry_text_column( 1 )

        self.set_border_width( 10 )
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous( 1 )
        self.add( self.grid )
        self.button = Gtk.Button( label = "Add" )
        self.grid.add( self.button ) #adds to first cell in grid
        self.button.connect( "clicked", self.on_button_clicked )
        self.entry = Gtk.Entry()
        self.current_walls = Gtk.ComboBox()
        self.grid.attach( option_combo, 1, 0, 1, 1 )

    def on_button_clicked( self, widget ):
        print( "Hello World I work" )

if __name__ == "__main__":
    win = mainWindow()
    win.connect( "delete-event", Gtk.main_quit )
    win.show_all()
    Gtk.main()
