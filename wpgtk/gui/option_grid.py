from gi import require_version
from ..data.config import settings, write_conf
from pywal import colors
require_version("Gtk",  "3.0")
from gi.repository import Gtk, Gdk  # noqa: E402

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
        color_list = ['Random'] + [str(x) for x in range(1, 16)]
        self.color_combo = Gtk.ComboBoxText()
        for elem in list(color_list):
            self.color_combo.append_text(elem)
        self.color_combo.connect("changed",  self.combo_box_change, "active")

        # Button
        self.color_button = Gtk.Button("Active/Inactive Color")
        self.save_button = Gtk.Button("Save")
        self.save_button.connect("pressed",  self.on_save_button)

        # Backend Combo
        self.backend_lbl = Gtk.Label("Select your backend:")
        self.backend_combo = Gtk.ComboBoxText()
        self.backend_list = colors.list_backends()

        for elem in self.backend_list:
            self.backend_combo.append_text(elem)
        self.backend_combo.connect("changed", self.combo_box_change, "backend")

        # Switches
        self.gtk_switch = Gtk.Switch()
        self.gtk_switch.connect("notify::active",  self.on_activate, "gtk")
        self.lbl_gtk = Gtk.Label("Reload GTK+")

        self.vte_switch = Gtk.Switch()
        self.vte_switch.connect(
            "notify::active",
            self.on_activate,
            "vte"
        )
        self.lbl_vte = Gtk.Label("Use VTE Fix")

        self.light_theme_switch = Gtk.Switch()
        self.light_theme_switch.connect(
            "notify::active",
            self.on_activate,
            "light_theme"
        )
        self.lbl_light_theme = Gtk.Label("Use light themes")

        self.wallpaper_switch = Gtk.Switch()
        self.wallpaper_switch.connect(
            "notify::active",
            self.on_activate,
            "set_wallpaper"
        )
        self.lbl_wallpaper = Gtk.Label("Set wallpaper")

        self.smart_sort_switch = Gtk.Switch()
        self.smart_sort_switch.connect(
            "notify::active",
            self.on_activate,
            "smart_sort"
        )
        self.lbl_smart_sort = Gtk.Label("Use smart sort")

        self.auto_adjust_switch = Gtk.Switch()
        self.auto_adjust_switch.connect(
            "notify::active",
            self.on_activate,
            "auto_adjust"
        )
        self.lbl_auto_adjust = Gtk.Label("Always auto adjust")

        self.reload_switch = Gtk.Switch()
        self.reload_switch.connect(
            "notify::active",
            self.on_activate,
            "reload"
        )
        self.lbl_reload = Gtk.Label("Reload other software")

        # edit cmd
        self.editor_lbl = Gtk.Label("Open optional files with:")
        self.editor_txt = Gtk.Entry()
        self.editor_txt.connect("changed", self.on_txt_change, "editor")

        # cmd
        self.command_lbl = Gtk.Label("Run command after")
        self.command_exe_lbl = Gtk.Label("Command: ")

        self.command_txt = Gtk.Entry()
        self.command_txt.connect("changed", self.on_txt_change, "command")

        self.command_switch = Gtk.Switch()
        self.command_switch.connect(
            "notify::active",
            self.on_activate,
            "execute_cmd"
        )

        self.alpha_lbl = Gtk.Label('Alpha:')
        self.alpha_txt = Gtk.Entry()
        self.alpha_txt.connect("changed", self.on_txt_change, "alpha")
        self.load_opt_list()

        # Switch Grid attach
        self.switch_grid.attach(self.lbl_wallpaper, 1, 1, 3, 1)
        self.switch_grid.attach(self.wallpaper_switch, 4, 1, 1, 1)

        self.switch_grid.attach(self.lbl_gtk, 5, 1, 3, 1)
        self.switch_grid.attach(self.gtk_switch, 9, 1, 1, 1)

        self.switch_grid.attach(self.lbl_auto_adjust, 5, 2, 3, 1)
        self.switch_grid.attach(self.auto_adjust_switch, 9, 2, 1, 1)

        self.switch_grid.attach(self.command_lbl, 1, 2, 3, 1)
        self.switch_grid.attach(self.command_switch, 4, 2, 1, 1)

        self.switch_grid.attach(self.lbl_light_theme, 1, 3, 3, 1)
        self.switch_grid.attach(self.light_theme_switch, 4, 3, 1, 1)

        self.switch_grid.attach(self.lbl_smart_sort, 1, 4, 3, 1)
        self.switch_grid.attach(self.smart_sort_switch, 4, 4, 1, 1)

        self.switch_grid.attach(self.lbl_vte, 5, 3, 3, 1)
        self.switch_grid.attach(self.vte_switch, 9, 3, 1, 1)

        self.switch_grid.attach(self.lbl_reload, 5, 4, 3, 1)
        self.switch_grid.attach(self.reload_switch, 9, 4, 1, 1)

        # Active Grid attach
        self.active_grid.attach(self.backend_lbl, 1, 1, 1, 1)
        self.active_grid.attach(self.backend_combo, 2, 1, 1, 1)
        self.active_grid.attach(self.color_button, 1, 2, 1, 1)
        self.active_grid.attach(self.color_combo, 2, 2, 1, 1)

        self.active_grid.attach(self.editor_lbl, 1, 3, 1, 1)
        self.active_grid.attach(self.editor_txt, 2, 3, 1, 1)

        self.active_grid.attach(self.command_exe_lbl, 1, 4, 1, 1)
        self.active_grid.attach(self.command_txt, 2, 4, 1, 1)

        self.active_grid.attach(self.alpha_lbl, 1, 5, 1, 1)
        self.active_grid.attach(self.alpha_txt, 2, 5, 1, 1)

        self.active_grid.attach(self.save_button, 1, 6, 2, 1)

        self.attach(self.switch_grid,  1,  1,  1,  1)
        self.attach(self.active_grid,  1,  2,  1,  1)

        self.save_button.set_sensitive(False)

    def on_activate(self,  switch,  *gparam):
        if(gparam[1] == 'execute_cmd'):
            self.command_txt.set_editable(switch.get_active())
        settings[gparam[1]] = str(switch.get_active()).lower()
        self.save_button.set_sensitive(True)

    def load_opt_list(self):
        current_backend = settings.get("backend", "wal")
        idx = self.backend_list.index(current_backend)
        self.backend_combo.set_active(idx)

        self.color_combo\
            .set_active(settings.getint("active", 0))
        self.gtk_switch\
            .set_active(settings.getboolean("gtk", True))
        self.command_switch\
            .set_active(settings.getboolean("execute_cmd", False))
        self.light_theme_switch\
            .set_active(settings.getboolean("light_theme", False))
        self.vte_switch\
            .set_active(settings.getboolean("vte", False))
        self.wallpaper_switch\
            .set_active(settings.getboolean("set_wallpaper", True))
        self.smart_sort_switch\
            .set_active(settings.getboolean("smart_sort", True))
        self.auto_adjust_switch\
            .set_active(settings.getboolean("auto_adjust", False))
        self.reload_switch\
            .set_active(settings.getboolean("reload", True))

        self.editor_txt\
            .set_text(settings.get("editor", "urxvt -e vim"))
        self.command_txt\
            .set_text(settings.get("command", "yes hi"))
        self.command_txt\
            .set_editable(settings.getboolean("execute_cmd", False))
        self.alpha_txt\
            .set_text(settings.get("alpha", "100"))

    def combo_box_change(self, combo, *gparam):
        x = combo.get_active()
        item = combo.get_active_text()

        if gparam[0] == "active":
            settings[gparam[0]] = str(x)
            color = Gdk.color_parse(self.parent.cpage.color_list[x])
            self.color_button.modify_bg(Gtk.StateType.NORMAL,  color)
        if gparam[0] == "backend":
            settings[gparam[0]] = item
        self.save_button.set_sensitive(True)

    def on_txt_change(self, gtk_entry, *gparam):
        settings[gparam[0]] = gtk_entry.get_text()
        self.save_button.set_sensitive(True)

    def on_save_button(self,  button):
        write_conf()
        self.save_button.set_sensitive(False)
