#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains helper functions and functions that control calls to database query functions residing in DB_Queries(DBQ). 

Created on Sun May 24 22:25:08 2020

@author: Gavin Leavitt

"""

import time
from geojson import Point, Feature, FeatureCollection, LineString, dumps
from application import DB_Queries as DBQ
from application import script_config as dbconfig
from geoalchemy2.shape import to_shape
from flask.json import jsonify
from shapely.geometry import mapping

def string_to_none(x):
    """
    Evaluates incoming value to convert empty strings, '', into None types.
    Postgres/SQLAlchemy doesn't handle empty strings well when inputting data into a int or float column.

    Parameters
    ----------
    x : String
        String to be inserted into DB.

    Returns
    -------
    x : String
        String or None value.

    """
    
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
    date_today = time.strftime('%Y-%m-%d', time.localtime(int(timestamp_e)))
    result = {"timestamp_e":timestamp ,"timestart":start_time,"Date":date_today}
    return result

def queries(geomdat):
    """
    Takes Flask API HTTP POST GPS data and issues pre-defined SQLAlchemy database query functions.
    Data is returned in a dict format that is prepared for insertion into the gps activity database table.

    Parameters
    ----------
    geomdat : String
        WKT representation of the incoming GPS point coordinates.
        
        *I created this before I understood  how to better work with coordinates in queries,
        this can possibly be improved in the future but is functional for now. 

    Returns
    -------
    res : Dictonary
        Dictonary with results of database queries, with the following keys:
            POI, City, county, road, dist_road, trail, and dist_trail.
        Empty result values are returned as None, a database friendy format.

    """
    # Build a dict with DB query results
    res = {}
    res["AOI"] = DBQ.AOI_I_Q(geomdat)
    res['city'] = DBQ.city_I_Q(geomdat)
    res["county"] = DBQ.county_I_Q(geomdat)
    roadinfo = DBQ.nearestroad(geomdat)
    res["road"] = roadinfo["street"]
    res["dist_road"] = roadinfo["distance"]
    # Check if the AOI intersection returned a result in the AOI list, if so calcuate the nearest trail and distance to trail
    if res["AOI"] in dbconfig.settings["AOI_Outdoors"]:
        outdoors = DBQ.nearesttrail(geomdat)
        res["trail"]=outdoors['trail']
        res['dist_trail']=outdoors['trail_distance']
    else:
        res['trail'],res['dist_trail']=None,None
    return res 

def to_geojson(recLimit,dataType):   
    """
    Queries spatial tables in Postgres database and returns the most recent records formatted as a geojson feature collection 
    (which contains geometries and properties). This function is reliant on the "geojson" library, I am unclear if this is 
    needed to return a geojson result as either a feature or a feature collection. The flask function jsonify may be able to 
    return a geojson result if the data are formatted properly. 
    
    *This method to generate a geojson feature collection uses shapely to create the individual geojson feature objects, however 
    I later discovered that I can use the geojson library to generate everything as seen in the "waterQualGeoJSON" function, 
    that method is likely better as it requires one less installed library, I will consider rewriting this to follow that method
    
    ##TODO:
    
    Build out to use reclimit to provide a dynamic number of results as requested in a URL query string.
    Rewrite to remove depenance on shapely 
    Rewrite to condense code and handle linestring/points at the same time
    
    Parameters
    ----------
    recLimit: Int
        Int of records to return, hard coded in a upstream function
        
    dataType: String
        Type of data to return, "gpspoints" or "gpstracks", used to control output type, linestring or point
        * I may be able to condense code and remove this variable 
    
    Returns
    -------
    feature_collection : geojson feature collection
        Geojson feature collection containing all queried records and all associated properties stored in Postgres
    """
    features = []
    #Get records from database to be converted to geojson.
    #TODO:
    # Clean up to one line when rewriting 
    dbres = DBQ.getrecords(recLimit,dataType)
    dbdat = dbres["dict"]

    for key in dbdat.keys():
        # Pop unnecessary entries, they don't convert to json properly, but the geom WKB element is needed, make it a variable before popping off
        dbdat[key].pop('_sa_instance_state')
        geom = dbdat[key]['geom']
        dbdat[key].pop('geom')
        # Format records as a list of geojson filters, dependaing on which GET request was sent
        if dataType == "gpspoints":
            print("Making gps point result!")
            geometryDat = Point((float(dbdat[key]['lon']), float(dbdat[key]['lat'])))
            # print(f"point ojbect: {geometryDat}")
            features.append(Feature(geometry=geometryDat, properties=dbdat[key]))
        elif dataType == "gpstracks":
            # to_shape is a geoalchemy method that converts a geometry to a shapely geometry
            # mapping is a shapely method that converts a geometry to a geojson object, a dictonary with formatted geom type and coordinates 
            geometryWKT = mapping(to_shape(geom))
            # Take the geojson formated geom and create a geojson feature with it and the rest of the record properties, add to list of features
            features.append(Feature(geometry=geometryWKT, properties=dbdat[key]))

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

def handleBeaches():
    """
    Handles calling database water quality queries and function to generate geojson results.

    Returns
    -------
    geojson_res : geojson feature collection object
        Water quality test results as a geojson feature collection object. This contains geometry and properties 
        of all queried records in a form that can be passed straight into Leaflet geojson. 
        
    """
    # Call database query to get most recent test results
    beach_results = DBQ.getBeachWaterQual()
    # geojson_dump = dumps(waterQualGeoJSON(beach_results))
    # Format results into geojson
    geojson_res = waterQualGeoJSON(beach_results)
    return geojson_res

def waterQualGeoJSON(records):
    """
    Processes water quality query results into a geojson Feature Collection.
    
    Parameters
    ----------
    records : List
        Nested lists containing SQL Alchemy query results: 
            3 query result objects:
                waterQuality, waterqualityMD5 beaches
            1 string: 
                geometry type of associated beach 
            2 floats: 
                x and y coordinates of the associated beach  

    Returns
    -------
    featCollect : Geojson feature collection object
        Most recent water quality results per beach, one result per beach, as a geojson.

    """ 
    resultDict = {}
    for i, item in enumerate(records):
        # print(i.waterQuality.id, i.waterQuality.FecColi, i.waterQuality.beach_rel.BeachName, i.waterQuality.beach_rel.geom)
        #print(i.waterQuality.id, i.waterQuality.FecColi, i.waterQuality.beach_rel.BeachName)
        # print(item.waterQuality.beach_rel.BeachName, item.waterQuality.FecColi, test[i][-1], test[i][-2])
        beachname = (item.waterQuality.beach_rel.BeachName)
        resultDict[beachname] = {}
        resultDict[beachname]['FecColi'] = item.waterQuality.FecColi
        resultDict[beachname]['TotColi'] = item.waterQuality.TotColi
        resultDict[beachname]['Entero'] = item.waterQuality.Entero
        resultDict[beachname]['ExceedsRatio'] = item.waterQuality.ExceedsRatio
        resultDict[beachname]['BeachStatus'] = (item.waterQuality.BeachStatus).rstrip()
        resultDict[beachname]['resample'] = (item.waterQuality.resample).rstrip()
        resultDict[beachname]['insDate'] = (item.waterQuality.hash_rel.insdate).strftime("%Y-%m-%d")
        resultDict[beachname]['pdfDate'] = (item.waterQuality.hash_rel.pdfdate).strftime("%Y-%m-%d")
        resultDict[beachname]['GeomType'] = (records[i][-3]).split("ST_")[1]
        resultDict[beachname]['Lon'] = round(records[i][-2], 5)
        resultDict[beachname]['Lat'] = round(records[i][-1], 5)
        resultDict[beachname]['Name'] = (item.waterQuality.beach_rel.BeachName).rstrip()
    featList = []
    for key in resultDict.keys():
        # Point takes items as long, lat Point must have (())
        beachPoint = Point((resultDict[key]['Lon'], resultDict[key]['Lat']))
        feature = Feature(geometry=beachPoint, properties=resultDict[key])
        featList.append(feature)

    featCollect = FeatureCollection(featList)
    return featCollect


    
