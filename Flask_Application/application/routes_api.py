#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This module contains the Flask API URL functions that grant access to the Postgres AWS RDS database through calls to functions in other application modules. 
These URLs are called by the GPS Tracking Dashboard and other scripts.
Users will not directly visit these URLs.  

Created on Fri May 22 17:45:44 2020

@author: Gavin Leavitt
"""
from application import app, application
from flask import request, Response, copy_current_request_context
from flask import jsonify
from application.WebAppProjects.location_tracker import DBQueriesTracker, objectGenerationTracker
from application.flaskAuth.authentication import auth
from application.WebAppProjects.strava_activities import WebHookFunctionsStrava, DBQueriesStrava, StravaAWSS3
from application.WebAppProjects.water_quality import DBQueriesWaterQuality
import os
from threading import Thread

# @app.route establishes the URL within the domain
# @auth.login_required sets up basic http auth for the URL and role sets the user level needed to access the URL







