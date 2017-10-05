from gi import require_version
require_version("Gtk", "3.0")
require_version("Gdk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from wpgtk.data import color, themer


class ColorDialog(Gtk.Dialog):

    def __init__(self, parent, current_file):
        Gtk.Dialog.__init__(self, "Pick a Color", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
        box = self.get_content_area()
        box.set_border_width(10)
        box.set_spacing(10)
        self.colorchooser = Gtk.ColorChooserWidget(show_editor=True)
        self.colorchooser.set_use_alpha(False)
        self.random_color_btn = Gtk.Button('Random from Current Selection')

        self.random_color_btn.connect('clicked',
                                      self.get_random_color,
                                      current_file)
        box.add(self.colorchooser)
        box.add(self.random_color_btn)
        self.show_all()

    def get_random_color(self, button, *gargs):
        random_color = color.get_random_color(gargs[0])
        random_gcolor = Gdk.RGBA()
        random_gcolor.parse(random_color)
        self.colorchooser.set_rgba(random_gcolor)
