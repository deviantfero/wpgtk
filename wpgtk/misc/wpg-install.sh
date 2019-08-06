#!/usr/bin/env bash

__ScriptVersion="0.1.5";

if [ -n "${XDG_CONFIG_HOME}" ]; then
  CONFIG="${XDG_CONFIG_HOME}"
else
  CONFIG="${HOME}/.config" 
fi

if [ -n "${XDG_DATA_HOME}" ]; then
  LOCAL="${XDG_DATA_HOME}"
else
  LOCAL="${HOME}/.local/share" 
fi

THEMES_DIR="${HOME}/.themes";
TEMPLATE_DIR="${PWD}/wpgtk-templates";
COLOR_OTHER="${CONFIG}/wpg/templates";

#===  FUNCTION  ================================================================
#         NAME:  wpg-install.sh
#  DESCRIPTION:  Installs various wpgtk themes.
#===============================================================================
usage()
{
  echo "Usage :  $0 [options] [--]

  Options:
  -h   Display this message
  -v   Display script version
  -o   Install openbox templates
  -t   Install tint2 template
  -g   Install gtk template
  -i   Install icon-set
  -r   Install rofi template
  -I   Install i3 template
  -p   Install polybar template
  -b   Install bspwm template
  -d   Install dunst template
  -H   Specify hash of wpgtk-templates repository to use
  "
}

checkprogram()
{
  command -v $1 >/dev/null 2>&1;
  if [[ $? -eq 1 ]]; then
    echo "Please install $1 before proceeding"; 
    exit 1;
  fi
}

getfiles()
{
  checkprogram 'git';
  checkprogram 'wpg';
  mkdir -p "${LOCAL}/themes/color_other";
  mkdir -p "${LOCAL}/icons";
  git clone https://github.com/deviantfero/wpgtk-templates "$TEMPLATE_DIR";
  if [[ $? -eq 0 ]]; then
    cd "$TEMPLATE_DIR";
    [[ ! -z "$commit" ]] && git checkout $commit;
    return 0;
  else
    exit 1;
  fi
}

install_tint2()
{
  echo -n "This might override your tint2 config, Continue?[Y/n]: ";
  read -r response;
  if [[ ! "$response" == "n" ]]; then
    echo "Installing tint2 config";
    echo ":: backing up current tint2 conf in tint2rc.old.bak";
    cp "${CONFIG}/tint2/tint2rc" "${CONFIG}/tint2/tint2rc.old.bak" 2>/dev/null;
    cp --remove-destination ./tint2/tint2rc "${CONFIG}/tint2/tint2rc" && \
    cp --remove-destination ./tint2/tint2rc.base "${COLOR_OTHER}" && \
      ln -sf "${CONFIG}/tint2/tint2rc" "${COLOR_OTHER}/tint2rc" && \
      echo ":: tint2 template install done."
    return 0;
  fi
  echo ":: tint2 template not installed";
}

install_rofi()
{
  echo -n "This might override your rofi config, Continue?[Y/n]: ";
  read -r response;
  if [[ ! "$response" == "n" ]]; then
    echo "Installing rofi config";
    echo ":: backing up current rofi conf in rofi.bak";
    cp "${CONFIG}/rofi/config" "${CONFIG}/rofi/config.bak" 2>/dev/null;
    cp --remove-destination ./rofi/config "${CONFIG}/rofi/config" && \
    cp --remove-destination ./rofi/rofi.base "${COLOR_OTHER}" && \
      ln -sf "${CONFIG}/rofi/config" "${COLOR_OTHER}/rofi" && \
      echo ":: rofi template install done."
    return 0;
  fi
  echo ":: rofi template not installed";
}

install_i3() 
{
  echo -n "This might override your i3 config, Continue?[Y/n]: ";
  read -r response;
  if [[ ! "$response" == "n" ]]; then
    echo "Installing i3 config";
    echo ":: backing up current i3 conf in config.bak";
    cp "${CONFIG}/i3/config" "${CONFIG}/i3/config.bak" 2>/dev/null;
    cp --remove-destination ./i3/config "${CONFIG}/i3/config" && \
    cp --remove-destination ./i3/i3.base "${COLOR_OTHER}" && \
      ln -sf "${CONFIG}/i3/config" "${COLOR_OTHER}/i3" && \
      echo ":: i3 template install done."
    return 0;
  fi
  echo ":: i3 template not installed";
}

install_polybar() 
{
  echo -n "This might override your polybar config, Continue?[Y/n]: ";
  read -r response;
  if [[ ! "$response" == "n" ]]; then
    echo "Installing polybar config";
    echo ":: backing up current polybar conf in config.bak";
    cp "${CONFIG}/polybar/config" "${CONFIG}/polybar/config.bak" 2>/dev/null;
    cp --remove-destination ./polybar/config "${CONFIG}/polybar/config" && \
    cp --remove-destination ./polybar/polybar.base "${COLOR_OTHER}" && \
      ln -sf "${CONFIG}/polybar/config" "${COLOR_OTHER}/polybar" && \
      echo ":: polybar template install done."
    return 0;
  fi
  echo ":: polybar template not installed";
}

install_gtk()
{
  echo "Installing gtk themes";
  cp -r ./FlatColor "${LOCAL}/themes/" && \

  cp --remove-destination ./FlatColor/gtk-2.0/gtkrc.base "${COLOR_OTHER}/gtk2.base" && \
    ln -sf "${LOCAL}/themes/FlatColor/gtk-2.0/gtkrc" "${COLOR_OTHER}/gtk2" && \
	ln -sf "${LOCAL}/themes/FlatColor" "${THEMES_DIR}/FlatColor" && \
	echo ":: gtk2 theme done" "${COLOR_OTHER}/gtk2";

  cp --remove-destination ./FlatColor/gtk-3.0/gtk.css.base "${COLOR_OTHER}/gtk3.0.base" && \
    ln -sf "${LOCAL}/themes/FlatColor/gtk-3.0/gtk.css" "${COLOR_OTHER}/gtk3.0" && \
    echo ":: gtk3.0 theme done"

  cp --remove-destination ./FlatColor/gtk-3.20/gtk.css.base "${COLOR_OTHER}/gtk3.20.base" && \
    ln -sf "${LOCAL}/themes/FlatColor/gtk-3.20/gtk.css" "${COLOR_OTHER}/gtk3.20" && \
    echo ":: gtk3.20 theme done"

  echo ":: FlatColor gtk themes install done."
}

install_icons()
{
  echo "Installing icon pack";
  cp -r flattrcolor "${LOCAL}/icons/" && \
  cp -r flattrcolor-dark "${LOCAL}/icons/" && \
    echo ":: flattr icons install done."
}

install_openbox()
{
  echo "Installing openbox themes";
  cp --remove-destination -r ./openbox/colorbamboo/* "${LOCAL}/themes/colorbamboo"

  if [[ $? -eq 0 ]]; then
	mv "${LOCAL}/themes/colorbamboo/openbox-3/themerc.base" "${COLOR_OTHER}/ob_colorbamboo.base" && \
	  ln -sf "${LOCAL}/themes/colorbamboo/openbox-3/themerc" "${COLOR_OTHER}/ob_colorbamboo" && \
	  ln -sf "${LOCAL}/themes/colorbamboo" "${THEMES_DIR}/colorbamboo" && \
	  echo ":: colorbamboo openbox themes install done.";
  fi
}

install_bspwm()
{
  echo "Installing bspwm colors";
  mv "./bspwm/bspwm_colors.base" "${COLOR_OTHER}/bspwm_colors.base";
  mv "./bspwm/bspwm_colors" "${COLOR_OTHER}/bspwm_colors";
  ln -sf "${CONFIG}/bspwm/bspwm_colors.sh" "${COLOR_OTHER}/bspwm_colors" && \
  printf 'bash %s/bspwm/bspwm_colors.sh &' ${CONFIG} >> "${CONFIG}/bspwm/bspwmrc";
  echo ":: bspwm colors install done.";
}

install_dunst()
{
  echo "Installing dunst colors";
  echo ":: backing up current dunst conf in dunstrc.bak";
  cp "${CONFIG}/dunst/dunstrc" "${CONFIG}/dunst/dunstrc.bak" 2>/dev/null;

  mv "./dunst/dunstrc.base" "${COLOR_OTHER}/dunstrc.base";
  mv "./dunst/dunstrc" "${COLOR_OTHER}/dunstrc";
  ln -sf "${CONFIG}/dunst/dunstrc" "${COLOR_OTHER}/dunstrc" && \
	echo ":: dunst colors install done.";
}

clean_up()
{
  rm -rf "$TEMPLATE_DIR";
}


#-----------------------------------------------------------------------
#  Handle command line arguments
#-----------------------------------------------------------------------

getargs()
{
  while getopts "H:bhvotgiIprd" opt
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
      I)      i3="true" ;;
      p) polybar="true" ;;
	  b)   bspwm="true" ;;
	  d)   dunst="true" ;;
      H) commit="${OPTARG}" ;;
      *)
        echo -e "\n  Option does not exist : $OPTARG\n"
        usage;
        exit 1
        ;;

      esac
    done
    shift "$((OPTIND - 1))"
}

main()
{
  getargs "$@";
  getfiles;
  [[ "$openbox" == "true" ]] && install_openbox;
  [[ "$tint2" == "true" ]] && install_tint2;
  [[ "$rofi" == "true" ]] && install_rofi;
  [[ "$gtk" == "true" ]] && install_gtk;
  [[ "$icons" == "true" ]] && install_icons;
  [[ "$polybar" == "true" ]] && install_polybar;
  [[ "$i3" == "true" ]] && install_i3;
  [[ "$bspwm" == "true" ]] && install_bspwm;
  [[ "$dunst" == "true" ]] && install_dunst;
  clean_up;
}

main "$@"
