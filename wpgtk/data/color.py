import shutil
import sys
from subprocess import call
import os
from colorsys import rgb_to_hls, hls_to_rgb
from random import randint
from . import config
import pywal


def get_color_list(image_name):
    image = pywal.image.get(os.path.join(config.WALL_DIR, image_name))
    color_dict = pywal.colors.get(image, config.WALL_DIR)
    return [color_dict['colors']['color%s' % i] for i in range(16)]


def is_dark_theme(color_list):
    fg_brightness = get_brightness(color_list[7])
    bg_brightness = get_brightness(color_list[0])
    return fg_brightness > bg_brightness


def get_random_color(image_name):
    image_path = os.path.join(config.WALL_DIR, image_name)
    if not config.RCC:
        config.RCC = pywal.colors.gen_colors(image_path, 36)
    return config.RCC[randint(0, len(config.RCC))]


def write_colors(img, color_list):
    image = pywal.image.get(os.path.join(config.WALL_DIR, img))
    color_dict = pywal.colors.get(image, config.WALL_DIR)

    for i in range(16):
        color_dict['colors']['color%s' % i] = color_list[i]
    color_dict['special']['background'] = color_list[0]
    color_dict['special']['foreground'] = color_list[15]

    cache_file = os.path.join(config.SCHEME_DIR,
                              str(image).replace('/', '_').replace('.', '_'))
    pywal.export.color(color_dict, "json", cache_file + ".json")
    pywal.export.color(color_dict,
                       "xresources",
                       os.path.join(config.XRES_DIR, (img + ".Xres")))


def change_colors(colors, which):
    opt = which
    if which in config.FILE_DIC:
        which = config.FILE_DIC[which]
    try:
        tmp_filename = which + '.base'
        with open(tmp_filename, 'r') as tmp_file:
            top = tmp_file.tell()
            first_line = tmp_file.readline()
            tmp_file.seek(top)
            tmp_data = tmp_file.read()

        # ignore the template if it has wpgtk-ignore in it
        if 'wpgtk-ignore' not in first_line:
            for k, v in colors['wpgtk'].items():
                tmp_data = tmp_data.replace(k, v.strip('#'))
            for i in range(16):
                replace_word = 'COLOR%d' % i if i < 10 else 'COLORX%d' % i
                replace_val = colors['colors']['color%s' % i].strip('#')
                tmp_data = tmp_data.replace(replace_word, replace_val)
            if colors['icons'] and opt == 'icon-step1':
                for k, v in colors['icons'].items():
                    tmp_data = tmp_data.replace(k, v.replace('#', ''))

            with open(which, 'w') as target_file:
                target_file.write(tmp_data)
            print("OK:: %s - CHANGED SUCCESSFULLY" %
                  opt.replace(config.OPT_DIR + '/', 'template :: '))
    except IOError as err:
        print("ERR::%s - "
              "BASE FILE DOES NOT EXIST" % opt, file=sys.stderr)


def auto_adjust_colors(color_list):
    if not config.wpgtk.getboolean('light_theme'):
        if not is_dark_theme(color_list):
            color7 = color_list[7]
            # switch bg for fg
            color_list[7] = color_list[0]
            color_list[0] = color7
        color8 = [add_brightness(color_list[0], 18)]
        color_list = color_list[:8] + color8 + \
            [add_brightness(x, 50) for x in color_list[1:8]]
    else:
        if is_dark_theme(color_list):
            color7 = color_list[7]
            # switch bg for fg
            color_list[7] = color_list[0]
            color_list[0] = color7
        color8 = [reduce_brightness(color_list[0], 18)]
        color_list = color_list[:8] + color8 + \
            [reduce_brightness(x, 60, 0.5) for x in color_list[1:8]]

    return color_list


def clean_icon_color(dirty_string):
    dirty_string = dirty_string.strip("\n")
    dirty_string = dirty_string.split("=")
    dirty_string = dirty_string.pop()
    return dirty_string


def get_brightness(hexv):
    rgb = list(int(hexv.strip('#')[i:i+2], 16) for i in (0, 2, 4))
    hls = rgb_to_hls(rgb[0], rgb[1], rgb[2])
    hls = list(hls)
    return hls[1]


def reduce_brightness(hex_string, amount, sat=0.1):
    rgb = pywal.util.hex_to_rgb(hex_string)
    hls = rgb_to_hls(rgb[0], rgb[1], rgb[2])
    hls = list(hls)

    hls[1] = max(hls[1] - amount, 5)
    hls[2] = max(hls[2] - sat, -0.90)

    rgb = hls_to_rgb(hls[0], hls[1], hls[2])
    rgb_int = [5 if elem <= 0 else 254 if elem > 255
               else int(elem) for elem in rgb]
    rgb_int = tuple(rgb_int)
    hex_result = '%02x%02x%02x' % rgb_int

    return "#%s" % hex_result


def add_brightness(hex_string, amount, sat=0.1):
    rgb = pywal.util.hex_to_rgb(hex_string)
    hls = rgb_to_hls(rgb[0], rgb[1], rgb[2])
    hls = list(hls)

    hls[1] = min(hls[1] + amount, 250)
    hls[2] = max(hls[2] - sat, -0.90)

    rgb = hls_to_rgb(hls[0], hls[1], hls[2])
    rgb_int = [254 if elem > 255 else 0 if elem <= 0
               else int(elem) for elem in rgb]
    rgb_int = tuple(rgb_int)
    hex_result = '%02x%02x%02x' % rgb_int

    return "#%s" % hex_result


def prepare_icon_colors(colors):
    try:
        glyph = reduce_brightness(colors['wpgtk']['COLORIN'], 15)
        file_current_glyph = open(config.FILE_DIC['icon-step1'], "r")
        current_back = ""
        current_front = ""
        current_glyph = ""
        for line in file_current_glyph:
            if("New" in line and "glyph" in line):
                current_glyph = clean_icon_color(line)
                break
        for line in file_current_glyph:
            if("New" in line and "front" in line):
                current_front = clean_icon_color(line)
                break
        for line in file_current_glyph:
            if("New" in line and "back" in line):
                current_back = clean_icon_color(line)
                break
        file_current_glyph.close()

        icon_dic = {"l=178984": "l=" + current_glyph,
                    "w=178984": "w=" + glyph,
                    "l=36d7b7": "l=" + current_front,
                    "w=36d7b7": "w=" + colors['wpgtk']['COLORACT'],
                    "l=1ba39c": "l=" + current_back,
                    "w=1ba39c": "w=" + colors['wpgtk']['COLORIN']}
        return icon_dic
    except IOError:
        print("ERR::ICONS - BASE FILES DO NOT EXIST", file=sys.stderr)
        return


def change_other_files(colors):
    other_path = os.path.join(config.HOME, ".themes/color_other")
    files = []
    for(dirpath, dirnames, filenames) in os.walk(other_path):
        files.extend(filenames)

    try:
        for word in files:
            if '.base' in word:
                original = word.split('.base', len(word)).pop(0)
                change_colors(colors, os.path.join(other_path, original))
    except Exception as e:
        print('ERR:: ' + str(e), file=sys.stderr)
        print('ERR::OPTIONAL FILE -' + original, file=sys.stderr)


def split_active(hexc, is_dark_theme=True):
    brightness = get_brightness(hexc)
    if is_dark_theme:
        return [reduce_brightness(hexc, brightness * 0.31),
                reduce_brightness(hexc, brightness * 0.61)]
    else:
        return [add_brightness(hexc, brightness * 0.31, 0), hexc]


def prepare_colors(image_name):
    image = pywal.image.get(os.path.join(config.WALL_DIR, image_name))
    cdic = pywal.colors.get(image, config.WALL_DIR)

    wpcol = cdic['wpgtk'] = {}
    cl = [cdic['colors']['color%s' % i] for i in range(16)]

    if(config.wpgtk.getint('active') > 0):
        wpcol['BASECOLOR'] = cl[config.wpgtk.getint('active') - 1]
    else:
        wpcol['BASECOLOR'] = cl[randint(0, 15)]

    wpcol['COLORBASE'] = cl[0]
    if is_dark_theme(cl):
        wpcol['COLORBG'] = reduce_brightness(cl[0], 10)
        wpcol['COLORTOOL'] = add_brightness(cl[0], 4)
        wpcol['COLORACT'], wpcol['COLORIN'] = split_active(wpcol['BASECOLOR'])
    else:
        wpcol['COLORBG'] = add_brightness(cl[0], 10)
        wpcol['COLORTOOL'] = reduce_brightness(cl[0], 4)
        wpcol['COLORACT'], wpcol['COLORIN'] = split_active(wpcol['BASECOLOR'],
                                                           False)
    wpcol['REPLAC'] = add_brightness(wpcol['COLORACT'], 70)

    cdic['icons'] = prepare_icon_colors(cdic)

    print("INF::FG: " + wpcol['COLORACT'])
    print("INF::BG: " + wpcol['COLORIN'])

    return cdic


def execute_gcolorchange(image_name):
    colors = prepare_colors(image_name)

    if config.wpgtk.getboolean('gtk'):
        change_colors(colors, 'gtk2')
        change_colors(colors, 'gtk3.0')
        change_colors(colors, 'gtk3.20')
        pywal.reload.gtk()

    if os.path.isfile(config.FILE_DIC['icon-step2']):
        change_colors(colors, 'icon-step1')
        call(config.FILE_DIC['icon-step2'])

    change_other_files(colors)
    if config.wpgtk.getboolean('tint2') or not shutil.which('tint2'):
        call(["pkill", "-SIGUSR1", "tint2"])
    if config.wpgtk.getboolean('openbox') and shutil.which('openbox'):
        call(["openbox", "--reconfigure"])
    print("OK::FINISHED")
