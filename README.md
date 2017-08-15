
# wpgtk

A universal theming software for all themes 
defined in text files, compatible with all terminals, 
with default themes for GTK2, GTK+, openbox and Tint2, that uses 
[pywal](https://github.com/dylanaraps/pywal) as it's core.

you can choose to interact with it in two ways, manage your themes 
from either a cli application or using a GUI.

#### [GUI](https://gfycat.com/DefinitiveSpiffyJohndory)

#### [Powerful command line interface](https://gfycat.com/NeighboringSarcasticEquine)


![interface_image](http://i.imgur.com/aWgqJPG.png)



## Getting Started

### Dependencies

* feh, or any other wallpaper setting software
* python-gobject
* python-imaging
* Pillow (python)
* xsltproc
* pywal

**_Attention:_** If you're using another terminal, you can load the colors on terminal startup
by running `(wpg -t)` in your terminal (if you use gnome-terminal, xfce4-terminal or Termite add `(wpg -V)` instead).  
You can add this to your terminal's settings, your shell `rc` file or anywhere else 
that allows you to run commands on startup.

# Installing

**_Warning:_** If you have a previous version of wpgtk installed
please delete the contents of your current `~/.wallpapers` as 
they may conflict with the new folder structure (for versions < 4.0 upgrading).

You can install via pip (as root):

```sh
# pip3 install wpgtk
```

or install the `wpgtk-git` package via the AUR.  

You can install color-adaptable themes with an included script,
after you install `wpg` you can run `wpg-install.sh`:

```
  Options:
  -h|help       Display this message
  -v|version    Display script version
  -o|openbox    Install openbox themes
  -t|tint2      Install tint2 theme
  -g|gtk        Install gtk theme
  -i|icons      Install icon-set
  -a|all        Install all themes
  ```

This will install all themes:
  ```
$ wpg-install.sh -a 
```

And if everything went fine you can now execute `wpg` and it will take
you to the user interface (you will need to install python3-gobject if
you did not install from the AUR).


for more details on the cli interface do:
```
$ wpg -h
```

# Theming

### General Usage

this is a list of useful wpg commands that you will be using if you want to use
the cli:
```
$ wpg -l #lists the currently added wallpapers
$ wpg -c #prints the current wallpaper
$ wpg -t #apply colorscheme to terminal (equivalent to wal -r)
$ wpg -z {wallpaper} #shuffles the given wallpaper's colorscheme
$ wpg --auto {wallpaper} #generates fg versions of the first 8 colors of the given wallpaper
$ wpg -d {wallpaper} #remove an existing wallpaper
$ wpg -h #display usage
$ wpg -s {wallpaper1} [{wallpaper2}] #sets the current wallpaper and colorscheme, wallpaper2 is optional
```

Files exported when creating a theme are all under the same directory `$HOME/.wallpapers`
this directory contains all exported formats that `pywal` and `wpgtk` have to offer, such
as:

* css variables under `$HOME/.wallpapers/current.css`
* json under `$HOME/.wallpapers/schemes/{image_name}.json`
* xres files under `$HOME/.wallpapers/xres/{image_name}.Xres`
* environment variables under `$HOME/.wallpapers/current.sh` 

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

### Configuration

The configuration file should be located at `$HOME/.wallpapers/wpg.conf`
There you can edit settings without the use of the gui.

# Loading at Startup
to load your new wallpaper at startup along with the colors add the following to your 
startup script or simply add it into your startup apps in your DE of choice.

```sh
bash ~/.wallpapers/wp_init.sh
```

# License

This project is licensed under the GPUv2 License - see the [LICENSE](LICENSE) file for details
