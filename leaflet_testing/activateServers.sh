#!/usr/bin/env bash
lxterminal -e python3 ./server.py &
lxterminal -e python3 /media/sf_OSGeoLive_Shared/MTB_Tracking/leaflet_testing/python/GoogleDriveGPSListening.py &
lxterminal -e geoserver_start.sh &
/bin/bash
