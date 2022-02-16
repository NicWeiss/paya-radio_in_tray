#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1

IP=$(ip route get 1.2.3.4 | awk '{print $7}')
PORT=$(cat config/config.yaml | shyaml get-value backend.port)

if [[ "$IP" == "" ]]; then
  IP='127.0.0.1'
fi

gunicorn --paste config/server.ini --timeout 9999999 -b $IP:$PORT
