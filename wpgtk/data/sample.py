import os
import pywal

from .config import SAMPLE_DIR

try:
    import Image
except ImportError:
    from PIL import Image


def create_sample(colors, f=os.path.join(SAMPLE_DIR, ".tmp.sample.png")):
    """Creates sample image from a pywal color dictionary"""
    im = Image.new("RGB", (480, 50), "white")
    pix = im.load()
    width_sample = im.size[0]//(len(colors)//2)

    for i, c in enumerate(colors[:8]):
        for j in range(width_sample*i, width_sample*i+width_sample):
            for k in range(0, 25):
                pix[j, k] = pywal.util.hex_to_rgb(c)

    for i, c in enumerate(colors[8:16]):
        for j in range(width_sample*i, width_sample*i+width_sample):
            for k in range(25, 50):
                pix[j, k] = pywal.util.hex_to_rgb(c)

    im.save(f)
