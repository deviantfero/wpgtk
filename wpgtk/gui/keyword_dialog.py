from gi import require_version
from gi.repository import Gtk
require_version("Gtk", "3.0")


class KeywordDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Name you keyword/value set", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
        self.name_text_input = Gtk.Entry()
        self.error_lbl = Gtk.Label()

        box = self.get_content_area()
        box.set_border_width(10)
        box.set_spacing(10)
        box.add(self.name_text_input)
        box.add(self.error_lbl)

        self.show_all()

    def get_section_name(self):
        if len(self.name_text_input.get_text()) <= 0:
            raise Exception('Empty name not allowed')

        return self.name_text_input.get_text()
