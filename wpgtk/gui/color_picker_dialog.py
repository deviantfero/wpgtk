import os

from PIL import Image

from ..data import util as data_util
from ..data import files
from ..data import themer
from ..data.config import WALL_DIR
from . import util as gui_util
from pywal.util import rgb_to_hex

from gi import require_version

require_version("Gtk", "4.0")
require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, Gdk  # noqa: E402


_SLIDER_CFG = {
    "hue": {
        "label": "Hue",
        "lower": 0,
        "upper": 360,
        "step": 1,
        "page": 30,
    },
    "sat": {
        "label": "Saturation",
        "lower": 0,
        "upper": 100,
        "step": 1,
        "page": 10,
    },
    "light": {
        "label": "Lightness",
        "lower": 0,
        "upper": 100,
        "step": 1,
        "page": 10,
    },
}

PAD = 10
LBL_W = 12


class ColorPickerDialog(Gtk.Window):
    """A colour picker dialog with HSL sliders, a hex entry, and a wallpaper
    colour picker displayed directly in the dialog.

    Parameters
    ----------
    parent : Gtk.Window
        Transient parent window.
    initial_color : Gdk.RGBA
        The colour to show when the dialog opens.
    callback : callable or None
        Called as ``callback(dialog, response, rgba)`` where *response* is
        ``Gtk.ResponseType.OK`` or ``Gtk.ResponseType.CANCEL`` and *rgba* is a
        ``Gdk.RGBA``.
    """

    def __init__(self, parent, initial_color, callback=None, wallpaper=None):
        Gtk.Window.__init__(
            self,
            title="Color Picker",
            modal=True,
            transient_for=parent,
            resizable=True,
        )
        self.parent = parent
        self.callback = callback
        self._default_wallpaper = wallpaper

        # Store colour internally as a hex string (the format the existing
        # data_util helpers expect).  Alpha is ignored.
        r = max(0, min(255, int(initial_color.red * 255)))
        g = max(0, min(255, int(initial_color.green * 255)))
        b = max(0, min(255, int(initial_color.blue * 255)))
        self._current_hex = rgb_to_hex([r, g, b])

        # Wallpaper image state (PIL image for pixel reading)
        self._pil_image = None
        self._img_w = 0
        self._img_h = 0

        self._build_ui()
        self.set_default_size(480, 640)

        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self._on_key_pressed)
        self.add_controller(key_controller)

    def _build_ui(self):
        grid = Gtk.Grid()
        grid.set_column_spacing(6)
        grid.set_row_spacing(6)
        gui_util.set_uniform_margins(grid, PAD)

        row = 0

        self.preview = Gtk.DrawingArea()
        self.preview.set_content_width(220)
        self.preview.set_content_height(40)
        self.preview.set_draw_func(self._draw_preview, None)
        grid.attach(self.preview, 0, row, 2, 1)
        row += 1

        hex_label = Gtk.Label(label="Hex:")
        hex_label.set_xalign(1.0)
        hex_label.set_width_chars(LBL_W)

        self.hex_entry = Gtk.Entry()
        self.hex_entry.set_max_length(7)
        self.hex_entry.set_width_chars(9)
        self.hex_entry.set_text(self._current_hex)
        self.hex_entry.connect("activate", self._on_hex_activated)
        self.hex_entry.set_hexpand(True)

        grid.attach(hex_label, 0, row, 1, 1)
        grid.attach(self.hex_entry, 1, row, 1, 1)
        row += 1

        self._sliders = {}
        self._slider_handlers = {}
        hls = data_util.hex_to_hls(self._current_hex)
        init_h = hls[0] * 360
        init_s = max(0, min(100, -hls[2] * 100))
        init_l = hls[1] / 255 * 100
        for channel, cfg in _SLIDER_CFG.items():
            lbl = Gtk.Label(label=cfg["label"], width_chars=LBL_W)
            lbl.set_xalign(1.0)

            initial = {"hue": init_h, "sat": init_s, "light": init_l}[channel]
            adj = Gtk.Adjustment(
                value=initial,
                lower=cfg["lower"],
                upper=cfg["upper"],
                step_increment=cfg["step"],
                page_increment=cfg["page"],
            )
            slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
            slider.set_draw_value(True)
            slider.set_value_pos(Gtk.PositionType.RIGHT)
            slider.set_hexpand(True)
            hid = slider.connect("value-changed", self._on_slider_changed, channel)

            self._sliders[channel] = slider
            self._slider_handlers[channel] = hid

            grid.attach(lbl, 0, row, 1, 1)
            grid.attach(slider, 1, row, 1, 1)
            row += 1

        pick_label = Gtk.Label(label="Pick From:")
        pick_label.set_xalign(1.0)
        pick_label.set_width_chars(LBL_W)

        wallpaper_list = list(files.get_file_list())
        default_idx = 0
        if self._default_wallpaper:
            for i, name in enumerate(wallpaper_list):
                if name == self._default_wallpaper:
                    default_idx = i
                    break
        else:
            for i, name in enumerate(wallpaper_list):
                if name == themer.get_current():
                    default_idx = i
                    break
        self._wallpaper_combo = Gtk.DropDown(model=Gtk.StringList.new(wallpaper_list))
        self._wallpaper_combo.set_hexpand(True)
        self._wallpaper_combo.connect("notify::selected", self._on_wallpaper_changed)

        grid.attach(pick_label, 0, row, 1, 1)
        grid.attach(self._wallpaper_combo, 1, row, 1, 1)
        row += 1

        self._image_display = Gtk.Picture()
        self._image_display.set_hexpand(True)
        self._image_display.set_vexpand(True)
        self._image_display.set_content_fit(Gtk.ContentFit.CONTAIN)
        self._image_display.set_cursor_from_name("eyedropper")

        # Click to pick a colour from the image
        click = Gtk.GestureClick()
        click.connect("pressed", self._on_image_click)
        self._image_display.add_controller(click)

        grid.attach(self._image_display, 0, row, 2, 1)
        row += 1

        # Now safe to trigger the initial load (image area already exists)
        self._wallpaper_combo.set_selected(default_idx)

        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_box.set_halign(Gtk.Align.END)

        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.connect("clicked", self._on_cancel_clicked)

        ok_btn = Gtk.Button(label="OK")
        ok_btn.connect("clicked", self._on_ok_clicked)

        btn_box.append(cancel_btn)
        btn_box.append(ok_btn)
        grid.attach(btn_box, 0, row, 2, 1)

        self.set_child(grid)

    def _load_wallpaper(self, name):
        """Load a wallpaper image into the display and the PIL reader."""
        path = os.path.join(WALL_DIR, name)
        try:
            self._image_display.set_filename(path)
            self._pil_image = Image.open(path).convert("RGB")
            self._img_w, self._img_h = self._pil_image.size
        except Exception:
            self._pil_image = None
            self._img_w = 0
            self._img_h = 0

    def _pixel_at(self, sx, sy):
        """Return hex colour at the given widget coordinates, or None."""
        if self._pil_image is None:
            return None

        alloc = self._image_display.get_allocation()
        a_w, a_h = alloc.width, alloc.height
        if a_w == 0 or a_h == 0:
            return None

        scale = min(a_w / self._img_w, a_h / self._img_h)
        disp_w = int(self._img_w * scale)
        disp_h = int(self._img_h * scale)
        ox = (a_w - disp_w) // 2
        oy = (a_h - disp_h) // 2

        ix = int((sx - ox) / scale)
        iy = int((sy - oy) / scale)
        ix = max(0, min(ix, self._img_w - 1))
        iy = max(0, min(iy, self._img_h - 1))
        return rgb_to_hex(self._pil_image.getpixel((ix, iy)))

    def _draw_preview(self, area, cr, width, height, _data):
        """Fill the preview area with the current colour."""
        rgba = Gdk.RGBA()
        rgba.parse(self._current_hex)
        cr.set_source_rgba(rgba.red, rgba.green, rgba.blue, rgba.alpha)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        cr.set_source_rgba(0.4, 0.4, 0.4, 1)
        cr.set_line_width(1)
        cr.rectangle(0.5, 0.5, width - 1, height - 1)
        cr.stroke()

    def _update_from_hex(self, hex_str):
        """Refresh all UI elements to reflect a new hex colour."""
        self._current_hex = hex_str
        self.hex_entry.set_text(hex_str)

        hls = data_util.hex_to_hls(hex_str)
        user_h = hls[0] * 360
        user_s = max(0, min(100, -hls[2] * 100))
        user_l = hls[1] / 255 * 100
        for channel, val in [("hue", user_h), ("sat", user_s), ("light", user_l)]:
            sl = self._sliders[channel]
            with sl.handler_block(self._slider_handlers[channel]):
                sl.set_value(val)

        self.preview.queue_draw()

    def _current_rgba(self):
        """Return the current colour as a ``Gdk.RGBA``."""
        rgba = Gdk.RGBA()
        rgba.parse(self._current_hex)
        return rgba

    def _on_wallpaper_changed(self, combo, pspec):
        idx = combo.get_selected()
        if idx == Gtk.INVALID_LIST_POSITION:
            return
        wallpaper_list = files.get_file_list()
        if 0 <= idx < len(wallpaper_list):
            self._load_wallpaper(wallpaper_list[idx])

    def _on_image_click(self, gesture, n_press, x, y):
        """Pick the colour from the clicked pixel on the wallpaper."""
        hex_str = self._pixel_at(int(x), int(y))
        if hex_str:
            self._update_from_hex(hex_str)

    def _on_slider_changed(self, slider, channel):
        user_val = slider.get_value()
        if channel == "hue":
            new_hex = data_util.set_hls_val(self._current_hex, channel, user_val / 360)
        elif channel == "sat":
            new_hex = data_util.set_hls_val(self._current_hex, channel, -user_val / 100)
        elif channel == "light":
            new_hex = data_util.set_hls_val(
                self._current_hex, channel, user_val / 100 * 255
            )
        else:
            new_hex = self._current_hex
        self._update_from_hex(new_hex)

    def _on_hex_activated(self, entry):
        text = entry.get_text().strip()
        if not text.startswith("#"):
            text = "#" + text
        rgba = Gdk.RGBA()
        if rgba.parse(text):
            self._update_from_hex(text)
        else:
            entry.set_text(self._current_hex)

    def _on_ok_clicked(self, button):
        if self.callback:
            self.callback(self, Gtk.ResponseType.OK, self._current_rgba())
        self.close()

    def _on_cancel_clicked(self, button):
        if self.callback:
            self.callback(self, Gtk.ResponseType.CANCEL, None)
        self.close()

    def _on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self._on_cancel_clicked(None)
            return True
        return False
