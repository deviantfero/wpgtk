#!/bin/bash

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
	else
		echo -e "\e[31mTINT2-THEME::NOT-INSTALLED"
		return 1
	fi
}

function install_color {
	echo "CREATING::DIRECTORIES"
	mkdir ~/.wallpapers 
	cp ./misc/.* ~/.wallpapers
	mkdir -p ~/.themes/color_other
	mkdir ~/.icons
	echo "INSTALLING::WPG"
	echo "INSTALLING::OPENBOX-THEME"
	cp -r ./themes/colorbamboo ~/.themes/
	cp -r ./themes/colorbamboo_nb ~/.themes/
	echo "INSTALLING::ICONS"
	cp -r ./themes/flattrcolor ~/.icons
	echo "INSTALLING::GTK-THEME"
	cp -r ./themes/FlatColor ~/.themes/
	tint2support
	echo -e "\e[34m:: DONE - SET THEMES AND RUN wpg\e[0m"
}

install_color
