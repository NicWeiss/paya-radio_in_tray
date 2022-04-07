#!/bin/bash

echo "[Installser] Install Reqirments"
pip install -r requirements.txt

echo "[Installser] Create link in main menu"
link="/home/$USER/.local/share/applications/Ya.Radio by NWeiss.desktop"
touch "$link"
cat <<EOF > "$link"
[Desktop Entry]
Type=Application
Version=1.0
Name=Ya.Radio by NWeiss
Comment=Ya.Radio by NWeiss
Exec=./start.sh
Terminal=false
Path=/home/$USER/scripts/python/yaradio/
Icon=/home/$USER/scripts/python/yaradio/backend/assets/icon.png
EOF


echo "[Installser] Done "
