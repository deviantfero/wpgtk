import shutil
import sys
import logging
from subprocess import call
from random import shuffle
from os.path import join, isfile
from random import randint
from . import config, files, util, sample
import pywal


def get_pywal_dict(filename):
    image = pywal.image.get(join(config.WALL_DIR, filename))
    return pywal.colors.get(image,
                            backend=config.wpgtk.get('backend', 'wal'),
                            cache_dir=config.WALL_DIR)


def get_color_list(filename, json=False):

    is_new = not isfile(files.get_cache_path(filename))

    theme = get_pywal_dict(filename) if not json\
        else pywal.util.read_file_json(filename)
    color_list = theme["color"] if "color" in theme \
        else list(theme["colors"].values())

    if is_new and not json:
        color_list = auto_adjust_colors(color_list)
        sample.create_sample(color_list, files.get_sample_path(filename))
        write_colors(filename, color_list)

    return color_list


def is_dark_theme(color_list):
    fg_brightness = util.get_hls_val(color_list[7], 'light')
    bg_brightness = util.get_hls_val(color_list[0], 'light')
    return fg_brightness > bg_brightness


def shuffle_colors(colors):
        shuffled_colors = colors[1:7]
        shuffle(shuffled_colors)
        colors = colors[:1] + shuffled_colors + colors[7:]
        return auto_adjust_colors(colors)


def write_colors(img, color_list):
    color_dict = get_pywal_dict(img)

    for i in range(16):
        color_dict['colors']['color%s' % i] = color_list[i]
    color_dict['special']['background'] = color_list[0]
    color_dict['special']['foreground'] = color_list[15]

    cache_file = files.get_cache_path(img)

    pywal.export.color(color_dict, "json", cache_file)
    pywal.export.color(color_dict,
                       "xresources",
                       join(config.XRES_DIR, (img + ".Xres")))


def change_colors(colors, which):
    opt = which
    if which in config.FILE_DIC:
        which = config.FILE_DIC[which]
    try:
        tmp_filename = which + '.base'
        with open(tmp_filename, 'r') as tmp_file:
            first_line = tmp_file.readline()
            tmp_file.seek(0)
            tmp_data = tmp_file.read()

        if 'wpgtk-ignore' not in first_line:
            for k, v in config.keywords.items():
                tmp_data = tmp_data.replace(util.build_key(k), v)
            for k, v in colors["wpgtk"].items():
                tmp_data = tmp_data.replace(util.build_key(k), v.strip('#'))
            for k, v in colors["colors"].items():
                k = util.build_key(k).upper()
                tmp_data = tmp_data.replace(k, v.strip('#'))

            if colors['icons'] and opt == 'icon-step1':
                for k, v in colors['icons'].items():
                    tmp_data = tmp_data.replace(k, v.replace('#', ''))

            with open(which, 'w') as target_file:
                target_file.write(tmp_data)
            logging.info("applying: %s" % opt.split('/').pop())
    except IOError as err:
        logging.error("%s - base file does not exist" % opt)


def auto_adjust_colors(clist):
    light = config.wpgtk.getboolean('light_theme')

    added_sat = 0.25 if light else 0.1
    bm = util.reduce_brightness if light else util.add_brightness

    if light == is_dark_theme(clist):
        # convert dark to light or the other way around
        sat_diff = -0.1 if light else 0.1
        clist = [clist[0]] \
            + [bm(x, 0, sat_diff) for x in clist[1:7]] \
            + clist[7:]

        color7 = clist[7]
        clist[7] = clist[0]
        clist[0] = color7

    color8 = [bm(clist[0], 20)]
    color15 = [bm(clist[7], 60)]
    clist = clist[:8] + color8 \
        + [bm(x, util.get_hls_val(x, 'light') * 0.3, added_sat)
           for x in clist[1:7]] + color15

    return clist


def prepare_icon_colors(colors):
    try:
        glyph = util.reduce_brightness(colors['wpgtk']['COLORIN'], 15)
        file_current_glyph = open(config.FILE_DIC['icon-step1'], "r")
        icon_dic = {}

        for line in file_current_glyph:
            if('glyphColorNew=' in line):
                icon_dic['oldglyph'] = line.split('=')[1].strip('\n')
            if('frontColorNew=' in line):
                icon_dic['oldfront'] = line.split('=')[1].strip('\n')
            if('backColorNew=' in line):
                icon_dic['oldback'] = line.split('=')[1].strip('\n')
        file_current_glyph.close()

        icon_dic['newglyph'] = glyph
        icon_dic['newfront'] = colors['wpgtk']['COLORACT']
        icon_dic['newback'] = colors['wpgtk']['COLORIN']

        return icon_dic
    except IOError:
        logging.error("icons - base file does not exists")
        return


def change_templates(colors):
    template_dir = config.FILE_DIC['templates']
    fl = files.get_file_list(template_dir, images=False)
    fl = list(filter(lambda x: '.base' in x, fl))

    try:
        for word in fl:
            original = word.split('.base', len(word)).pop(0)
            change_colors(colors, join(template_dir, original))
    except Exception as e:
        logging.error(str(e))
        logging.error('optional file ' + original, file=sys.stderr)


def split_active(hexc, is_dark_theme=True):
    brightness = util.get_hls_val(hexc, 'light')
    if is_dark_theme:
        return [util.reduce_brightness(hexc, brightness * 0.20),
                util.reduce_brightness(hexc, brightness * 0.45)]
    else:
        return [util.add_brightness(hexc, brightness * 0.30), hexc]


def prepare_colors(image_name):
    image = pywal.image.get(join(config.WALL_DIR, image_name))
    cdic = get_pywal_dict(image)

    wpcol = cdic['wpgtk'] = {}
    cl = [cdic['colors']['color%s' % i] for i in range(16)]

    # getting base colors
    if(config.wpgtk.getint('active') > 0):
        bc = cl[config.wpgtk.getint('active') - 1]
    else:
        bc = cl[randint(0, 15)]

    wpcol['COLORACT'], wpcol['COLORIN'] = split_active(bc, is_dark_theme(cl))
    cdic['icons'] = prepare_icon_colors(cdic)

    return cdic


def apply_colorscheme(image_name):
    colors = prepare_colors(image_name)

    if config.wpgtk.getboolean('gtk'):
        pywal.reload.gtk()

    if isfile(config.FILE_DIC['icon-step2']):
        change_colors(colors, 'icon-step1')
        call(config.FILE_DIC['icon-step2'])

    change_templates(colors)

    if config.wpgtk.getboolean('tint2') or not shutil.which('tint2'):
        call(["pkill", "-SIGUSR1", "tint2"])
    if config.wpgtk.getboolean('openbox') and shutil.which('openbox'):
        call(["openbox", "--reconfigure"])
