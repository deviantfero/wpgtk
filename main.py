#!/usr/bin/python
from gi import require_version
require_version( "Gtk", "3.0" )
#making sure it uses v3.0
from gi.repository import Gtk

class MyWindow( Gtk.Window ):

    def __init__( self ):
        Gtk.Window.__init__( self, title = "Hello Fuckers" )

        self.grid = Gtk.Grid()
        self.add( self.grid )
        self.button = Gtk.Button( label = "Click Here" )
        self.button2 = Gtk.Button( label = "Click Me Next!" )
        self.grid.add( self.button )
        self.grid.attach( self.button2, 1, 0, 2, 1 )
        self.button.connect( "clicked", self.on_button_clicked )

    def on_button_clicked( self, widget ):
        print( "Hello World" )

win = MyWindow()
win.connect( "delete-event", Gtk.main_quit )
win.show_all()
Gtk.main()
