#!/usr/bin/env python3
import fileinput
from subprocess import call
from os import walk
from sys import argv
from colorsys import rgb_to_hls
from colorsys import hls_to_rgb
from getpass import getuser
from random import randint
from os.path import isfile

homedir = "/home/" + getuser()
walldir = homedir + "/.wallpapers/"

replace_active = "COLORACT"
replace_inactive = "COLORIN"

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
    f.close()
    return color

def read_colors( xres_file ):
    xres_file = "." + xres_file + ".Xres"
    try:
        f = open( walldir + xres_file, "r" )
    except IOError as err:
        print( err )
        print( err.args )
        print( err.filename )
        empty = []
        for x in range( 0, 16 ):
            empty.append( '000000' )
        return empty
    xres_list = [ line for line in f ]
    xres_list = list( map(lambda x: x.split("#", len(x)), xres_list ) )
    xres_list = [ word[1].strip( "\n" ) for word in xres_list ]
    f.close()
    return xres_list

def write_colors( xres_file, color_list ):
    col_file = "." + xres_file + ".colors"
    xres_file = "." + xres_file + ".Xres"
    try:
        f = open( walldir + xres_file, "w" )
        fc = open( walldir + col_file, "w" )
        temp = open( walldir + ".tmp.colors", "w" )
    except IOError as err:
        print( err )
        print( err.args )
        print( err.filename )
    if( isfile( walldir + xres_file ) and isfile( walldir + col_file) ):
        for i, c in enumerate(color_list):
            f.write( "*color" + str(i) + ": #" + c + "\n" )
            fc.write( "export COLOR" + str(i) + '="#' + c + '"\n' )
            temp.write( "#" + c + "\n" )
    else:
        print( "not writing" )
    f.close()
    fc.close()
    temp.close()

def write_tmp( color_list ):
    f = open( walldir + ".tmp.colors", "w" )
    for c in color_list:
        f.write( "#" + c + "\n" )
    f.close()

def replace_in_file( file_to_operate, target, newstring ):
    with fileinput.FileInput( file_to_operate, inplace=True, backup=False ) as file:
        for line in file:
            print( line.replace( target, newstring ), end='' )

def clean_icon_color( dirty_list ):
    dirty_list = dirty_list.pop()
    dirty_list = dirty_list.strip( "\n" )
    dirty_list = dirty_list.split( "=" )
    dirty_list = dirty_list.pop()
    return dirty_list

def darkness(hexv):
    rgb = list( int(hexv[i:i+2], 16) for i in ( 0, 2, 4 ) )
    hls = rgb_to_hls( rgb[0], rgb[1], rgb[2] )
    hls = list(hls)
    return hls[1]


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
    button_color_hover = add_brightness( active, 70 )
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        replace_in_file( realdir, replace_inactive, inactive )
        replace_in_file( realdir, replace_active, active )
        replace_in_file( realdir, "REPLAC", button_color_hover )
        replace_in_file( realdir, "REPLAD", inactive )
    backupdir = homedir + "/.themes/colorbamboo_nb/openbox-3/themerc.base"
    realdir = homedir + "/.themes/colorbamboo_nb/openbox-3/themerc"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        replace_in_file( realdir, replace_inactive, inactive )
        replace_in_file( realdir, replace_active, active )
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
        call( ["cp", backupdir, realdir] )
        current_glyph = clean_icon_color( current_glyph )
        current_front = clean_icon_color( current_front )
        current_back = clean_icon_color( current_back )
        print( current_front )
        file_current_glyph.close()

        replace_in_file( realdir, "l=178984", "l=" + current_glyph )
        replace_in_file( realdir, "w=178984", "w=" + glyph )
        replace_in_file( realdir, "l=36d7b7", "l=" + current_front )
        replace_in_file( realdir, "w=36d7b7", "w=" + active )
        replace_in_file( realdir, "l=1ba39c", "l=" + current_back )
        replace_in_file( realdir, "w=1ba39c", "w=" + inactive )
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
        replace_in_file( realdir, replace_inactive, inactive )
        replace_in_file( realdir, replace_active, active )
        call( [ "killall", "-SIGUSR1", "tint2" ] )
        print( "CHANGED::TINT2" )
    else:
        print( "FAILED TO CHANGE::TINT2 - BASE FILE DOES NOT EXIST" )

def change_colors_gtk2( active, inactive ):
    backupdir = homedir + "/.themes/FlatColor/gtk-2.0/gtkrc.base"
    realdir = homedir + "/.themes/FlatColor/gtk-2.0/gtkrc"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        replace_in_file( realdir, replace_active, active )
        print( "CHANGED::GTK2" )
    else:
        print( "FAILED TO CHANGE::GTK2 - BASE FILE DOES NOT EXIST" )

def change_colors_gtk3( active, inactive ):
    backupdir = homedir + "/.themes/FlatColor/gtk-3.0/gtk.css.base"
    realdir = homedir + "/.themes/FlatColor/gtk-3.0/gtk.css"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        replace_in_file( realdir, replace_active, active )
        print( "CHANGED::GTK3" )
    else:
        print( "FAILED TO CHANGE::GTK3 - BASE FILE DOES NOT EXIST" )
    backupdir = homedir + "/.themes/FlatColor/gtk-3.20/gtk.css.base"
    realdir = homedir + "/.themes/FlatColor/gtk-3.20/gtk.css"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        replace_in_file( realdir, replace_active, active )
        print( "CHANGED::GTK3.20" )
    else:
        print( "FAILED TO CHANGE::GTK3.20 - BASE FILE DOES NOT EXIST" )

def change_other_files( active, inactive ):
    other_path = "/home/" + getuser() + "/.themes/color_other/"
    files = []
    for( dirpath, dirnames, filenames ) in walk( other_path ):
        files.extend( filenames )
    if( files ):
        for word in files:
            if ".base" in word:
                original = word.split( ".base", len(word) ).pop(0)
                call([ "cp", other_path + word, other_path + original ])
                replace_in_file( other_path + original, replace_inactive, active )
                replace_in_file( other_path + original, replace_active, inactive )
                print( "CHANGED::OPTIONAL FILES - " + original )
    else:
        print( "NO OPTIONAL FILES DETECTED::NOT CHANGED" )

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
    elif base_brightness <= 10:
        redux_list.append(-35)
        redux_list.append(-15)
    elif base_brightness <= 60:
        redux_list.append(-20)
        redux_list.append(-5)
    elif base_brightness <= 70:
        redux_list.append(0)
        redux_list.append(15)
    elif base_brightness <= 80:
        redux_list.append(5)
        redux_list.append(20)
    elif base_brightness <= 125:
        redux_list.append(20)
        redux_list.append(55)
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
    fg_icon = active
    bg_icon = inactive
    glyph = reduce_brightness( inactive, 15 )
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
    change_other_files( active, inactive )
    print( "SUCCESS" )

if __name__ == "__main__":
    image_name = argv[1]
    execute_gcolorchange( image_name )
