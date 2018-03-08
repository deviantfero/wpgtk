from colorsys import rgb_to_hls, hls_to_rgb
from pywal.util import rgb_to_hex, hex_to_rgb


def get_hls_val(hexv, what):
    whatdict = {'hue': 0, 'light': 1, 'sat': 2}
    hls = hex_to_hls(hexv)

    return hls[whatdict[what]]


def set_hls_val(hexv, what, val):
    whatdict = {'hue': 0, 'light': 1, 'sat': 2}
    hls = list(hex_to_hls(hexv))

    hls[whatdict[what]] = val
    return hls_to_hex(hls)


def hex_to_hls(hex_string):
    r, g, b = hex_to_rgb(hex_string)
    return rgb_to_hls(r, g, b)


def hls_to_hex(hls):
    h, l, s = hls
    r, g, b = hls_to_rgb(h, l, s)
    rgb_int = [max(min(int(elem), 255), 0) for elem in [r, g, b]]
    rgb_int = tuple(rgb_int)

    hex_result = '%02x%02x%02x' % rgb_int
    return "#%s" % hex_result


def reduce_brightness(hex_string, amount, sat=0):
    h, l, s = hex_to_hls(hex_string)
    l = max(l - amount, 1)
    s = max(s - sat, -1)

    return hls_to_hex([h, l, s])


def add_brightness(hex_string, amount, sat=0):
    h, l, s = hex_to_hls(hex_string)
    l = min(l + amount, 255)
    s = max(s - sat, -1)

    return hls_to_hex([h, l, s])


def build_key(keyword):
    return "<{}>".format(keyword)
