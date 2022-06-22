#!/bin/bash

CONFIG_EXAMPLE=./config/config.yaml.example
CONFIG=./config/config.yaml

if [ ! -f "$CONFIG_EXAMPLE" ]; then
  cp "$CONFIG_EXAMPLE" "$CONFIG" || echo 'exist'
fi

echo "[Installser] Install Reqirments"
pip install -r requirements.txt

echo "[Installser] Create link in main menu"
link="/home/$USER/.local/share/applications/Paya.desktop"
path=$(pwd)
touch "$link"
cat <<EOF >"$link"
[Desktop Entry]
Type=Application
Version=1.0
Name=Paya
Comment=radio in tray
Exec=./start.sh
Terminal=false
Path=$path
Icon=$path/backend/assets/icon.png
EOF

echo "[Installser] Done "
