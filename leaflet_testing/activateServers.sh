#!/usr/bin/env bash
lxterminal -e python3 ./server.py &
lxterminal -e python3 ./GoogleDriveGPSListening20200429.py &
lxterminal -e geoserver_start.sh &
/bin/bash
