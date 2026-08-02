# import os
# import shutil
# import pywal

# from ..data.config import SAMPLE_DIR
# from ..data import color
# from ..data import util
from ..data import files

# from ..data import sample
# from ..data import themer
from . import util as gui_util

from gi import require_version

require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GLib  # noqa: E402
# from gi.repository.GdkPixbuf import Pixbuf  # noqa: E402

# TODO: remove current_walls call, use simple list
# TODO: only update pixbuf if parent has same color scheme


class ColorPickerDialog(Gtk.Window):
    def __init__(self, parent, color):
        Gtk.Window.__init__(
            self,
            title="Color Picker",
            modal=True,
            transient_for=parent,
            resizable=False,
        )
        self.parent = parent

        # Handle exit with Esc
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self._on_key_pressed)
        self.add_controller(key_controller)

    def _on_cancel_clicked(self, button):
        # self.callback(Gtk.ResponseType.CANCEL, None)
        self.close()

    def _on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self._on_cancel_clicked(None)
            return True

        return False  # Event not handled
