from gi import require_version
import os
import pathlib

require_version("GdkPixbuf", "2.0")
require_version("Gtk", "4.0")
from gi.repository import GdkPixbuf, Gtk, Gdk  # noqa: E402


def get_preview_pixbuf(image_name):
    """
    Get a GdkPixbuf preview for an image file.

    This function takes an image file name as input, checks if the file exists,
    and creates a GdkPixbuf preview for display. If the file is a GIF,
    it extracts the static image from the animation, scales it to 500x333 px
    using the nearest-neighbor interpolation. For other image formats, it
    scales the image to the same dimensions while preserving the aspect ratio.

    Parameters:
    - image_name (str): The path to the image file.

    Returns:
    GdkPixbuf.Pixbuf or None: The GdkPixbuf preview if successful, or None if
    the file does not exist.
    """
    if os.path.isfile(image_name):
        if pathlib.Path(image_name).suffix == ".gif":
            pixbuf = GdkPixbuf.PixbufAnimation.new_from_file(image_name)
            pixbuf = GdkPixbuf.PixbufAnimation.get_static_image(pixbuf)
            pixbuf = GdkPixbuf.Pixbuf.scale_simple(
                pixbuf, 500, 333, GdkPixbuf.InterpType.NEAREST
            )
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                image_name, width=500, height=333, preserve_aspect_ratio=False
            )

        return pixbuf
    else:
        return None


def get_sample_pixbuf(sample_name):
    """
    Get a GdkPixbuf sample for an image file.

    This function takes the name of an image file as input, checks if the file
    exists, and creates a GdkPixbuf sample for display. The image is scaled to
    500x500 pixels.

    Parameters:
    - sample_name (str): The path to the image file.

    Returns:
    GdkPixbuf.Pixbuf or None: The GdkPixbuf sample if successful, or None if
    the file does not exist
    """
    if os.path.isfile(sample_name):
        return GdkPixbuf.Pixbuf.new_from_file_at_size(
            sample_name, width=500, height=500
        )
    else:
        return None


def draw_sample(area, cr, width, height, get_pixbuf):
    """
    Draw a scaled pixbuf centred horizontally into a Cairo context.

    Intended as a draw function for Gtk.DrawingArea.set_draw_func. Scales the
    pixbuf to fit within the given dimensions while preserving the aspect ratio
    then paints it aligned to the top and centred horizontally.

    Parameters:
    - area (Gtk.DrawingArea): the drawing area widget
    - cr (cairo.Context): the Cairo context to draw into
    - width (int): allocated width of the drawing area
    - height (int): allocated height of the drawing area
    - get_pixbuf (callable): called with no arguments to retrieve the current
        GdkPixbuf.Pixbuf to draw; does nothing if it returns None

    Returns:
    """
    pixbuf = get_pixbuf()
    if pixbuf is None:
        return
    img_w = pixbuf.get_width()
    img_h = pixbuf.get_height()
    scale = min(width / img_w, height / img_h)
    dest_w = max(1, int(img_w * scale))
    dest_h = max(1, int(img_h * scale))
    scaled = pixbuf.scale_simple(dest_w, dest_h, GdkPixbuf.InterpType.BILINEAR)
    x = int((width - dest_w) / 2)
    Gdk.cairo_set_source_pixbuf(cr, scaled, x, 0)
    cr.paint()


def set_widget_colors(button, background="#000", foreground="#fff"):
    """
    Set a style for background and foreground on a widget

    This function applies a css provider to the widget passed as parameter
    the css provider includes a basic style string that utilizes the
    background and foreground paramters to change those properties on
    the widget

    Parameters:
    - widget (Gtk.Widget): a GTK widget instance
    - background (str): background color to apply in style
    - foreground (str): foreground color to apply in style

    Returns:
    """
    css_provider = Gtk.CssProvider()
    css = f"""
    button {{
        background-color: {background};
        color: {foreground};
    }}
    """
    css_provider.load_from_data(css.encode())
    button.get_style_context().add_provider(
        css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


def set_uniform_margins(widget, margin):
    """
    Set uniform margins on all sides of a widget

    Parameters:
    - widget (Gtk.Widget): a GTK widget instance
    - margin (integer): the margin amount to apply

    Returns:
    """
    widget.set_margin_top(margin)
    widget.set_margin_bottom(margin)
    widget.set_margin_start(margin)
    widget.set_margin_end(margin)
