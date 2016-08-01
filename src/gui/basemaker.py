from os import walk, symlink, remove
from gi import require_version
from shutil import copy2
from subprocess import Popen, call
require_version( "Gtk", "3.0" )
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib 
from gi.repository.GdkPixbuf import Pixbuf

PAD = 10
config_path = GLib.get_home_dir() + '/.themes/color_other/'
icon = 'document-open'

def get_basef( directory ):
    files = []
    for( dirpath, dirnames, filenames ) in walk( directory ):
        files.extend( filenames )
    return files

def connect_conf( filepath ):
    filename = filepath.split( '/', len(filepath) ).pop()
    print( 'ADD::' + filename + '@' + filepath )
    try:
        copy2( filepath, filepath + '.bak' )
        print( '::MAKING BACKUP CONFIG' )
        print( '::CREATING BASE' )
        copy2( filepath, config_path + filename + '.base' )
        copy2( filepath, config_path + filename )
        call( [ 'rm', filepath ] )
        symlink( config_path + filename, filepath )
        print( '::CREATING SYMLINK' )
    except Exception as e:
        print( "ERROR" )

class fileGrid(Gtk.Grid):

    """A helper for choosing config files
    that will be modified with wpgtk's help"""

    def __init__( self, parent ):
        Gtk.Grid.__init__( self )
        self.current = None
        self.sel_file = ''

        self.parent = parent
        self.set_border_width( PAD )
        self.set_column_homogeneous( 1 )
        self.set_row_spacing( PAD )
        self.set_column_spacing( PAD )


        self.grid_edit = Gtk.Grid()
        self.grid_edit.set_column_homogeneous( 1 )
        self.grid_edit.set_row_spacing( PAD )
        self.grid_edit.set_column_spacing( PAD )

        self.button_add = Gtk.Button( 'Add' )
        self.button_add.connect( 'clicked', self.on_add_clicked )
        self.button_rm = Gtk.Button( 'Remove' )
        self.button_rm.connect( 'clicked', self.on_rm_clicked )
        self.button_open = Gtk.Button( 'Edit' )
        self.button_open.connect( 'clicked', self.on_open_clicked )

        self.liststore = Gtk.ListStore( Pixbuf, str )
        self.file_view = Gtk.IconView.new()
        self.file_view.set_model( self.liststore )
        self.file_view.set_activate_on_single_click( True )
        self.file_view.set_pixbuf_column( 0 )
        self.file_view.set_text_column( 1 )
        self.file_view.connect( 'item-activated', self.on_file_click  )

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy( Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC )
        self.scroll.set_min_content_height( 400 )
        self.scroll.add( self.file_view )

        self.item_names = [ filen for filen in get_basef( config_path ) if '.base' in filen ]

        for filen in self.item_names:
            pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
            self.liststore.append([pixbuf, filen])

        self.grid_edit.attach( self.button_add, 0, 0, 2, 1 )
        self.grid_edit.attach( self.button_rm, 0, 1, 1, 1 )
        self.grid_edit.attach( self.button_open, 1, 1, 1, 1 )
        self.grid_edit.attach( self.scroll, 0, 2, 2, 1 )

        self.attach( self.grid_edit, 0, 0, 1, 1 )

    def on_add_clicked( self, widget ):
        print( "Adding..." )
        filechooser = Gtk.FileChooserDialog( "Select an Image", self.parent, Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK) )
        response = filechooser.run()

        if response == Gtk.ResponseType.OK:
            filepath = filechooser.get_filename()
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
            connect_conf( filepath )
            self.item_names = [ filen for filen in get_basef( config_path ) if '.base' in filen ]
            self.liststore = Gtk.ListStore( Pixbuf, str )
            for filen in self.item_names:
                pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
                self.liststore.append([pixbuf, filen])
            self.file_view.set_model( self.liststore )
        filechooser.destroy()
        self.file_view.unselect_all()


    def on_open_clicked( self, widget ):
        if self.current != None:
            Popen( [ 'xdg-open', config_path + self.item_names[self.current] ] )
            self.current = None
        self.file_view.unselect_all()

    def on_rm_clicked( self, widget ):
        if self.current != None:
            item = self.item_names.pop( self.current )
            remove( config_path + item )
            self.liststore = Gtk.ListStore( Pixbuf, str )
            for filen in self.item_names:
                pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
                self.liststore.append([pixbuf, filen])
            self.file_view.set_model( self.liststore )
            self.current = None
        self.file_view.unselect_all()


    def on_file_click(self, widget, pos):
        self.current = int(str(pos))
        self.sel_file = self.liststore[self.current][1]
