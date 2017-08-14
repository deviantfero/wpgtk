from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk


class ColorDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Pick a Color", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
        box = self.get_content_area()
        box.set_border_width(10)
        self.colorchooser = Gtk.ColorChooserWidget(show_editor=True)
        self.colorchooser.set_use_alpha(False)
        box.add(self.colorchooser)
        self.show_all()
