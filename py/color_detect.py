import sys
import colorsys
from colorz import colorz
from math import sqrt

try:
    import Image
except ImportError:
    from PIL import Image

if len(sys.argv) < 2:
  print "Usage: {0} FILENAME [num_colors]".format(sys.argv[0])
  sys.exit()


print sys.argv[1]

WALLPAPER = sys.argv[1]
filename = WALLPAPER.split('/').pop()
COLORS = ".{0}.colors".format(filename)
XRESOURCES = ".{0}.Xres".format(filename)
SAMPLE = ".{0}.sample.png".format(filename)

cols = ''
xres = ''

def torgb(hexv):
    hexv = hexv[1:]
    r, g, b = (
        int(hexv[0:2], 16) / 256.0,
        int(hexv[2:4], 16) / 256.0,
        int(hexv[4:6], 16) / 256.0,
    )
    return r, g, b

def normalize(hexv, minv=128, maxv=256):
    r, g, b = torgb(hexv)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    minv = minv / 256.0
    maxv = maxv / 256.0
    if v < minv:
        v = minv
    if v > maxv:
        v = maxv
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return '#{:02x}{:02x}{:02x}'.format(int(r * 256), int(g * 256), int(b * 256))

def darkness(hexv):
  r, g, b = torgb(hexv)
  darkness = sqrt((255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2)
  return darkness

def to_hsv(c):
    r, g, b = torgb(c)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v

def hex_color_to_rgb(color):
    color = color[1:] if color[0]=="#" else color
    return (
        int(color[:2], 16),
        int(color[2:4], 16),
        int(color[4:], 16)
        )

def create_sample(f, colors):
    im = Image.new("RGB", (1000, 100), "white")
    pix = im.load()

    width_sample = im.size[0]/len(colors)

    for i, c in enumerate(colors):
        for j in range(width_sample*i, width_sample*i+width_sample):
            for k in range(0, 100):
                pix[j, k] = hex_color_to_rgb(c)

    im.save(f)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        n = 16
    else:
        n = int(sys.argv[2])


    i = 0
    # sort by value, saturation, then hue
    colors = colorz(WALLPAPER, n=n)
    colors.sort(key=lambda  x:darkness(x), reverse=True)
    for c in colors:
        if i == 0:
            c = normalize(c, minv=0, maxv=32)
        elif i == 8:
            c = normalize(c, minv=128, maxv=192)
        elif i < 8:
            c = normalize(c, minv=160, maxv=224)
        else:
            c = normalize(c, minv=200, maxv=256)
        c = normalize(c, minv=32, maxv=224)
        xres += """*color{}: {}\n""".format(i, c)
        cols += """export COLOR{}="{}"\n""".format(i, c)
        i += 1

    create_sample(SAMPLE, colors)
    with open(XRESOURCES, 'w') as f:
        f.write(xres)
    with open(COLORS, 'w') as f:
        f.write(cols)
