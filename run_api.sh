#!/usr/bin/env bash
set -e
export DISPLAY=:0.0
export XAUTHORITY=/home/pi/.Xauthority
#source "/opt/python3-flask-env/bin/activate"
source /home/pi/OnOffAPI/.venv/bin/activate
python3 -u /home/pi/OnOffAPI/rest_api.py
