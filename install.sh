#!/bin/bash

pacman -S xclip xsel

CONFIG_EXAMPLE=./config/config.example
CONFIG=./config/config.yaml

if [ ! -f "$CONFIG_EXAMPLE" ]; then
  cp "$CONFIG_EXAMPLE" "$CONFIG"
fi

echo "[Installser] Install Reqirments"
pip install -r requirements.txt

echo "[Installser] Create link in main menu"
link="/home/$USER/.local/share/applications/Ya.Radio_by_NWeiss.desktop"
path=$(pwd)
touch "$link"
cat <<EOF >"$link"
[Desktop Entry]
Type=Application
Version=1.0
Name=Ya.Radio by NWeiss
Comment=Ya.Radio by NWeiss
Exec=./start.sh
Terminal=false
Path=$path
Icon=$path/backend/assets/icon.png
EOF

echo "[Installser] Done "
