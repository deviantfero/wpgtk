#!/bin/bash

function tint2support {
	echo
	echo "INSTALLING::TINT2-THEME"
	echo
	echo "THIS WILL OVERRIDE YOUR TINT2 THEME"
	echo
	echo -n "INSTALLING::TINT2-THEME"
	cp ./themes/tint2rc ~/.config/tint2/
	cp ./themes/tint2rc.base ~/.config/tint2/
}

function install_color {
	echo "CREATING::DIRECTORIES"
	mkdir ~/.wallpapers 
	mkdir ~/.themes
	mkdir ~/.icons
	echo "INSTALLING::WPG"
	sudo cp -r ./py/ ../pkg
	sudo cp -r ./src/ ../pkg
	sudo cp ./wp ./wpg ../pkg
	sudo cp ./functions ../pkg
	echo "INSTALLING::OPENBOX-THEME"
	cp -r ./themes/colorbamboo ~/.themes/
	cp -r ./themes/colorbamboo_nb ~/.themes/
	echo "INSTALLING::ICONS"
	cp -r ./themes/flattrcolor ~/.icons
	echo "INSTALLING::GTK-THEME"
	cp -r ./themes/FlatColor ~/.themes/
	tint2support
	echo "DONE - SET YOUR THEMES AND RUN wpg"
}

install_color
