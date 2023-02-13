from ..data import util
from gi import require_version
require_version("Gtk", "3.0")
require_version("Gdk", "3.0")
from gi.repository import Gtk  # noqa: E402
from gi.repository import Gdk  # noqa: E402


class ColorDialog(Gtk.Dialog):

    def __init__(self, parent, current_file, gcolor):
        Gtk.Dialog.__init__(self, "Pick a Color", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
        box = self.get_content_area()
        box.set_border_width(10)
        box.set_spacing(10)

        sat_box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)
        light_box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)

        self.colorchooser = Gtk.ColorChooserWidget(show_editor=True)
        self.colorchooser.set_use_alpha(False)
        self.colorchooser.set_rgba(gcolor)

        r, g, b, _ = list(map(lambda x: round(x*100*2.55), gcolor))
        hue, light, sat = util.rgb_to_hls(r, g, b)

        self.sat_lbl = Gtk.Label('Saturation')
        self.light_lbl = Gtk.Label('Light    ')

        sat_range = Gtk.Adjustment(0, 0, 1, 0.1, 0.1, 0)
        self.sat_slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,
                                    adjustment=sat_range)
        self.sat_slider.set_value(-sat)
        self.sat_slider.set_digits(2)
        self.sat_slider.connect('value-changed', self.slider_changed, 'sat')

        light_range = Gtk.Adjustment(5, 0, 255, 1, 10, 0)
        self.light_slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,
                                      adjustment=light_range)
        self.light_slider.set_value(light)
        self.light_slider.connect('value-changed',
                                  self.slider_changed, 'light')

        box.add(self.colorchooser)

        sat_box.pack_start(self.sat_lbl, True, True, 0)
        sat_box.pack_start(self.sat_slider, True, True, 0)

        light_box.pack_start(self.light_lbl, True, True, 0)
        light_box.pack_start(self.light_slider, True, True, 0)

        box.add(light_box)
        box.add(sat_box)

        self.show_all()

    def slider_changed(self, slider, *arg):
        newval = -slider.get_value() if arg[0] == 'sat' else slider.get_value()

        red, green, blue, _ = self.colorchooser.get_rgba()
        rgb = list(map(lambda x: round(x*100*2.55), [red, green, blue]))
        newhex = util.set_hls_val(util.rgb_to_hex(rgb), arg[0], newval)

        new_gcolor = Gdk.RGBA()
        new_gcolor.parse(newhex)
        self.colorchooser.set_rgba(new_gcolor)
