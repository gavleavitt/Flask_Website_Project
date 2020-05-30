#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 17:45:44 2020

@author: user
"""
from application import app, models, db
from application import authentication as authmod
from application import functions as func
from flask import request
from flask import jsonify
from flask import make_response
import sys
import json
from sqlalchemy import Date
import time
from application import script_config as dbconfig
from application import DB_Queries as DBQ
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/gpsdat", methods=['POST'])
@authmod.auth.login_required(role='admin')
def handle_gps():
    if request.method == 'POST':
        if request.is_json:
            print("Hit server with POST request and valid json mime type!",file=sys.stdout)
            #data = request.get_json(force = True)
            data = request.get_json()
            print("Request data has been fetched!",file=sys.stdout)
            geomdat = (f"SRID={dbconfig.settings['srid']};POINT({data['Longitude']} {data['Latitude']})") 
            times = func.converttime(data['Timestamp'],data['Start_timestamp'])
            #intersects = DBQ.POI_I_Q(geomdat)
            #print (f"Intersection test: {intersects}")
            querydat = DBQ.queries(geomdat)
            newrecord = models.gpsdatmodel(lat=data['Latitude'], lon=data['Longitude'], satellites=int(data['Satellites']), 
                altitude=float(data['Altitude']), speed=float(data['Speed']),accuracy=data['Accuracy'].split(".")[0], 
                direction=data['Direction'].split(".")[0], provider=data['Provider'],
                timestamp_epoch= times['timestamp_e'], timeutc=data['Time_UTC'],date=data['Date'], startstamp=times['timestart'], 
                battery=data['Battery'].split(".")[0], androidid=data['Android_ID'],serial=data['Serial'], profile=data['Profile'],
                hhop=func.string_to_none((data['hdop'])), vdop=func.string_to_none((data['vdop'])), pdop=func.string_to_none((data['pdop'])),
                activity = data['Activity'],travelled=data['Dist_Travelled'].split(".")[0],
                POI = querydat['POI'], city = querydat['city'], county = querydat['county'], nearestroad = querydat['road'], dist_nearestroad = querydat['dist_road'],
                nearesttrail = querydat['trail'], dist_nearesttrail = querydat['dist_trail'],
                geom=geomdat)
            print(newrecord.__dict__)
            db.session.add(newrecord)
            db.session.commit()
            print("Data added and committed to postgres!",file=sys.stdout)
            resp = jsonify(success=True)
            return resp
            #return {"message": f"GPS entry {newrecord.date} has been created successfully."}
        else:
            print("Got a POST request but the payload isnt in JSON!", file=sys.stdout)
            return {"error": "The request payload is not in JSON format"}
    

@app.route("/getgeojson", methods=['GET'])
@authmod.auth.login_required(role='viewer')
def get_geojson():
    print("Hit with a get request!")
    result = func.to_geojson()
    return result