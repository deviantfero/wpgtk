from gi.repository import Gtk, Gdk
from gi import require_version
from wpgtk.data import config
# making sure it uses v3.0
require_version("Gtk",  "3.0")

PAD = 10


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
        self.tint2_switch.connect('notify::active',  self.on_activate, 'tint2')
        self.lbl_tint2 = Gtk.Label('Reload Tint2')
        self.gtk_switch = Gtk.Switch()
        self.gtk_switch.connect('notify::active',  self.on_activate, 'gtk')
        self.lbl_gtk = Gtk.Label('Reload GTK2')
        self.openbox_switch = Gtk.Switch()
        self.openbox_switch.connect('notify::active',
                                    self.on_activate, 'openbox')
        self.lbl_openbox = Gtk.Label('Reload openbox')
        self.light_theme_switch = Gtk.Switch()
        self.light_theme_switch.connect('notify::active',
                                        self.on_activate, 'light_theme')
        self.lbl_light_theme = Gtk.Label('Use Light Theme')

        # edit cmd
        self.editor_lbl = Gtk.Label('Open optional files with:')
        self.editor_txt = Gtk.Entry()
        self.editor_txt.connect("changed", self.on_txt_change, 'editor')

        # cmd

        self.command_lbl = Gtk.Label('Run command after Colorize')
        self.command_exe_lbl = Gtk.Label('Command: ')
        self.command_txt = Gtk.Entry()
        self.command_txt.connect("changed", self.on_txt_change, 'command')
        self.command_switch = Gtk.Switch()
        self.command_switch.connect('notify::active',
                                    self.on_activate, 'execute_cmd')

        self.load_opt_list()

        # Switch Grid attach
        self.switch_grid.attach(self.lbl_tint2, 1, 1, 3, 1)
        self.switch_grid.attach(self.tint2_switch, 4, 1, 1, 1)
        self.switch_grid.attach(self.lbl_gtk, 5, 1, 3, 1)
        self.switch_grid.attach(self.gtk_switch, 9, 1, 1, 1)
        self.switch_grid.attach(self.command_lbl, 1, 2, 3, 1)
        self.switch_grid.attach(self.command_switch, 4, 2, 1, 1)
        self.switch_grid.attach(self.lbl_openbox, 5, 2, 3, 1)
        self.switch_grid.attach(self.openbox_switch, 9, 2, 1, 1)
        self.switch_grid.attach(self.lbl_light_theme, 1, 3, 3, 1)
        self.switch_grid.attach(self.light_theme_switch, 4, 3, 1, 1)

        # cmd Grid attach

        # Active Grid attach
        self.active_grid.attach(self.lbl_active, 1, 1, 2, 1)
        self.active_grid.attach(self.color_combo, 1, 2, 1, 1)
        self.active_grid.attach(self.color_button, 2, 2, 1, 1)
        self.active_grid.attach(self.editor_lbl, 1, 3, 1, 1)
        self.active_grid.attach(self.editor_txt, 2, 3, 1, 1)
        self.active_grid.attach(self.command_exe_lbl, 1, 4, 1, 1)
        self.active_grid.attach(self.command_txt, 2, 4, 1, 1)
        self.active_grid.attach(self.save_button, 1, 5, 2, 1)
        self.active_grid.attach(self.lbl_save, 1, 6, 2, 1)

        self.attach(self.switch_grid,  1,  1,  1,  1)
        self.attach(self.active_grid,  1,  2,  1,  1)

    def on_activate(self,  switch,  *gparam):
        if(gparam[1] == 'execute_cmd'):
            self.command_txt.set_editable(switch.get_active())
        config.wpgtk[gparam[1]] = str(switch.get_active()).lower()
        self.lbl_save.set_text('')

    def load_opt_list(self):
        self.color_combo.set_active(config.wpgtk.getint('active', 0))
        self.gtk_switch.set_active(config.wpgtk.getboolean('gtk', True))
        self.tint2_switch.set_active(config.wpgtk.getboolean('tint2', True))
        self.command_switch.set_active(config.wpgtk.getboolean('execute_cmd', False))
        self.openbox_switch.set_active(config.wpgtk.getboolean('openbox', True))
        self.editor_txt.set_text(config.wpgtk.get('editor', 'urxvt -e vim'))
        self.command_txt.set_text(config.wpgtk.get('command', 'yes hi'))
        self.command_txt.set_editable(config.wpgtk.getboolean('execute_cmd', False))
        self.light_theme_switch.set_active(config.wpgtk.getboolean('light_theme', False))

    def combo_box_change(self,  combo):
        config.wpgtk['active'] = str(combo.get_active())
        color = Gdk.color_parse(
                self.parent.cpage.color_list[combo.get_active() - 1])
        self.color_button.modify_bg(Gtk.StateType.NORMAL,  color)
        self.lbl_save.set_text('')

    def on_txt_change(self, gtk_entry, *gparam):
        config.wpgtk[gparam[0]] = gtk_entry.get_text()
        self.lbl_save.set_text('')

    def on_save_button(self,  button):
        config.write_conf()
        self.lbl_save.set_text('Saved')
