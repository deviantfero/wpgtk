from gi import require_version
from . import util
from ..data.config import user_keywords, settings, write_conf
from pywal import colors

require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa: E402

PAD = 10


class OptionsGrid(Gtk.Grid):
    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.parent = parent
        self.set_column_homogeneous(1)
        self.set_row_spacing(PAD)
        self.set_column_spacing(PAD)

        # Switch Grid
        self.switch_grid = Gtk.Grid()
        self.switch_grid.set_column_homogeneous(1)
        util.set_uniform_margins(self, PAD)
        self.switch_grid.set_row_spacing(PAD)
        self.switch_grid.set_column_spacing(PAD)

        # Active Color Grid
        self.active_grid = Gtk.Grid()
        self.active_grid.set_column_homogeneous(1)
        self.active_grid.set_row_spacing(PAD)
        self.active_grid.set_column_spacing(PAD)

        # Setting up ComboBox
        color_list = ["Random"] + [str(x) for x in range(1, 16)]
        self.color_combo = Gtk.DropDown(model=Gtk.StringList.new(color_list))
        self.color_combo.connect("notify::selected", self._combo_box_change, "active")

        # Button
        self.color_button = Gtk.Button(label="Active/Inactive Color")
        self.save_button = Gtk.Button(label="Save")
        self.save_button.connect("clicked", self._on_save_button)

        # Backend Combo
        self.backend_lbl = Gtk.Label(label="Select your backend:")
        self.backend_list = colors.list_backends()
        self.backend_combo = Gtk.DropDown(model=Gtk.StringList.new(self.backend_list))

        # Keyword Combo
        self.keyword_lbl = Gtk.Label(label="Select your keywords:")
        self.keyword_list = list(user_keywords.sections())
        self.keyword_combo = Gtk.DropDown(model=Gtk.StringList.new(self.keyword_list))

        self.backend_combo.connect("notify::selected", self._combo_box_change, "backend")
        self.keyword_combo.connect("notify::selected", self._combo_box_change, "keywords")

        # Switches
        self.gtk_switch = Gtk.Switch()
        self.gtk_switch.connect("notify::active", self._on_activate, "gtk")
        self.lbl_gtk = Gtk.Label(label="Reload GTK+")

        self.vte_switch = Gtk.Switch()
        self.vte_switch.connect("notify::active", self._on_activate, "vte")
        self.lbl_vte = Gtk.Label(label="Use VTE Fix")

        self.light_theme_switch = Gtk.Switch()
        self.light_theme_switch.connect(
            "notify::active", self._on_activate, "light_theme"
        )
        self.lbl_light_theme = Gtk.Label(label="Use light themes")

        self.wallpaper_switch = Gtk.Switch()
        self.wallpaper_switch.connect(
            "notify::active", self._on_activate, "set_wallpaper"
        )
        self.lbl_wallpaper = Gtk.Label(label="Set wallpaper")

        self.smart_sort_switch = Gtk.Switch()
        self.smart_sort_switch.connect(
            "notify::active", self._on_activate, "smart_sort"
        )
        self.lbl_smart_sort = Gtk.Label(label="Use smart sort")

        self.auto_adjust_switch = Gtk.Switch()
        self.auto_adjust_switch.connect(
            "notify::active", self._on_activate, "auto_adjust"
        )
        self.lbl_auto_adjust = Gtk.Label(label="Always auto adjust")

        self.reload_switch = Gtk.Switch()
        self.reload_switch.connect("notify::active", self._on_activate, "reload")
        self.lbl_reload = Gtk.Label(label="Reload other software")

        self.terminal_switch = Gtk.Switch()
        self.terminal_switch.connect("notify::active", self._on_activate, "terminal")
        self.lbl_terminal = Gtk.Label(label="Change terminal colors")

        # edit cmd
        self.editor_lbl = Gtk.Label(label="Open optional files with:")
        self.editor_txt = Gtk.Entry()
        self.editor_txt.connect("changed", self._on_txt_change, "editor")

        # cmd
        self.command_lbl = Gtk.Label(label="Run command after")
        self.command_exe_lbl = Gtk.Label(label="Command: ")

        self.command_txt = Gtk.Entry()
        self.command_txt.connect("changed", self._on_txt_change, "command")

        self.command_switch = Gtk.Switch()
        self.command_switch.connect("notify::active", self._on_activate, "execute_cmd")

        self.alpha_lbl = Gtk.Label(label="Alpha:")
        self.alpha_txt = Gtk.Entry()
        self.alpha_txt.connect("changed", self._on_txt_change, "alpha")
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

        self.switch_grid.attach(self.lbl_terminal, 1, 5, 3, 1)
        self.switch_grid.attach(self.terminal_switch, 4, 5, 1, 1)

        # Active Grid attach
        self.active_grid.attach(self.backend_lbl, 1, 1, 1, 1)
        self.active_grid.attach(self.backend_combo, 2, 1, 1, 1)
        self.active_grid.attach(self.color_button, 1, 2, 1, 1)
        self.active_grid.attach(self.color_combo, 2, 2, 1, 1)
        self.active_grid.attach(self.keyword_lbl, 1, 3, 1, 1)
        self.active_grid.attach(self.keyword_combo, 2, 3, 1, 1)

        self.active_grid.attach(self.editor_lbl, 1, 4, 1, 1)
        self.active_grid.attach(self.editor_txt, 2, 4, 1, 1)

        self.active_grid.attach(self.command_exe_lbl, 1, 5, 1, 1)
        self.active_grid.attach(self.command_txt, 2, 5, 1, 1)

        self.active_grid.attach(self.alpha_lbl, 1, 6, 1, 1)
        self.active_grid.attach(self.alpha_txt, 2, 6, 1, 1)

        self.active_grid.attach(self.save_button, 1, 7, 2, 1)

        self.attach(self.switch_grid, 1, 1, 1, 1)
        self.attach(self.active_grid, 1, 2, 1, 1)

        self.save_button.set_sensitive(False)

    def _on_activate(self, switch, *gparam):
        if gparam[1] == "execute_cmd":
            self.command_txt.set_editable(switch.get_active())
        settings[gparam[1]] = str(switch.get_active()).lower()
        self.save_button.set_sensitive(True)

    def load_opt_list(self):
        current_backend = settings.get("backend", "wal")
        idx = self.backend_list.index(current_backend)
        self.backend_combo.set_selected(idx)

        current_keywords = settings.get("keywords", "default")
        idx = self.keyword_list.index(current_keywords)
        self.keyword_combo.set_selected(idx)

        self.color_combo.set_selected(settings.getint("active", 0))
        self.gtk_switch.set_active(settings.getboolean("gtk", True))
        self.command_switch.set_active(settings.getboolean("execute_cmd", False))
        self.light_theme_switch.set_active(settings.getboolean("light_theme", False))
        self.vte_switch.set_active(settings.getboolean("vte", False))
        self.wallpaper_switch.set_active(settings.getboolean("set_wallpaper", True))
        self.smart_sort_switch.set_active(settings.getboolean("smart_sort", True))
        self.auto_adjust_switch.set_active(settings.getboolean("auto_adjust", False))
        self.reload_switch.set_active(settings.getboolean("reload", True))
        self.terminal_switch.set_active(settings.getboolean("terminal", True))

        self.editor_txt.set_text(settings.get("editor", "urxvt -e vim"))
        self.command_txt.set_text(settings.get("command", "yes hi"))
        self.command_txt.set_editable(settings.getboolean("execute_cmd", False))
        self.alpha_txt.set_text(settings.get("alpha", "100"))

    def _combo_box_change(self, combo, pspec, key):
        x = combo.get_selected()
        selected_item = combo.get_selected_item()
        item = selected_item.get_string() if selected_item is not None else None

        if key == "active":
            settings[key] = str(x)
            bgcolor = f"#{self.parent.cpage.color_list[x]}"
            util.set_widget_colors(self.color_button, background=bgcolor)
        if key == "backend":
            settings[key] = item
        self.save_button.set_sensitive(True)

    def _on_txt_change(self, gtk_entry, *gparam):
        settings[gparam[0]] = gtk_entry.get_text()
        self.save_button.set_sensitive(True)

    def _on_save_button(self, button):
        write_conf()
        self.save_button.set_sensitive(False)
