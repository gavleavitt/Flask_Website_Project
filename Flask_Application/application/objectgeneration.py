#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module creates the SQLAlchemy objects that will be added to the Postgres session by calling on the appropriate functions. 
No functions in this module commit these objects to the database. 

Created on Mon Jun 22 19:29:11 2020

@author: Gavin Leavitt
"""

from application import app, models, db
from application import functions as func
from application import script_config as dbconfig

def gpstrackobj(data):
    """
    Return activity status and a new track record if movement has been detected.
    This is a higher level function for generating a new track object and calls on helper functions residing within the functions module. 
    Movement status is based on whether or not the gps record has moved > 3 m, or 10 feet. 

    Parameters
    ----------
    data : Dict
        Dictionary of POST JSON data.

    Returns
    -------
    data: Dict
        Dict containing the gps track object (to be inserted into DB) and activity status (yes/no).

    """
    coordinates = (f"{data['Longitude']} {data['Latitude']}")
    times = func.converttime(data['Timestamp'],data['Start_timestamp'])
    tracks = func.handletracks(coordinates, times["Date"], data['Provider'])
    print(f"!! tracks result is: {tracks}")
    if tracks["activity"] == "Yes":
        model = models.gpstracks(timestamp_epoch= times['timestamp_e'],timeutc=data['Time_UTC'],date=times["Date"],
                                 startstamp=times['timestart'],androidid=data['Android_ID'],serial=data['Serial'],
                                 profile=data['Profile'],length=tracks['length'], gpsid=None, geom=tracks['Linestring'])
    else:
        model = None
    return {"model":model,"activity":tracks["activity"]}
    

def newgpsrecord(data,actStatus):    
    """
    

    Parameters
    ----------
    data : Dict
        Dictionary of POST JSON data.
    actStatus : String
        Activity status, yes/no.

    Returns
    -------
    model: Object
        gpsdatmodel object containing data to be inserted into DB.

    """
    geomdat = (f"SRID={dbconfig.settings['srid']};POINT({data['Longitude']} {data['Latitude']})")
    querydat = func.queries(geomdat)
    times = func.converttime(data['Timestamp'],data['Start_timestamp'])
    model = models.gpsdatmodel(lat=data['Latitude'], lon=data['Longitude'], satellites=int(data['Satellites']),
        altitude=float(data['Altitude']), speed=float(data['Speed']),accuracy=data['Accuracy'].split(".")[0],
        direction=data['Direction'].split(".")[0], provider=data['Provider'],
        timestamp_epoch= times['timestamp_e'], timeutc=data['Time_UTC'],date=times['Date'], startstamp=times['timestart'],
        battery=data['Battery'].split(".")[0], androidid=data['Android_ID'],serial=data['Serial'], profile=data['Profile'].replace("+"," "),
        hhop=func.string_to_none((data['hdop'])), vdop=func.string_to_none((data['vdop'])), pdop=func.string_to_none((data['pdop'])),
        activity = actStatus,travelled=data['Dist_Travelled'].split(".")[0],
        AOI = querydat['AOI'], city = querydat['city'], county = querydat['county'], nearestroad = querydat['road'], dist_nearestroad = querydat['dist_road'],
        nearesttrail = querydat['trail'], dist_nearesttrail = querydat['dist_trail'],
        geom=geomdat)
    return model