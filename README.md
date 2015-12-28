# wp

wp is a small tool I use to generate color schemes from images, and manage desktop wallpapers.

The color extraction scripts were taken from [this blog post](http://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/)
 with normalization reddit user radiosilence.

<<<<<<< HEAD
## Dependencies

As far as I know this only relies on PIL, python image library. I was able to fulfill this dependency with the `python-pillow` package on Arch Linux.
On other systems, `pip install Pillow`.
=======
### Examples

![Example Image](http://i.imgur.com/HXIm9v4.png?1)
![Another Example](http://i.imgur.com/1AdvJ8h.png?1)

### Version
1.0.2
>>>>>>> 955b1de142ce105bef7cf8fbdc40dea8a5713502

## Usage

```
$ wp add [file]
```

<<<<<<< HEAD
Generates color files .[file].colors and .[file].Xres which can be sourced by shell
scripts and xrdb respectivly. The color files and the image are added to the backgrounds directory.
=======
Arch
```sh
$ sudo pacman -S python2-pillow feh
```
*buntu
```sh
$ sudo apt-get install feh python-pip build-dep python-imaging libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev && pip install Pillow
```
although you may already have most of these installed by default, i put them on here just in case.

if you need a pair of colors predefined, just specify them on your .Xresources
i.e background and foreground
>>>>>>> 955b1de142ce105bef7cf8fbdc40dea8a5713502

```
$ wp change [file]
```

Changes the background image to a random image from the ~/.wallpapers directory, or the file passed, and  loads the .Xres file
into xrdb so xterm or urxvt will use the colors. It also links a script to ~/.colors. If you `source ~/.colors` in a script 
you can use the generated colors with `$COLOR0`, `$COLOR1`, ...


<<<<<<< HEAD
=======
### Installation
do the following
```sh
$ git clone http://github.com/deviantfero/wpgtk
$ cd ~/wpgtk
$ sh ./install.sh
>>>>>>> 955b1de142ce105bef7cf8fbdc40dea8a5713502
```
$ wp rm [file]
```
<<<<<<< HEAD

Removes the image and it's color files from the backgrounds directory.

=======
this will take care of placing the files where they are meant to be in /usr/local/bin/
### Loading at Startup
to load your new wallpaper at startup along with the colors add the following to your startup script or simply add it into your startup apps in your DE of choice, if you already use feh as your wallpaper manager, remember to remove it from your start up config.
```sh
~/.wallpapers/wp_init.sh
>>>>>>> 955b1de142ce105bef7cf8fbdc40dea8a5713502
```
$ wp ls
```

Lists the images in the backgrounds folder.
