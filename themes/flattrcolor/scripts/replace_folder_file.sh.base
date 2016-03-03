#!/bin/bash
backColor=34495d
frontColor=1abc9c
paperColor=ffffff
glyphColorOriginal=304050
glyphColorNew=304050

xsltproc --stringparam backColor $backColor --stringparam frontColor $frontColor --stringparam paperColor $paperColor change_folder_colors.xslt $1 > tmp.svg && mv tmp.svg $1
sed -i "s/#$glyphColorOriginal;/#$glyphColorNew;/g" $1
