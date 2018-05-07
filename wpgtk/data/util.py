import logging
import shutil
import sys
from subprocess import call
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

    return rgb_to_hex(rgb_int)


def alter_brightness(hex_string, amount, sat=0):
    h, l, s = hex_to_hls(hex_string)
    l = max(min(l + amount, 255), 1)
    s = min(max(s - sat, -1), 0)

    return hls_to_hex([h, l, s])


def setup_log():
    logging.basicConfig(format="[%(levelname)s]"
                               " %(module)-13s %(message)s",
                        level=logging.INFO,
                        stream=sys.stdout)
    logging.addLevelName(logging.ERROR, "err")
    logging.addLevelName(logging.INFO, "inf")
    logging.addLevelName(logging.WARNING, "wrn")


def xrdb_merge(file):
    call(['xrdb', '-merge', file])


def build_key(keyword):
    return "<{}>".format(keyword)


def reload_tint2():
    if shutil.which('tint2'):
        call(["pkill", "-SIGUSR1", "tint2"])


def reload_openbox():
    if shutil.which('openbox'):
        call(["openbox", "--reconfigure"])
