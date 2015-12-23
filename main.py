#!/usr/bin/python
from gi import require_version
require_version( "Gtk", "3.0" )
from os import walk
import os.path #fetch filenames
from getpass import getuser #findout the username so the route is absolute
#making sure it uses v3.0
from gi.repository import Gtk, GdkPixbuf

class fileList():

    def __init__( self, path ):
        self.files = []
        self.file_names_only = []
        number_list = []
        elem_counter = 1
        for( dirpath, dirnames, filenames ) in walk( "/home/" + getuser() + "/.wallpapers" ):
            self.files.extend( filenames )

        self.files = [ elem for elem in self.files if not ".Xres" in elem ]
        self.files = [ elem for elem in self.files if not ".sample" in elem ]
        self.files = [ elem for elem in self.files if not ".colors" in elem ]
        # filter function goes up there
        self.file_names_only = self.files

        for elem in self.files:
            number_list.append( elem_counter )
            elem_counter += 1
        self.files = list( zip( number_list, self.files ) )

    def show_list( self ):
        print( self.files )
    
    def show_files_only( self ):
        print( self.file_names_only )

#-------------------------------------------------------------------------------------
class mainWindow( Gtk.Window ):

    def __init__( self ):
        Gtk.Window.__init__( self, title = "WP - Wallpaper Manager" )
        
        filepath = "/home/" + getuser() + "/.wallpapers/"
        current_walls = fileList( filepath )
        current_walls.show_files_only()
        image_name = filepath + ".current"
        image_name = os.path.realpath( image_name )

        #these variables are just to get the image and preview of current wallpaper
        route_list = image_name.split( "/", image_name.count("/") )
        file_name = route_list[4]
        sample_name = filepath + "." + file_name + ".sample.png"

        option_list = Gtk.ListStore( int, str )
        for x in range( 0, len(current_walls.files) ):
            option_list.append( list( current_walls.files[x] ) )
        option_combo = Gtk.ComboBox.new_with_model_and_entry( option_list )
        option_combo.set_entry_text_column( 1 )

        self.set_border_width( 10 )
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous( 1 )
        self.grid.set_row_spacing( 10 )
        self.grid.set_column_spacing( 10 )
        self.add( self.grid )
        self.preview = Gtk.Image()
        self.sample = Gtk.Image()
        self.pixbuf_preview = GdkPixbuf.Pixbuf.new_from_file_at_scale( image_name, width=500, height=333, preserve_aspect_ratio=False )
        self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( sample_name, width=500, height=500 )
        self.preview.set_from_pixbuf( self.pixbuf_preview )
        self.sample.set_from_pixbuf( self.pixbuf_sample )
        self.add_button = Gtk.Button( label = "Add" )
        self.set_button = Gtk.Button( label = "Set" )
        self.grid.add( self.add_button ) #adds to first cell in grid
        #self.grid.attach( self.set_button, 0, 1, 2, 1 )
        self.grid.attach( self.preview, 0, 1, 2, 1 )
        self.grid.attach( self.sample, 0, 2, 2, 1 )
        self.add_button.connect( "clicked", self.on_add_clicked )
        self.set_button.connect( "clicked", self.on_set_clicked )
        self.entry = Gtk.Entry()
        self.current_walls = Gtk.ComboBox()
        self.grid.attach( option_combo, 1, 0, 1, 1 )

    def on_add_clicked( self, widget ):
        print( "Add" )
        current_walls = fileList( "/home/fernando/.wallpapers" )
        filepath = "/home/fernando/.wallpapers/" + current_walls.file_names_only[0]
        self.pixbuf_preview = GdkPixbuf.Pixbuf.new_from_file_at_scale( filepath, width=500, height=333, preserve_aspect_ratio=False )
        self.preview.set_from_pixbuf( self.pixbuf_preview )
        

    def on_set_clicked( self, widget ):
        print( "Set" )

if __name__ == "__main__":
    win = mainWindow()
    win.connect( "delete-event", Gtk.main_quit )
    win.show_all()
    Gtk.main()
