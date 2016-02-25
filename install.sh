#!/bin/bash

function install_dependencies {
	echo "INSTALLING DEPENDENCIES"
	version= sh -c "uname -r | grep ARCH"

	if [ -n $version ]; then
		echo "ARCH LINUX DETECTED::"
		sh -c "sudo pacman -S python2-pillow feh python-gobject gtk3 libxslt"
		echo "DEPENDENCIES INSTALL COMPLETE"
	else
		version= sh -c "uname -r | grep GENERIC"
		if [ -n $version ]; then
			echo "DEBIAN OR *BUNTU DETECTED"
			sh -c "sudo apt-get install feh python3-gi python-gobject python-pip python-imaging libfreetype6 libfreetype6-dev xsltproc && pip install Pillow"
		else
			echo "ANOTHER DISTRO DETECTED:: INSTALL DEPENDENCIES FOR YOUR DISTRO"
			echo
		fi
	fi
}

function install_color {
	echo "CREATING::DIRECTORIES"
	mkdir ~/.wallpapers 
	mkdir ~/.themes
	mkdir ~/.icons
	echo "INSTALLING::WPG"
	sudo cp -r ./py/ /usr/local/bin/
	sudo cp -r ./src/ /usr/local/bin/
	sudo cp ./wp ./wpg /usr/local/bin
	sudo cp ./functions /usr/local/bin
	echo "INSTALLING::OPENBOX-THEME"
	cp -r ./themes/colorbamboo ~/.themes/ 
	rm ~/.themes/colorbamboo/openbox-3/themerc.base
	cp -r ./themes/colorbamboo_nb ~/.themes/
	rm ~/.themes/colorbamboo_nb/openbox-3/themerc.base
	echo "INSTALLING::ICONS"
	cp -r ./themes/flattrcolor ~/.icons
	echo "INSTALLING::GTK-THEME"
	sudo cp -r ./themes/FlatColor ~/.themes/
	rm ~/.themes/FlatColor/gtk-2.0/gtkrc.base
	echo "REMOVING DYNAMIC THEME ELMENTS"
	rm ~/.themes/FlatColor/gtk-3.0/gtk.css.base
	echo "DONE - SET YOUR THEMES AND RUN wpg"
	sudo chmod +x /usr/local/bin/wpg
	sudo chmod +x /usr/local/bin/wp
}

install_dependencies
install_color
