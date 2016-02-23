#!/bin/bash
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
	echo "DONE - SET YOUR THEMES AND RUN wpg"
	sudo chmod +x /usr/local/bin/wpg
	sudo chmod +x /usr/local/bin/wp
}

install_color
