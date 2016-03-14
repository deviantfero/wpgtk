# wpg
### An accesible and easy to install colorscheme and theme generator for Openbox, tint2 and GTK.

See What it can do!

http://s1.webmshare.com/99Kna.webm

wpg is a GUI for a little program called wp ( original source below ) to manage your wallpapers in a simple way, it integrates a script wich takes the colors in the image of your preference and sets up an .Xresources file to match your term colors with your wallpaper

* it can take a little while to generate the color pallete though, be warned

### Now avialable in AUR

```sh
yaourt -S wpgtk-git
```

### Installation 
if you are in ubuntu, debian or Arch linux, the installer will take care of dependencies on it's own.

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

### Dependencies

wpg has some dependencies:

* python2-pillow ( on arch )
* feh
* python-gobject
* you need to use urxvt or xterm for it to work on your terminal colors

Arch
```sh
$ sudo pacman -S python2-pillow feh python-gobject gtk3 libxslt
```
*buntu
```sh
$ sudo apt-get install feh python3-gi python-gobject python-pip python-imaging xsltproc && pip install Pillow
```
although you may already have most of these installed by default, i put them on here just in case.

if you need a pair of colors predefined, just specify them on your .Xresources
i.e background and foreground

If you want the background color that wp gives you, on your terminal set your bg color to 0
or don't specify any at all on .Xresources

also you need to uninstall any other wallpaper manager as it will override this one at startup

### Credit
I found the script by other means, but i found out the author of the color script that i made
the GUI for, i'll leave the link to the original repo down below 

it's http://github.com/everett1992/wp

### Loading at Startup
to load your new wallpaper at startup along with the colors add the following to your startup script or simply add it into your startup apps in your DE of choice, if you already use feh as your wallpaper manager, remember to remove it from your start up config.

```sh
~/.wallpapers/wp_init.sh
```

### Version
2.0

### Features added

* Now your window borders change with your wallpaper
* Now your Icon set changes with your wallpaper
* It also changes a special GKT theme automatically
* it uses random colors from the image, so you can repeat until you're satisfied
* It comes with special themes solely for this task of being dynamic, so no need for any complicated configuration
* you can modify the themes to a certain degree. So feel free to do it!

### Examples
![Dynamic themes](http://i.imgur.com/MGPtHXs.png)
![Dynamic bar](http://i.imgur.com/1d8ragK.png)
![Dynamic theme2](http://i.imgur.com/wzBV8nV.png)
![Dynamic bar2](http://i.imgur.com/ucBAOXT.png)

### New features images

![IMG 1](http://i.imgur.com/xXIB7QH.png)
![IMG 1](http://i.imgur.com/fpbmtPi.png)

You can now choose a colorscheme generated for a wallpaper in whichever wallpaper you'd like!

And it will affect your windows, bar and GTK theme too!

