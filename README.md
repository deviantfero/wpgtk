
# wpgtk

A universal theming software for all themes 
defined in text files, compatible with all terminals, 
with default themes for GTK2, GTK+, openbox and Tint2, that uses 
[pywal](https://github.com/dylanaraps/pywal) as it's core.

you can choose to interact with it in two ways, manage your themes 
from either a cli application or using a GUI.

### Features

* #### [GUI](https://gfycat.com/RigidAnxiousElk)

* #### [Powerful command line interface](https://gfycat.com/NeighboringSarcasticEquine)

* #### [Templates](https://gfycat.com/VacantHeavyAmericansaddlebred)


![interface_image](http://i.imgur.com/2cquXzm.png)



## Getting Started

### Dependencies

* feh, or any other wallpaper setting software
* python-gobject
* python-imaging
* Pillow (python)
* xsltproc
* pywal

**_Attention:_** If you're using another terminal, you can load the colors on terminal startup
by running `(wpg -t &)` in your terminal or `(wpg -vt &)` if you're using a VTE terminal.  
You can add this to your terminal's settings, your shell `rc` file or anywhere else 
that allows you to run commands on startup.

# Installing

**_Warning:_** If you have a previous version of wpgtk installed
please delete the contents of your current `~/.wallpapers` as 
they may conflict with the new folder structure (for versions < 4.0 upgrading).

You can install via pip (as root):

```c
# pip3 install wpgtk
```

or install the `wpgtk-git` package via the AUR.  

You can install color-adaptable themes with an included script,
after you install `wpg` you can run `wpg-install.sh`:

```
  echo "Usage :  wpg-install.sh [options] [--]

  Options:
  -h   Display this message
  -v   Display script version
  -o   Install openbox themes
  -t   Install tint2 theme
  -g   Install gtk theme
  -i   Install icon-set
  -r   Install rofi theme
  -I   Install i3 theme
  -p   Install polybar theme
  ```

You can combine this flags to install only the themes you need.
  ```sh
# install everything!

$ wpg-install.sh -otgirIp

# maybe you want an openbox setup

$ wpg-install.sh -otgir

# or maybe an i3 setup

$ wpg-install.sh -rgIp
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

```
usage: wpg [-h] [-s [S [S ...]]] [-r] [-m] [-a [A [A ...]]] [-l] [--version]
           [-d [D [D ...]]] [-c] [-e [E [E ...]]] [-z [Z [Z ...]]] [-t] [-v]
           [-x] [-y [Y [Y ...]]]

optional arguments:
  -h, --help      show this help message and exit
  -s [S [S ...]]  set the wallpaper and colorscheme, apply changes system-wide
  -r              restore the wallpaper and colorscheme
  -m              pick a random wallpaper and set it
  -a [A [A ...]]  add images to the wallpaper folder and generate colorschemes
  -l              see which wallpapers are available
  --version       print the current version
  -d [D [D ...]]  delete the wallpaper(s) from wallpaper folder
  -c              shows the current wallpaper
  -e [E [E ...]]  auto adjusts the given colorscheme(s)
  -z [Z [Z ...]]  shuffles the given colorscheme(s)
  -t              send color sequences to all terminals VTE true
  -v              use VTE sequences to generate and set themes
  -x              add, remove and list templates instead of themes
  -y [Y [Y ...]]  add an existent basefile template [config, basefile]

```

for those using VTE terminals such as `termite` or `xfce4-terminal` you can suffix -v to all
previous flags to get rid of incompatible artifacts showing up in your screen, for example
to pick a random wallpaper you would do `wpg -vm` to avoid those artifacts in your terminal.

Files exported when creating a theme are all under the same directory `$HOME/.wallpapers`
this directory contains all exported formats that `pywal` and `wpgtk` have to offer, such
as:

* css variables under `$HOME/.wallpapers/current.css`
* json under `$HOME/.wallpapers/schemes/{image_name}.json`
* xres files under `$HOME/.wallpapers/xres/{image_name}.Xres`
* environment variables under `$HOME/.wallpapers/current.sh` 

### Configuration

The configuration file should be located at `$HOME/.wallpapers/wpg.conf`
There you can edit settings without the use of the gui.

# Templates

You can add text files for which `wpgtk` will create a copy and a backup and
add a modifiable `template` file to `~/.themes/color_other` with file extension `.base`
in this files some keywords will be searched and replaced with the respective hexcodematching those keywords, 
an thenm replace the original configuration keeping it in sync with the colorscheme, these keywords are:

```
#COLOR0 #COLORX10
#COLOR1 #COLORX11
#COLOR2 #COLORX12
#COLOR3 #COLORX13
#COLOR4 #COLORX14
#COLOR5 #COLORX15
#COLOR6
#COLOR7
#COLOR8
#COLOR9

#COLORIN (active color)
#COLORACT (inactive color)

wpgtk-ignore: by placing this keyword on the first line of a basefile,
it will be temporarily disabled, leaving you with the last theme you chose.
```

#### Example
I added a file called `rofi.txt` and wpgtk created a template under `~/.themes/color_other/rofi.txt.base` 
in which I can put keywords that will later be replaced when I change colorschemes with `wpgtk` in the
original file, giving me a dynamic file that changes with my colorscheme.

```
# location: ~/.themes/color_other/rofi.txt.base

color-window "#COLOR0, #COLOR0, #COLOR0"
color-normal "#COLOR0, white, #COLOR0, #COLORACT, white"
color-active "#COLOR0, #COLORACT, #COLOR0, #COLORACT, white"
```

This is the result after applying a colorscheme:

```
# location: ~/Code/scripts/rofi.txt

color-window "#22231D, #22231D, #22231D"
color-normal "#22231D, white, #22231D, #4c837b, white"
color-active "#22231D, #4c837b, #22231D, #4c837b, white"
```


### Restoring old templates

You can also re-add old templates you archive, to do this, you must use the cli and execute the following
command:

```
$ wpg -y /path/to/config-file /path/to/saved-base-file
```

This will reconnect the base file template to the original configuration file and keep it in sync again
with the colorscheme.


# Loading at Startup
to load your new wallpaper at startup along with the colors add the following to your 
startup script or simply add it into your startup apps in your DE of choice.

```sh
bash ~/.wallpapers/wp_init.sh
```

# License

This project is licensed under the GPUv2 License - see the [LICENSE](LICENSE) file for details
