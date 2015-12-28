# wp

wp is a small tool I use to generate color schemes from images, and manage desktop wallpapers.

The color extraction scripts were taken from [this blog post](http://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/)
 with normalization reddit user radiosilence.

## Dependencies

As far as I know this only relies on PIL, python image library. I was able to fulfill this dependency with the `python-pillow` package on Arch Linux.
On other systems, `pip install Pillow`.

## Usage

```
$ wp add [file]
```

Generates color files .[file].colors and .[file].Xres which can be sourced by shell
scripts and xrdb respectivly. The color files and the image are added to the backgrounds directory.

```
$ wp change [file]
```

Changes the background image to a random image from the ~/.wallpapers directory, or the file passed, and  loads the .Xres file
into xrdb so xterm or urxvt will use the colors. It also links a script to ~/.colors. If you `source ~/.colors` in a script 
you can use the generated colors with `$COLOR0`, `$COLOR1`, ...


```
$ wp rm [file]
```

Removes the image and it's color files from the backgrounds directory.

```
$ wp ls
```

Lists the images in the backgrounds folder.
