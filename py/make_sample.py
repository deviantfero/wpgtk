#!/bin/env python2

from os.path import expanduser

try:
    import Image
except ImportError:
    from PIL import Image

def read_colors( f ):
    rf = open( f, 'r' )
    return rf.read().split('\n')

def hex_color_to_rgb(color):
    color = color[1:] if color[0]=="#" else color
    return (
        int(color[:2], 16),
        int(color[2:4], 16),
        int(color[4:], 16)
        )

def create_sample(f, colors):
    colors.pop()
    im = Image.new("RGB", (1000, 100), "white")
    pix = im.load()

    width_sample = im.size[0]/len(colors)

    for i, c in enumerate(colors):
        for j in range(width_sample*i, width_sample*i+width_sample):
            for k in range(0, 100):
                pix[j, k] = hex_color_to_rgb(c)
    im.save(f)

WALLDIR = expanduser( '~' ) + "/.wallpapers/"
create_sample( WALLDIR + ".tmp.sample.png", read_colors(WALLDIR + ".tmp.colors") )
