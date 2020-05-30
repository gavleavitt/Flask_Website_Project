#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:25:08 2020

@author: user
"""
import time
from geojson import Point, Feature, FeatureCollection, dumps
from application import DB_Queries as DBQ

def string_to_none(x):
    if x == '':
        return None
    else:
        return x
    
def converttime(timestamp_e,timestart):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp_e)))
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestart)))
    result = {"timestamp_e":timestamp ,"timestart":start_time}
    return result

def geomformat(srid,lat,lon):
    pass

def to_geojson():   
    features = []
    ##try to use properties = dict{dbdat}
    dbdat = DBQ.getrecords(1)
    for key in dbdat.keys():
            #Pop unnecessary entries
        dbdat[key].pop('_sa_instance_state')
        dbdat[key].pop('geom')
        #print((float(dbdat[key]['lon']), float(dbdat[key]['lat'])))
        my_point = Point((float(dbdat[key]['lon']), float(dbdat[key]['lat'])))
        features.append(Feature(geometry=my_point, properties=dbdat[key]))
    feature_collection = FeatureCollection(features)
    #result = dumps(feature_collection, sort_keys=True)
    #print(feature_collection.is_valid)
    return feature_collection
    
    
    