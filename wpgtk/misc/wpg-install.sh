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
SRC_DIR="${PWD}/wpgtk-templates";
TEMPLATE_DIR="${CONFIG}/wpg/templates";

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
  -B   Install bpytop template
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
  git clone https://github.com/deviantfero/wpgtk-templates "$SRC_DIR";
  if [[ $? -eq 0 ]]; then
    cd "$SRC_DIR";
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
    cp --remove-destination ./tint2/tint2rc.base "${TEMPLATE_DIR}" && \
      ln -sf "${CONFIG}/tint2/tint2rc" "${TEMPLATE_DIR}/tint2rc" && \
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
    cp --remove-destination ./rofi/rofi.base "${TEMPLATE_DIR}" && \
      ln -sf "${CONFIG}/rofi/config" "${TEMPLATE_DIR}/rofi" && \
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
    cp --remove-destination ./i3/i3.base "${TEMPLATE_DIR}" && \
      ln -sf "${CONFIG}/i3/config" "${TEMPLATE_DIR}/i3" && \
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
    cp --remove-destination ./polybar/polybar.base "${TEMPLATE_DIR}" && \
      ln -sf "${CONFIG}/polybar/config" "${TEMPLATE_DIR}/polybar" && \
      echo ":: polybar template install done."
    return 0;
  fi
  echo ":: polybar template not installed";
}

install_gtk()
{
  echo "Installing gtk themes";
  cp -r ./FlatColor "${LOCAL}/themes/" && \

  mkdir -p "${THEMES_DIR}" && \

  cp --remove-destination ./FlatColor/gtk-2.0/gtkrc.base "${TEMPLATE_DIR}/gtk2.base" && \
    ln -sf "${LOCAL}/themes/FlatColor/gtk-2.0/gtkrc" "${TEMPLATE_DIR}/gtk2" && \
	ln -sf "${LOCAL}/themes/FlatColor" "${THEMES_DIR}/FlatColor" && \
	echo ":: gtk2 theme done" "${TEMPLATE_DIR}/gtk2";

  cp --remove-destination ./FlatColor/gtk-3.0/gtk.css.base "${TEMPLATE_DIR}/gtk3.0.base" && \
    ln -sf "${LOCAL}/themes/FlatColor/gtk-3.0/gtk.css" "${TEMPLATE_DIR}/gtk3.0" && \
    echo ":: gtk3.0 theme done"

  cp --remove-destination ./FlatColor/gtk-3.20/gtk.css.base "${TEMPLATE_DIR}/gtk3.20.base" && \
    ln -sf "${LOCAL}/themes/FlatColor/gtk-3.20/gtk.css" "${TEMPLATE_DIR}/gtk3.20" && \
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

  mkdir -p "${THEMES_DIR}"

  if [[ $? -eq 0 ]]; then
	mv "${LOCAL}/themes/colorbamboo/openbox-3/themerc.base" "${TEMPLATE_DIR}/ob_colorbamboo.base" && \
	  ln -sf "${LOCAL}/themes/colorbamboo/openbox-3/themerc" "${TEMPLATE_DIR}/ob_colorbamboo" && \
	  ln -sf "${LOCAL}/themes/colorbamboo" "${THEMES_DIR}/colorbamboo" && \
	  echo ":: colorbamboo openbox themes install done.";
  fi
}

install_bspwm()
{
  echo "Installing bspwm colors";
  mv "./bspwm/bspwm_colors.base" "${TEMPLATE_DIR}/bspwm_colors.base";
  mv "./bspwm/bspwm_colors" "${TEMPLATE_DIR}/bspwm_colors";
  ln -sf "${CONFIG}/bspwm/bspwm_colors.sh" "${TEMPLATE_DIR}/bspwm_colors" && \
  printf 'bash %s/bspwm/bspwm_colors.sh &' ${CONFIG} >> "${CONFIG}/bspwm/bspwmrc";
  echo ":: bspwm colors install done.";
}

install_dunst()
{
  echo "Installing dunst colors";
  echo ":: backing up current dunst conf in dunstrc.bak";
  cp "${CONFIG}/dunst/dunstrc" "${CONFIG}/dunst/dunstrc.bak" 2>/dev/null;

  mv "./dunst/dunstrc.base" "${TEMPLATE_DIR}/dunstrc.base";
  mv "./dunst/dunstrc" "${TEMPLATE_DIR}/dunstrc";
  ln -sf "${CONFIG}/dunst/dunstrc" "${TEMPLATE_DIR}/dunstrc" && \
	echo ":: dunst colors install done.";
}

install_bpytop()
{
  echo "Installing bpytop theme";
  echo ":: backing up current bpytop flatcolor theme in flatcolor.theme.bak";
  cp "${CONFIG}/bpytop/themes/flatcolor.theme" "${CONFIG}/bpytop/themes/flatcolor.theme.bak" 2>/dev/null;
  mv "./bpytop/bpytop.base" "${TEMPLATE_DIR}/bpytop.base";
  mv "./bpytop/bpytop" "${TEMPLATE_DIR}/bpytop";
  ln -sf "${CONFIG}/bpytop/themes/flatcolor.theme" "${TEMPLATE_DIR}/bpytop" && \
	echo ":: backing up current bpytop config to bpytop.conf.bak";
  sed -i.bak "s/^color_theme=.*/color_theme=+flatcolor/" ${CONFIG}/bpytop/bpytop.conf
	echo ":: bpytop theme install done, 'flatcolor' theme applied";
}

clean_up()
{
  rm -rf "$SRC_DIR";
}


#-----------------------------------------------------------------------
#  Handle command line arguments
#-----------------------------------------------------------------------

getargs()
{
  while getopts "H:bhvotgiIprdB" opt
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
      B)  bpytop="true" ;;
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
  [[ "$bpytop" == "true" ]] && install_bpytop;
  clean_up;
}

main "$@"

