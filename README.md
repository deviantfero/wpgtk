# wpg
### An accesible and easy to install colorscheme and theme generator for Openbox, tint2 and GTK.

See What it can do!

#### ![Watch a video demonstration, Click here!](http://s1.webmshare.com/99Kna.webm)
![Dynamic themes](http://i.imgur.com/MGPtHXs.png)

wpg is a GUI for a little program called wp ( original source below ) to manage your wallpapers in a simple way, it integrates a script wich takes the colors in the image of your preference and sets up an .Xresources file to match your term colors with your wallpaper

**_it can take a little while to generate the color pallet._**

----

### Now avialable in AUR

```sh
yaourt -S wpgtk-git
```
---

### Version
2.2

###### Features added

* Now your window borders change with your wallpaper
* Now your Icon set changes with your wallpaper
* It also changes a special GKT theme automatically
* It uses random colors from the image, so you can repeat until you're satisfied
* It comes with special themes solely for the purpose of being dynamic, so no need for any complicated configuration
* you can modify the themes to a certain degree. So feel free to do it!
* It saves all colors of the current wallpapers in two files, one named ".colors" and another named ".main_colors" the latter contains the colors used by window borders at that time.
* If you specify a color in your .Xresources it will not be overriden by wpgtk
* You can now choose a colorscheme generated for a wallpaper in whichever wallpaper you'd like.
* If you need a pair of colors predefined, just specify them on your .Xresources
* If you want the background color that wp gives you, on your terminal set your bg color to 0 like this

```sh
URxvt*background: 0
```

---

### Installation 
if you are in ubuntu, debian or Arch linux, the installer will take care of dependencies on it's own.

do the following
```sh
$ git clone http://github.com/deviantfero/wpgtk
$ cd ~/wpgtk
$ sh ./installcolor.sh
```

after doing this there just a few more steps to get a dynamic theme going
* Select colorbamboo or colorbamboo_nb (no_borders) as your openbox window theme
* Select Flatcolor as your GTK theme
* Select flattrcolor as your Icon theme
* you're good to go!

**_you need to uninstall any other wallpaper manager as it will override this one at startup._**

now to actually run the program just
```sh
$ wpg
```

##### Loading at Startup
to load your new wallpaper at startup along with the colors add the following to your startup script or simply add it into your startup apps in your DE of choice, if you already use feh as your wallpaper manager, remember to remove it from your start up config.

```sh
bash ~/.wallpapers/wp_init.sh
```

###### Dependencies

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
---

### Credit
I found the script by other means, but i found out the author of the color script that i made
the GUI for, i'll leave the link to the original repo down below 

it's http://github.com/everett1992/wp

### Examples
![Dynamic bar](http://i.imgur.com/1d8ragK.png)
![Dynamic theme2](http://i.imgur.com/wzBV8nV.png)
![Dynamic bar2](http://i.imgur.com/ucBAOXT.png)
![IMG 1](http://i.imgur.com/xXIB7QH.png)
![IMG 1](http://i.imgur.com/fpbmtPi.png)

