from gi.repository import Gtk, Gdk
from getpass import getuser
from gi import require_version
from ..data.conf_parser import parse_conf, write_conf
# making sure it uses v3.0
require_version("Gtk",  "3.0")

PAD = 10
HOME = "/home/" + getuser()
WALLDIR = HOME + "/.wallpapers/"


class OptionsGrid(Gtk.Grid):
    def __init__(self,  parent):
        Gtk.Grid.__init__(self)
        self.parent = parent
        self.set_border_width(PAD)
        self.set_column_homogeneous(1)
        self.set_row_spacing(PAD)
        self.set_column_spacing(PAD)

        # Switch Grid
        self.switch_grid = Gtk.Grid()
        self.switch_grid.set_border_width(PAD)
        self.switch_grid.set_column_homogeneous(1)
        self.switch_grid.set_row_spacing(PAD)
        self.switch_grid.set_column_spacing(PAD)

        # Active Color Grid
        self.active_grid = Gtk.Grid()
        self.active_grid.set_border_width(PAD)
        self.active_grid.set_column_homogeneous(1)
        self.active_grid.set_row_spacing(PAD)
        self.active_grid.set_column_spacing(PAD)

        # Setting up ComboBox
        colors = ['Random'] + [str(x) for x in range(1, 16)]
        option_list = Gtk.ListStore(str)
        for elem in list(colors):
            option_list.append([elem])

        # ComboBox
        self.color_combo = Gtk.ComboBox.new_with_model(option_list)
        self.renderer_text = Gtk.CellRendererText()
        self.color_combo.pack_start(self.renderer_text,  True)
        self.color_combo.add_attribute(self.renderer_text,  'text',  0)
        self.color_combo.set_entry_text_column(0)
        self.color_combo.connect("changed",  self.combo_box_change)

        # Button
        self.color_button = Gtk.Button()
        self.lbl_active = Gtk.Label('Active/Inactive Color:')
        self.save_button = Gtk.Button('Save')
        self.save_button.connect("pressed",  self.on_save_button)
        self.lbl_save = Gtk.Label('')

        # Switches
        self.tint2_switch = Gtk.Switch()
        self.tint2_switch.connect('notify::active',  self.on_tint2_active)
        self.lbl_tint2 = Gtk.Label('Colorize Tint2')
        self.gtk_switch = Gtk.Switch()
        self.gtk_switch.connect('notify::active',  self.on_gtk_active)
        self.lbl_gtk = Gtk.Label('Colorize GTK')

        self.opt_list = parse_conf()
        self.load_opt_list()

        # Switch Grid attach
        self.switch_grid.attach(self.lbl_tint2, 1, 1, 3, 1)
        self.switch_grid.attach(self.tint2_switch, 4, 1, 1, 1)
        self.switch_grid.attach(self.lbl_gtk, 5, 1, 3, 1)
        self.switch_grid.attach(self.gtk_switch, 9, 1, 1, 1)

        # Active Grid attach
        self.active_grid.attach(self.lbl_active, 1, 1, 1, 1)
        self.active_grid.attach(self.color_combo, 1, 2, 1, 1)
        self.active_grid.attach(self.color_button, 2, 2, 1, 1)
        self.active_grid.attach(self.save_button, 1, 3, 2, 1)
        self.active_grid.attach(self.lbl_save, 1, 4, 2, 1)

        self.attach(self.switch_grid,  1,  1,  1,  1)
        self.attach(self.active_grid,  1,  2,  1,  1)

    def on_tint2_active(self,  switch,  gparam):
        if switch.get_active():
            self.opt_list['TN2'] = True
        else:
            self.opt_list['TN2'] = False
        self.lbl_save.set_text('')

    def on_gtk_active(self,  switch,  gparam):
        if switch.get_active():
            self.opt_list['GTK'] = True
        else:
            self.opt_list['GTK'] = False
        self.lbl_save.set_text('')

    def load_opt_list(self):
        self.color_combo.set_active(self.opt_list['ACT'])
        self.gtk_switch.set_active(self.opt_list['GTK'])
        self.tint2_switch.set_active(self.opt_list['TN2'])

    def combo_box_change(self,  combo):
        self.opt_list['ACT'] = combo.get_active()
        color = Gdk.color_parse(
                '#' + self.parent.cpage.color_list[combo.get_active()])
        self.color_button.modify_bg(Gtk.StateType.NORMAL,  color)
        self.lbl_save.set_text('')

    def on_save_button(self,  button):
        write_conf(opt=self.opt_list)
        self.lbl_save.set_text('Saved')
