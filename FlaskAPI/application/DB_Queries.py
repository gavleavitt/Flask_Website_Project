#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:40:53 2020

@author: Gavin Leavitt

This module contains PostgresSQL database query functions that are called by the functions module.  

"""
from application import application, models, db
from application.models import gpsdatmodel, gpstracks, POI, CaliforniaPlaces, CACounty 
from application import functions as func
from application import script_config as dbconfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from application.models import gpsdatmodel as gpsdat
from sqlalchemy import func as sqlfunc
from datetime import datetime
from flask.json import jsonify
from geojson import Point, Feature, FeatureCollection, LineString
from geoalchemy2.shape import to_shape

def POI_I_Q(geomdat):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the POI PostGIS table and returns a string of results.
    
    The POI table contains hand digitized locations of interest.
    
    Currently only single POI results are returned, however this will change as POIs are added.
    
    Parameters
    ----------
    geomdat : TYPE
        DESCRIPTION.

    Returns
    -------
    result : String
        POI results as a string with individual results comma seperated or None in case
            of empty result.
        A comma seperated string is returned for easier processing and insertion into
        dictonary created by the queries function.

    """
    #SQLAlchemy and GeoAlchemy SQL query
    query = db.session.query(models.POI).filter(models.POI.geom.ST_Intersects(geomdat))
    #Get the size of the result, used for building out the string result.
    query_count = 0
    for i in query:
        query_count += 1    
    
    if query_count > 0:
        result = ""
        count = 0
        #Iterate over SQL Alchemy result object, if greater than 1 result build out with comma seperation.
        for POI in query:
            if count > 0:
                #result object columns can be individually called with their column names, only want location info.
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
    geomdat : TYPE
        DESCRIPTION.

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
    geomdat : TYPE
        DESCRIPTION.

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
    Issues a SQLAlchemy/GeoAlchemy intersection query against the roads PostGIS table and returns a dictonary of nearest road
    and distance to road in feet.
   
    SQL expression is in raw form until it can be converted to SQLAlchemy format.
    
    Query uses bounding box index location (<-> in SQL) to get candiate roads (40 records) then passes the results into the
    ST_Distance function to get the nearest road. Points are transformed into the local coordinate
    system California State Plane 4 (EPSG 2228) for better accurary and so that results are in feet instead of degrees, 
    the default of WGS 1984 (EPSG 4326).
    
    The bounding box index calculations are fast but not entirely accurate, this method is useful for creating a smaller
    list of results to run more costly ST_Distance calculations on.
    
    Parameters
    ----------
    coordinate : TYPE
        DESCRIPTION.

    Returns
    -------
    result : Dictonary
        Dictonary with the keys: "street" and "distance".
            street:
                String of nearest street
            distance:
                Distance in feet to nearest road
        Results should never be empty, no matter how far away nearest road is.

    """
    #Raw SQL expression using triple quotes to maintain formatting in SQL form.
    # sql = text(    """WITH nearestcanidates AS (
    # SELECT
    #     roads.full_name,
    #     roads.geom
    # FROM
    #     	roads AS roads
    # ORDER BY
    #     	roads.geom <-> (ST_GeomFromText(:param, 4326))
    # LIMIT 40)

    # SELECT 
    #     nearestcanidates.full_name,
    #     ST_Distance(
    #             ST_Transform(nearestcanidates.geom,2228),
    #             ST_Transform(ST_GeomFromText(:param, 4326),2228)
    #             ) AS distance
    # FROM
    #     nearestcanidates
    # ORDER BY
    #     distance
    # LIMIT 1""")
    
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
    for dat in query:
        result["street"] = dat[0]
        result["distance"] = dat[1] * 3.28
        query_count += 1
    if query_count == 0:
        result['street'],result['distance'] = None,None
    return result    

def nearesttrail(coordinate):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the trails PostGIS table and returns a dictonary of nearest trail
    and distance to trail in feet. Trails with name "Unknown" are excluded from results.
   
    SQL expression is in raw form until it can be converted to SQLAlchemy format.
    
    Query uses bounding box index location (<-> in SQL) to get candiate trails (40 records) then passes the results into the
    ST_Distance function to get the nearest trail. Points are transformed into the local coordinate
    system California State Plane 4 (EPSG 2228) for better accurary and so that results are in feet instead of degrees, 
    the default of WGS 1984 (EPSG 4326).
    
    The bounding box index calculations are fast but not entirely accurate, this method is useful for creating a smaller
    list of results to run more costly ST_Distance calculations on.
    
    Parameters
    ----------
    coordinate : TYPE
        DESCRIPTION.

    Returns
    -------
    result : Dictonary
        Dictonary with the keys: "trail" and "trail_distance"
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

def getrecords(rec_limit,dataType):
    """
    Queries PostgresSQL gps data table for records.

    Parameters
    ----------
    rec_limit : INT
        Size of records to return from databas.

    Returns
    -------
    res_dict : Dictonary
        Dictonary with all database column names as keys.


    SQL Alchemy ORM approach, see https://docs.sqlalchemy.org/en/13/orm/query.html and see:
        https://hackersandslackers.com/database-queries-sqlalchemy-orm/
    """
    #Query based on GET request recieved
    #SQL Alchemy ORM query returning newest records based on the utc timestamp field, .all() method creates a object that's easier to work with
    if dataType == "gpspoints":
        #query = db.session.query(models.gpsdatmodel).order_by(models.gpsdatmodel.timeutc.desc()).limit(rec_limit).all()
        query = db.session.query(gpsdatmodel).order_by(gpsdatmodel.timeutc.desc()).limit(rec_limit)
    #SQL Alchemy ORM query returning all gps tracks for the current day, this will likely need to be adjusted to account for time-zones
    #to ensure that "todaydate" always returns date time in california 
    elif dataType == "gpstracks":
        todaydate = datetime.today().strftime('%Y-%m-%d')        
        query = db.session.query(gpstracks).filter_by(date=todaydate)
        
        #Unused:
        #Taken from https://gis.stackexchange.com/questions/233184/converting-geoalchemy2-elements-wkbelement-to-wkt
        #Queries Postgres table and returns a tuple of 2 items, one with a gpstracks result object, the other with a geojson string representation
        #of the coordinates
        #query = db.session.query(gpstracks, sqlfunc.ST_AsGeoJSON(gpstracks.geom)).filter_by(date=todaydate).all()
        
    res_dict = {}
    for row in query:  
        #Create a dictonary for every row in the result object and add to result dictonary, with the record ID as the key to the nested dictonary
        #.__dict__ is used to make a dictonary from parameters in the query object, this is used for easier processing
        res_dict[row.__dict__['id']] = row.__dict__ 
        
        #Unused:
        #Build dictonary using different parameters depending on the type of GET request recieved, the db queries return different result objects
        #that must be parsed differently
        # if dataType == "gpspoints": 
        #     res_dict[row.__dict__['id']] = row.__dict__ 
        # elif dataType == "gpstracks":
        #     res_dict[row[0].__dict__['id']] = row[0].__dict__
    #Returning single dict so return can be built out with more entries if needed.        
    return {"dict":res_dict}

def gethashpass(username):
    """
    Get the hashed password from PostgreSQL database using the username supplied by HTTP Basic Auth.

    Parameters
    ----------
    username : TYPE
        DESCRIPTION.

    Returns
    -------
    res_dict : Dictonary
        keys:
            username (string, parameter)
         value:
            hashed password (string)
            None (if no matching user in table)
    
    A dictonary is returned to maintain connection between username supplied and password.
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
    username : TYPE
        DESCRIPTION.

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
    
    Parameters
    ----------
    coordinate1 : TYPE
        DESCRIPTION.
    coordinate2 : TYPE
        DESCRIPTION.

    Returns
    -------
    dist : TYPE
        DESCRIPTION.

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
    
    Returns a dictonary with a single top level key and a nested dictonary of record details, kept logic for multiple top level keys in 
    case I need to build this function out. 

    Parameters
    ----------
    coordinate : TYPE
        DESCRIPTION.
    datetoday : TYPE
        DESCRIPTION.

    Returns
    -------
    res_dict : TYPE
        DESCRIPTION.

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