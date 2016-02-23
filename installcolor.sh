#!/bin/bash

function tint2support {
	echo
	echo
	echo "INSTALLING::TINT2-THEME"
	echo
	echo "THIS WILL OVERRIDE YOUR TINT2 THEME"
	echo
	echo -n "do you want to continue[Y/n]: "
	read election
	if [[ "$election" == "y" || "$election" == "Y" ]]; then
		echo -n "INSTALLING::TINT2-THEME"
		cp ./themes/tint2rc ~/.config/tint2/
		cp ./themes/tint2rc.base ~/.config/tint2/
	else
		echo "TINT2-THEME::NOT-INSTALLED"
		return 1
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
	cp -r ./themes/colorbamboo_nb ~/.themes/
	echo "INSTALLING::ICONS"
	cp -r ./themes/flattrcolor ~/.icons
	echo "INSTALLING::GTK-THEME"
	sudo cp -r ./themes/FlatColor ~/.themes/
	tint2support
	echo "DONE - SET YOUR THEMES AND RUN wpg"
	sudo chmod +x /usr/local/bin/wpg && sudo chmod +x /usr/local/bin/wp
}

install_color
