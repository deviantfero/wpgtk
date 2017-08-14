import os
from . import config

try:
    import Image
except ImportError:
    from PIL import Image
    
import pywal


def create_sample(colors, f=os.path.join(config.WALL_DIR, ".tmp.sample.png")):
    im = Image.new("RGB", (1000, 100), "white")
    pix = im.load()

    width_sample = im.size[0]//len(colors)

    for i, c in enumerate(colors):
        for j in range(width_sample*i, width_sample*i+width_sample):
            for k in range(0, 100):
                pix[j, k] = pywal.util.hex_to_rgb(c)
    im.save(f)
