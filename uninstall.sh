#!/bin/bash

function uninstall_color {
	echo "UNINSTALLING::WPG"
	sudo rm -r /usr/local/bin/wpgtk/
	sudo rm /usr/local/bin/wpg
	sudo rm /usr/local/bin/wal
	echo "DONE - wpg HAS BEEN UNINSTALLED"
}

uninstall_color
