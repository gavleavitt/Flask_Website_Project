#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This module contains the Flask API URL functions that grant access to the Postgres AWS RDS database through calls to functions in other application modules. 
These URLs are called by the GPS Tracking Dashboard and other scripts.
Users will not directly visit these URLs.  

Created on Fri May 22 17:45:44 2020

@author: Gavin Leavitt
"""
from application import app, application, models_tracker, db, StravaWebHook, logger, DB_Queries_Strava, getStravaActivities
from application import functions as func
from application import DB_Queries as DBQ
from application import DB_Queries_Strava as DQS
from application import objectgeneration_tracker as OBG
from application.authentication import auth
from flask import request, Response
from flask import jsonify
import sys
from application import script_config
from application import stravaAuth
import os



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
    if request.method == 'POST':
        if request.is_json:
            print("Hit server with POST request and valid json mime type!", file=sys.stdout)
            data = request.get_json()
            print("Request data has been fetched!", file=sys.stdout)
            # Create a new dict to hold new objects that will be added to PostGresSQL
            newObjDict = {}
            trackrecord = OBG.gpstrackobj(data)
            # Check if there has been movement, if so add to new object dictionary, otherwise no entry will be made
            if trackrecord["activity"] == "Yes":
                newObjDict["track"] = trackrecord["model"]
            # Add new gps record object to new objects dictionary
            newObjDict["gpspoint"] = OBG.newgpsrecord(data, trackrecord["activity"])
            print(newObjDict["gpspoint"].__dict__)
            # Iterate over new objdict, can allow building out so many things can be commited to db
            # This allows for empty models to be skipped
            newObjs = []
            for obj in newObjDict.keys():
                newObjs.append(newObjDict[obj])
            # Add new objects to session and commit them
            db.session.add_all(newObjs)
            db.session.commit()
            print("Data added and committed to postgres!", file=sys.stdout)
            # Return a json success code
            resp = jsonify(success=True)
            return resp
            # return {"message": f"GPS entry {newrecord.date} has been created successfully."}
        else:
            # POST request is not in json, return error 
            print("Got a POST request but the payload isnt in JSON!", file=sys.stdout)
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
    print("Hit with a point get request!")
    result = DBQ.getFeatCollection(reclimit=1, datatype="gpspoints")
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
    print("Hit with a gpstrack get request!")
    result = DBQ.getFeatCollection(reclimit="all", datatype="gpstracks")
    return result





@app.route(script_config.strava_callback_url, methods=['GET', 'POST'])
def handle_sub_callback():
    """
    Handles requests to Strava subscription callback URL.

    GET:
        Webhoook Subscription Creation Process:
            CallbackURL is sent a GET request containing a challenge code. This code is sent back to requester to verify
            the callback.

             The initial request to create a new webhook subscription, called by visiting URL containing
             handle_Create_Strava_Sub(), is then provided with verification creation and the new subscription ID.
    POST:
        Webhook subscription update message. Sent when a activity on a subscribed account is created, updated, or deleted,
        or when a privacy related profile setting is changed.

        All update messages are inputted into Postgres.

        Currently, only activity creation events are handled, additional development is needed to handle other events.

    Returns
    -------
    GET request:
        JSON, echoed Strava challenge text.
    POST request:
        Success code if data are successfully added to Postgres/PostGIS. Strava must receive a 200 code in response to
        POST.
    """
    application.logger.debug("Got a callback request!")
    # Get application access credentials
    client = stravaAuth.gettoken()
    # Get request as part of new subscription creation process
    if request.method == 'GET':
        application.logger.debug("Got a GET callback request from Strava to verify webhook!")
        # Extract challenge of verification token
        callBackContent = request.args.get("hub.challenge")
        callBackVerifyToken = request.args.get("hub.verify_token")
        # Form callback response as dict
        callBackResponse = {"hub.challenge": callBackContent}
        # Check if tokens match, i.e. if GET request is from Strava
        if callBackVerifyToken == os.getenv('STRAVA_VERIFY_TOKEN'):
            try:
                application.logger.debug(f"Strava callback verification succeeded, responding with the challenge code"
                                         f" message {callBackResponse}")
                # Return challenge code as dict. Using Flask API automatically converts it to JSON with HTTP 200 success
                # code
                return callBackResponse
            except Exception as e:
                application.logger.error(f"Strava callback verification failed with the error {e}")
                return Response(status=500)
        else:
            application.logger.error(f"Strava verification token doesn't match!")
            raise ValueError('Strava token verification failed.')
            return Response(status=500)
    # POST request containing webhook subscription message
    elif request.method == 'POST':
        application.logger.debug("New activity incoming! Got a POST callback request from Strava")
        try:
            # Convert JSON body to dict
            callbackContent = request.get_json()
            # application.logger.debug(f"Update content is {callbackContent}")
            # application.logger.debug(f"Update content dir is {dir(callbackContent)}")
            # Call function to handle update message and new activity
            StravaWebHook.handle_sub_update(client, callbackContent)
            application.logger.debug("Inserted webhook update and activity details into postgres tables!")
            # return success code, Strava expects this code
            return Response(status=200)
        except Exception as e:
            application.logger.error(f"Strava subscription update failed with the error {e}")
            return Response(status=500)

@app.route("/api/v0.1/stravaroutes", methods=['GET'])
def stravaActAPI():
    actLimit = int(request.args.get("actlimit"))
    res = DQS.getStravaMaskedActGeoJSON(actLimit)
    return res
