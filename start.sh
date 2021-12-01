#!/bin/bash

gunicorn --paste settings.ini --timeout 9999999 -b 127.0.0.1:7778
