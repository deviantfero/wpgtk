from gi import require_version

from . import util

require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk  # noqa: E402


class KeywordDialog(Gtk.Window):
    def __init__(self, parent, callback):
        super().__init__(title="Name your keyword/value set")
        self.callback = callback

        self.set_transient_for(parent)
        self.set_default_size(200, 100)
        self.set_modal(True)
        self.set_resizable(False)

        self.name_text_input = Gtk.Entry()
        # Handle Enter key
        self.name_text_input.connect("activate", lambda e: self.on_ok_clicked(None))
        self.error_lbl = Gtk.Label()

        # Handle exit with Esc
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)

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

    def get_section_name(self):
        if len(self.name_text_input.get_text()) <= 0:
            raise Exception("Empty name not allowed")

        return self.name_text_input.get_text()

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

    def on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.on_cancel_clicked(None)
            return True

        return False  # Event not handled
