import os
import shutil
import pywal

from ..data.config import SAMPLE_DIR
from ..data import color
from ..data import util
from ..data import files
from ..data import sample
from ..data import themer

from .color_picker import ColorDialog
from gi import require_version
from gi.repository import Gtk, Gdk, GdkPixbuf
require_version("Gtk", "3.0")

# TODO: remove current_walls call, use simple ist
# TODO: use simple text combo
# TODO: only update pixbuf if parent has same color scheme
current_walls = files.get_file_list()
PAD = 10


class ColorGrid(Gtk.Grid):
    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.parent = parent
        self.set_border_width(PAD)
        self.set_column_homogeneous(1)
        self.set_row_spacing(PAD)
        self.set_column_spacing(PAD)

        self.colorgrid = Gtk.Grid()
        self.colorgrid.set_border_width(PAD)
        self.colorgrid.set_column_homogeneous(1)
        self.colorgrid.set_row_spacing(PAD)
        self.colorgrid.set_column_spacing(PAD)

        self.sat_add = Gtk.Button("+")
        self.sat_add.set_sensitive(False)

        self.sat_red = Gtk.Button("-")
        self.sat_red.set_sensitive(False)

        self.sat_add.connect("pressed", self.hls_change, "sat", "add")
        self.sat_red.connect("pressed", self.hls_change, "sat", "red")
        self.sat_lbl = Gtk.Label("Saturation:")

        self.light_add = Gtk.Button("+")
        self.light_add.set_sensitive(False)

        self.light_red = Gtk.Button("-")
        self.light_red.set_sensitive(False)

        self.light_add.connect("pressed", self.hls_change, "light", "add")
        self.light_red.connect("pressed", self.hls_change, "light", "red")
        self.light_lbl = Gtk.Label("Brightness:")

        self.sat_light_grid = Gtk.Grid()
        self.sat_light_grid.set_column_homogeneous(1)
        self.sat_light_grid.set_column_spacing(PAD)
        self.sat_light_grid.set_row_spacing(PAD)

        self.button_grid = Gtk.Grid()
        self.button_grid.set_column_homogeneous(1)
        self.button_grid.set_column_spacing(PAD)
        self.button_grid.set_row_spacing(PAD)

        self.combo_grid = Gtk.Grid()
        self.combo_grid.set_column_homogeneous(1)
        self.combo_grid.set_column_spacing(PAD)
        self.combo_grid.set_row_spacing(PAD)

        self.color_list = ['000000'] * 16
        self.button_list = [Gtk.Button('000000') for x in range(16)]
        self.selected_file = ""
        for button in self.button_list:
            button.connect("pressed", self.on_color_click)
            button.set_sensitive(False)

        cont = 0
        for y in range(0, 8, 2):
            for x in range(0, 4):
                label = Gtk.Label(cont)
                self.colorgrid.attach(label, x, y, 1, 1)
                self.colorgrid.attach(self.button_list[cont], x, y + 1, 1, 1)
                cont += 1

        sample_name = os.path.join(SAMPLE_DIR, ".no_sample.sample.png")
        self.sample = Gtk.Image()
        if(os.path.isfile(sample_name)):
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size(
                                                            sample_name,
                                                            width=500,
                                                            height=300)
            self.sample.set_from_pixbuf(self.pixbuf_sample)

        self.shuffle_button = Gtk.Button("Shuffle colors")
        self.shuffle_button.connect("pressed", self.on_shuffle_click)
        self.shuffle_button.set_sensitive(False)

        self.import_button = Gtk.Button("import")
        self.import_button.set_sensitive(False)
        self.import_button.connect("pressed", self.on_import_click)

        self.ok_button = Gtk.Button("Save")
        self.ok_button.connect("pressed", self.on_ok_click)
        self.ok_button.set_sensitive(False)

        self.auto_button = Gtk.Button("Auto-adjust")
        self.auto_button.connect("pressed", self.on_auto_click)
        self.auto_button.set_sensitive(False)

        self.reset_button = Gtk.Button("Reset")
        self.reset_button.set_sensitive(False)
        self.reset_button.connect("pressed", self.on_reset_click)

        self.done_lbl = Gtk.Label("")

        option_list = Gtk.ListStore(str)
        for elem in list(files.get_file_list()):
            option_list.append([elem])

        self.option_combo = Gtk.ComboBox.new_with_model(option_list)
        self.renderer_text = Gtk.CellRendererText()
        self.option_combo.pack_start(self.renderer_text, True)
        self.option_combo.add_attribute(self.renderer_text, "text", 0)
        self.option_combo.set_entry_text_column(0)
        self.option_combo.connect("changed", self.combo_box_change)

        self.combo_grid.attach(self.option_combo, 0, 0, 3, 1)
        self.combo_grid.attach(self.reset_button, 3, 0, 1, 1)

        self.button_grid.attach(self.ok_button, 0, 0, 1, 1)
        self.button_grid.attach(self.auto_button, 1, 0, 1, 1)
        self.button_grid.attach(self.shuffle_button, 2, 0, 1, 1)
        self.button_grid.attach(self.import_button, 3, 0, 1, 1)

        self.sat_light_grid.attach(self.sat_lbl, 0, 0, 1, 1)
        self.sat_light_grid.attach(self.sat_red, 1, 0, 1, 1)
        self.sat_light_grid.attach(self.sat_add, 2, 0, 1, 1)

        self.sat_light_grid.attach(self.light_lbl, 3, 0, 1, 1)
        self.sat_light_grid.attach(self.light_red, 4, 0, 1, 1)
        self.sat_light_grid.attach(self.light_add, 5, 0, 1, 1)

        self.attach(self.combo_grid, 0, 0, 1, 1)
        self.attach(self.button_grid, 0, 1, 1, 1)
        self.attach(self.colorgrid, 0, 2, 1, 1)
        self.attach(self.sample, 0, 3, 1, 1)
        self.attach(self.sat_light_grid, 0, 4, 1, 1)
        self.attach(self.done_lbl, 0, 5, 1, 1)

    def render_buttons(self):
        for x, button in enumerate(self.button_list):
            gcolor = Gdk.color_parse(self.color_list[x])
            if util.get_hls_val(self.color_list[x], 'light') < 99:
                fgcolor = Gdk.color_parse('#FFFFFF')
            else:
                fgcolor = Gdk.color_parse('#000000')
            button.set_label(self.color_list[x])
            button.set_sensitive(True)
            button.modify_bg(Gtk.StateType.NORMAL, gcolor)
            button.modify_fg(Gtk.StateType.NORMAL, fgcolor)

    def render_theme(self):
        sample_path = files.get_sample_path(self.selected_file)

        try:
            self.color_list = color.get_color_list(self.selected_file)
        except SystemExit:
            self.color_list = themer.set_fallback_theme(self.selected_file)
        self.render_buttons()

        try:
            self.pixbuf_sample = GdkPixbuf.Pixbuf\
                .new_from_file_at_size(sample_path, width=500, height=300)
        except:
            sample.create_sample(self.color_list, sample_path)
            self.pixbuf_sample = GdkPixbuf.Pixbuf\
                .new_from_file_at_size(sample_path, width=500, height=300)

        self.sample.set_from_pixbuf(self.pixbuf_sample)
        self.parent.sample.set_from_pixbuf(self.pixbuf_sample)

    def hls_change(self, widget, *gparam):
        if gparam[0] == "sat":
            val = 0.05 if gparam[1] == "add" else -0.05
            self.color_list = [util.alter_brightness(x, 0, val)
                               for x in self.color_list]
        elif gparam[0] == "light":
            val = 10 if gparam[1] == "add" else -10
            self.color_list = [util.alter_brightness(x, val, 0)
                               for x in self.color_list]
        self.render_buttons()
        self.render_sample()

    def render_sample(self):
        sample.create_sample(self.color_list)
        sample_path = os.path.join(SAMPLE_DIR, ".tmp.sample.png")
        self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size(
                sample_path,
                width=500,
                height=300)
        self.sample.set_from_pixbuf(self.pixbuf_sample)

    def on_ok_click(self, widget):
        color.write_colors(self.selected_file, self.color_list)
        tmpfile = os.path.join(SAMPLE_DIR, ".tmp.sample.png")

        if(os.path.isfile(tmpfile)):
            shutil.move(
                os.path.join(SAMPLE_DIR, ".tmp.sample.png"),
                files.get_sample_path(self.selected_file))

            self.done_lbl.set_text("Changes saved")
            sample_path = files.get_sample_path(self.selected_file)
            self.parent.pixbuf_sample = GdkPixbuf.Pixbuf\
                                                 .new_from_file_at_size(sample_path, width=500, height=300)
            self.parent.sample.set_from_pixbuf(self.pixbuf_sample)

    def on_auto_click(self, widget):
        self.color_list = color.auto_adjust(self.color_list)
        self.render_buttons()
        self.render_sample()

    def on_reset_click(self, widget):
        themer.reset_theme(self.selected_file)
        self.render_theme()

    def on_import_click(self, widget):
        fcd = Gtk.FileChooserDialog(
                      'Select a colorscheme', self.parent,
                      Gtk.FileChooserAction.OPEN,
                      (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                       Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter = Gtk.FileFilter()
        filter.set_name("JSON colorscheme")
        filter.add_mime_type("application/json")
        fcd.add_filter(filter)
        response = fcd.run()

        if response == Gtk.ResponseType.OK:
            self.color_list = color.get_color_list(fcd.get_filename(), True)
            self.render_buttons()
            self.render_sample()
        fcd.destroy()

    def on_shuffle_click(self, widget):
        self.color_list = color.shuffle_colors(self.color_list)
        self.render_buttons()
        self.render_sample()

    def on_color_click(self, widget):
        self.done_lbl.set_text("")
        gcolor = Gdk.RGBA()
        gcolor.parse(widget.get_label())
        dialog = ColorDialog(self.parent, self.selected_file, gcolor)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            r, g, b, _ = dialog.colorchooser.get_rgba()
            rgb = list(map(lambda x: round(x*100*2.55), [r, g, b]))
            hex_color = pywal.util.rgb_to_hex(rgb)
            widget.set_label(hex_color)

            gcolor = Gdk.color_parse(hex_color)
            if util.get_hls_val(hex_color, 'light') < 100:
                fgcolor = Gdk.color_parse('#FFFFFF')
            else:
                fgcolor = Gdk.color_parse('#000000')

            widget.set_sensitive(True)
            widget.modify_bg(Gtk.StateType.NORMAL, gcolor)
            widget.modify_fg(Gtk.StateType.NORMAL, fgcolor)

            for i, c in enumerate(self.button_list):
                if c.get_label() != self.color_list[i]:
                    self.color_list[i] = c.get_label()
            self.render_sample()
        dialog.destroy()

    def combo_box_change(self, widget):
        self.done_lbl.set_text("")
        x = self.option_combo.get_active()

        self.auto_button.set_sensitive(True)
        self.shuffle_button.set_sensitive(True)
        self.ok_button.set_sensitive(True)
        self.import_button.set_sensitive(True)
        self.light_add.set_sensitive(True)
        self.light_red.set_sensitive(True)
        self.reset_button.set_sensitive(True)
        self.sat_add.set_sensitive(True)
        self.sat_red.set_sensitive(True)

        current_walls = files.get_file_list()
        self.selected_file = current_walls[x]
        self.render_theme()
