#!/usr/bin/env python3
from gi import require_version
require_version( 'Gtk', '3.0' )
#making sure it uses v3.0
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
from gi.repository.GdkPixbuf import Pixbuf
from .data.color_parser import *
from .data.file_list import *
from .data.transformers import *
from .data.theme_interface import *
from time import sleep
from .gui.color_picker import ColorDialog
from .gui.base_maker import FileGrid
from .gui.color_grid import ColorGrid
from .gui.option_grid import OptionsGrid
import shutil

version = '4.0'
PAD = 10

#GLOBAL DEFS
FILEPATH = GLib.get_home_dir() + '/.wallpapers/'
current_walls = FileList( FILEPATH )

class mainWindow( Gtk.Window ):

    def __init__( self ):
        Gtk.Window.__init__( self, title = 'wpgtk ' + version )

        image_name = FILEPATH + '.current'
        image_name = os.path.realpath( image_name )
        self.set_default_size( 200, 200 )


        #these variables are just to get the image and preview of current wallpaper
        route_list = image_name.split( '/', image_name.count('/') )
        file_name = route_list[4]
        print( 'INF::CURRENT WALL: ' + file_name )
        sample_name = FILEPATH + 'sample/' + file_name + '.sample.png'

        self.notebook = Gtk.Notebook()
        self.add( self.notebook )

        self.wpage = Gtk.Grid()
        self.wpage.set_border_width( PAD )
        self.wpage.set_column_homogeneous( 1 )
        self.wpage.set_row_spacing( PAD )
        self.wpage.set_column_spacing( PAD )

        self.cpage = ColorGrid( self )
        self.fpage = FileGrid( self )
        self.optpage = OptionsGrid( self )

        self.notebook.append_page( self.wpage, Gtk.Label( 'Wallpapers' ) )
        self.notebook.append_page( self.cpage, Gtk.Label( 'Colors' ) )
        self.notebook.append_page( self.fpage, Gtk.Label( 'Optional Files' ) )
        self.notebook.append_page( self.optpage, Gtk.Label( 'Options' ) )

        option_list = Gtk.ListStore( str )
        for elem in list(current_walls.files):
            option_list.append( [elem] )
        self.option_combo = Gtk.ComboBox.new_with_model( option_list )
        self.renderer_text = Gtk.CellRendererText()
        self.option_combo.pack_start( self.renderer_text, True )
        self.option_combo.add_attribute( self.renderer_text, 'text', 0 )
        self.option_combo.set_entry_text_column( 0 )

        self.textbox = Gtk.Label()
        self.textbox.set_text( 'Select colorscheme' )
        self.colorscheme = Gtk.ComboBox.new_with_model( option_list )
        self.colorscheme.pack_start( self.renderer_text, True )
        self.colorscheme.add_attribute( self.renderer_text, 'text', 0 )
        self.colorscheme.set_entry_text_column( 0 )

        self.set_border_width( 10 )
        #another container will be added so this will probably change
        #self.add( self.wpage )
        self.preview = Gtk.Image()
        self.sample = Gtk.Image()

        if( os.path.isfile( image_name ) and os.path.isfile(sample_name) ):
            self.pixbuf_preview = GdkPixbuf.Pixbuf.new_from_file_at_scale( image_name, width=500, height=333, preserve_aspect_ratio=False )
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( sample_name, width=500, height=500 )
            self.preview.set_from_pixbuf( self.pixbuf_preview )
            self.sample.set_from_pixbuf( self.pixbuf_sample )

        self.add_button = Gtk.Button( label = 'Add' )
        self.set_button = Gtk.Button( label = 'Set' )
        self.set_button.set_sensitive( False )
        self.rm_button = Gtk.Button( label = 'Remove' )
        self.wpage.attach( self.option_combo, 1, 1, 2, 1 ) #adds to first cell in wpage
        self.wpage.attach( self.colorscheme, 1, 2, 2, 1 )
        self.wpage.attach( self.set_button, 3, 1, 1, 1 )
        self.wpage.attach( self.add_button, 3, 2, 2, 1 )
        self.wpage.attach( self.rm_button, 4, 1, 1, 1 )
        self.wpage.attach( self.preview, 1, 3, 4, 1 )
        self.wpage.attach( self.sample, 1, 4, 4, 1 )
        self.add_button.connect( 'clicked', self.on_add_clicked )
        self.set_button.connect( 'clicked', self.on_set_clicked )
        self.rm_button.connect( 'clicked', self.on_rm_clicked )
        self.option_combo.connect( 'changed', self.combo_box_change )
        self.colorscheme.connect( 'changed', self.colorscheme_box_change )
        self.entry = Gtk.Entry()
        self.current_walls = Gtk.ComboBox()

    def on_add_clicked( self, widget ):
        FILEPATH = ""
        filechooser = Gtk.FileChooserDialog( 'Select an Image', self, Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK) )
        response = filechooser.run()

        if response == Gtk.ResponseType.OK:
            FILEPATH = filechooser.get_filename()
        filechooser.destroy()

        if( '\\' in FILEPATH or ' ' in FILEPATH):
            filename = FILEPATH.split( '/', len(FILEPATH) )
            filename = filename.pop()
            if( ' ' in filename ):
                filename = filename.replace( ' ', '' )
            elif( '\\' in filename ):
                filename = filename.replace( '\\', '' )
            try:
                shutil.copy( FILEPATH, filename)
            except Exception:
                print("ERROR:: file {} already exists".format(filename), file=sys.stderr)
            create_theme(filename)
            os.remove(filename)
        else:
            create_theme(FILEPATH)
        option_list = Gtk.ListStore( str )
        current_walls = FileList( FILEPATH )

        for elem in list(current_walls.files):
            option_list.append( [elem] )
        self.option_combo.set_model( option_list )
        self.option_combo.set_entry_text_column( 0 )
        self.colorscheme.set_model( option_list )
        self.colorscheme.set_entry_text_column( 0 )
        self.cpage.update_combo( option_list )


    def on_set_clicked( self, widget ):
        x = self.option_combo.get_active()
        y = self.colorscheme.get_active()
        path = GLib.get_home_dir() + '/.wallpapers/'
        current_walls = FileList( path )
        if( len(current_walls.file_names_only) > 0 ):
            FILENAME = current_walls.file_names_only[x]
            colorscheme_file = current_walls.file_names_only[y]
            colorscheme = 'xres/' + colorscheme_file + '.Xres'
            colorscheme_sample = 'sample/' + current_walls.file_names_only[y] + '.sample.png'
            if( not os.path.isfile( path + colorscheme ) or not os.path.isfile( path + colorscheme_sample ) ):
                print( ':: ' + path + colorscheme + ' NOT FOUND' )
                print( ':: GENERATING COLORS' )
                create_theme(path + FILENAME)
                self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( path + colorscheme_sample, width=500, height=500 )
                self.sample.set_from_pixbuf( self.pixbuf_sample )
            set_theme(FILENAME, colorscheme_file, self.optpage.opt_list)

    def on_rm_clicked( self, widget ):
        x = self.option_combo.get_active()
        current_walls = FileList( GLib.get_home_dir() + '/.wallpapers' )
        if( len(current_walls.file_names_only) > 0 ):
            FILENAME = current_walls.file_names_only[x]
            delete_theme(FILENAME)
            option_list = Gtk.ListStore( str )
            current_walls = FileList( FILENAME )
            for elem in list(current_walls.files):
                option_list.append( [elem] )
            self.option_combo.set_model( option_list )
            self.option_combo.set_entry_text_column( 0 )
            self.colorscheme.set_model( option_list )
            self.colorscheme.set_entry_text_column( 0 )
            self.cpage.update_combo( option_list )

    def combo_box_change( self, widget ):
        self.set_button.set_sensitive( True )
        x = self.option_combo.get_active()
        self.colorscheme.set_active( x )
        current_walls = FileList( GLib.get_home_dir() + '/.wallpapers' )
        selected_file = current_walls.file_names_only[x]
        selected_sample = 'sample/' + selected_file + '.sample.png'
        FILEPATH = GLib.get_home_dir() + '/.wallpapers/' + selected_file
        samplepath = GLib.get_home_dir() + '/.wallpapers/' + selected_sample

        self.pixbuf_preview = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            FILEPATH,
            width=500,
            height=333,
            preserve_aspect_ratio=False
        )

        self.preview.set_from_pixbuf( self.pixbuf_preview )

    def colorscheme_box_change( self, widget ):
        x = self.colorscheme.get_active()
        current_walls = FileList( GLib.get_home_dir() + '/.wallpapers' )
        selected_file = current_walls.file_names_only[x]
        selected_sample = 'sample/' + selected_file + '.sample.png'
        samplepath = GLib.get_home_dir() + '/.wallpapers/' + selected_sample
        nosamplepath = GLib.get_home_dir() + '/.wallpapers/' + '.no_sample.sample.png'
        if( os.path.isfile( samplepath ) ):
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( samplepath, width=500, height=500 )
        else:
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( nosamplepath, width=500, height=500 )
        self.sample.set_from_pixbuf( self.pixbuf_sample )
        self.cpage.set_edit_combo( x )

def run():
    win = mainWindow()
    win.connect( 'delete-event', Gtk.main_quit )
    win.show_all()
    Gtk.main()

if __name__ == '__main__':
    run()
