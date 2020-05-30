#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:40:53 2020

@author: user
"""
from application import app, models, db
from application import functions as func
from application import script_config as dbconfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text



def queries(geomdat):
    """
    
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
    
    """
    query = db.session.query(models.POI).filter(models.POI.geom.ST_Intersects(geomdat))
    
    query_count = 0
    for i in query:
        query_count += 1    
    
    if query_count > 0:
        result = ""
        count = 0
        for POI in query:
            if count > 0:
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

    """
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

    """
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
    SQL Alchemy ORM approach, see https://docs.sqlalchemy.org/en/13/orm/query.html and see:
        https://hackersandslackers.com/database-queries-sqlalchemy-orm/
    """

    query = db.session.query(models.gpsdatmodel).order_by(models.gpsdatmodel.timeutc.desc()).limit(rec_limit).all()
    res_dict = {}
    #row_count = 0
    for row in query:
        #print(row.__dict__)
        res_dict[row.__dict__['id']] = row.__dict__
        #row_count += 1 
    return res_dict