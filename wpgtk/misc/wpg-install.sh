#!/bin/bash

__ScriptVersion="0.1"
THEME_DIR=$PWD/wpgtk-themes

#===  FUNCTION  ================================================================
#         NAME:  wpg-install
#  DESCRIPTION:  Installs various wpgtk themes.
#===============================================================================
function usage ()
{
  echo "Usage :  $0 [options] [--]

  Options:
  -h|help       Display this message
  -v|version    Display script version
  -o|openbox    Install openbox themes
  -t|tint2      Install tint2 theme
  -g|gtk        Install gtk theme
  -i|icons      Install icon-set
  -a|all        Install all themes
  "
} 

function checkgit () 
{
  command -v git 2>&1 > /dev/null || (echo "Please install git before proceeding" && exit 1);
}

function getfiles () 
{
  checkgit;
  mkdir -p $HOME/.themes;
  mkdir -p $HOME/.icons;
  git clone https://github.com/deviantfero/wpgtk-themes $THEME_DIR;
  cd $THEME_DIR;
}

function install_tint2 () 
{
  echo -n "This might override your tint2 config, Continue?[Y/n]: ";
  read response;
  if [[ ! "$response" == "n" ]]; then
    echo "Installing tint2 config";
    cp ./tint2/* $HOME/.config/tint2/ && \
      echo ":: tint2 conf install done.";
    return 0;
  fi
  echo ":: tint2 conf not installed";
}

function install_gtk ()
{
  echo "Installing gtk themes";
  cp -r ./FlatColor $HOME/.themes/ && \
    echo ":: gtk themes install done."
}

function install_icons()
{
  echo "Installing icon pack";
  cp -r flattrcolor $HOME/.icons/ && \
    echo ":: icons install done."
}

function install_openbox()
{
  echo "Installing openbox themes";
  cp -r ./openbox/* $HOME/.themes/ && \
    echo ":: openbox themes install done.";
}

function install_all()
{
  install_tint2;
  install_gtk;
  install_icons;
  install_openbox;
}

function clean_up()
{
  rm -rf $THEME_DIR;
}


#-----------------------------------------------------------------------
#  Handle command line arguments
#-----------------------------------------------------------------------

while getopts ":hvotgia" opt
do
  case $opt in
    h|help)  
      usage; 
      exit 0   
      ;;
    v|version)  
      echo "$0 -- Version $__ScriptVersion"; 
      exit 0;
      ;;
    o|openbox)
      getfiles;
      install_openbox;
      clean_up;
      exit 0;
      ;;
    i|icons)
      getfiles;
      install_icons;
      clean_up;
      exit 0;
      ;;
    g|gtk)
      getfiles;
      install_gtk;
      clean_up;
      exit 0;
      ;;
    t|tint2)
      getfiles;
      install_tint2;
      clean_up;
      exit 0;
      ;;
    a|all)
      getfiles;
      install_all;
      clean_up;
      exit 0;
      ;;
    *)  
      echo -e "\n  Option does not exist : $OPTARG\n"
      usage; 
      exit 1   
      ;;

    esac    
  done
  shift $(($OPTIND-1))
