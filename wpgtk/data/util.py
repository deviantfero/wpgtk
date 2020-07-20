import logging
import sys
import subprocess
from math import sqrt
from colorsys import rgb_to_hls, hls_to_rgb

from pywal.util import rgb_to_hex, hex_to_rgb


def get_distance(hex_src, hex_tgt):
    """gets color distance between to hex values"""
    r1, g1, b1 = hex_to_rgb(hex_src)
    r2, g2, b2 = hex_to_rgb(hex_tgt)

    return sqrt((r2 - r1)**2 + (g2 - g1)**2 + (b2 - b1)**2)


def get_hls_val(hexv, what):
    """gets a color in hue light and saturation format"""
    whatdict = {'hue': 0, 'light': 1, 'sat': 2}
    hls = hex_to_hls(hexv)

    return hls[whatdict[what]]


def set_hls_val(hexv, what, val):
    """assign a value to a hls color and return a
    converted hex value"""
    whatdict = {'hue': 0, 'light': 1, 'sat': 2}
    hls = list(hex_to_hls(hexv))

    hls[whatdict[what]] = val
    return hls_to_hex(hls)


def hex_to_hls(hex_string):
    """convert a hex value to hls coordinates"""
    r, g, b = hex_to_rgb(hex_string)
    return rgb_to_hls(r, g, b)


def hls_to_hex(hls):
    """convert a hls coordinate to hex code"""
    h, l, s = hls
    r, g, b = hls_to_rgb(h, l, s)
    rgb_int = [max(min(int(elem), 255), 0) for elem in [r, g, b]]

    return rgb_to_hex(rgb_int)


def alter_brightness(hex_string, amount, sat=0):
    """alters amount of light and saturation in a color"""
    h, l, s = hex_to_hls(hex_string)
    l = max(min(l + amount, 255), 1)
    s = min(max(s - sat, -1), 0)

    return hls_to_hex([h, l, s])


def setup_log():
    logging.basicConfig(format="[%(levelname)s]"
                               " %(module)-13s %(message)s",
                        level=logging.INFO,
                        stream=sys.stdout)
    logging.addLevelName(logging.ERROR, "e")
    logging.addLevelName(logging.INFO, "i")
    logging.addLevelName(logging.WARNING, "w")


def silent_call(cmd):
    """Call a system command and hide it's output"""
    subprocess.call(cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)


def silent_Popen(cmd):
    """Popen a system command and hide it's output"""
    subprocess.Popen(cmd,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)


def get_pid(name):
    """Check if a process is running, borrowed from a newer pywal version"""
    try:
        subprocess.check_output(["pidof", "-s", name])
    except subprocess.CalledProcessError:
        return False

    return True
