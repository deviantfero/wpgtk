# wpg

wpg is a GUI for a little program called wp ( original source below ) to manage your wallpapers in a simple way, it integrates a script wich takes the colors in the image of your preference and sets up an .Xresources file to match your term colors with your wallpaper

it can take a little while to generate the color pallete though, be warned

### Examples

![Example Image](http://i.imgur.com/HXIm9v4.png?1)
![Another Example](http://i.imgur.com/1AdvJ8h.png?1)

### Version
1.0.2

### Dependencies

wpg has some dependencies:

* python2-pillow ( on arch )
* feh
* you need to use urxvt or xterm for it to work

Arch
```sh
$ sudo pacman -S python2-pillow feh
```
*buntu
```sh
$ sudo apt-get install feh pip && pip install Pillow
```

if you need a pair of colors predefined, just specify them on your .Xresources
i.e background and foreground

also you need to uninstall any other wallpaper manager as it will override this one at startup

### Credit
I found the script by other means, but i found out the author of the color script that i made
the GUI for, i'll leave the link to the original repo down below 

it's http://github.com/everett1992/wp

### Installation
do the following
```sh
$ git clone http://github.com/deviantfero/wpgtk
$ cd ~/wpgtk
$ sh ./install.sh
```
now to actually run the program just
```sh
$ wpg
```
this will take care of placing the files where they are meant to be in /usr/local/bin/
### Loading at Startup
to load your new wallpaper at startup along with the colors add the following to your startup script or simply add it into your startup apps in your DE of choice, if you already use feh as your wallpaper manager, remember to remove it from your start up config.
```sh
~/.wallpapers/wp_init.sh
```
