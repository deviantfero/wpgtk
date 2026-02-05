from gi import require_version

from . import util

require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa: E402


class KeywordDialog(Gtk.Window):
    def __init__(self, parent, callback):
        super().__init__(title="Name your keyword/value set")
        self.callback = callback

        self.set_transient_for(parent)
        self.set_default_size(200, 100)
        self.set_modal(True)
        self.set_resizable(False)

        self.name_text_input = Gtk.Entry()
        self.error_lbl = Gtk.Label()

        ok_button = Gtk.Button(label="OK")
        cancel_button = Gtk.Button(label="Cancel")

        ok_button.connect("clicked", self.on_ok_clicked)
        cancel_button.connect("clicked", self.on_cancel_clicked)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.END)
        button_box.append(cancel_button)
        button_box.append(ok_button)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        util.set_uniform_margins(box, 10)
        box.append(self.name_text_input)
        box.append(self.error_lbl)
        box.append(button_box)

        self.set_child(box)

    def on_ok_clicked(self, button):
        try:
            name = self.get_section_name()
            self.callback(Gtk.ResponseType.OK, name)
            self.close()
        except Exception as e:
            self.error_lbl.set_text(str(e))
            self.error_lbl.set_visible(True)

    def on_cancel_clicked(self, button):
        self.callback(Gtk.ResponseType.CANCEL, None)
        self.close()
