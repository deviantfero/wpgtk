#!/bin/bash
#This will replace the colors in a folder svg file. The one hack is that to change the foreground 
#shape colors you must provide the old color and this color cannot be repeated anywhere that you do
#not want it to change. The folder back, paper, and front colors are precise replacements in
#xml. However, the glyph color replacement is a regular expression search/replace. To change the
#glyph color again, you must replace the original value with the new value and run it again. 

backColor=34495d		#default is 34495d
frontColor=1abc9c		#default is 1abc9c
paperColor=ffffff		#default is ffffff
glyphColorOriginal=304050	#default is 304050, 
				#if you change the color to e.g. ff3366 in glyphColorNew, change
				#the value in glyphColorOriginal as well so it matches the new one
				#thus when you change the color it actually makes the change.
glyphColorNew=304050

xsltproc --stringparam backColor $backColor --stringparam frontColor $frontColor --stringparam paperColor $paperColor change_folder_colors.xslt $1 > tmp.svg && mv tmp.svg $1
sed -i "s/#$glyphColorOriginal;/#$glyphColorNew;/g" $1
