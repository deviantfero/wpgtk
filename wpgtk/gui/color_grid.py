from random import shuffle
from gi import require_version
require_version( "Gtk", "3.0" )
#making sure it uses v3.0
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
from gi.repository.GdkPixbuf import Pixbuf
from ..data.color_parser import *
from ..data.conf_parser import *
from ..data.file_list import *
from ..data.transformers import *
from ..data.make_sample import *
from .color_picker import ColorDialog

FILEPATH = GLib.get_home_dir() + "/.wallpapers/"
OPTIONS = parse_conf()
current_walls = FileList( FILEPATH )
PAD = 10

class ColorGrid( Gtk.Grid ):
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

        sample_name = FILEPATH + ".no_sample.sample.png"
        self.sample = Gtk.Image()
        if( os.path.isfile(sample_name) ):
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( sample_name, width=500, height=300 )
            self.sample.set_from_pixbuf( self.pixbuf_sample )

        sampler_name = FILEPATH + ".nsampler.sample.png"
        self.sampler = Gtk.Image()
        if( os.path.isfile(sampler_name) ):
            self.pixbuf_sampler = GdkPixbuf.Pixbuf.new_from_file_at_size( sampler_name, width=500, height=300 )
            self.sampler.set_from_pixbuf( self.pixbuf_sampler )


        self.shuffle_button = Gtk.Button( "Shuffle colors" )
        self.shuffle_button.connect( "pressed", self.on_shuffle_click )
        self.shuffle_button.set_sensitive( False )

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

        self.button_grid.attach( self.ok_button, 0, 0, 1, 1 )
        self.button_grid.attach( self.auto_button, 1, 0, 1, 1 )
        self.button_grid.attach( self.shuffle_button, 2, 0, 1, 1 )

        self.attach( self.option_combo, 0, 0, 1, 1 )
        self.attach( self.button_grid, 0, 1, 1, 1 )
        self.attach( self.colorgrid, 0, 2, 1, 1 )
        self.attach( self.sample, 0, 3, 1, 1 )
        self.attach( self.sampler, 0, 4, 1, 1 )
        self.attach( self.done_lbl, 0, 5, 1, 1 )


    def make_button( self, hex_color ):
        button = Gtk.Button( hex_color )
        return button

    def render_buttons(self):
        for x in range( 0, 16 ):
            color = Gdk.color_parse( '#' + self.color_list[x] )
            if get_darkness( self.color_list[x] ) < 100:
                fgcolor = Gdk.color_parse( '#FFFFFF' )
            else:
                fgcolor = Gdk.color_parse( '#101010' )
            self.button_list[x].set_label( self.color_list[x] )
            self.button_list[x].set_sensitive( True )
            self.button_list[x].modify_bg( Gtk.StateType.NORMAL, color )
            self.button_list[x].modify_fg( Gtk.StateType.NORMAL, fgcolor )

    def render_sample(self):
        sample_path = FILEPATH + ".tmp.sample.png"
        self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( sample_path, width=500, height=300 )
        self.sample.set_from_pixbuf( self.pixbuf_sample )
        self.done_lbl.set_text( "Auto-adjust done" )

    def update_combo( self, option_list ):
        self.option_combo.set_model( option_list )
        self.option_combo.set_entry_text_column( 0 )

    def set_edit_combo( self, x ):
        self.option_combo.set_active( x )

    def on_ok_click( self, widget ):
        current_walls = FileList( GLib.get_home_dir() + "/.wallpapers" )
        if( len(current_walls.file_names_only) > 0 ):
            x = self.option_combo.get_active()
            write_colors( current_walls.file_names_only[x], self.color_list )
            tmpfile = FILEPATH + ".tmp.sample.png"
            if( os.path.isfile(tmpfile) ):
                os.system( "mv " + FILEPATH + ".tmp.sample.png "
                        + FILEPATH + "sample/" + current_walls.file_names_only[x] + ".sample.png" )
                self.done_lbl.set_text( "Changes saved" )
                x = self.parent.colorscheme.get_active()
                selected_file = current_walls.file_names_only[x]
                selected_sample = "sample/" + selected_file + ".sample.png"
                sample_path = FILEPATH + selected_sample
                self.parent.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( sample_path, width=500, height=300 )
                self.parent.sample.set_from_pixbuf( self.pixbuf_sample )

    def on_auto_click( self, widget ):
        color8 = self.color_list[0:1][0]
        if(not OPTIONS['INV']):
            color8 = [add_brightness(color8, 18)]
            self.color_list = self.color_list[:8:] + color8 + [add_brightness( x, 50 ) for x in self.color_list[1:8:]]
        else:
            color8 = [reduce_brightness(color8, 18)]
            self.color_list = self.color_list[:8:] + color8 + [reduce_brightness(x, 50) for x in self.color_list[1:8:]]
        self.render_buttons()
        create_sample(self.color_list[:])
        self.render_sample()

    def on_shuffle_click(self, widget):
        shuffled_colors = self.color_list[1:8]
        shuffle(shuffled_colors)
        list_tail = shuffled_colors + self.color_list[8:]
        self.color_list = self.color_list[:1] + list_tail
        self.on_auto_click(widget)

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
            color = Gdk.color_parse( '#' + hex_color )
            if get_darkness( hex_color ) < 100:
                fgcolor = Gdk.color_parse( '#FFFFFF' )
            else:
                fgcolor = Gdk.color_parse( '#101010' )
            widget.set_sensitive( True )
            widget.modify_bg( Gtk.StateType.NORMAL, color )
            widget.modify_fg( Gtk.StateType.NORMAL, fgcolor )
            for i, c in enumerate( self.button_list ):
                if c.get_label() != self.color_list[i]:
                    self.color_list[i] = c.get_label()
            create_sample(self.color_list[:])
            self.render_sample()
        dialog.destroy()

    def combo_box_change( self, widget ):
        self.done_lbl.set_text( "" )
        x = self.option_combo.get_active()
        self.auto_button.set_sensitive( True )
        self.shuffle_button.set_sensitive( True )
        self.ok_button.set_sensitive( True )
        current_walls = FileList( GLib.get_home_dir() + "/.wallpapers" )
        selected_file = current_walls.file_names_only[x]
        selected_sample = "sample/" + selected_file + ".sample.png"
        sample_path = GLib.get_home_dir() + "/.wallpapers/" + selected_sample
        self.color_list = read_colors( selected_file )
        self.render_buttons()
        self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size( sample_path, width=500, height=300 )
        self.sample.set_from_pixbuf( self.pixbuf_sample )
        if(OPTIONS['INV']):
            self.color_list = self.color_list[::-1]
