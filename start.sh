#!/bin/bash
source ./venv/bin/activate
export PYTHONDONTWRITEBYTECODE=1
export KIVY_NO_ARGS=1

IP=$(ip route get 1.2.3.4 | awk '{print $7}')
PORT=$(cat config/config.yaml | shyaml get-value backend.port)

if [[ "$IP" == "" ]]; then
  IP='127.0.0.1'
fi

gunicorn --paste config/paya_server.ini --timeout 9999999 -b $IP:$PORT
