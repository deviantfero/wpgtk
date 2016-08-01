#!/usr/bin/env python3
from gi import require_version
require_version( "Gtk", "3.0" )
from os import walk
from subprocess import Popen, call
import os.path #fetch filenames
#making sure it uses v3.0
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib 
from gi.repository.GdkPixbuf import Pixbuf
from data.colorparser import execute_gcolorchange
from data.colorparser import add_brightness
from data.colorparser import read_colors
from data.colorparser import write_colors
from data.colorparser import write_tmp
from time import sleep
from gui.colorpicker import ColorDialog
from gui.basemaker import fileGrid

version = "3.0"
PAD = 10

def hex_to_rgb( color ):
    rgb = list( int(hex_string[i:i+2], 16) for i in ( 0, 2, 4 ) )
    return rgb

def rgb_to_hex( rgb ):
    rgb_int = []
    for elem in rgb:
        rgb_int.append( int( (elem + 0.002) * 255) )
    rgb_int = tuple( rgb_int )
    hex_result = '%02x%02x%02x' % rgb_int
    return hex_result

class fileList():
    def __init__( self, path ):
        self.files = []
        self.file_names_only = []
        number_list = []
        elem_counter = 1
        for( dirpath, dirnames, filenames ) in walk( GLib.get_home_dir() + "/.wallpapers" ):
            self.files.extend( filenames )

        self.files = [ elem for elem in self.files if not ".Xres" in elem ]
        self.files = [ elem for elem in self.files if not ".sample" in elem ]
        self.files = [ elem for elem in self.files if not ".colors" in elem ]
        self.files = [ elem for elem in self.files if not ".current" in elem ]
        self.files = [ elem for elem in self.files if not ".sh" in elem ]
        # filter function goes up there
        self.file_names_only = self.files

    def show_list( self ):
        print( self.files )
    
    def show_files_only( self ):
        print( self.file_names_only )

#--some important global definitions
filepath = GLib.get_home_dir() + "/.wallpapers/"
current_walls = fileList( filepath )
#current_walls.show_files_only() #DEBUG ONLY
#--some important global definitions

class colorGrid( Gtk.Grid ):
    def __init__( self, parent ):
        Gtk.Grid.__init__( self )
        self.parent = parent
        self.set_border_width( PAD )
        self.set_column_homogeneous( 1 )
        self.set_row_spacing( PAD )
        self.set_column_spacing( PAD )

        self.colorgrid = Gtk.Grid()
        self.colorgrid.set_border_width( PAD )
        self.colorgrid.set_column_homogeneous( 1 )
        self.colorgrid.set_row_spacing( PAD )
        self.colorgrid.set_column_spacing( PAD )

        self.button_grid = Gtk.Grid()
        self.button_grid.set_column_homogeneous( 1 )
        self.button_grid.set_column_spacing( PAD )

        self.color_list = []
        self.button_list = []
        for x in range( 0, 16 ):
            self.color_list.append( '000000' )
        for x in range( 0, 16 ):
            self.button_list.append( self.make_button( self.color_list[x]) )
            self.button_list[x].connect( "pressed", self.on_color_click )
            self.button_list[x].set_sensitive( False )

        cont = 0
        for y in range( 0, 8, 2 ):
            for x in range( 0, 4 ):
                label = Gtk.Label( cont )
                self.colorgrid.attach( label, x, y, 1, 1 )
                cont += 1

        cont = 0
        for y in range( 1, 9, 2 ):
            for x in range( 0, 4 ):
                self.colorgrid.attach( self.button_list[cont], x, y, 1, 1 )
                cont += 1

        sample_name = filepath + ".no_sample.sample.png"
        self.sample = Gtk.Image()
        if( os.path.isfile(sample_name) ):
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( sample_name, width=500, height=300 )
            self.sample.set_from_pixbuf( self.pixbuf_sample )

        sampler_name = filepath + ".nsampler.sample.png"
        self.sampler = Gtk.Image()
        if( os.path.isfile(sampler_name) ):
            self.pixbuf_sampler = GdkPixbuf.Pixbuf.new_from_file_at_size( sampler_name, width=500, height=300 )
            self.sampler.set_from_pixbuf( self.pixbuf_sampler )


        self.ok_button = Gtk.Button( "Save" )
        self.ok_button.connect( "pressed", self.on_ok_click )
        self.ok_button.set_sensitive( False )

        self.auto_button = Gtk.Button( "Auto-adjust" )
        self.auto_button.connect( "pressed", self.on_auto_click )
        self.auto_button.set_sensitive( False )

        self.done_lbl = Gtk.Label( "" )

        option_list = Gtk.ListStore( str )
        for elem in list(current_walls.files):
            option_list.append( [elem] )
        self.option_combo = Gtk.ComboBox.new_with_model( option_list )
        self.renderer_text = Gtk.CellRendererText()
        self.option_combo.pack_start( self.renderer_text, True )
        self.option_combo.add_attribute( self.renderer_text, "text", 0 )
        self.option_combo.set_entry_text_column( 0 )
        self.option_combo.connect( "changed", self.combo_box_change )

        self.button_grid.attach( self.ok_button, 0, 1, 1, 1 )
        self.button_grid.attach( self.auto_button, 1, 1, 1, 1 )

        self.attach( self.option_combo, 0, 0, 1, 1 )
        self.attach( self.button_grid, 0, 1, 1, 1 )
        self.attach( self.colorgrid, 0, 2, 1, 1 )
        self.attach( self.sample, 0, 3, 1, 1 )
        self.attach( self.sampler, 0, 4, 1, 1 )
        self.attach( self.done_lbl, 0, 5, 1, 1 )

    def make_button( self, hex_color ):
        button = Gtk.Button( hex_color )
        return button

    def update_combo( self, option_list ):
        self.option_combo.set_model( option_list )
        self.option_combo.set_entry_text_column( 0 )

    def set_edit_combo( self, x ):
        self.option_combo.set_active( x )

    def on_ok_click( self, widget ):
        current_walls = fileList( GLib.get_home_dir() + "/.wallpapers" )
        if( len(current_walls.file_names_only) > 0 ):
            x = self.option_combo.get_active()
            write_colors( current_walls.file_names_only[x], self.color_list )
            tmpfile = filepath + ".tmp.sample.png"
            if( os.path.isfile(tmpfile) ):
                os.system( "mv " + filepath + ".tmp.sample.png " 
                        + filepath + "." + current_walls.file_names_only[x] + ".sample.png" )
                self.done_lbl.set_text( "Changes saved" )
                x = self.parent.colorscheme.get_active()
                selected_file = current_walls.file_names_only[x]
                selected_sample = "." + selected_file + ".sample.png"
                sample_path = filepath + selected_sample
                self.parent.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( sample_path, width=500, height=300 )
                self.parent.sample.set_from_pixbuf( self.pixbuf_sample )
    
    def on_auto_click( self, widget ):
        current_walls = fileList( GLib.get_home_dir() + "/.wallpapers" )
        self.color_list = self.color_list[:8:] + [ add_brightness( x, 50 ) for x in self.color_list[:8:] ]
        for x in range( 0, 16 ):
            self.button_list[x].set_label( self.color_list[x] )
        write_tmp( self.color_list )
        os.system( "wpcscript tmp 1>/dev/null" )
        sample_path = filepath + ".tmp.sample.png"
        self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( sample_path, width=500, height=300 )
        self.sample.set_from_pixbuf( self.pixbuf_sample )
        self.done_lbl.set_text( "Auto-adjust done" )

    def on_color_click( self, widget ):
        self.done_lbl.set_text( "" )
        color = Gdk.RGBA()
        color.parse("#" + widget.get_label())
        dialog = ColorDialog( self.parent )
        dialog.colorchooser.set_rgba( color ) 
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            color = dialog.colorchooser.get_rgba()
            rgb = [ color.red, color.green, color.blue ]
            hex_color = rgb_to_hex( rgb )
            widget.set_label( hex_color )
            for i, c in enumerate( self.button_list ):
                if c.get_label() != self.color_list[i]:
                    self.color_list[i] = c.get_label()
            write_tmp( self.color_list )
            os.system( "wpcscript tmp 1>/dev/null" )
            sample_path = filepath + ".tmp.sample.png"
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( sample_path, width=500, height=300 )
            self.sample.set_from_pixbuf( self.pixbuf_sample )

        dialog.destroy()

    def combo_box_change( self, widget ):
        self.done_lbl.set_text( "" )
        x = self.option_combo.get_active()
        self.auto_button.set_sensitive( True )
        self.ok_button.set_sensitive( True )
        current_walls = fileList( GLib.get_home_dir() + "/.wallpapers" )
        selected_file = current_walls.file_names_only[x]
        selected_sample = "." + selected_file + ".sample.png"
        sample_path = GLib.get_home_dir() + "/.wallpapers/" + selected_sample
        self.color_list = read_colors( selected_file )
        for x in range( 0, 16 ):
            self.button_list[x].set_label( self.color_list[x] )
            self.button_list[x].set_sensitive( True )
        self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( sample_path, width=500, height=300 )
        self.sample.set_from_pixbuf( self.pixbuf_sample )
        

class mainWindow( Gtk.Window ):

    def __init__( self ):
        Gtk.Window.__init__( self, title = "wpgtk " + version )

        image_name = filepath + ".current"
        image_name = os.path.realpath( image_name )
        self.set_default_size( 200, 200 )
        
        print( "CURRENT WALL: " + image_name )

        #these variables are just to get the image and preview of current wallpaper
        route_list = image_name.split( "/", image_name.count("/") )
        file_name = route_list[4]
        sample_name = filepath + "." + file_name + ".sample.png"

        self.notebook = Gtk.Notebook()
        self.add( self.notebook )

        self.wpage = Gtk.Grid()
        self.wpage.set_border_width( PAD )
        self.wpage.set_column_homogeneous( 1 )
        self.wpage.set_row_spacing( PAD )
        self.wpage.set_column_spacing( PAD )
        
        self.cpage = colorGrid( self )

        self.fpage = fileGrid( self )

        self.notebook.append_page( self.wpage, Gtk.Label( "Wallpapers" ) )
        self.notebook.append_page( self.cpage, Gtk.Label( "Colors" ) )
        self.notebook.append_page( self.fpage, Gtk.Label( "Optional Files" ) )

        option_list = Gtk.ListStore( str )
        for elem in list(current_walls.files):
            option_list.append( [elem] )
        self.option_combo = Gtk.ComboBox.new_with_model( option_list )
        self.renderer_text = Gtk.CellRendererText()
        self.option_combo.pack_start( self.renderer_text, True )
        self.option_combo.add_attribute( self.renderer_text, "text", 0 )
        self.option_combo.set_entry_text_column( 0 )

        self.textbox = Gtk.Label()
        self.textbox.set_text( "Select colorscheme" )
        self.colorscheme = Gtk.ComboBox.new_with_model( option_list )
        self.colorscheme.pack_start( self.renderer_text, True )
        self.colorscheme.add_attribute( self.renderer_text, "text", 0 )
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

        self.add_button = Gtk.Button( label = "Add" )
        self.set_button = Gtk.Button( label = "Set" )
        self.rm_button = Gtk.Button( label = "Remove" )
        self.wpage.attach( self.option_combo, 1, 1, 2, 1 ) #adds to first cell in wpage
        self.wpage.attach( self.colorscheme, 1, 2, 2, 1 )
        self.wpage.attach( self.set_button, 3, 1, 1, 1 )
        self.wpage.attach( self.add_button, 3, 2, 2, 1 )
        self.wpage.attach( self.rm_button, 4, 1, 1, 1 )
        self.wpage.attach( self.preview, 1, 3, 4, 1 )
        self.wpage.attach( self.sample, 1, 4, 4, 1 )
        self.add_button.connect( "clicked", self.on_add_clicked )
        self.set_button.connect( "clicked", self.on_set_clicked )
        self.rm_button.connect( "clicked", self.on_rm_clicked )
        self.option_combo.connect( "changed", self.combo_box_change )
        self.colorscheme.connect( "changed", self.colorscheme_box_change )
        self.entry = Gtk.Entry()
        self.current_walls = Gtk.ComboBox()

    def on_add_clicked( self, widget ):
        filechooser = Gtk.FileChooserDialog( "Select an Image", self, Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK) )
        response = filechooser.run()

        if response == Gtk.ResponseType.OK:
            filepath = filechooser.get_filename()
        filechooser.destroy()

        if( "\\" in filepath ):
            filepath = filepath.replace( "\\", "\\\\" )
        if( " " in filepath ):
            filepath = filepath.replace( " ", "\ " )
            filename = filepath.split( "/", len(filepath) )
            filename = filename.pop()
            if( " " in filename ):
                filename = filename.replace( " ", "\ " )
            elif( "\\" in filename ):
                filename = filename.replace( "\\", "\\\\" )
            Popen( "cp " + filepath + " ./" + filename, shell=True )
            Popen( "wpcscript add " + "./" + filename, shell=True )
            Popen( "rm ./" + filename, shell=True )
        else:
            Popen( "wpcscript add " + filepath, shell=True )
        option_list = Gtk.ListStore( str )
        current_walls = fileList( filepath )

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
        path = GLib.get_home_dir() + "/.wallpapers/"
        current_walls = fileList( path )
        if( len(current_walls.file_names_only) > 0 ):
            filepath = current_walls.file_names_only[x]
            colorscheme_file = current_walls.file_names_only[y]
            colorscheme = "." + colorscheme_file + ".Xres"
            colorscheme_sample = "." + current_walls.file_names_only[y] + ".sample.png"
            if( not os.path.isfile( path + colorscheme ) or not os.path.isfile( path + colorscheme_sample ) ):
                print( ":: " + path + colorscheme + " NOT FOUND" )
                print( ":: GENERATING COLORS" )
                call( [ "wpcscript", "add", path + filepath ] )
                self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( path + colorscheme_sample, width=500, height=500 )
                self.sample.set_from_pixbuf( self.pixbuf_sample )
            Popen( [ "wpcscript", "change", filepath ] )
            Popen( [ "xrdb", "-merge", path + colorscheme] )
            init_file = open( GLib.get_home_dir() + "/.wallpapers/wp_init.sh", "w" )
            init_file.writelines( [ "#!/bin/bash\n", "wpcscript change " + filepath + " && " ] )
            init_file.writelines( "xrdb -merge " + path + colorscheme + "\n" )
            init_file.close()
            Popen( [ "chmod", "+x", GLib.get_home_dir() + "/.wallpapers/wp_init.sh" ] )
            if( os.path.isfile(GLib.get_home_dir() + "/.themes/colorbamboo/openbox-3/themerc.base") ):
                execute_gcolorchange( colorscheme_file )

    def on_rm_clicked( self, widget ):
        x = self.option_combo.get_active()
        current_walls = fileList( GLib.get_home_dir() + "/.wallpapers" )
        if( len(current_walls.file_names_only) > 0 ):
            filepath = current_walls.file_names_only[x]
            Popen( [ "wpcscript", "rm", filepath ] )
            Popen( [ "rm", GLib.get_home_dir() + "/.wallpapers/" + "." + filepath + ".sample.png" ] )
            option_list = Gtk.ListStore( str )
            current_walls = fileList( filepath )
            for elem in list(current_walls.files):
                option_list.append( [elem] )
            self.option_combo.set_model( option_list )
            self.option_combo.set_entry_text_column( 0 )
            self.colorscheme.set_model( option_list )
            self.colorscheme.set_entry_text_column( 0 )
            self.cpage.update_combo( option_list )

    def combo_box_change( self, widget ):
        x = self.option_combo.get_active()
        self.colorscheme.set_active( x )
        current_walls = fileList( GLib.get_home_dir() + "/.wallpapers" )
        selected_file = current_walls.file_names_only[x]
        selected_sample = "." + selected_file + ".sample.png"
        filepath = GLib.get_home_dir() + "/.wallpapers/" + selected_file
        samplepath = GLib.get_home_dir() + "/.wallpapers/" + selected_sample
        self.pixbuf_preview = GdkPixbuf.Pixbuf.new_from_file_at_scale( filepath, width=500, height=333, preserve_aspect_ratio=False )
        self.preview.set_from_pixbuf( self.pixbuf_preview )

    def colorscheme_box_change( self, widget ):
        x = self.colorscheme.get_active()
        current_walls = fileList( GLib.get_home_dir() + "/.wallpapers" )
        selected_file = current_walls.file_names_only[x]
        selected_sample = "." + selected_file + ".sample.png"
        samplepath = GLib.get_home_dir() + "/.wallpapers/" + selected_sample
        nosamplepath = GLib.get_home_dir() + "/.wallpapers/" + ".no_sample.sample.png"
        if( os.path.isfile( samplepath ) ):
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( samplepath, width=500, height=500 )
        else:
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( nosamplepath, width=500, height=500 )
        self.sample.set_from_pixbuf( self.pixbuf_sample )
        self.cpage.set_edit_combo( x )

if __name__ == "__main__":
    win = mainWindow()
    win.connect( "delete-event", Gtk.main_quit )
    win.show_all()
    Gtk.main()
