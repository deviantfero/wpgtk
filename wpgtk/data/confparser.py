from getpass import getuser
import re

HOME = "/home/" + getuser()
WALLDIR = HOME + "/.wallpapers/"
ACT = 0
TN2 = 1
GTK = 2
DEFAULT = [0, True, True]


def parse_conf( filename=WALLDIR+'wpg.conf' ):
    test = re.compile("^#")
    tmp = DEFAULT

    try:
        f = open( filename, 'r' )
    except IOError as err:
        print( err )
        print( err.args )
        print( err.filename )
        print( 'ERR:: Default Config Loaded' )
        return DEFAULT
    opt_list = [ line.replace('\n', '').replace(' ', '') for line in f if not test.match(line) ]

    try:
        for el in opt_list:
            el = el.split( '=' )
            if el[0] == 'active_color':
                if int(el[1]) > 0 and int(el[1]) < 16:
                    tmp[ACT] = int(el[1])
                else:
                    tmp[ACT] = 0
            elif el[0] == 'tint2_colorize':
                if el[1].lower() == 'false':
                    tmp[TN2] = False
                else:
                    tmp[TN2] = True
            elif el[0] == 'gtk_colorize':
                if el[1].lower() == 'false':
                    tmp[GTK] = False
                else:
                    tmp[GTK] = True
        if len(tmp) == 3:
            opt_list = tmp
        else:
            opt_list = DEFAULT
            print( 'ERR:: ' + filename + ' Corrupt loading default' )
    except Exception as e:
        print( 'ERR:: ' + str(e) )
        return DEFAULT

    f.close()
    return opt_list

def write_conf( filename=WALLDIR+'wpg.conf', opt=DEFAULT ):
    try:
        f = open( filename, 'w' )
        f.write( 'active_color = ' + str(opt[ACT]) )
        f.write( 'tint2_colorize = ' + opt[TN2] )
        f.write( 'gtk_colorize = ' + opt[GTK] )
        f.close()
    except IOError as err:
        print( err )
        print( err.args )
        print( err.filename )
