#!/usr/bin/env python3
import fileinput
import sys
import shutil
from subprocess import call
from os import walk
from sys import argv
from colorsys import rgb_to_hls
from colorsys import hls_to_rgb
from getpass import getuser
from random import randint
from os.path import isfile, isdir

HOME = "/home/" + getuser()
WALLDIR = HOME + "/.wallpapers/"

r_active = "COLORACT"
r_inactive = "COLORIN"
r_bg = "COLORBG"
r_base = "COLORBASE"
r_tool = "COLORTOOL"

r_words = {"active":     "COLORACT",
           "inactive":   "COLORIN",
           "background": "COLORBG",
           "base":       "COLORBASE",
           "tooltip":    "COLORTOOL" }


def read_colors( name ):
    col_file = "cache/" + name + ".col"
    try:
        f = open( WALLDIR + col_file, "r" )
    except IOError as err:
        print( "file could not open", file=sys.stderr )
        print( err.filename, file=sys.stderr )
        empty = []
        for x in range( 0, 16 ):
            empty.append( '000000' )
        return empty

    colors = [c[1:-1] for c in f]
    f.close()
    return colors

def read_color_in_line( cfile, line_get=0 ):
    color_list = read_colors(cfile)
    if line_get == 0 and line_get < 16:
        color = color_list[randint(1, 15)]
    else:
        color = color_list[int(line_get)]
    return color

def write_colors( name, color_list ):
    col_file = "cache/" + name + ".col"
    xres_file = "xres/" + name + ".Xres"
    try:
        f = open( WALLDIR + xres_file, "w" )
        fc = open( WALLDIR + col_file, "w" )
    except IOError as err:
        print( err, file=sys.stderr )
        print( err.args, file=sys.stderr )
        print( err.filename, file=sys.stderr )
    if( isfile( WALLDIR + xres_file ) and isfile( WALLDIR + col_file) ):
        for i, c in enumerate(color_list):
            f.write( "*color" + str(i) + ": #" + c + "\n" )
            fc.write( '#' + c + '\n' )

        # Write terminal config
        for term in ["URxvt", "XTerm"]:
            f.write(term + "*foreground: #" + color_list[15] + "\n")
            f.write(term + "*background: #" + color_list[0] + "\n")

        f.write("URxvt*cursorColor: #" + color_list[15] + "\n")
        f.write("XTerm*cursorColor: #" + color_list[0] + "\n")

        # Write emacs config
        f.write("emacs*background: #{}\n".format(color_list[0]))
        f.write("emacs*foreground: #{}\n".format(color_list[15]))

        # Write rofi config
        f.write("rofi.color-window: argb:FF{0[0]}, #{0[0]}, #{0[10]}\n".format(color_list))
        f.write("rofi.color-normal: argb:FF{0[0]}, #{0[15]}, #{0[0]}, #{0[10]}, #{0[0]}\n".format(color_list))
        f.write("rofi.color-active: argb:FF{0[0]}, #{0[15]}, #{0[0]}, #{0[10]}, #{0[0]}\n".format(color_list))
        f.write("rofi.color-urgent: argb:FF{0[0]}, #{0[9]}, #{0[0]}, #{0[9]}, #{0[15]}\n".format(color_list))
    else:
        print( "ERR::NOT WRITING", file=sys.stderr )

    f.close()
    fc.close()

def replace_in_file( file_to_operate, target, newstring ):
    try:
        with fileinput.FileInput( file_to_operate, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( target, newstring ), end='' )
    except IOError:
        print(err.filename)

def replace_colors( file_to_operate, c_list ):
    for x, color in enumerate(c_list):
        if x < 10:
            replace_in_file( file_to_operate, "COLOR" + str(x), color )
        else:
            replace_in_file( file_to_operate,  "COLORX" + str(x), color )

def clean_icon_color( dirty_list ):
    dirty_list = dirty_list.pop()
    dirty_list = dirty_list.strip( "\n" )
    dirty_list = dirty_list.split( "=" )
    dirty_list = dirty_list.pop()
    return dirty_list

def get_darkness(hexv):
    rgb = list( int(hexv[i:i+2], 16) for i in ( 0, 2, 4 ) )
    hls = rgb_to_hls( rgb[0], rgb[1], rgb[2] )
    hls = list(hls)
    return hls[1]


def reduce_brightness( hex_string, reduce_lvl ):
    rgb = list( int(hex_string[i:i+2], 16) for i in ( 0, 2, 4 ) )
    hls = rgb_to_hls( rgb[0], rgb[1], rgb[2] )
    hls = list(hls)
    if( hls[1] - reduce_lvl > 0 ):
        hls[1] = hls[1] - reduce_lvl
        rgb = hls_to_rgb( hls[0], hls[1], hls[2] )
        rgb_int = []
        for elem in rgb:
            if( elem <= 0 ):
                elem = 5
            rgb_int.append( int(elem) )
        rgb_int = tuple( rgb_int )
        hex_result = '%02x%02x%02x' % rgb_int
        print(hex_result)
        return hex_result
    else:
        return reduce_brightness( hex_string, reduce_lvl - 5 )

def add_brightness( hex_string, reduce_lvl ):
    rgb = list( int(hex_string[i:i+2], 16) for i in ( 0, 2, 4 ) )
    hls = rgb_to_hls( rgb[0], rgb[1], rgb[2] )
    hls = list(hls)
    if( hls[1] + reduce_lvl < 250 ):
        hls[1] = hls[1] + reduce_lvl
        rgb = hls_to_rgb( hls[0], hls[1], hls[2] )
        rgb_int = []
        for elem in rgb:
            if( elem > 255 ):
                elem = 254
            rgb_int.append( int(elem) )
        rgb_int = tuple( rgb_int )
        hex_result = '%02x%02x%02x' % rgb_int
        return hex_result
    else:
        return add_brightness( hex_string, reduce_lvl - 5 )
    rgb = hls_to_rgb( hls[0], hls[1], hls[2] )
    rgb_int = []
    for elem in rgb:
        rgb_int.append( int(elem) )
    rgb_int = tuple( rgb_int )
    hex_result = '%02x%02x%02x' % rgb_int
    return hex_result

def change_colors_ob( active, inactive, cl ):
    if not shutil.which("openbox"):
        print( "ERR::NO OPENBOX INSTALL!", file=sys.stderr )
        return
    backupdir = HOME + "/.themes/colorbamboo/openbox-3/themerc.base"
    realdir = HOME + "/.themes/colorbamboo/openbox-3/themerc"
    button_color_hover = add_brightness( active, 70 )
    bgs = [ cl[0], reduce_brightness(cl[0], 2), add_brightness(cl[0],10) ]
    try:
        shutil.copy2(backupdir, realdir)
        replace_in_file( realdir, r_active, active )
        replace_in_file( realdir, r_inactive, inactive )
        replace_in_file( realdir, r_bg, bgs[0] )
        replace_in_file( realdir, r_base, bgs[1] )
        replace_in_file( realdir, r_tool, bgs[2] )
        replace_in_file( realdir, "REPLAC", button_color_hover )
        replace_in_file( realdir, "REPLAD", inactive )
        backupdir = HOME + "/.themes/colorbamboo_nb/openbox-3/themerc.base"
        realdir = HOME + "/.themes/colorbamboo_nb/openbox-3/themerc"
        shutil.copy2(backupdir, realdir)
        replace_in_file( realdir, r_inactive, inactive )
        replace_in_file( realdir, r_active, active )
        print( "OK::OPENBOX" )
        call( ["openbox", "--reconfigure"] )
    except IOError:
        print( "ERR::OPENBOX - BASE FILE DOES NOT EXIST", file=sys.stderr )


def change_colors_icons( active, inactive, glyph ):
    backupdir = HOME + "/.icons/flattrcolor/scripts/replace_folder_file.sh.base"
    realdir = HOME + "/.icons/flattrcolor/scripts/replace_folder_file.sh"
    xsl_file = HOME + "/.icons/flattrcolor/scripts/change_folder_colors.xslt"
    executable = HOME + "/.icons/flattrcolor/scripts/replace_script.sh"
    try:
        file_current_glyph = open( realdir, "r" )
        current_glyph = []
        current_front = []
        current_back = []
        for line in file_current_glyph:
            if( "New" in line and "glyph" in line ):
                current_glyph.append( line )
                break
        for line in file_current_glyph:
            if( "New" in line and "front" in line ):
                current_front.append( line )
                break
        for line in file_current_glyph:
            if( "New" in line and "back" in line ):
                current_back.append( line )
                break
        shutil.copy2(backupdir, realdir)
        current_glyph = clean_icon_color( current_glyph )
        current_front = clean_icon_color( current_front )
        current_back = clean_icon_color( current_back )
        file_current_glyph.close()

        replace_in_file( realdir, "l=178984", "l=" + current_glyph )
        replace_in_file( realdir, "w=178984", "w=" + glyph )
        replace_in_file( realdir, "l=36d7b7", "l=" + current_front )
        replace_in_file( realdir, "w=36d7b7", "w=" + active )
        replace_in_file( realdir, "l=1ba39c", "l=" + current_back )
        replace_in_file( realdir, "w=1ba39c", "w=" + inactive )
        call( executable, shell=True )
        print( "OK::ICONS" )
        print( "INF::CURRENT GLYPH: " + current_glyph )
    except IOError:
        print( "ERR::ICONS - BASE FILES DO NOT EXIST", file=sys.stderr )

def change_colors_tint2( active, inactive, c_list, colorize=True ):
    if not shutil.which("tint2"):
        print( "ERR::TINT2 - NOT INSTALLED", file=sys.stderr )
        return
    if colorize:
        backupdir = HOME + "/.config/tint2/tint2rc.base"
    else:
        backupdir = HOME + "/.config/tint2/tint2rcnocolor.base"
    realdir = HOME + "/.config/tint2/tint2rc"
    try:
        shutil.copy2(backupdir, realdir)
        replace_in_file( realdir, r_words["inactive"], inactive )
        replace_in_file( realdir, r_words["active"], active )
        if colorize:
            replace_colors( realdir, c_list )
        call( [ "killall", "-SIGUSR1", "tint2" ] )
        print( "OK::TINT2" )
    except IOError:
        print( "ERR::TINT2 - BASE FILE DOES NOT EXIST", file=sys.stderr )

def change_colors_gtk2( active, inactive, cl, colorize=True ):
    if colorize:
        backupdir = HOME + "/.themes/FlatColor/gtk-2.0/gtkrc.base"
    else:
        backupdir = HOME + "/.themes/FlatColor/gtk-2.0/gtkrcnocolor.base"
    realdir = HOME + "/.themes/FlatColor/gtk-2.0/gtkrc"
    bgs = [ cl[0], reduce_brightness(cl[0], 5), add_brightness(cl[0],10) ]
    try:
        shutil.copy2(backupdir, realdir)
        replace_in_file( realdir, r_active, active )
        if colorize:
            replace_in_file( realdir, r_bg, bgs[0] )
            replace_in_file( realdir, r_base, bgs[1] )
            replace_in_file( realdir, r_tool, bgs[2] )
        print( "OK::GTK2" )
    except IOError:
        print( "ERR::GTK2 - BASE FILE DOES NOT EXIST", file=sys.stderr )

def change_colors_gtk3( active, inactive, cl, colorize=True ): #cl is a color list
    backupdir = HOME + "/.themes/FlatColor/gtk-3.0/gtk.css.base"
    realdir = HOME + "/.themes/FlatColor/gtk-3.0/gtk.css"
    bgs = [ cl[0], reduce_brightness(cl[0], 2), add_brightness(cl[0],10) ]
    if( isfile( backupdir ) ):
        shutil.copy2(backupdir, realdir)
        replace_in_file( realdir, r_active, active )
        if colorize:
            replace_in_file( realdir, r_bg, bgs[0] )
            replace_in_file( realdir, r_base, bgs[1] )
            replace_in_file( realdir, r_tool, bgs[2] )
        print( "OK::GTK3" )
    else:
        print( "ERR::GTK3 - BASE FILE DOES NOT EXIST", file=sys.stderr )
    if colorize:
        backupdir = HOME + "/.themes/FlatColor/gtk-3.20/gtk.css.base"
    else:
        backupdir = HOME + "/.themes/FlatColor/gtk-3.20/gtknocolor.css.base"
    realdir = HOME + "/.themes/FlatColor/gtk-3.20/gtk.css"
    if( isfile( backupdir ) ):
        shutil.copy2(backupdir, realdir)
        replace_in_file( realdir, r_active, active )
        replace_in_file( realdir, r_bg, bgs[0] )
        replace_in_file( realdir, r_base, bgs[1] )
        replace_in_file( realdir, r_tool, bgs[2] )
        print( "OK::GTK3.20" )
    else:
        print( "ERR::GTK3.20 - BASE FILE DOES NOT EXIST", file=sys.stderr )

def change_other_files( active, inactive, c_list ):
    other_path = HOME + "/.themes/color_other/"
    files = []
    for( dirpath, dirnames, filenames ) in walk( other_path ):
        files.extend( filenames )
    if( files ):
        try:
            for word in files:
                if ".base" in word:
                    original = word.split( ".base", len(word) ).pop(0)
                    shutil.copy2(other_path + word, other_path + original)
                    replace_in_file( other_path + original, r_active, active )
                    replace_in_file( other_path + original, r_inactive, inactive )
                    for x in range( 0, 16 ):
                        if x < 10:
                            replace_in_file( other_path + original, "COLOR" + str(x), c_list[x] )
                        else:
                            replace_in_file( other_path + original,  "COLORX" + str(x), c_list[x] )
                    print( "OK::OPTIONAL FILES - " + original )
        except Exception as e:
            print( 'ERR:: ' + str(e), file=sys.stderr )
            print( 'ERR::OPTIONAL FILE -' + original, file=sys.stderr )
    else:
        print( "INF::NO OPTIONAL FILES DETECTED" )

def define_redux( hexvalue ):
    base_brightness = get_darkness(hexvalue)
    if( hexvalue == "4A838F" ):
        return [0, 50]
    elif base_brightness >= 190:
        return [60, 115]
    elif base_brightness >= 160:
        return [50, 105]
    elif base_brightness <= 10:
        return [-35, -15]
    elif base_brightness <= 60:
        return [-20, -5]
    elif base_brightness <= 70:
        return [0, 15]
    elif base_brightness <= 80:
        return [5, 20]
    elif base_brightness <= 125:
        return [20, 55]
    else:
        return [30, 75]

def execute_gcolorchange( image_name, opt ):
    #--Getting random color from an .Xres file--#
    image_colors = read_colors( image_name )
    base_color = read_color_in_line( image_name, opt['ACT'] )
    base_brightness = get_darkness( base_color )
    #--Defining how dark the windows have to be--#
    redux_list = define_redux( base_color )
    base_redux = redux_list[0]
    inact_redux = redux_list[1]
    active = reduce_brightness( base_color, base_redux )
    inactive = reduce_brightness( base_color, inact_redux )
    glyph = reduce_brightness( inactive, 15 )
    print( "INF::FG: " + active )
    print( "INF::BG: " + inactive )
    bg_fg_file = open( HOME + "/.main_colors", "w" )
    bg_fg_file.write( "FG:" + active + "\n" )
    bg_fg_file.write( "BG:" + inactive + "\n" )
    change_colors_ob( active, inactive, image_colors )
    change_colors_tint2( active, inactive, image_colors, opt['TN2'] )
    change_colors_gtk2( active, inactive, image_colors, opt['GTK'] )
    change_colors_gtk3( active, inactive, image_colors, opt['GTK'] )
    change_colors_icons( active, inactive, glyph )
    change_other_files( active, inactive, image_colors )
    print( "OK::FINISHED" )

if __name__ == "__main__":
    image_name = argv[1]
    execute_gcolorchange( image_name )
