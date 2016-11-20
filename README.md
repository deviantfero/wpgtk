# wpg
### An accesible and easy to install colorscheme and theme generator for Openbox, tint2 and GTK2/3.

#### it's also compatible with most software that uses written configs, such as i3, bspwm, termite, etc.

#### Video

[Video DEMO](https://my.mixtape.moe/dpetjt.webm)

![Dynamic themes](http://i.imgur.com/VNC7O57.png)
![Borderless](http://i.imgur.com/LXZKLRY.png)

wpg is a GUI for a program called wp, to manage your wallpapers in a simple way, it integrates a script wich takes the colors in the image of your preference and sets up an .Xresources file to match your term colors with your wallpaper, you can also modify those generated colorschemes color by color to your content.

**_it can take a little while to generate the color pallet._**

----

### in AUR

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
* If you specify a color in your .Xresources, it will not be overriden by wpgtk
* If you need a pair of colors predefined, just specify them on your .Xresources
* you can now modify the colorschemes you are provided color by color.



### Optional config files ( support for other wm, and pretty much everything )

----

_**example**_
just use the Optional Files tab in wpg, click on add and select the desired configuration file, wpg will automatically backup your current config, and will create a .base file for you which you can edit via the "edit" button in this tab.

this is how it looks when you add an extra config file

![WINDOW](http://i.imgur.com/TZbfCpV.png)
![RESULT](http://i.imgur.com/cT7OYwM.png)

![Take a look](http://s1.webmshare.com/NdM8M.webm)

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

###### Dependencies

wpg has some dependencies:

* python2-pillow ( on arch )
* feh
* python-gobject
* you need to use urxvt or xterm for it to work on your terminal colors without the need of optional configs

#### Ubuntu or Debian
```sh
$ sudo apt-get install feh python3-gi python-gobject python-pip python-imaging xsltproc && pip install Pillow
```

```sh
$ git clone http://github.com/deviantfero/wpgtk
$ cd ~/wpgtk
$ sh ./installcolor.sh
```
#### Arch

```sh
$ sudo pacman -S python2-pillow feh python-gobject gtk3 libxslt
```
Alternatively, there is also an AUR package (For arch users wpgtk-git,) which will handle the install and dependencies for you.

after doing this there just a few more steps to get a dynamic theme going
* Select colorbamboo or colorbamboo_nb (no_borders) as your openbox window theme
* Select Flatcolor as your GTK theme
* Select flattrcolor as your Icon theme

**_you need to uninstall any other wallpaper manager as it will override this one at startup._**

now to actually run the program just
```sh
$ wpg
```

#### Loading at Startup
to load your new wallpaper at startup along with the colors add the following to your startup script or simply add it into your startup apps in your DE of choice, if you already use feh as your wallpaper manager, remember to remove it from your start up config.

```sh
bash ~/.wallpapers/wp_init.sh
```
---

### Credit
I found the script by other means, but i found out the author of the color script that i made
the GUI for, i'll leave the link to the original repo down below 

it's http://github.com/everett1992/wp

