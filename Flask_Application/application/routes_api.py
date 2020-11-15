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
from flask import request, Response
from flask import jsonify
from application import script_config
from application.projects.location_tracker import DBQueriesTracker, objectGenerationTracker
from application.flaskAuth.authentication import auth
from application.projects.strava_activities import WebHookFunctionsStrava, DBQueriesStrava

# @app.route establishes the URL within the domain
# @auth.login_required sets up basic http auth for the URL and role sets the user level needed to access the URL
@app.route("/api/v0.1/postgpsdata", methods=['POST'])
@auth.login_required(role='admin')
def handle_gps():
    """
    Handles incoming GPS HTTP POST requests by kicking off the workflow to process ancillary data, 
    generate models, and commit new data to the DB.
   
    Requires admin level access.
    -------
    TYPE
        JSON response code, success or error.

    """
    # print("Hit with a post request!")
    if request.method == 'POST':
        if request.is_json:
            # print("Hit server with POST request and valid json mime type!", file=sys.stdout)
            data = request.get_json()
            # print(data)
            objectGenerationTracker.handleTrackerPOST(data)
            # Return a json success code
            resp = jsonify(success=True)
            return resp
            # return {"message": f"GPS entry {newrecord.date} has been created successfully."}
        else:
            # POST request is not in json, return error 
            # print("Got a POST request but the payload isnt in JSON!", file=sys.stdout)
            return {"error": "The request payload is not in JSON format"}


@app.route("/api/v0.1/getpoint", methods=['GET'])
@auth.login_required(role='viewer')
def get_pointgeojson():
    """
    Handles HTTP GET requests of GPS points, kicks off the process to generate and return a geoson GPS data point.
    
    Currently this is hard coded to return only the most recent point.
    
    Requires at least viewer authentication

    Returns
    -------
    result : geojson
        Geojson representation of the gps point spatial data.

    """
    # print("Hit with a point get request!")
    result = DBQueriesTracker.getTrackerFeatCollection(reclimit=1, datatype="gpspoints")
    return result


@app.route("/api/v0.1/gettracks", methods=['GET'])
@auth.login_required(role='viewer')
def get_trackgeojson():
    """
    Handles HTTP GET requests of GPS tracks, this is hard coded in the DB query helper function to only query the records for the same day.
    
    Requires at least viewer authentication.

    Returns
    -------
    result :  geojson
        Geojson representation of the gps tracks spatial data

    """
    # print("Hit with a gpstrack get request!")
    result = DBQueriesTracker.getTrackerFeatCollection(reclimit="all", datatype="gpstracks")
    return result


@app.route(script_config.strava_callback_url, methods=['GET', 'POST'])
def subCallback():
    """
    Strava subscription callback URL.

    Returns
    -------
    GET request:
        JSON, echoed Strava challenge text.
    POST request:
        Success code if data are successfully added to Postgres/PostGIS. Strava must receive a 200 code in response to
        POST.
    """
    application.logger.debug("Got a callback request!")
    statusCode = WebHookFunctionsStrava.handleSubCallback(request)
    application.logger.debug("Callback request has been handled, returning success code!")
    return Response(status=statusCode)

@app.route("/api/v0.1/stravaroutes", methods=['GET'])
def stravaActAPI():
    actLimit = int(request.args.get("actlimit"))
    res = DBQueriesStrava.getStravaMaskedActGeoJSON(actLimit)
    return res
