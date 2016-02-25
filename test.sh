version= sh -c "uname -r | grep GENERIC"

if [[ $version ]]; then
	echo "ARCH LINUX GURLZ"
else
	echo "NOT UBUNTU"
fi
