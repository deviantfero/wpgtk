#!/bin/bash

function install_dependencies {
	echo "INSTALLING DEPENDENCIES"
	version="$( uname -r | grep ARCH )"

	if [ -n "$version"  ]; then
		echo ":: ARCH LINUX DETECTED"
		sh -c "sudo pacman -S python2-pillow feh python-gobject gtk3 libxslt"
		echo ":: DEPENDENCIES INSTALL COMPLETE"
	else
		version="$( uname -a | grep -Eo "(eneric|bian)" )"
		if [ -n "$version" ]; then
			echo ":: DEBIAN OR *BUNTU DETECTED"
			sh -c "sudo apt-get install feh python3-gi python-gobject xsltproc python-pip python-imaging && pip install Pillow"
		else
			echo ":: ANOTHER DISTRO DETECTED:: INSTALL DEPENDENCIES FOR YOUR DISTRO"
			echo
		fi
	fi
}

function tint2support {
	echo
	echo
	echo -e "\e[93m\e[5mINSTALLING::TINT2-THEME\e[0m"
	echo
	echo -e "\e[31mTHIS WILL OVERRIDE YOUR TINT2 THEME"
	echo
	echo -ne "\e[0mdo you want to continue[Y/n]: "
	read election
	if [[ "$election" == "y" || "$election" == "Y" ]]; then
		echo "INSTALLING::TINT2-THEME"
		cp ./themes/tint2rc ~/.config/tint2/
		cp ./themes/tint2rc.base ~/.config/tint2/
		cp ./themes/tint2rcnocolor.base ~/.config/tint2
	else
		echo -e "\e[31mTINT2-THEME::NOT-INSTALLED"
		return 1
	fi
}

function install_color {
	echo "CREATING::DIRECTORIES"
	mkdir ~/.wallpapers 
	mkdir -p ~/.themes/color_other
	mkdir ~/.icons
	echo "INSTALLING::WPG"
	sudo cp -r ./wpgtk/ /usr/local/bin/
	sudo chmod -R ugo+rx /usr/local/bin/wpgtk
	sudo cp ./wpcscript ./wpg /usr/local/bin
	sudo cp ./functions /usr/local/bin
	cp ./misc/* ~/.wallpapers/
	echo "INSTALLING::OPENBOX-THEME"
	cp -r ./themes/colorbamboo ~/.themes/
	cp -r ./themes/colorbamboo_nb ~/.themes/
	echo "INSTALLING::ICONS"
	cp -r ./themes/flattrcolor ~/.icons
	echo "INSTALLING::GTK-THEME"
	cp -r ./themes/FlatColor ~/.themes/
	tint2support
	echo -e "\e[34m:: DONE - SET THEMES AND RUN wpg\e[0m"
	sudo chmod +x /usr/local/bin/wpg && sudo chmod +x /usr/local/bin/wpcscript
}

usr="$(whoami)"
if [[ "$usr" != "root" ]]; then
	install_dependencies &&
	install_color
else
	echo "don't run as sudo"
fi
