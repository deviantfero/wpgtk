import logging
import os

from subprocess import Popen
from ..data.config import OPT_DIR, settings
from ..data import files

from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from gi import require_version
require_version("Gtk", "3.0")

PAD = 10
icon = 'document-open'


class TemplateGrid(Gtk.Grid):

    """A helper for choosing config files
    that will be modified with wpgtk's help"""

    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.current = None
        self.sel_file = ''

        self.parent = parent
        self.set_border_width(PAD)
        self.set_column_homogeneous(1)
        self.set_row_spacing(PAD)
        self.set_column_spacing(PAD)

        self.grid_edit = Gtk.Grid()
        self.grid_edit.set_column_homogeneous(1)
        self.grid_edit.set_row_spacing(PAD)
        self.grid_edit.set_column_spacing(PAD)

        self.button_add = Gtk.Button('Add')
        self.button_add.connect('clicked', self.on_add_clicked)
        self.button_rm = Gtk.Button('Remove')
        self.button_rm.connect('clicked', self.on_rm_clicked)
        self.button_edit = Gtk.Button('Edit')
        self.button_edit.connect('clicked', self.on_open_clicked)

        self.liststore = Gtk.ListStore(Pixbuf, str)
        self.file_view = Gtk.IconView.new()
        self.file_view.set_model(self.liststore)
        self.file_view.set_activate_on_single_click(True)
        self.file_view.set_pixbuf_column(0)
        self.file_view.set_text_column(1)
        self.file_view.connect('item-activated', self.on_file_click)

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_min_content_height(400)
        self.scroll.add(self.file_view)

        self.item_names = files.get_file_list(OPT_DIR, r".*\.base$")

        for filen in self.item_names:
            pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
            self.liststore.append([pixbuf, filen])

        self.grid_edit.attach(self.button_add, 0, 0, 2, 1)
        self.grid_edit.attach(self.button_edit, 0, 1, 1, 1)
        self.grid_edit.attach(self.button_rm, 1, 1, 1, 1)
        self.grid_edit.attach(self.scroll, 0, 2, 2, 1)

        self.attach(self.grid_edit, 0, 0, 1, 1)

    def on_add_clicked(self, widget):
        filechooser = Gtk.FileChooserDialog("Select an Image", self.parent,
                                            Gtk.FileChooserAction.OPEN,
                                            (Gtk.STOCK_CANCEL,
                                             Gtk.ResponseType.CANCEL,
                                             Gtk.STOCK_OPEN,
                                             Gtk.ResponseType.OK))
        filefilter = Gtk.FileFilter()
        filechooser.set_select_multiple(True)
        filefilter.set_name("Text")
        filefilter.add_mime_type("text/*")
        filechooser.add_filter(filefilter)
        response = filechooser.run()

        if response == Gtk.ResponseType.OK:
            for f in filechooser.get_filenames():
                files.add_template(f)
            self.item_names = files.get_file_list(OPT_DIR, r".*\.base$")
            self.liststore = Gtk.ListStore(Pixbuf, str)
            for filen in self.item_names:
                pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
                self.liststore.append([pixbuf, filen])
            self.file_view.set_model(self.liststore)
        filechooser.destroy()
        self.file_view.unselect_all()

    def on_open_clicked(self, widget):
        if self.current is not None:
            item = self.item_names[self.current]
            args_list = settings['editor'].split(' ')
            args_list.append(os.path.join(OPT_DIR, item))
            try:
                Popen(args_list)
            except Exception as e:
                logging.error("malformed editor command")
            self.current = None
        self.file_view.unselect_all()

    def on_rm_clicked(self, widget):
        if self.current is not None:
            item = self.item_names.pop(self.current)
            files.delete_template(item)
            self.liststore = Gtk.ListStore(Pixbuf, str)
            for filen in self.item_names:
                pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
                self.liststore.append([pixbuf, filen])
            self.file_view.set_model(self.liststore)
            self.current = None
        self.file_view.unselect_all()

    def on_file_click(self, widget, pos):
        self.current = int(str(pos))
        self.sel_file = self.liststore[self.current][1]
