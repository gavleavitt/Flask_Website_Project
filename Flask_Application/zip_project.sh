#!/bin/bash
zip -r flaskdeployment.zip . -x ".flaskenv" ".env"  __pycache__/\* \*.zip migrations/\* application/__pycache__/\* *zip*