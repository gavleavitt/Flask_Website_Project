#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:40:53 2020

@author: Gavin Leavitt

This module contains PostgresSQL database query functions. 

"""
from application import app, models, db
from application import functions as func
from application import script_config as dbconfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text



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
    res["POI"] = POI_I_Q(geomdat)
    res['city'] = city_I_Q(geomdat)
    res["county"] = county_I_Q(geomdat)
    roadinfo = nearestroad(geomdat)
    res["road"] = roadinfo["street"]
    res["dist_road"] = roadinfo["distance"]
    if res["POI"] in dbconfig.settings["POI_Outdoors"]:
        outdoors = nearesttrail(geomdat)
        res["trail"]=outdoors['trail']
        res['dist_trail']=outdoors['trail_distance']
    else:
        res['trail'],res['dist_trail']=None,None
    return res 

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

    query = db.session.query(models.CaliforniaPlace).filter(models.CaliforniaPlace.geom.ST_Intersects(geomdat))
    
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

    query = db.session.query(models.CACounty).filter(models.CACounty.geom.ST_Intersects(geomdat))
    
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
    sql = text(    """WITH nearestcanidates AS (
    SELECT
        roads.name,
        roads.geom
    FROM
        	moco_roads AS roads
    ORDER BY
        	roads.geom <-> (ST_GeomFromText(:param, 4326))
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
    LIMIT 1""")
    #Execute database query using the coordinates as a variable.
    print(f"Going to run query with coordinate: {coordinate}")
    query = db.session.execute(sql,{"param":coordinate})
    result = {}
    query_count = 0
    for dat in query:
        result["street"] = dat[0]
        result["distance"] = dat[1]
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

def getrecords(rec_limit):
    """
    Queries PostgresSQL database for newest records.

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
    #SQL Alchemy ORM query returning newest records based on the utc timestamp field, .all() method creates a object that's easier to work with
    query = db.session.query(models.gpsdatmodel).order_by(models.gpsdatmodel.timeutc.desc()).limit(rec_limit).all()
    res_dict = {}
    #row_count = 0
    for row in query:
        #print(row.__dict__)
        #Create a dictonary for every row in the result object and add to result dictonary, with the record ID as the key to the nested dictonary
        #.__dict__ is used to make a dictonary from parameters in the query object, this is used for easier processing.
        res_dict[row.__dict__['id']] = row.__dict__
        #row_count += 1 
    return res_dict

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
    
