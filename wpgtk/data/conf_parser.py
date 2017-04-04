from getpass import getuser
import re
import sys

HOME = "/home/" + getuser()
CONFDIR = HOME + "/.wallpapers/"
DEFAULT = {
    'ACT': 0,
    'TN2': True,
    'GTK': True,
    'INV': False
}


def parse_conf( filename=CONFDIR+'wpg.conf' ):
    test = re.compile("^#")
    tmp = DEFAULT

    try:
        f = open( filename, 'r' )
    except IOError as err:
        print( err )
        print( err.args )
        print( err.filename )
        print( 'ERR:: Default Config Loaded', sys.stderr )
        write_conf()
        return DEFAULT
    opt_list = [ line.replace('\n', '').replace(' ', '') for line in f if not test.match(line) ]

    try:
        for el in opt_list:
            el = el.split( '=' )
            if el[0] == 'active_color':
                if int(el[1]) > 0 and int(el[1]) < 16:
                    tmp['ACT'] = int(el[1])
                else:
                    tmp['ACT'] = 0
            elif el[0] == 'tint2_colorize':
                tmp['TN2'] = not el[1].lower() == 'false'
            elif el[0] == 'gtk_colorize':
                tmp['GTK'] = not el[1].lower() == 'false'
            elif el[0] == 'clear_theme':
                tmp['INV'] = not el[1].lower() == 'false'
    except Exception as e:
        print( 'ERR:: ' + str(e), file=sys.stderr )
        print( 'ERR:: ' + filename + ' Corrupt loading default', file=sys.stderr )
        return DEFAULT

    f.close()
    return tmp

def write_conf( filename=CONFDIR+'wpg.conf', opt=DEFAULT ):
    opt = { y: str(opt[y]) + '\n' for y in opt }
    try:
        f = open( filename, 'w' )
        f.write( 'active_color = ' + opt['ACT'] )
        f.write( 'tint2_colorize = ' + opt['TN2'] )
        f.write( 'gtk_colorize = ' + opt['GTK'] )
        print( 'CFG:: Config written to ' + CONFDIR + 'wpg.conf')
        f.close()
    except IOError as err:
        print( err, file=sys.stderr )
        print( err.args, file=sys.stderr )
        print( err.filename, file=sys.stderr )
