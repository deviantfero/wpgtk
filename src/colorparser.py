#!/usr/bin/env python3
import fileinput
from subprocess import call
from sys import argv
from colorsys import rgb_to_hls
from colorsys import hls_to_rgb
from getpass import getuser
from random import randint
from os.path import isfile

homedir = "/home/" + getuser()
walldir = homedir + "/.wallpapers/"

replacebg = "4A838F"
replacefg = "2C4448"

def replace_in_file( file_to_operate, target, newstring ):
    with fileinput.FileInput( file_to_operate, inplace=True, backup=False ) as file:
        for line in file:
            print( line.replace( target, newstring ), end='' )

def darkness(hexv):
    rgb = list( int(hexv[i:i+2], 16) for i in ( 0, 2, 4 ) )
    hls = rgb_to_hls( rgb[0], rgb[1], rgb[2] )
    hls = list(hls)
    return hls[1]

def read_color_in_line( xres_file ):
    xres_file = "." + xres_file + ".Xres"
    try:
        f = open( walldir + xres_file, "r" )
    except IOError as err:
        print( err )
        print( err.args )
        print( err.filename )
        return "4A838F"
    line_get = randint( 1, 15 )
    xres_list = [ line for line in f ]
    color = xres_list[ line_get ]
    color = color.split( " ", len( color ) )
    color = color[1]
    color = color.strip( '#' )
    color = color.strip( '\n' )
    return color

def reduce_brightness( hex_string, reduce_lvl ):
    rgb = list( int(hex_string[i:i+2], 16) for i in ( 0, 2, 4 ) )
    hls = rgb_to_hls( rgb[0], rgb[1], rgb[2] )
    hls = list(hls)
    hls[1] = hls[1] - reduce_lvl
    rgb = hls_to_rgb( hls[0], hls[1], hls[2] )
    rgb_int = []
    for elem in rgb:
        rgb_int.append( int(elem) )
    rgb_int = tuple( rgb_int )
    hex_result = '%02x%02x%02x' % rgb_int
    return hex_result

def add_brightness( hex_string, reduce_lvl ):
    rgb = list( int(hex_string[i:i+2], 16) for i in ( 0, 2, 4 ) )
    hls = rgb_to_hls( rgb[0], rgb[1], rgb[2] )
    hls = list(hls)
    hls[1] = hls[1] + reduce_lvl
    rgb = hls_to_rgb( hls[0], hls[1], hls[2] )
    rgb_int = []
    for elem in rgb:
        rgb_int.append( int(elem) )
    rgb_int = tuple( rgb_int )
    hex_result = '%02x%02x%02x' % rgb_int
    return hex_result

def change_colors_ob( active, inactive ):
    backupdir = homedir + "/.themes/colorbamboo/openbox-3/themerc.base"
    realdir = homedir + "/.themes/colorbamboo/openbox-3/themerc"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        replace_in_file( realdir, replacebg, active )
        replace_in_file( realdir, replacefg, inactive )
    backupdir = homedir + "/.themes/colorbamboo_nb/openbox-3/themerc.base"
    realdir = homedir + "/.themes/colorbamboo_nb/openbox-3/themerc"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        replace_in_file( realdir, replacebg, active )
        replace_in_file( realdir, replacefg, inactive )
        print( "CHANGED::OPENBOX" )
    else:
        print( "FAILED TO CHANGE::OPENBOX - BASE FILE DOES NOT EXIST" )

    if( isfile(homedir + "/.config/openbox/menu.xml") ):
        call( ["openbox", "--reconfigure"] )
    else:
        print( "NO OPENBOX INSTALL!" )

def change_colors_icons( active, inactive, glyph ):
    backupdir = homedir + "/.icons/flattrcolor/scripts/replace_folder_file.sh.base"
    realdir = homedir + "/.icons/flattrcolor/scripts/replace_folder_file.sh"
    xsl_file = homedir + "/.icons/flattrcolor/scripts/change_folder_colors.xslt"
    executable = homedir + "/.icons/flattrcolor/scripts/replace_script.sh"
    if( isfile( backupdir ) ):
        file_current_glyph = open( realdir, "r" )
        current_glyph = []
        for line in file_current_glyph:
            if( "New" in line ):
                current_glyph.append( line )
                break
        current_glyph = current_glyph.pop()
        current_glyph = current_glyph.strip( "\n" )
        current_glyph = current_glyph.split( "=" )
        current_glyph = current_glyph.pop()
        file_current_glyph.close()

        call( ["cp", backupdir, realdir] )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "34495d", inactive ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "1abc9c", active ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "l=304050", "l=" + current_glyph ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "w=304050", "w=" + glyph ), end='' )
        call( executable, shell=True )
        print( "CHANGED::ICONS" )
        print( "CURRENT GLYPH: " + current_glyph )
    else:
        print( "FAILED TO CHANGE::ICONS - BASE FILES DO NOT EXIST" )

def change_colors_tint2( active, inactive ):
    backupdir = homedir + "/.config/tint2/tint2rc.base"
    realdir = homedir + "/.config/tint2/tint2rc"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        replace_in_file( realdir, replacebg.lower(), active )
        replace_in_file( realdir, replacefg.lower(), inactive )
        call( [ "killall", "-SIGUSR1", "tint2" ] )
        print( "CHANGED::TINT2" )
    else:
        print( "FAILED TO CHANGE::TINT2 - BASE FILE DOES NOT EXIST" )

def change_colors_gtk2( active, inactive ):
    backupdir = homedir + "/.themes/FlatColor/gtk-2.0/gtkrc.base"
    realdir = homedir + "/.themes/FlatColor/gtk-2.0/gtkrc"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        replace_in_file( realdir, replacebg, active )
        print( "CHANGED::GTK2" )
    else:
        print( "FAILED TO CHANGE::GTK2 - BASE FILE DOES NOT EXIST" )

def change_colors_gtk3( active, inactive ):
    backupdir = homedir + "/.themes/FlatColor/gtk-3.0/gtk.css.base"
    realdir = homedir + "/.themes/FlatColor/gtk-3.0/gtk.css"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        replace_in_file( realdir, replacebg.lower(), active )
        print( "CHANGED::GTK3" )
    else:
        print( "FAILED TO CHANGE::GTK3 - BASE FILE DOES NOT EXIST" )

def define_redux( hexvalue ):
    base_brightness = darkness(hexvalue)
    redux_list = []
    if( hexvalue == "4A838F" ):
        redux_list.append(0) 
        redux_list.append(50)
    elif base_brightness >= 190:
        redux_list.append( 60 )
        redux_list.append( 115 )
    elif base_brightness >= 160:
        redux_list.append(50)
        redux_list.append(105)
    elif base_brightness <= 125:
        redux_list.append(20)
        redux_list.append(55)
    elif base_brightness <= 100:
        redux_list.append(10)
        redux_list.append(15)
    else:
        redux_list.append(30)
        redux_list.append(75)
    return redux_list

def execute_gcolorchange( image_name ):
    #--Getting random color from an .Xres file--#
    base_color = read_color_in_line( image_name )
    base_brightness = darkness( base_color )
    #--Defining how dark the windows have to be--#
    redux_list = define_redux( base_color )
    base_redux = redux_list[0]
    inact_redux = redux_list[1]
    active = reduce_brightness( base_color, base_redux )
    inactive = reduce_brightness( base_color, inact_redux )
    fg_icon = base_color
    bg_icon = reduce_brightness( base_color, 40 )
    glyph = reduce_brightness( base_color, 70 )
    print( "BASE BRIGHTNESS: " + str( base_brightness ) )
    print( "FG: " + active )
    print( "BG: " + inactive )
    bg_fg_file = open( homedir + "/.main_colors", "w" )
    bg_fg_file.write( "FG:" + active + "\n" )
    bg_fg_file.write( "BG:" + inactive + "\n" )
    change_colors_ob( active, inactive )
    change_colors_tint2( active, inactive )
    change_colors_gtk2( active, inactive )
    change_colors_gtk3( active, inactive )
    change_colors_icons( fg_icon, bg_icon, glyph )
    print( "SUCCESS" )

if __name__ == "__main__":
    image_name = argv[1]
    execute_gcolorchange( image_name )
