#!/bin/bash

gunicorn --paste settings.ini -b 127.0.0.1:7778
