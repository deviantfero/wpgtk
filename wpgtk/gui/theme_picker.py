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

require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

PAD = 10


class mainWindow(Gtk.Window):
    def __init__(self, args):
        Gtk.Window.__init__(self, title="wpgtk " + __version__)

        image_name = os.path.join(WPG_DIR, ".current")
        image_name = os.path.realpath(image_name)
        self.set_default_size(200, 200)
        self.args = args

        # these variables are just to get the image
        # and preview of current wallpaper
        file_name = themer.get_current()
        logging.info("current wallpaper: " + file_name)
        sample_name = files.get_sample_path(file_name)
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.wpage = Gtk.Grid()
        self.wpage.set_border_width(PAD)
        self.wpage.set_column_homogeneous(1)
        self.wpage.set_row_spacing(PAD)
        self.wpage.set_column_spacing(PAD)

        self.cpage = color_grid.ColorGrid(self)
        self.fpage = template_grid.TemplateGrid(self)
        self.optpage = option_grid.OptionsGrid(self)
        self.keypage = keyword_grid.KeywordGrid(self)

        self.notebook.append_page(self.wpage, Gtk.Label("Wallpapers"))
        self.notebook.append_page(self.cpage, Gtk.Label("Colors"))
        self.notebook.append_page(self.fpage, Gtk.Label("Templates"))
        self.notebook.append_page(self.keypage, Gtk.Label("Keywords"))
        self.notebook.append_page(self.optpage, Gtk.Label("Options"))

        option_list = Gtk.ListStore(str)
        current_idx = None

        for i, elem in enumerate(files.get_file_list()):
            if elem == themer.get_current():
                current_idx = i

            option_list.append([elem])
        self.option_combo = Gtk.ComboBox.new_with_model(option_list)
        self.renderer_text = Gtk.CellRendererText()
        self.option_combo.pack_start(self.renderer_text, True)
        self.option_combo.add_attribute(self.renderer_text, "text", 0)
        self.option_combo.set_entry_text_column(0)

        self.textbox = Gtk.Label()
        self.textbox.set_text("Select colorscheme")
        self.colorscheme = Gtk.ComboBox.new_with_model(option_list)
        self.colorscheme.pack_start(self.renderer_text, True)
        self.colorscheme.add_attribute(self.renderer_text, "text", 0)
        self.colorscheme.set_entry_text_column(0)

        self.set_border_width(10)
        self.preview = Gtk.Image()
        self.sample = Gtk.Image()

        self.get_image_preview(image_name, sample_name)

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
        self.add_button.connect("clicked", self.on_add_clicked)
        self.set_button.connect("clicked", self.on_set_clicked)
        self.rm_button.connect("clicked", self.on_rm_clicked)
        self.option_combo.connect("changed", self.combo_box_change)
        self.colorscheme.connect("changed", self.colorscheme_box_change)
        self.entry = Gtk.Entry()
        self.current_walls = Gtk.ComboBox()

        if current_idx is not None:
            self.option_combo.set_active(current_idx)
            self.colorscheme.set_active(current_idx)
            self.cpage.option_combo.set_active(current_idx)
            self.set_button.set_sensitive(True)

    def on_add_clicked(self, widget):
        filechooser = Gtk.FileChooserDialog(
            "Select an Image",
            self,
            Gtk.FileChooserAction.OPEN,
            (
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
            ),
        )

        filechooser.set_select_multiple(True)
        filefilter = Gtk.FileFilter()
        filefilter.set_name("Images")
        filefilter.add_mime_type("image/png")
        filefilter.add_mime_type("image/jpg")
        filefilter.add_mime_type("image/gif")
        filefilter.add_mime_type("image/jpeg")
        filechooser.add_filter(filefilter)
        response = filechooser.run()

        if response == Gtk.ResponseType.OK:
            option_list = Gtk.ListStore(str)

            for f in filechooser.get_filenames():
                themer.create_theme(f)

            for elem in list(files.get_file_list()):
                option_list.append([elem])

            self.option_combo.set_model(option_list)
            self.option_combo.set_entry_text_column(0)
            self.colorscheme.set_model(option_list)
            self.colorscheme.set_entry_text_column(0)

            self.cpage.option_combo.set_model(option_list)

        filechooser.destroy()

    def on_set_clicked(self, widget):
        x = self.option_combo.get_active()
        y = self.colorscheme.get_active()
        current_walls = files.get_file_list()
        if current_walls:
            filename = current_walls[x]
            colorscheme_file = current_walls[y]
            themer.set_theme(filename, colorscheme_file)

    def on_rm_clicked(self, widget):
        x = self.option_combo.get_active()
        current_walls = files.get_file_list()
        if current_walls:
            filename = current_walls[x]
            themer.delete_theme(filename)
            option_list = Gtk.ListStore(str)
            for elem in list(files.get_file_list()):
                option_list.append([elem])
            self.option_combo.set_model(option_list)
            self.option_combo.set_entry_text_column(0)
            self.colorscheme.set_model(option_list)

            self.cpage.option_combo.set_model(option_list)

    def combo_box_change(self, widget):
        self.set_button.set_sensitive(True)
        x = self.option_combo.get_active()
        self.colorscheme.set_active(x)
        selected_file = files.get_file_list()[x]
        filepath = os.path.join(WALL_DIR, selected_file)

        self.set_image_preview(filepath)

    def colorscheme_box_change(self, widget):
        x = self.colorscheme.get_active()
        self.cpage.option_combo.set_active(x)

    # called on opening to looad the current image
    def get_image_preview(self, image_name, sample_name):
        pixbuf_preview = util.get_preview_pixbuf(image_name)
        pixbuf_sample = util.get_sample_pixbuf(sample_name)

        if pixbuf_preview is not None:
            self.preview.set_from_pixbuf(pixbuf_preview)

        if pixbuf_sample is not None:
            self.sample.set_from_pixbuf(pixbuf_sample)

    # called when combo box changes the selected image
    def set_image_preview(self, filepath):
        pixbuf_preview = util.get_preview_pixbuf(filepath)

        if pixbuf_preview is not None:
            self.preview.set_from_pixbuf(pixbuf_preview)


def run(args):
    win = mainWindow(args)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
