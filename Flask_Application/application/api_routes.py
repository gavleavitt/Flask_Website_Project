#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This module contains the Flask API URL functions that grant access to the Postgres AWS RDS database through calls to functions in other application modules. 
These URLs are called by the GPS Tracking Dashboard and other scripts.
Users will not directly visit these URLs.  

Created on Fri May 22 17:45:44 2020

@author: Gavin Leavitt
"""
from application import app, application, models, db
from application import functions as func
from application import objectgeneration as OBG
from application.authentication import auth
from flask import request
from flask import jsonify
import sys


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
            print("Hit server with POST request and valid json mime type!",file=sys.stdout)
            data = request.get_json()
            print("Request data has been fetched!",file=sys.stdout)            
            #Create a new dict to hold new objects that will be added to PostGresSQL
            newObjDict = {}
            trackrecord = OBG.gpstrackobj(data)
            #Check if there has been movement, if so add to new object dictionary, otherwise no entry will be made
            if trackrecord["activity"] == "Yes":
                newObjDict["track"] = trackrecord["model"]
            #Add new gps record object to new objects dictionary
            newObjDict["gpspoint"] = OBG.newgpsrecord(data,trackrecord["activity"])
            print(newObjDict["gpspoint"].__dict__)
            #Iterate over new objdict, can allow building out so many things can be commited to db
            #This allows for empty models to be skipped
            newObjs = []
            for obj in newObjDict.keys():
                newObjs.append(newObjDict[obj])
            # Add new objects to session and commit them
            db.session.add_all(newObjs)
            db.session.commit()
            print("Data added and committed to postgres!",file=sys.stdout)
            # Return a json success code
            resp = jsonify(success=True)
            return resp
            #return {"message": f"GPS entry {newrecord.date} has been created successfully."}
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
      
    ##TODO:
    Build to return as many points as requested using query strings.

    Returns
    -------
    result : geojson
        Geojson representation of the gps point spatial data.

    """
    print("Hit with a point get request!")
    result = func.to_geojson(recLimit = 1, dataType = "gpspoints")
    return result

@app.route("/api/v0.1/gettracks", methods=['GET'])
@auth.login_required(role='viewer')
def get_trackgeojson():
    """
    Handles HTTP GET requests of GPS tracks, this is hard coded in the DB query helper function to only query the records for the same day.
    
    Requires at least viewer authentication.
    
    ##TODO:
    Build to return as many tracks as requested using query strings.

    Returns
    -------
    result :  geojson
        Geojson representation of the gps tracks spatial data

    """
    print("Hit with a get request!")
    result = func.to_geojson(recLimit = "all", dataType = "gpstracks")
    return result
