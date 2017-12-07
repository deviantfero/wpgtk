import os
import shutil
import pywal
from wpgtk.data import color
from wpgtk.data import config, files, sample
from .color_picker import ColorDialog
from random import shuffle
from gi import require_version
from gi.repository import Gtk, Gdk, GdkPixbuf
require_version("Gtk", "3.0")


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

        self.button_grid = Gtk.Grid()
        self.button_grid.set_column_homogeneous(1)
        self.button_grid.set_column_spacing(PAD)

        self.color_list = []
        self.button_list = []
        self.selected_file = ""
        for x in range(0, 16):
            self.color_list.append('000000')
        for x in range(0, 16):
            self.button_list.append(self.make_button(self.color_list[x]))
            self.button_list[x].connect("pressed", self.on_color_click)
            self.button_list[x].set_sensitive(False)

        cont = 0
        for y in range(0, 8, 2):
            for x in range(0, 4):
                label = Gtk.Label(cont)
                self.colorgrid.attach(label, x, y, 1, 1)
                cont += 1

        cont = 0
        for y in range(1, 9, 2):
            for x in range(0, 4):
                self.colorgrid.attach(self.button_list[cont], x, y, 1, 1)
                cont += 1

        sample_name = os.path.join(config.WALL_DIR, ".no_sample.sample.png")
        self.sample = Gtk.Image()
        if(os.path.isfile(sample_name)):
            self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size(
                                                            sample_name,
                                                            width=500,
                                                            height=300)
            self.sample.set_from_pixbuf(self.pixbuf_sample)

        sampler_name = os.path.join(config.WALL_DIR, ".nsampler.sample.png")
        self.sampler = Gtk.Image()
        if(os.path.isfile(sampler_name)):
            self.pixbuf_sampler = GdkPixbuf.Pixbuf.new_from_file_at_size(
                                                            sampler_name,
                                                            width=500,
                                                            height=300)
            self.sampler.set_from_pixbuf(self.pixbuf_sampler)

        self.shuffle_button = Gtk.Button("Shuffle colors")
        self.shuffle_button.connect("pressed", self.on_shuffle_click)
        self.shuffle_button.set_sensitive(False)

        self.ok_button = Gtk.Button("Save")
        self.ok_button.connect("pressed", self.on_ok_click)
        self.ok_button.set_sensitive(False)

        self.auto_button = Gtk.Button("Auto-adjust")
        self.auto_button.connect("pressed", self.on_auto_click)
        self.auto_button.set_sensitive(False)

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

        self.button_grid.attach(self.ok_button, 0, 0, 1, 1)
        self.button_grid.attach(self.auto_button, 1, 0, 1, 1)
        self.button_grid.attach(self.shuffle_button, 2, 0, 1, 1)

        self.attach(self.option_combo, 0, 0, 1, 1)
        self.attach(self.button_grid, 0, 1, 1, 1)
        self.attach(self.colorgrid, 0, 2, 1, 1)
        self.attach(self.sample, 0, 3, 1, 1)
        self.attach(self.sampler, 0, 4, 1, 1)
        self.attach(self.done_lbl, 0, 5, 1, 1)

    def make_button(self, hex_color):
        button = Gtk.Button(hex_color)
        return button

    def render_buttons(self):
        for x in range(0, 16):
            gcolor = Gdk.color_parse(self.color_list[x])
            if color.get_brightness(self.color_list[x]) < 99:
                fgcolor = Gdk.color_parse('#FFFFFF')
            else:
                fgcolor = Gdk.color_parse('#101010')
            self.button_list[x].set_label(self.color_list[x])
            self.button_list[x].set_sensitive(True)
            self.button_list[x].modify_bg(Gtk.StateType.NORMAL, gcolor)
            self.button_list[x].modify_fg(Gtk.StateType.NORMAL, fgcolor)

    def render_sample(self):
        sample_path = os.path.join(config.WALL_DIR, ".tmp.sample.png")
        self.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size(
                str(sample_path),
                width=500,
                height=300)
        self.sample.set_from_pixbuf(self.pixbuf_sample)
        self.done_lbl.set_text("Auto-adjust done")

    def update_combo(self, option_list):
        self.option_combo.set_model(option_list)
        self.option_combo.set_entry_text_column(0)

    def set_edit_combo(self, x):
        self.option_combo.set_active(x)

    def on_ok_click(self, widget):
        current_walls = files.get_file_list()
        if len(current_walls) > 0:
            x = self.option_combo.get_active()
            color.write_colors(current_walls[x], self.color_list)
            tmpfile = os.path.join(config.WALL_DIR, ".tmp.sample.png")
            if(os.path.isfile(tmpfile)):
                shutil.move(os.path.join(config.WALL_DIR, ".tmp.sample.png"),
                            os.path.join(config.SAMPLE_DIR,
                            (current_walls[x] + ".sample.png")))
                self.done_lbl.set_text("Changes saved")
                x = self.parent.colorscheme.get_active()
                selected_sample = "sample/" + self.selected_file + ".sample.png"
                sample_path = os.path.join(config.WALL_DIR, selected_sample)
                self.parent.pixbuf_sample = GdkPixbuf.Pixbuf.new_from_file_at_size(
                                                                   sample_path,
                                                                   width=500,
                                                                   height=300)
                self.parent.sample.set_from_pixbuf(self.pixbuf_sample)

    def on_auto_click(self, widget):
        self.color_list = color.auto_adjust_colors(self.color_list)
        self.render_buttons()
        sample.create_sample(self.color_list[:])
        self.render_sample()

    def on_shuffle_click(self, widget):
        shuffled_colors = self.color_list[1:7]
        shuffle(shuffled_colors)
        list_tail = shuffled_colors + self.color_list[7:]
        self.color_list = self.color_list[:1] + list_tail
        self.on_auto_click(widget)

    def on_color_click(self, widget):
        self.done_lbl.set_text("")
        gcolor = Gdk.RGBA()
        gcolor.parse(widget.get_label())
        dialog = ColorDialog(self.parent, self.selected_file)
        dialog.colorchooser.set_rgba(gcolor)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            gcolor = dialog.colorchooser.get_rgba()
            rgb = list(map(lambda x: round(x*100*2.55),
                           [gcolor.red, gcolor.green, gcolor.blue]))
            hex_color = pywal.util.rgb_to_hex(rgb)
            widget.set_label(hex_color)
            gcolor = Gdk.color_parse(hex_color)
            if color.get_brightness(hex_color) < 100:
                fgcolor = Gdk.color_parse('#FFFFFF')
            else:
                fgcolor = Gdk.color_parse('#101010')
            widget.set_sensitive(True)
            widget.modify_bg(Gtk.StateType.NORMAL, gcolor)
            widget.modify_fg(Gtk.StateType.NORMAL, fgcolor)
            for i, c in enumerate(self.button_list):
                if c.get_label() != self.color_list[i]:
                    self.color_list[i] = c.get_label()
            sample.create_sample(self.color_list[:])
            self.render_sample()
        dialog.destroy()

    def combo_box_change(self, widget):
        self.done_lbl.set_text("")
        config.RCC = []
        x = self.option_combo.get_active()
        self.auto_button.set_sensitive(True)
        self.shuffle_button.set_sensitive(True)
        self.ok_button.set_sensitive(True)
        current_walls = files.get_file_list()
        self.selected_file = current_walls[x]
        sample_path = os.path.join(config.SAMPLE_DIR,
                                   (self.selected_file + '.sample.png'))
        self.color_list = color.get_color_list(self.selected_file)
        self.render_buttons()
        self.pixbuf_sample = GdkPixbuf.Pixbuf\
            .new_from_file_at_size(sample_path, width=500, height=300)
        self.sample.set_from_pixbuf(self.pixbuf_sample)
