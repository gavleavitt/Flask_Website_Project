#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:25:08 2020

@author: gavinl

This module contains helper python functions for the application.
"""
import time
from geojson import Point, Feature, FeatureCollection
from application import DB_Queries as DBQ

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

def to_geojson():   
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
    dbdat = DBQ.getrecords(1)
    #Use keys in dict to base appends on, each key is a unique record from database
    for key in dbdat.keys():
        #Pop unnecessary entries
        dbdat[key].pop('_sa_instance_state')
        dbdat[key].pop('geom')
        #Make a new formated coordinate point for Feature object 
        my_point = Point((float(dbdat[key]['lon']), float(dbdat[key]['lat'])))
        features.append(Feature(geometry=my_point, properties=dbdat[key]))
    #convert to geojson FeatureCollection object 
    feature_collection = FeatureCollection(features)
    return feature_collection
    
    
    