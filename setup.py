"""wpgtk - setup.py"""
import os
import setuptools
import sys

if sys.version_info.major < 3 or sys.version_info.minor < 5:
    print("error: wpgtk requires Python 3.5 or greater.", file=sys.stderr)
    quit(1)

import wpgtk

try:
    LONG_DESC = open('README.md').read()
except:
    LONG_DESC = '-'
    pass

VERSION = wpgtk.__version__
DOWNLOAD = "https://github.com/deviantfero/wpgtk/archive/%s.tar.gz" % VERSION

HOME = os.getenv("HOME", os.path.expanduser("~"))
CONFIG = os.getenv("XDG_CONFIG_HOME", os.path.join(HOME, ".config"))
WPG_DIR = os.path.join(CONFIG, "wpg")
WALL_DIR = os.path.join(WPG_DIR, "wallpapers")


setuptools.setup(
    name="wpgtk",
    packages=setuptools.find_packages(),
    version=VERSION,
    author="Fernando Vásquez",
    author_email="fmorataya.04@gmail.com",
    description="GTK+ theme/wallpaper manager which uses pywal as its core",
    long_description=LONG_DESC,
    license="GPL2",
    url="https://github.com/deviantfero/wpgtk",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
    ],
    entry_points={
        "console_scripts": ["wpg=wpgtk.__main__:main"]
    },
    python_requires=">=3.5",
    install_requires=[
        'Pillow>=4.2.1',
        'pywal>=3.0.0',
    ],
    include_package_data=True,
    data_files=[('etc/wpgtk', ['wpgtk/misc/wpg.conf']),
                ('bin/', ['wpgtk/misc/wpg-install.sh']),
                ('share/bash-completion/completions/', ['completions/bash/wpg']),
                ('share/zsh/site-functions/', ['completions/zsh/_wpg'])]
)
