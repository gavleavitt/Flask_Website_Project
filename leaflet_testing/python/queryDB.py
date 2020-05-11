#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 23:16:38 2020

@author: user
"""

from __future__ import print_function
import psycopg2

def queryDB(coordinate,conn,POI_Outdoors):
    """
    Takes GPS coordinates and passes them to database queries.
    
    Checks against various locations within the State of California.
    
    Parameters:
        coordniate: [List],(string); Coordinates in WGS 1984 stored in a list of 1 (psycopg2 requires list inputs), in the form of:
            "POINT(lon lat)"
        conn: POSTGRES connection
    Returns:
    Dictonary: Results placed into dictonary with the following keys:
        POI, City, County, Trail, Road
            If no result then empty lists are returned. 
        String: If not in Calfifornia a string is returned
    """  
    result_county = queryDB_CA_county(coordinate,conn)
    if len(result_county) > 0:
        result = dict()
        POIResult = queryDB_POI(coordinate,conn)
        result_city = queryDB_CA_city(coordinate,conn) 
        result['POI'] = POIResult
        result['City'] = result_city
        result['County'] = result_county
        result['Trail'] = None
        if result['POI'] in POI_Outdoors:
            result['Trail'] = QueryDB_trails(coordinate,conn)
        else:
            result['Trail'] = (None,None)
        result['Road'] = queryDB_CA_Road(coordinate,conn)
    else:
        result = "Out of State!"
    print("Finished performing spatial queries on the database!")
    return result
    

    
def queryDB_POI(coordinate,conn):
    """
    Queries POSTGRES DB to return instersection of GPS coordinate and POI dataset. 
       
    Parameters:
        coordniate: [List],(string); Coordinates in WGS 1984 stored in a list of 1 (psycopg2 requires list inputs), in the form of:
            "POINT(lon lat)"
        conn: POSTGRES connection
    
    Returns:
        string: POI name if appliciable, None if there is no intersection.
    
    """    
    sql_POI_I = '''
    SELECT 
        "POI".location  
    FROM 
        "POI"
    WHERE
        ST_Intersects("POI".geom,ST_GeomFromText(%s, 4326)) 
    '''  
    cur = conn.cursor()
    cur.execute(sql_POI_I, coordinate)
    result = cur.fetchall()
    if len(result) > 0:
        return result[0][0]
    else:
        return None

def queryDB_CA_county(coordinate,conn):
    """
    Queries POSTGRES DB to return instersection of GPS coordinate and California counties dataset. 
    
    Parameters:
        coordinate: List; Coordinates in WGS 1984 stored as a string in a list of 1, in the form of:
            "POINT(lon lat)"
        conn: POSTGRES connection
    Returns:
        string: County name if appliciable, None if there is no intersection.
    """    
    sql_county_I = '''
    SELECT 
        "CA_Counties".name
    FROM 
        "CA_Counties"
    WHERE
        ST_Intersects("CA_Counties".geom,ST_GeomFromText(%s, 4326)) 
    '''  
    cur = conn.cursor()
    cur.execute(sql_county_I, coordinate)
    result = cur.fetchall()
    if len(result) > 0: 
        return result[0][0] 
    else:
        return None

def queryDB_CA_city(coordinate,conn):
    """
    Queries POSTGRES DB to return instersection of GPS coordinate and California cities dataset. 
       
    Parameters:
        coordniate: [List],(string); Coordinates in WGS 1984 stored in a list of 1 (psycopg2 requires list inputs), in the form of:
            "POINT(lon lat)"
        conn: POSTGRES connection
    
    Returns:
    string: City name if appliciable, string '-1' if there is no intersection.
    """   
    
    sql_CA_I = '''
    SELECT 
        "California_Places".name
    FROM 
        "California_Places"
    WHERE
        ST_Intersects("California_Places".geom,ST_GeomFromText(%s, 4326)) 
    '''  
    cur = conn.cursor()
    cur.execute(sql_CA_I, coordinate)
    result = cur.fetchall()
    if len(result) > 0:
        return result[0][0]
    else:
        return None
       

def queryDB_CA_Road(coordinate,conn):
    """
    Queries POSTGRES DB to return the nearest road and its distance from the current GPS location.
    
    Function starts with a Index-based KNN search see:
    https://postgis.net/workshops/postgis-intro/knn.html
    
    This is fast since it uses distances between bounding boxes and avoids using a search radius
    or comparing everything in database. However this method is prone to errors so the 
    best 40 results are then sorted by their distances apart with only the nearest
    record being returned. 
    
    Distances are transformed from WGS 1984 to EPSG 2228, California State Plane 4,
    so results can be more accurate and distance apart is returned in feet.
    
    Parameters:
    coordniate: [List],(string); Coordinates in WGS 1984 stored in a list of 1 (psycopg2 requires list inputs), in the form of:
        "POINT(lon lat)"
    conn: POSTGRES connection
    Returns:
    list: (road,distance(feet)); Nearest road and distance to road in feet.   
    """
    sql_road = '''
    WITH nearestcanidates AS (
    SELECT
        	roads.name,
        roads.geom
    FROM
        	moco_roads AS roads
    ORDER BY
        	roads.geom <-> (ST_GeomFromText(%s, 4326))
    LIMIT 40)

    SELECT 
        nearestcanidates.name,
        ST_Distance(
                ST_Transform(nearestcanidates.geom,2228),
                ST_Transform(ST_GeomFromText(%s, 4326),2228)
                ) AS distance
    FROM
        nearestcanidates
    ORDER BY
        distance
    LIMIT 1
    '''
    #Need the gps coordinate in a list as many times as %s appears, each entry must be a string
    coor_expand = [str(coordinate[0]),str(coordinate[0])]
    cur = conn.cursor()
    cur.execute(sql_road, coor_expand)
    result = cur.fetchall()
    return (result[0][0],float(str(result[0][1])[0:6]))

def QueryDB_trails(coordinate,conn):
    """
    Queries POSTGRES DB to return the nearest trail and its distance from the current GPS location.
    
    
    Parameters:
    coordniate: [List],(string); Coordinates in WGS 1984 stored in a list of 1 (psycopg2 requires list inputs), in the form of:
        "POINT(lon lat)"
    conn: POSTGRES connection
    
    Returns:
    list: (trail,distance(feet)); Nearest trail and distance to trail in feet.      
    
    """
    sql_trail = '''
    WITH nearestcanidates AS (
    SELECT
        	trails.name,
        trails.geom
    FROM
        "OSM_Central_CA_Trails" AS trails
    WHERE
        trails.name <> 'Unknown'
    ORDER BY
        	trails.geom <-> (ST_GeomFromText(%s, 4326))
    LIMIT 40)

    SELECT 
        nearestcanidates.name,
        ST_Distance(
                ST_Transform(nearestcanidates.geom,2228),
                ST_Transform(ST_GeomFromText(%s, 4326),2228)
                ) AS distance
    FROM
        nearestcanidates
    ORDER BY
        distance
    LIMIT 1
    '''
    coor_expand = [str(coordinate[0]),str(coordinate[0])]
    cur = conn.cursor()
    cur.execute(sql_trail, coor_expand)
    result = cur.fetchall()
    return (result[0][0],float(str(result[0][1])[0:6]))
