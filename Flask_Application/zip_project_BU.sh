#!/bin/bash
zip -r flaskdeployment.zip . -x ".*" __pycache__/\* \*.zip migrations/\* application/__pycache__/\* *zip*