import logging
import os

from subprocess import Popen
from ..data.config import OPT_DIR, settings
from ..data import files
from . import util

from gi import require_version

require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GLib  # noqa: E402
from gi.repository.GdkPixbuf import Pixbuf  # noqa: E402

PAD = 10
icon = "document-open"


class TemplateGrid(Gtk.Grid):
    """A helper for choosing config files
    that will be modified with wpgtk's help"""

    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.current = None
        self.sel_file = ""

        self.parent = parent
        self.set_column_homogeneous(1)
        util.set_uniform_margins(self, PAD)
        self.set_row_spacing(PAD)
        self.set_column_spacing(PAD)

        self.grid_edit = Gtk.Grid()
        self.grid_edit.set_column_homogeneous(1)
        self.grid_edit.set_row_spacing(PAD)
        self.grid_edit.set_column_spacing(PAD)

        self.button_add = Gtk.Button(label="Add")
        self.button_add.connect("clicked", self.on_add_clicked)
        self.button_rm = Gtk.Button(label="Remove")
        self.button_rm.connect("clicked", self.on_rm_clicked)
        self.button_edit = Gtk.Button(label="Edit")
        self.button_edit.connect("clicked", self.on_open_clicked)

        self.liststore = Gtk.ListStore(Pixbuf, str)
        self.file_view = Gtk.IconView.new()
        self.file_view.set_model(self.liststore)
        self.file_view.set_activate_on_single_click(True)
        self.file_view.set_pixbuf_column(0)
        self.file_view.set_text_column(1)
        self.file_view.set_item_width(96)
        self.file_view.connect("item-activated", self.on_file_click)

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_min_content_height(400)
        self.scroll.set_child(self.file_view)

        self.item_names = files.get_file_list(OPT_DIR, r".*\.base$")
        self.icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        self._icon_pixbuf = self._load_icon_pixbuf()

        for filen in self.item_names:
            self.liststore.append([self._icon_pixbuf, filen])

        self.grid_edit.attach(self.button_add, 0, 0, 2, 1)
        self.grid_edit.attach(self.button_edit, 0, 1, 1, 1)
        self.grid_edit.attach(self.button_rm, 1, 1, 1, 1)
        self.grid_edit.attach(self.scroll, 0, 2, 2, 1)

        self.attach(self.grid_edit, 0, 0, 1, 1)

    def _load_icon_pixbuf(self):
        paintable = self.icon_theme.lookup_icon(
            icon, None, 64, 1, Gtk.TextDirection.LTR, Gtk.IconLookupFlags.FORCE_REGULAR
        )
        icon_file = paintable.get_file()
        if icon_file:
            return Pixbuf.new_from_file_at_size(icon_file.get_path(), 64, 64)
        return None

    def _refresh_liststore(self):
        self.item_names = files.get_file_list(OPT_DIR, r".*\.base$")
        self.liststore.clear()
        for filen in self.item_names:
            self.liststore.append([self._icon_pixbuf, filen])
        self.file_view.unselect_all()

    def on_add_clicked(self, widget):
        filechooser = Gtk.FileDialog()
        filechooser.set_title("Select a file")

        filefilter = Gtk.FileFilter()
        filefilter.set_name("Text")
        filefilter.add_mime_type("text/*")
        filechooser.set_default_filter(filefilter)

        filechooser.open_multiple(parent=self.parent, callback=self.on_add_finish)

    def on_add_finish(self, dialog, result):
        try:
            picked_files = dialog.open_multiple_finish(result)
            for gfile in picked_files:
                files.add_template(gfile.get_path())
            self._refresh_liststore()
        except GLib.Error as error:
            print(f"Error opening file: {error.message}")

    def on_open_clicked(self, widget):
        if self.current is not None:
            item = self.item_names[self.current]
            args_list = settings["editor"].split(" ")
            args_list.append(os.path.join(OPT_DIR, item))
            try:
                Popen(args_list)
            except Exception:
                logging.error("malformed editor command")
            self.current = None
        self.file_view.unselect_all()

    def on_rm_clicked(self, widget):
        if self.current is not None:
            item = self.item_names.pop(self.current)
            files.delete_template(item)
            self._refresh_liststore()
            self.current = None
        self.file_view.unselect_all()

    def on_file_click(self, widget, pos):
        self.current = int(str(pos))
        self.sel_file = self.liststore[self.current][1]
