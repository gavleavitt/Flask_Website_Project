#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 17:45:44 2020

@author: user
"""
from application import app, models, db
from application import functions as func
from application import objectgeneration as OBG
from application.authentication import auth
from flask import request
from flask import jsonify
#from flask import make_response
import sys
#from sqlalchemy import Date
#import time
from application import script_config as dbconfig
from application import DB_Queries as DBQ
#from flask_httpauth import HTTPBasicAuth
#from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/gpsdat", methods=['POST'])
@auth.login_required(role='admin')
def handle_gps():
    """
    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if request.method == 'POST':
        if request.is_json:
            print("Hit server with POST request and valid json mime type!",file=sys.stdout)
            data = request.get_json()
            print("Request data has been fetched!",file=sys.stdout)            
            #Create a new dict to hold new objects that will be added to PostGresSQL
            newObjDict = {}
            trackrecord = OBG.gpstrackobj(data)
            #Check if there has been movement, if so add to new object dictonary, otherwise no entry will be made
            if trackrecord["activity"] == "Yes":
                newObjDict["track"] = trackrecord["model"]
            #Add new gps record object to new objects dictonary
            newObjDict["gpspoint"] = OBG.newgpsrecord(data,trackrecord["activity"])
            print(newObjDict["gpspoint"].__dict__)
            #Iterate over new objdict, can allow building out so many things can be commited to db
            #This allows for empty models to be skipped
            newObjs = []
            for obj in newObjDict.keys():
                newObjs.append(newObjDict[obj])          
            db.session.add_all(newObjs)
            db.session.commit()
            print("Data added and committed to postgres!",file=sys.stdout)
            resp = jsonify(success=True)
            return resp
            #return {"message": f"GPS entry {newrecord.date} has been created successfully."}
        else:
            print("Got a POST request but the payload isnt in JSON!", file=sys.stdout)
            return {"error": "The request payload is not in JSON format"}


@app.route("/api/v0.1/getgeojson", methods=['GET'])
@auth.login_required(role='viewer')
def get_pointgeojson():
    """


    Returns
    -------
    result : TYPE
        DESCRIPTION.

    """
    print("Hit with a point get request!")
    result = func.to_geojson(recLimit = 1, dataType = "gpspoints")
    return result

@app.route("/api/v0.1/gettracks", methods=['GET'])
@auth.login_required(role='viewer')
def get_trackgeojson():
    """


    Returns
    -------
    result : TYPE
        DESCRIPTION.

    """
    print("Hit with a get request!")
    result = func.to_geojson(recLimit = "all", dataType = "gpstracks")
    return result
