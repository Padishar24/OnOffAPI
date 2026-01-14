#!/usr/bin/env bash
set -e
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/run/user/1000
#mkdir -p "$XDG_RUNTIME_DIR"
#chmod 700 "$XDG_RUNTIME_DIR"

#source "/opt/python3-flask-env/bin/activate"
source /home/pi/OnOffAPI/.venv/bin/activate
python3 -u /home/pi/OnOffAPI/rest_api.py
