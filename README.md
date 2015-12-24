# wpg

wpg is a little programm to manage your wallpapers in a simple way, it integrates a script wich takes the colors in the image of your preference and sets up an .Xresources file to match your term colors with your wallpaper

  - Simple wallpaper management\
[Example Image](/img/screenshot.png)

### Version
1.0.1

### Dependencies

wpg has some dependencies:

* python2-pillow ( on arch )
* feh

also you need to uninstall any other wallpaper manager as it will override this one at startup

### Credit
i couldn't find credit on the colorscript that i got namely "wp" & "./py/\*" so if anybody happens to know who was the original author of this program "wp" & "./py/\*" please let me know.
### Instalation
do the following
```sh
$ git clone http://github.com/deviantfero/wpgtk
$ cd ~/wpgtk
$ sh ./install.sh
```
now to actually run the program just
```sh
$ wpg
```
this will take care of placing the files where they are meant to be in /usr/local/bin/
### Loading at Startup
to load your new wallpaper at startup along with the colors add the following to your startup script or simply add it into your startup apps in your DE of choice
```sh
~/.wallpapers/wp_init.sh
```
