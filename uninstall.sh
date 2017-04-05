#!/bin/bash

function install_dependencies {
	echo "UNINSTALLING DEPENDENCIES"
	version="$( uname -r | grep ARCH )"

	if [ -n "$version"  ]; then
		echo "ARCH LINUX DETECTED::"
		sh -c "sudo pacman -Rs python-pillow feh python-gobject gtk3 libxslt"
		echo "DEPENDENCIES INSTALL COMPLETE"
	else
		version="$( uname -r | grep -Eo "(eneric|64)" )"
		if [ -n "$version" ]; then
			echo "DEBIAN OR *BUNTU DETECTED"
			sh -c "sudo apt-get install feh python3-gi python-gobject python-pip python-imaging xsltproc && pip install Pillow"
		else
			echo "ANOTHER DISTRO DETECTED:: INSTALL DEPENDENCIES FOR YOUR DISTRO"
			echo
		fi
	fi
}

function tint2support {
	echo
	echo
	echo "UNINSTALLING::TINT2-THEME"
	echo
	echo "THIS WILL OVERRIDE YOUR TINT2 THEME"
	echo
	echo -n "do you want to continue[Y/n]: "
	read election
	if [[ "$election" == "y" || "$election" == "Y" ]]; then
		echo -n "UNINSTALLING::TINT2-THEME"
		cp ./themes/tint2rc ~/.config/tint2/
		cp ./themes/tint2rc.base ~/.config/tint2/
	else
		echo "TINT2-THEME::NOT-INSTALLED"
		return 1
	fi
}

function uninstall_color {
	echo "UNINSTALLING::WPG"
	sudo rm -r /usr/local/bin/wpgtk/
	sudo rm /usr/local/bin/wpg
	sudo rm /usr/local/bin/wal
	echo "DONE - wpg HAS BEEN UNINSTALLED"
}

uninstall_color
