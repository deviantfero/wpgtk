import shutil
import sys
from subprocess import call
from random import shuffle
from os.path import join, isfile
from random import randint
from . import config, files, util, logger, sample
import pywal


def get_color_list(filename, json=False):
    if not json:
        image = pywal.image.get(join(config.WALL_DIR, filename))
        theme = pywal.colors.get(image, config.WALL_DIR)
    else:
        theme = pywal.util.read_file_json(filename)
        if 'color' in theme:
            return theme['color']

    return [theme['colors']['color%s' % i] for i in range(16)]


def is_dark_theme(color_list):
    fg_brightness = util.get_hls_val(color_list[7], 'light')
    bg_brightness = util.get_hls_val(color_list[0], 'light')
    return fg_brightness > bg_brightness


def get_random_color(image_name):
    image_path = join(config.WALL_DIR, image_name)
    if not config.RCC:
        config.RCC = pywal.colors.gen_colors(image_path, 48)
    return config.RCC[randint(0, len(config.RCC) - 1)]


def shuffle_colors(filename):
    try:
        colors = get_color_list(filename)
        shuffled_colors = colors[1:7]
        shuffle(shuffled_colors)
        colors = colors[:1] + shuffled_colors + colors[7:]
        sample.create_sample(colors, join(config.SAMPLE_DIR,
                             filename + '.sample.png'))
        write_colors(filename, colors)
    except IOError as e:
        logger.log.error('file not available')


def write_colors(img, color_list):
    image = pywal.image.get(join(config.WALL_DIR, img))
    color_dict = pywal.colors.get(image, config.WALL_DIR)

    for i in range(16):
        color_dict['colors']['color%s' % i] = color_list[i]
    color_dict['special']['background'] = color_list[0]
    color_dict['special']['foreground'] = color_list[15]

    cache_file = files.get_cache_filename(img)

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
            logger.log.info("%s - CHANGED SUCCESSFULLY" %
                            opt.replace(config.OPT_DIR + '/', 'template :: '))
    except IOError as err:
        logger.log.error("%s - base file does not exist" % opt)


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
        logger.log.error("icons - base file does not exists")
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
        logger.log.error(str(e))
        logger.log.error('optional file ' + original, file=sys.stderr)


def split_active(hexc, is_dark_theme=True):
    brightness = util.get_hls_val(hexc, 'light')
    if is_dark_theme:
        return [util.reduce_brightness(hexc, brightness * 0.20),
                util.reduce_brightness(hexc, brightness * 0.45)]
    else:
        return [util.add_brightness(hexc, brightness * 0.30), hexc]


def prepare_colors(image_name):
    image = pywal.image.get(join(config.WALL_DIR, image_name))
    cdic = pywal.colors.get(image, config.WALL_DIR)

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
    logger.log.info("done")
