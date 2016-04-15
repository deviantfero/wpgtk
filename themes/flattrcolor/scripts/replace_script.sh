#!/bin/bash
function replaceall {
	cd ~/.icons/flattrcolor/scripts
	#sh ./replace_folder_file.sh change_folder_colors.xslt
	sh ./change_all_folders.sh
}

replaceall
