#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:25:08 2020

@author: gavinl

This module contains helper functions and functions that control calls to database query functions residing in DB_Queries(DBQ). 
"""
import time
from geojson import Point, Feature, FeatureCollection, LineString
from application import DB_Queries as DBQ
from application import script_config as dbconfig
from geoalchemy2.shape import to_shape
from flask.json import jsonify
from shapely.geometry import mapping

def string_to_none(x):
    if x == '':
        return None
    else:
        return x
    
def converttime(timestamp_e,timestart):
    """
    Converts times that are received in the http POST into a dict of times that are formatted to local time.

    Parameters
    ----------
    timestamp_e : UTC Time(since epoch)
        timestamp for the current record.
    timestart : UTC Time(since epoch)
        start timestamp of the current recording session.

    Returns
    -------
    result : dict{} with keys "timestamp_e","timestart"
        Times converted to local time from UTC. 

    """
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp_e)))
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestart)))
    result = {"timestamp_e":timestamp ,"timestart":start_time}
    return result

def queries(geomdat):
    """
    Takes Flask API HTTP POST GPS data and issues pre-defined SQLAlchemy database query functions.
    Data is returned in a dict format that is prepared for insertion into the gps activity database table.

    Parameters
    ----------
    geomdat : TYPE
        DESC

    Returns
    -------
    res : Dictonary
        Dictonary with results of database queries, with the following keys:
            POI, City, county, road, dist_road, trail, and dist_trail.
        Empty result values are returned as None, a database friendy format.

    """
    
    res = {}
    res["POI"] = DBQ.POI_I_Q(geomdat)
    res['city'] = DBQ.city_I_Q(geomdat)
    res["county"] = DBQ.county_I_Q(geomdat)
    roadinfo = DBQ.nearestroad(geomdat)
    res["road"] = roadinfo["street"]
    res["dist_road"] = roadinfo["distance"]
    if res["POI"] in dbconfig.settings["POI_Outdoors"]:
        outdoors = DBQ.nearesttrail(geomdat)
        res["trail"]=outdoors['trail']
        res['dist_trail']=outdoors['trail_distance']
    else:
        res['trail'],res['dist_trail']=None,None
    return res 
def to_geojson(recLimit,dataType):   
    """
    Queries gps table in POSTGRES database and returns the most recent record formated as geojson.
    Consider expanding to incldue a variable for number of records to return.

    Returns
    -------
    feature_collection : geojson feature collection
        DESCRIPTION.

    """
    features = []
    #Get records from database to be converted to geojson.
    dbres = DBQ.getrecords(recLimit,dataType)
    dbdat = dbres["dict"]

    for key in dbdat.keys():
        #Pop unnecessary entries, they don't convert to json properly, but the geom WKB element is needed, make it a variable before popping off
        dbdat[key].pop('_sa_instance_state')
        geom = dbdat[key]['geom']
        dbdat[key].pop('geom')
        #Format records as a list of geojson filters, dependaing on which GET request was sent 
        if dataType == "gpspoints":
            print("Making gps point result!")
            geometryDat = Point((float(dbdat[key]['lon']), float(dbdat[key]['lat'])))
            #print(f"point ojbect: {geometryDat}")
            features.append(Feature(geometry=geometryDat, properties=dbdat[key]))
        elif dataType == "gpstracks":
            # print("Making  gps track result!")
            #to_shape is a geoalchemy method that converts a geometry to a shapely geometry
            #mapping is a shapely method that cnverts a geometry to a geojson object, a dictonary with formatted geom type and coordinates 
            geometryWKT = mapping(to_shape(geom))
            #take the geojson formated geom and create a geojson feature with it and the rest of the record properties, add to list of features
            features.append(Feature(geometry=geometryWKT, properties=dbdat[key]))
            # print(b)
            #Convert WKT to a list of coordinates that can be inputted in LineString
            # geometryliststr = geometryWKT.replace("(","").replace(")","").replace("LINESTRING ","").split(", ")
            # for i in geometryliststr:
            #     a = i.split(" ")
            #     for coor in a:
            #         coor = float(coor)
            # #print(f"!! Attributes to be used for geom: {dbdat[key][1]['geojson_geom']}")
            # features.append(Feature(geometry=dbdat[key][1]['geojson_geom'], properties=dbdat[key][0]))
    #Take list of geojson formatted features and convert to geojson FeatureCollection object 
    feature_collection = FeatureCollection(features)
    return feature_collection
    

def handletracks(coordinate2, datetoday, locationtype):
    """
    Determines if the incoming record is the first of the day, which returns no activty, then determines if movement has occured between 
    the incoming record and most recent record for the day. Movement is determined if the distance is greater than 3m, or 10ft, between points.
    Returns a dict of movement status and a linestring, if movement has occurred, for the trackrecord model and insertion into postgres.  

    Parameters
    ----------
    coordinate2 : string
        Incoming gps point in the form of "lon lat".
    datetoday : string
        Date (local time) of incoming gps point, in the form of "YYYY-MM-DD"

    Returns
    -------
    dict
        keys:
            "activty":movement status as "Yes" or "No"
            "Linestring": Only created if movement status is "Yes". Contains the WKT string representation of "LINESTRING" for input in PostGIS 
                model geometry column
                
    """
    record = DBQ.getpathpointrecords(datetoday)
    print(f"!!!! Record result is: {record}")
    #check if a previous record exists, if not then this is the first record of the day and no movement could have occurred
    if record != None:
        #Convert keys to list
        recid = list(record.keys())
        #Reverse sort keys, list[0] is the key, gpsdat id, of the most recent record
        recid.sort(reverse=True)
        #format data to be sent to geoalchemy functions as WKT
        #Previous record, pulled from postgres and formatted in WKT
        coor1_Q_str = (f"POINT({record[recid[0]]['lon']} {record[recid[0]]['lat']})")
        #Incoming record
        coor2_Q_str = (f"POINT({coordinate2})")
        dist = DBQ.getdist(coor1_Q_str,coor2_Q_str)
        if (dist > 10 and locationtype != 'network') or dist > 100:
            print("Movement!")
            #Movement greater than 10m, returns dictonary with linestring formmated WKT record and activity type
            return {'Linestring':f'SRID={dbconfig.settings["srid"]};LINESTRING({record[recid[0]]["lon"]} {record[recid[0]]["lat"]}, {coordinate2})',"activity":"Yes","length":dist}  
        else:
            return {"activity":"No"}
    else:
        #No previous record, first of the day thus no movement, or no movement greater than 10 feet since last record
        print("No movement!")
        return {"activity":"No"}