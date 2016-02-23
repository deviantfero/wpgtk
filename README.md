# wpg

wpg is a GUI for a little program called wp ( original source below ) to manage your wallpapers in a simple way, it integrates a script wich takes the colors in the image of your preference and sets up an .Xresources file to match your term colors with your wallpaper

it can take a little while to generate the color pallete though, be warned

### Examples

![Example Image](http://i.imgur.com/LktnkQh.png)
![Another Example](http://i.imgur.com/pBwTumC.png)

### New Feature
![IMG 2](http://i.imgur.com/uy3ZNuL.png)
![IMG 1](http://i.imgur.com/r39E6Fl.png)

You can now choose a colorscheme generated for a wallpaper in whichever wallpaper you'd like!


### Version
2.0

### Features added

* Now your window borders change with your wallpaper
* Now your Icon set changes with your wallpaper
* It also changes a special GKT theme automatically
* it uses random colors from the image, so you can repeat until you're satisfied

### Dependencies

wpg has some dependencies:

* python2-pillow ( on arch )
* feh
* python-gobject
* you need to use urxvt or xterm for it to work on your terminal colors

Arch
```sh
$ sudo pacman -S python2-pillow feh python-gobject
```
*buntu
```sh
$ sudo apt-get install feh python-pip build-dep python-imaging libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev && pip install Pillow
```
although you may already have most of these installed by default, i put them on here just in case.

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
$ sh ./installcolor.sh
```
do this if you want a dynamic theme.

after doing this there just a few more steps to get a dynamic theme going
* Select colorbamboo or colorbamboo_nb (no_borders) as your openbox window theme
* Select Flatcolor as your GTK theme
* Select flattrcolor as your Icon theme
* you're good to go!

```sh
$ git clone http://github.com/deviantfero/wpgtk
$ cd ~/wpgtk
$ sh ./install.sh
```
do this is if you don't want a dynamic theme.

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
