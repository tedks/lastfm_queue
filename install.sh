#!/bin/bash

################################ USAGE #######################################

usage=$(
cat <<EOF
Usage:
$0 [OPTION]
-h, --help      show this message.
-l, --local     install the plugin locally (default).
-g, --global    install the plugin globally.

EOF
)

########################### OPTIONS PARSING #################################

#parse options
TMP=`getopt --name=$0 -a --longoptions=local,global,help -o l,g,h -- $@`

if [[ $? == 1 ]]
then
    echo
    echo "$usage"
    exit
fi

eval set -- $TMP

until [[ $1 == -- ]]; do
    case $1 in
        -l|--local)
            LOCAL=true
            ;;
        -g|--global)
            LOCAL=false
            ;;
        -h|--help)
            echo "$usage"
            exit
            ;;
    esac
    shift # move the arg list to the next option or '--'
done
shift # remove the '--', now $1 positioned at first argument if any

#default values
LOCAL=${LOCAL:=true}

########################## START INSTALLATION ################################

GLIB_SCHEME="org.gnome.rhythmbox.plugins.lastfm_queue.gschema.xml"
GLIB_DIR="/usr/share/glib-2.0/schemas/"
SCRIPT_NAME=`basename "$0"`
SCRIPT_PATH=${0%`basename "$0"`}

#install the glib schema
echo "Installing glib schemas (admin password needed):"
sudo cp "${SCRIPT_PATH}${GLIB_SCHEME}" "$GLIB_DIR"
sudo glib-compile-schemas "$GLIB_DIR"

#install the plugin; the install path depends on the install mode
if [[ $LOCAL == true ]]
then
    echo "Installing plugin locally"
    PLUGIN_PATH="/home/${USER}/.local/share/rhythmbox/plugins/lastfm_queue/"
    
    #build the dirs
    mkdir -p $PLUGIN_PATH

    #copy the files
    cp -r "${SCRIPT_PATH}"* "$PLUGIN_PATH"

    #remove the install script from the dir (not needed)
    rm "${PLUGIN_PATH}${SCRIPT_NAME}"
else
    echo "Installing plugin globally"
    PLUGIN_PATH="/usr/lib/rhythmbox/plugins/lastfm_queue/"
    
    #build the dirs
    sudo mkdir -p $PLUGIN_PATH

    #copy the files
    sudo cp -r "${SCRIPT_PATH}"* "$PLUGIN_PATH"

    #remove the install script from the dir (not needed)
    sudo rm "${PLUGIN_PATH}${SCRIPT_NAME}"
fi

echo "Finished installing the plugin. Enjoy :]"
