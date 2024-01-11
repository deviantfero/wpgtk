from gi import require_version
import os
import pathlib

require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf  # noqa: E402


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
