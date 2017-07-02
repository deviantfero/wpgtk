
# wpgtk

A universal theming software for all themes 
defined in text files, compatible with all terminals, 
with default themes for GTK2, GTK+, openbox and Tint2, that uses 
[wal](https://github.com/dylanaraps/wal) as it's core, in which 
you can choose to interact with in two possible ways, so you can
enjoy the powerful `wal` while having an easy to use GUI AND a powerful cli tool.

#### [GUI](http://i.imgur.com/oJ0yakG.gif)

#### [Powerful command line interface](http://i.imgur.com/MM5yVZq.gif)

#### [Combine wallpapers and colors](http://i.imgur.com/qo5Hsoh.gif)


## Getting Started

### Dependencies

this dependencies are included in the install scripts for apt distros and arch

* feh
* python-gobject
* python-imaging
* Pillow (python)
* xsltproc
* wal
* urxvt or xterm for it to work on your terminal colors without the need of optional configs


# Installing

**_Warning:_** If you have a previous version of wpgtk installed
please delete the contents of your current `~/.wallpapers` as 
they may conflict with the new folder structure.

You can either clone this repository by doing

```sh
$ git clone https://github.com/deviantfero/wpgtk
```

or install the `wpgtk-git` package via the AUR.

If you cloned the repository  and have either Arch linux or a debian based
distribution directly you can run the `install.sh` script inside the 
cloned repository.

```
$ ./install.sh
```

And if everything went fine you can now execute `wpg` and it will take
you to the user interface.

You can set the default themes that the application installs if you want
to use color adaptable themes out of the box, these are installed under 
`~/.themes/`, `FlatColor` for gtk and GTK+, `colorbamboo` and `colorbamboo-nb` for openbox.

for more details on the cli interface do:
```
$ wpg -h
```

# Theming

### General Usage
In order to start creating colorschemes and themes in `wpgtk` you need
to add wallpapers, there's two ways you can do this:

### Console
```
$ wpg -a /path/to/image
```

### GUI
![add](http://i.imgur.com/0y4qHJx.png)

this is a list of useful wpg commands that you will be using if you want to use
the cli:
```
$ wpg -l #lists the currently added wallpapers
$ wpg -c #prints the current wallpaper
$ wpg -t #apply colorscheme to terminal (equivalent to wal -r)
$ wpg -z wallpaper #shuffles the given wallpaper's colorscheme
$ wpg --auto wallpaper #generates fg versions of the first 8 colors of the given wallpaper
$ wpg -d wallpaper #remove an existing wallpaper
$ wpg -h #display usage
$ wpg -s wallpaper1 [wallpaper2] #sets the current wallpaper and colorscheme, wallpaper2 is optional
```

Files exported when creating a theme are all under the same directory `$HOME/.wallpapers`
this directory contains all exported formats that `wall` and `wpgtk` have to offer, such
as:

* scss variables under `$HOME/.wallpapers/cache/scss`
* simple hexes under `$HOME/.wallpapers/cache/wallpaper_name.col`
* xres files under `$HOME/.wallpapers/xres/wallpaper_name.Xres`
* environment variables under `$HOME/.colors` 

### Optional files

Using the GUI you can add optional files for which `wpgtk` will create a copy and
add a modifiable file to the `~/.themes/color_other` under the file extension `.base`
in which some keywords will be replaced with the respective colors matching 
those keywords, these keywords are:

```assembly
from color 0 to color 9
#COLORY
where Y is the number of color

from color 10 to 15
#COLORXYY 
where Y is the number of color desired

also
#COLORIN (active color)
#COLORACT (inactive color)
```

after doing this `wpgtk` will replace this new file with the original.

# Loading at Startup
to load your new wallpaper at startup along with the colors add the following to your startup script or simply add it into your startup apps in your DE of choice, if you already use feh as your wallpaper manager, remember to remove it from your start up config.

```sh
bash ~/.wallpapers/wp_init.sh
```

# License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
