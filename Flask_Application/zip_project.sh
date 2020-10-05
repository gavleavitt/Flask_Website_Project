#!/bin/bash
zip -r flaskdeployment.zip . -x ".flaskenv" "zip_project_windows.bat" ".env"  __pycache__/\* \*.zip migrations/\* application/__pycache__/\* *zip*