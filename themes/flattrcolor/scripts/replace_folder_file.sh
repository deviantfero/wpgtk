#!/bin/bash
#	default color: 178984
glyphColorOriginal=71744d
glyphColorNew=524954

#	Front
#	default color: 36d7b7
frontColorOriginal=c4c886
frontColorNew=9b8aa0

#	Back
#	default color: 1ba39c
backColorOriginal=959865
backColorNew=716475

#	Paper
#	default color: ffffff
paperColorOriginal=ffffff
paperColorNew=ffffff

sed -i "s/#$glyphColorOriginal;/#$glyphColorNew;/g" $1
sed -i "s/#$frontColorOriginal;/#$frontColorNew;/g" $1
sed -i "s/#$backColorOriginal;/#$backColorNew;/g" $1
sed -i "s/#$paperColorOriginal;/#$paperColorNew;/g" $1
