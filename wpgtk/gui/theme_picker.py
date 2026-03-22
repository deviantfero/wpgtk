import logging
import os

from . import color_grid
from . import template_grid
from . import option_grid
from . import keyword_grid
from . import util
from ..data import files
from ..data import themer
from ..data.config import WALL_DIR, WPG_DIR, __version__

from gi import require_version

require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib  # noqa: E402

PAD = 10


class MainWindow(Gtk.Window):
    def __init__(self, args):
        super().__init__(title="wpgtk " + __version__)

        image_name = os.path.join(WPG_DIR, ".current")
        image_name = os.path.realpath(image_name)
        self.set_default_size(200, 200)
        self.args = args

        # these variables are just to get the image
        # and preview of current wallpaper
        file_name = themer.get_current()
        sample_name = files.get_sample_path(file_name)
        logging.info("current wallpaper: " + file_name)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        util.set_uniform_margins(self.box, PAD)

        self.notebook = Gtk.Notebook()
        self.notebook.set_vexpand(True)
        self.box.append(self.notebook)
        self.set_child(self.box)

        self.wpage = Gtk.Grid()
        self.wpage.set_column_homogeneous(1)
        self.wpage.set_row_spacing(PAD)
        self.wpage.set_column_spacing(PAD)
        util.set_uniform_margins(self.wpage, PAD)

        self.cpage = color_grid.ColorGrid(self)
        self.fpage = template_grid.TemplateGrid(self)
        self.optpage = option_grid.OptionsGrid(self)
        self.keypage = keyword_grid.KeywordGrid(self)

        self.notebook.append_page(self.wpage, Gtk.Label(label="Wallpapers"))
        self.notebook.append_page(self.cpage, Gtk.Label(label="Colors"))
        self.notebook.append_page(self.fpage, Gtk.Label(label="Templates"))
        self.notebook.append_page(self.keypage, Gtk.Label(label="Keywords"))
        self.notebook.append_page(self.optpage, Gtk.Label(label="Options"))

        current_idx = None

        self.option_combo = Gtk.ComboBoxText()
        self.colorscheme = Gtk.ComboBoxText()
        self.textbox = Gtk.Label()
        self.textbox.set_text("Select colorscheme")

        for i, elem in enumerate(files.get_file_list()):
            if elem == themer.get_current():
                current_idx = i
            self.option_combo.append_text(elem)
            self.colorscheme.append_text(elem)

        self.preview = Gtk.Picture.new_for_filename(image_name)
        self.sample = Gtk.Picture.new_for_filename(sample_name)

        self.preview.set_content_fit(Gtk.ContentFit.CONTAIN)
        self.sample.set_content_fit(Gtk.ContentFit.CONTAIN)

        self.add_button = Gtk.Button(label="Add")
        self.set_button = Gtk.Button(label="Set")
        self.rm_button = Gtk.Button(label="Remove")
        # adds to first cell in wpage
        self.wpage.attach(self.option_combo, 1, 1, 2, 1)
        self.wpage.attach(self.colorscheme, 1, 2, 2, 1)
        self.wpage.attach(self.set_button, 3, 1, 1, 1)
        self.wpage.attach(self.add_button, 3, 2, 2, 1)
        self.wpage.attach(self.rm_button, 4, 1, 1, 1)
        self.wpage.attach(self.preview, 1, 3, 4, 1)
        self.wpage.attach(self.sample, 1, 4, 4, 1)
        self.add_button.connect("clicked", self._on_add_clicked)
        self.set_button.connect("clicked", self._on_set_clicked)
        self.rm_button.connect("clicked", self._on_rm_clicked)
        self.option_combo.connect("changed", self._combo_box_change)
        self.colorscheme.connect("changed", self._colorscheme_box_change)
        self.entry = Gtk.Entry()
        self.current_walls = Gtk.ComboBox()

        if current_idx is not None:
            self.option_combo.set_active(current_idx)
            self.colorscheme.set_active(current_idx)
            self.cpage.option_combo.set_active(current_idx)
            self.set_button.set_sensitive(True)

    def _on_add_clicked(self, widget):
        filechooser = Gtk.FileDialog()

        filefilter = Gtk.FileFilter()
        filefilter.set_name("Images")
        filefilter.add_mime_type("image/png")
        filefilter.add_mime_type("image/jpg")
        filefilter.add_mime_type("image/gif")
        filefilter.add_mime_type("image/jpeg")
        filechooser.set_default_filter(filefilter)

        filechooser.open_multiple(parent=self, callback=self._on_add_finish)

    def _on_add_finish(self, dialog, result):
        try:
            picked_files = dialog.open_multiple_finish(result)

            for gfile in picked_files:
                themer.create_theme(gfile.get_path())

            file_list = list(files.get_file_list())
            for combo in (self.option_combo, self.colorscheme, self.cpage.option_combo):
                combo.remove_all()
                for filename in file_list:
                    combo.append_text(filename)
        except GLib.Error as error:
            print(f"Error opening file: {error.message}")

    def _on_set_clicked(self, widget):
        x = self.option_combo.get_active()
        y = self.colorscheme.get_active()
        current_walls = files.get_file_list()
        if current_walls:
            filename = current_walls[x]
            colorscheme_file = current_walls[y]
            themer.set_theme(filename, colorscheme_file)

    def _on_rm_clicked(self, widget):
        x = self.option_combo.get_active()
        current_walls = files.get_file_list()
        if current_walls:
            filename = current_walls[x]
            themer.delete_theme(filename)
            file_list = list(files.get_file_list())
            for combo in (self.option_combo, self.colorscheme, self.cpage.option_combo):
                combo.remove_all()
                for elem in file_list:
                    combo.append_text(elem)

    def _combo_box_change(self, widget):
        self.set_button.set_sensitive(True)
        x = self.option_combo.get_active()
        self.colorscheme.set_active(x)
        selected_file = files.get_file_list()[x]
        filepath = os.path.join(WALL_DIR, selected_file)

        self.preview.set_filename(filepath)

    def _colorscheme_box_change(self, widget):
        x = self.colorscheme.get_active()
        self.cpage.option_combo.set_active(x)


def run(args):
    app = Gtk.Application(application_id="com.deviantfero.wpgtk")

    def on_activate(app):
        win = MainWindow(args)
        win.set_application(app)
        win.present()

    app.connect("activate", on_activate)
    return app.run(None)
