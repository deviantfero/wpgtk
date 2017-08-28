#!/usr/bin/env bash

__ScriptVersion="0.1.5";
THEME_DIR="${PWD}/wpgtk-themes";
COLOR_OTHER="${HOME}/.themes/color_other";

#===  FUNCTION  ================================================================
#         NAME:  wpg-install
#  DESCRIPTION:  Installs various wpgtk themes.
#===============================================================================
function usage ()
{
  echo "Usage :  $0 [options] [--]

  Options:
  -h   Display this message
  -v   Display script version
  -o   Install openbox themes
  -t   Install tint2 theme
  -g   Install gtk theme
  -i   Install icon-set
  -r   Install rofi theme
  -a   Install all themes
  "
}

function checkprogram ()
{
  command -v $1 >/dev/null 2>&1;
  if [[ $? -eq 1 ]]; then
    echo "Please install $1 before proceeding"; 
    exit 1;
  fi
}

function getfiles ()
{
  checkprogram 'git';
  checkprogram 'wpg';
  mkdir -p "${HOME}/.themes/color_other";
  mkdir -p "${HOME}/.icons";
  git clone https://github.com/deviantfero/wpgtk-themes "$THEME_DIR";
  if [[ $? -eq 0 ]]; then
    cd "$THEME_DIR";
    return 0;
  else
    exit 1;
  fi
}

function install_tint2 ()
{
  echo -n "This might override your tint2 config, Continue?[Y/n]: ";
  read -r response;
  if [[ ! "$response" == "n" ]]; then
    echo "Installing tint2 config";
    echo ":: backing up current tint2 conf in tint2rc.old.bak";
    cp "${HOME}/.config/tint2/tint2rc" "${HOME}/.config/tint2/tint2rc.old.bak" 2>/dev/null;
    cp --remove-destination ./tint2/tint2rc "${HOME}/.config/tint2/tint2rc" && \
    cp --remove-destination ./tint2/tint2rc.base "${COLOR_OTHER}" && \
      ln -sf "${HOME}/.config/tint2/tint2rc" "${COLOR_OTHER}/tint2rc" && \
      echo ":: tint2 template install done."
    return 0;
  fi
  echo ":: tint2 template not installed";
}

function install_rofi ()
{
  echo -n "This might override your rofi config, Continue?[Y/n]: ";
  read -r response;
  if [[ ! "$response" == "n" ]]; then
    echo "Installing rofi config";
    echo ":: backing up current rofi conf in rofi.bak";
    cp "${HOME}/.config/rofi/config" "${HOME}/.config/rofi/config.bak" 2>/dev/null;
    cp --remove-destination ./rofi/config "${HOME}/.config/rofi/config" && \
    cp --remove-destination ./rofi/rofi.base "${COLOR_OTHER}" && \
      ln -sf "${HOME}/.config/rofi/config" "${COLOR_OTHER}/rofi" && \
      echo ":: rofi template install done."
    return 0;
  fi
  echo ":: rofi template not installed";
}

function install_gtk ()
{
  echo "Installing gtk themes";
  cp -r ./FlatColor "${HOME}/.themes/" && \
    echo ":: FlatColor gtk themes install done."
}

function install_icons()
{
  echo "Installing icon pack";
  cp -r flattrcolor "${HOME}/.icons/" && \
    echo ":: flattr icons install done."
}

function install_openbox()
{
  echo "Installing openbox themes";
  cp --remove-destination -r ./openbox/colorbamboo/* "${HOME}/.themes/colorbamboo"
  if [[ $? -eq 0 ]]; then
    mv "${HOME}/.themes/colorbamboo/openbox-3/themerc.base" "${COLOR_OTHER}/ob_colorbamboo.base";
    ln -sf "${HOME}/.themes/colorbamboo/openbox-3/themerc" "${COLOR_OTHER}/ob_colorbamboo" && \
      echo ":: colorbamboo openbox themes install done.";
  fi
}

function clean_up()
{
  rm -rf "$THEME_DIR";
}


#-----------------------------------------------------------------------
#  Handle command line arguments
#-----------------------------------------------------------------------

function getargs()
{
  while getopts ":hvotgir" opt
  do
    case $opt in
      h)
        usage;
        exit 0
        ;;
      v)
        echo "$0 -- Version $__ScriptVersion";
        exit 0;
        ;;
      o) openbox="true" ;;
      i)   icons="true" ;;
      g)     gtk="true" ;;
      t)   tint2="true" ;;
      r)    rofi="true" ;;
      *)
        echo -e "\n  Option does not exist : $OPTARG\n"
        usage;
        exit 1
        ;;

      esac
    done
    shift "$((OPTIND - 1))"
}

function main()
{
  getargs "$@";
  getfiles;
  [[ "$openbox" == "true" ]] && install_openbox;
  [[ "$tint2" == "true" ]] && install_tint2;
  [[ "$rofi" == "true" ]] && install_rofi;
  [[ "$gtk" == "true" ]] && install_gtk;
  [[ "$icons" == "true" ]] && install_icons;
  clean_up;
}

main "$@"
