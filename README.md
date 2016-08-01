# wpg
### An accesible and easy to install colorscheme and theme generator for Openbox, tint2 and GTK.

See What it can do!

http://webmshare.com/play/zMm1z
![Dynamic themes](http://i.imgur.com/hLsd4jt.png)
![Borderless](http://i.imgur.com/G2oTjMQ.png)

wpg is a GUI for a program called wp, to manage your wallpapers in a simple way, it integrates a script wich takes the colors in the image of your preference and sets up an .Xresources file to match your term colors with your wallpaper, you can also modify those generated colorschemes color by color to your content.

**_it can take a little while to generate the color pallet._**

----

### Now avialable in AUR

```sh
wpgtk-git
```
---

### Version
3.0

###### Features added

* Special Openbox theme so that window borders change with your wallpaper
* Special Icon set included that changes with your wallpaper
* It also changes a special GTK theme automatically
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

* you can now modify the colorschemes you are provided color by color, no more same color in 2 spaces, now you are in control



### Optional config files ( support for other wm, and pretty much everything )

----

_**example**_
just use the Optional Files tab in wpg, click on add and select the desired configuration file, wpg will automatically backup your current config, and will create a .base file for you which you can edit via the "edit" button in this tab.

this is how it looks when you add an extra config file

![WINDOW](http://i.imgur.com/Z49jP62.png)
![RESULT](http://i.imgur.com/o18TSr9.png)

now your config is a symbolic link to the copy that is in the ~/.themes/colors_other directory, which gets modified each time you change your colorscheme according to a .base file matching the config's name.

this would be .base file of your wm config after you edit it of course
```
-- example 
#COLOR0
#COLOR1
#COLORX10 it has the X so it doesn't conflict with COLOR1 when replacing, this is true from color 10 to 15
#COLORIN (active color)
#COLORACT (inactive color)
```

so, this is the base file...

![INPUT](http://i.imgur.com/ZyxsoKi.png)

this would be the output config that's already linked in your config's original folder, so it's all done on the fly.

![OUTPUT](http://i.imgur.com/lFkuQ8X.png)

---

### Installation 
if you are in Ubuntu, Debian or Arch linux, the installer will take care of dependencies on it's own.

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

