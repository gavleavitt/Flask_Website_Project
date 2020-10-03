#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains PostgresSQL database query functions that are called by the functions and authentication modules.

Created on Mon May 25 17:40:53 2020

@author: Gavin Leavitt


"""
from application import application, models, db
import pytz
from application.models import gpsdatmodel, gpstracks, AOI, CaliforniaPlaces, CACounty, waterQuality, waterQualityMD5, beaches, stateStandards
from application import functions as func
from application import script_config as dbconfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, distinct
from application.models import gpsdatmodel as gpsdat
from sqlalchemy import func as sqlfunc
from datetime import datetime
from flask.json import jsonify
import geojson
from geojson import Point, Feature, FeatureCollection, LineString
# from geoalchemy2.shape import to_shape

def AOI_I_Q(geomdat):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the AOI PostGIS table and returns a string of results.
    
    The AOI table contains hand digitized locations of interest.
    
    Currently only single POI results are returned, however this will change as POIs are added.
    
    Parameters
    ----------
    geomdat : String
        WKT representation of the incoming GPS point coordinates.

    Returns
    -------
    result : String
        AOI results as a string with individual results comma seperated or None in case
            of empty result.
        A comma seperated string is returned for easier processing and insertion into
        dictionary created by the queries function.

    """
    #SQLAlchemy and GeoAlchemy SQL query
    query = db.session.query(models.AOI).filter(models.AOI.geom.ST_Intersects(geomdat))
    #Get the size of the result, used for building out the string result.
    query_count = 0
    for i in query:
        query_count += 1    
    
    if query_count > 0:
        result = ""
        count = 0
        # Iterate over SQL Alchemy result object, if greater than 1 result build out with comma seperation.
        for POI in query:
            if count > 0:
                # result object columns can be individually called with their column names, only want location info.
                result += "," + POI.location
                count += 1
            else:
                result += POI.location
                count += 1
    else:  
      return None
    return result
    
def city_I_Q(geomdat):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the city PostGIS table and returns a string of results.

    Parameters
    ----------
    geomdat : String
        WKT representation of the incoming GPS point coordinates.
        
    Returns
    -------
    result : String
        String of intersecting city or None if empty result.
        Should only ever be a single result but logic is included in case of multiple
        records returned.

    """

    query = db.session.query(CaliforniaPlaces).filter(CaliforniaPlaces.geom.ST_Intersects(geomdat))
    
    query_count = 0
    for i in query:
        query_count += 1    
    # Logic to create a comma separted string of all results in case multiple cities 
    # are returned, this should not happen under normal circumstances 
    if query_count > 0:
        result = ""
        count = 0
        for city in query:
            if count > 0:
                result += "," + city.name
                count += 1
            else:
                result += city.name
                count += 1
    else:
        return None
    return result

def county_I_Q(geomdat):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the county PostGIS table and returns a string of results.

    Parameters
    ----------
    geomdat : String
        WKT representation of the incoming GPS point coordinates.

    Returns
    -------
    TYPE
        String of intersecting city or None if empty result.
        Should only ever be a single result but logic is included in case of multiple
        records returned.

    """

    query = db.session.query(CACounty).filter(CACounty.geom.ST_Intersects(geomdat))
    
    query_count = 0
    for i in query:
        query_count += 1    
    # Logic to create a comma separted string of all results in case multiple counties
    # are returned, this should not happen under normal circumstances 
    if query_count > 0:
        result = ""
        count = 0
        for county in query:
            if count > 0:
                result += "," + county.name
                count += 1
            else:
                result += county.name
                count += 1
    else:
        return "Out of State!"
    return result


def nearestroad(coordinate):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the roads PostGIS table and returns a dictionary of nearest road
    and distance to road in feet.
   
    SQL expression is in raw form until it can be converted to SQLAlchemy format.
    
    Query uses bounding box index location (<-> in SQL) to get candiate roads (40 records) then passes the results into the
    ST_Distance_Sphere function to get the nearest road. ST_Distance_Sphere assumes the data are in WGS 84 and returns distance in meters. 
    
    The bounding box index calculations are fast but not entirely accurate, this method is useful for creating a smaller
    list of results to run more costly ST_Distance_Sphere calculations on.
    
    Parameters
    ----------
    coordinate: String
        WKT representation of the incoming GPS point coordinates.
        

    Returns
    -------
    result : dictionary
        dictionary with the keys: "street" and "distance".
            street:
                String of nearest street
            distance:
                Distance in feet to nearest road
        Results should never be empty, no matter how far away nearest road is.

    """
    sql = text(    """WITH nearestcanidates AS (
    SELECT
        roads.name,
        roads.geom
    FROM
        	roads AS roads
    WHERE
        roads.name IS NOT NULL
    ORDER BY
        	roads.geom <-> (ST_GeomFromText(:param, 4326))
    LIMIT 40)

    SELECT 
        nearestcanidates.name,
        ST_Distance_Sphere(
                nearestcanidates.geom,
                ST_GeomFromText(:param, 4326)
                ) AS distance
    FROM
        nearestcanidates
    ORDER BY
        distance
    LIMIT 1""")
    
    #Execute database query using the coordinates as a variable.
    print(f"Going to run query with coordinate: {coordinate}")
    query = db.session.execute(sql,{"param":coordinate})
    result = {}
    query_count = 0
    # Build out dict with each result in query
    for dat in query:
        result["street"] = dat[0]
        # Convert meters (default unit of postgis function) to feet
        result["distance"] = dat[1] * 3.28
        query_count += 1
    if query_count == 0:
        result['street'],result['distance'] = None, None
    return result    

def nearesttrail(coordinate):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the trails PostGIS table and returns a dictionary of nearest trail
    and distance to trail in feet. Trails with name "Unknown" are excluded from results.
   
    SQL expression is in raw form until it can be converted to SQLAlchemy format.
    
    Query uses bounding box index location (<-> in SQL) to get candiate roads (40 records) then passes the results into the
    ST_Distance_Sphere function to get the nearest road. ST_Distance_Sphere assumes the data are in WGS 84 and returns distance in meters. 
    
    The bounding box index calculations are fast but not entirely accurate, this method is useful for creating a smaller
    list of results to run more costly ST_Distance_Sphere calculations on.
    
    Parameters
    ----------
    coordinate: String
        WKT representation of the incoming GPS point coordinates.
        
    Returns
    -------
    result : dictionary
        dictionary with the keys: "trail" and "trail_distance"
            street:
                String of nearest trail
            distance:
                Distance in feet to nearest trail
       
    Results should never be empty, no matter how far nearest trail is.
    """
    #Raw SQL query with triple quotes to maintain formatting, see function comments for descripton
    sql = ('''
    WITH nearestcanidates AS (
    SELECT
        trails.name,
        trails.geom
    FROM
        "OSM_Central_CA_Trails" AS trails
    WHERE
        trails.name <> 'Unknown'
    ORDER BY
        	trails.geom <-> (ST_GeomFromText(:param, 4326))
    LIMIT 40)

    SELECT 
        nearestcanidates.name,
        ST_Distance(
                ST_Transform(nearestcanidates.geom,2228),
                ST_Transform(ST_GeomFromText(:param, 4326),2228)
                ) AS distance
    FROM
        nearestcanidates
    ORDER BY
        distance
    LIMIT 1
    ''')
    query = db.session.execute(sql,{"param":coordinate})
    result = {}
    query_count = 0
    for dat in query:
        result["trail"] = dat[0]
        result["trail_distance"] = dat[1]
        query_count += 1
    if query_count == 0:
        result['trail'],result['trail_distance'] = None,None
    return result

def getFeatCollection(datatype, reclimit):
    """
    Queries PostgreSQL using SQLAlchemy and GeoAlchemy functions, returns data formatted as a geoJSON feature collection.
    All stored attribute information are returned along with the geometries. gpstracks are returned for the current day,
    using the pytz library to set the today date to the US/Pacific timezone, instead of using the system clock. This
    enables the map to be accurate for the west coast, where most of the usage of the app will take place.

    Parameters
    ----------
    datatype: String. Type of data being queried, points or tracks
    reclimit: Int. Number of gpspoints to return

    Returns
    -------
    GeoJSON Feature Collection of datatype parameter containing all stored attribute information.

    """
    if datatype == "gpspoints":
        # Query using GeoAlchemy PostGIS function to get geojson representation of geometry and regular query to get
        # tabular data
        query = db.session.query(sqlfunc.ST_AsGeoJSON(gpsdatmodel.geom), gpsdatmodel).limit(reclimit)
    elif datatype == "gpstracks":
        # todaydate = datetime.today().strftime('%Y-%m-%d')
        # Set timezine to US/Pacific
        tz = pytz.timezone("US/Pacific")
        # Set the current date in the set timezone
        todaydate = tz.localize(datetime.today(), is_dst=None).strftime('%Y-%m-%d')
        # Query using GeoAlchemy PostGIS function to get geojson representation of geometry and regular query to get
        # tabular data
        query = db.session.query(sqlfunc.ST_AsGeoJSON(gpstracks.geom), gpstracks).filter_by(date=todaydate)
    features = []
    for row in query:
        # Build a dictionary of the attribute information
        prop_dict = row[1].builddict()
        # Take ST_AsGeoJSON() result and load as geojson object
        geojson_geom = geojson.loads(row[0])
        # Build the feature and add to feature list
        features.append(Feature(geometry=geojson_geom, properties=prop_dict))
    # Build the feature collection result
    feature_collection = FeatureCollection(features)
    return feature_collection

# def getrecords(rec_limit,dataType):
#     """
#     Queries PostgresSQL GPS data table for records. These results are used to generate geojson data
#     that are provided to the live dashboard.
#
#     Parameters
#     ----------
#     rec_limit : INT
#         Size of records to return from database, currently hard-coded to 1 upstream.
#         #TODO:
#         Build out to allow multiple returned records based on URL query strings
#
#     Returns
#     -------
#     res_dict : dictionary
#         dictionary with all database column names as keys.
#
#
#     SQL Alchemy ORM approach, see https://docs.sqlalchemy.org/en/13/orm/query.html and see:
#         https://hackersandslackers.com/database-queries-sqlalchemy-orm/
#     """
#     #Query based on GET request recieved
#     #SQL Alchemy ORM query returning newest records based on the utc timestamp field, .all() method creates a object that's easier to work with
#     if dataType == "gpspoints":
#         query = db.session.query(gpsdatmodel).order_by(gpsdatmodel.timeutc.desc()).limit(rec_limit)
#     #SQL Alchemy ORM query returning all gps tracks for the current day, this will likely need to be adjusted to account for time-zones
#     #to ensure that "todaydate" always returns date time in california
#     elif dataType == "gpstracks":
#         todaydate = datetime.today().strftime('%Y-%m-%d')
#         query = db.session.query(gpstracks).filter_by(date=todaydate)
#
#     res_dict = {}
#     for row in query:
#         #Create a nested dictionary for every row in the result object and add to result dictionary, with the record ID as the key to the nested dictionary
#         #.__dict__ is used to make a dictionary from parameters in the query object, this is used for easier processing
#         # However key value pairs are added that are popped off in another function to avoid issues converting them to geojson
#         res_dict[row.__dict__['id']] = row.__dict__
#
#     #Returning single dict so return can be built out with more entries if needed.
#     return {"dict":res_dict}

def gethashpass(username):
    """
    Get the hashed password from PostgreSQL database using the username supplied by HTTP Basic Auth.

    Parameters
    ----------
    username : String
        Username as provided by user in the auth prompt.

    Returns
    -------
    res_dict : dictionary
        keys:
            username (string, parameter)
         value:
            hashed password (string)
            None (if no matching user in table)
    
    A dictionary is returned to maintain connection between username supplied and password.
    """
    query = db.session.query(models.User.hashpass).filter(models.User.user==username).all()
    res_dict = {}
    for row in query:
        res_dict[username] = row.hashpass
    if len(res_dict) == 0:
        return None
    else:
        return res_dict
    
def getroles(username):
    """
    Queries PostgreSQL database for user roles using username supplied by Flask HTTP Basic Auth.

    Parses roles into a list.

    Parameters
    ----------
    username : String
        Username as provided by user in the auth prompt.

    Returns
    -------
    res : List
        List of strings containing user roles.
        All roles need to be returned.
    None if empty results, user not in database.
    """
    query = db.session.query(models.Roles.roles).filter(models.Roles.user==username).all()
    res = ()
    #Add query object results to tuple
    for row in query:
        res += row
    if len(res) == 0:
        return None
    #Roles are stored as comma seperated strings
    #Convert result tuple into a list of strings split by commas
    else:
        res = list(res)
        res = res[0].split(",")
        return res
            
def getdist(coordinate1, coordinate2):
    """
    Get the distance between the newest incoming point and the most recent previously recorded
    point, distance is reported as meters by default by ST_Distance_Sphere. 
    
    Parameters
    ----------
    coordinate:1 String
        WKT representation of the most recently recorded GPS point coordinates.
    coordinate2: String
        WKT representation of the incoming GPS point coordinates.

    Returns
    -------
    dist : Float
        Distance in meters between the newest and most recent recorded points.

    """
    #Geoalchemy ORM expression
    res = db.session.query(sqlfunc.ST_Distance_Sphere(sqlfunc.ST_GeomFromText(coordinate1),sqlfunc.ST_GeomFromText(coordinate2)))
    #coordinate1 = coordinate1
    #res = db.session.query(sqlfunc.ST_Distance_Sphere(coordinate1,coordinate2))
    dist = None
    for i in res:
        #Make sure the data comes through as a float, not a ORM object
        dist = float(i[0])
        #Round off number, don't need high precision 
        dist = round(dist,1)
    return dist
    
def getpathpointrecords(datetoday):
    """
    Gets the most recently recorded GPS point, used to check for movement and to generate a GPS track. This entire function may not be needed
    and can likely be combined with "getrecords".
    
    Returns a dictionary with a single top level key and a nested dictionary of record details, kept logic for multiple top level keys in 
    case I need to build this function out. 

    Parameters
    ----------
    datetoday : String
        String of current date in the form of %Y-%m-%d, set to local timezone ('America/Los_Angeles'). 

    Returns
    -------
    res_dict : Dictionary
       Results of gps point query with details as keys.

    """
    records = db.session.query(gpsdat.id,gpsdat.lat,gpsdat.lon,gpsdat.geom,gpsdat.timeutc,gpsdat.date).\
        filter(gpsdat.date == datetoday).\
        order_by(gpsdat.timeutc.desc()).limit(1).all()
    res_dict = {}
    row_count = 0
    for row in records:
        row_count += 1
    if row_count > 0:
        for row in records:
            res_dict[row.id] = {"id":row.id,"lat":row.lat,"lon":row.lon,"utc":row.timeutc,"date":row.date,"geom":row.geom}
        return res_dict
    else:
        return None

def getStandards():
    """
    Get the state health standards for ocean water quality tests. 

    Returns
    -------
    recDict : Dictionary
        Dict of State health standards, with the standard name as the keys and values as values.

    """
    records = db.session.query(stateStandards).all()
    recDict = {}
    for i in records:
        recDict[i.Name] = i.StandardMPN        
    return recDict
    
def getBeachWaterQual():
    """
    Queries Postgres AWS RDS to return the most recent water quality report data for each beach that is tested in SB 
    County.
    
    Data are spread across tables with mapped relationships. 
    
    This query joins the relevant tables and uses "distinct" on the waterQuality beach ID field, selecting only one
    record per beach, then "order_by" is used on the joined MD5 table to grab only the most recent record per beach.
    
    :return: List:
        Nested lists containing SQL Alchemy query results: 
            3 query result objects:
                waterQuality, waterqualityMD5 beaches
            1 string: 
                geometry type of associated beach 
            2 floats: 
                x and y coordinates of the associated beach  
    """
    records = db.session.query(waterQuality, waterQualityMD5, beaches, sqlfunc.ST_GeometryType(beaches.geom), sqlfunc.st_x(beaches.geom), sqlfunc.st_y(beaches.geom)) \
        .join(waterQualityMD5) \
        .join(beaches) \
        .distinct(waterQuality.beach_id)\
        .order_by(waterQuality.beach_id,  waterQualityMD5.insdate.desc()).all()
    return records