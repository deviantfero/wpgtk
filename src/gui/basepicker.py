from os import walk
from gi import require_version
require_version( "Gtk", "3.0" )
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib 

PAD = 10
config_path = GLib.get_home_dir() + '/.themes/color_other/'
files = []

class FileGrid(Gtk.Grid):

    """A helper for choosing config files
    that will be modified with wpgtk's help"""

    def __init__( self, parent ):
        Gtk.Grid.__init__( self )
        self.parent = parent
        self.set_border_width( PAD )
        self.set_column_homogeneous( 1 )
        self.set_row_spacing( PAD )
        self.set_column_spacing( PAD )

        self.grid_edit = Gtk.Grid()
        self.grid_edit.set_border_width( PAD )
        self.grid_edit.set_column_homogeneous( 1 )
        self.grid_edit.set_row_spacing( PAD )
        self.grid_edit.set_column_spacing( PAD )

        self.button_add = Gtk.Button( "Add" )
        self.button_rm = Gtk.Button( "Remove" )

