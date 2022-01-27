#!/bin/bash

IP=$(ip route get 1.2.3.4 | awk '{print $7}')

if [[ "$IP" == "" ]]; then
  IP='127.0.0.1'
fi

gunicorn --paste settings.ini --timeout 9999999 -b $IP:7778
