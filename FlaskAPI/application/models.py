#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 01:09:08 2020

@author: user
"""
from application import app, application 
from application import db
from sqlalchemy import ARRAY, BigInteger, Boolean, CheckConstraint, Column, Date, DateTime, Float, Integer, Numeric, String, Table, Text, Time, TEXT
from sqlalchemy.schema import FetchedValue
from geoalchemy2.types import Geometry
from geoalchemy2 import Geometry
from flask_sqlalchemy import SQLAlchemy


class gpstracks(db.Model):
    __tablename__ = 'gpstracks'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp_epoch = db.Column(db.DateTime())
    timeutc = db.Column(db.DateTime())
    date = db.Column(db.Date())
    startstamp = db.Column(db.DateTime())
    gpsid = db.Column(db.Integer())
    androidid = db.Column(db.String(30))
    serial = db.Column(db.String(30))
    profile = db.Column(db.String(30))
    geom = db.Column(Geometry('Linestring', 4326, from_text='ST_GeomFromEWKT', name='geometry'))
    
class gpsdatmodel(db.Model):
    __tablename__ = 'gpsapidata'

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float())
    lon = db.Column(db.Float())
    satellites = db.Column(db.Integer())
    altitude = db.Column(db.Float())
    speed = db.Column(db.Float())
    accuracy = db.Column(db.Float())
    direction = db.Column(db.Integer())
    provider = db.Column(db.String(30))
    timestamp_epoch = db.Column(db.DateTime())
    timeutc = db.Column(db.DateTime())
    date = db.Column(db.Date())
    startstamp = db.Column(db.DateTime())
    battery = db.Column(db.Integer())
    androidid = db.Column(db.String(30))
    serial = db.Column(db.String(30))
    profile = db.Column(db.String(30))
    hhop = db.Column(db.Float())
    vdop = db.Column(db.Float())
    pdop = db.Column(db.Float())
    activity = db.Column(db.String(30))
    travelled = db.Column(db.Float())
    nearestroad = db.Column(db.String(30))
    dist_nearestroad = db.Column(db.Float())
    nearesttrail = db.Column(db.String(30))
    dist_nearesttrail = db.Column(db.Float())
    POI = db.Column(db.String(30))
    city = db.Column(db.String(30))
    county = db.Column(db.String(30))
    #geom = db.Column(Geometry('POINT',srid=4326))
    geom = db.Column(Geometry('POINT', 4326, from_text='ST_GeomFromEWKT', name='geometry'))
    #geom = db.Column(Geometry('POINT', 4326))
    #see https://stackoverflow.com/questions/39215278/alembic-migration-for-geoalchemy2-raises-nameerror-name-geoalchemy2-is-not-de

class User(db.Model):
    __tablename__ = 'app_users'
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String())
    hashpass = db.Column(db.String(120))

    
class Roles(db.Model):
    __tablename__ = 'app_roles'
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String())
    roles = db.Column(db.String())
    

class AllStravaActivity(db.Model):
    __tablename__ = 'All_Strava_Activities'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    geom = db.Column(Geometry('MULTILINESTRING', 4326, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    ActName = db.Column(db.String)
    Date = db.Column(db.Date)
    Filename = db.Column(db.String)
    ActType = db.Column(db.String)
    Bike = db.Column(db.String)
    Elapsed_Ti = db.Column(db.Integer)
    Distance = db.Column(db.Float(53))
    layer = db.Column(db.String)
    path = db.Column(db.String)



class CACounty(db.Model):
    __tablename__ = 'CA_Counties'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    geom = db.Column(Geometry('MULTIPOLYGON', 4326, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    statefp = db.Column(db.String(2))
    countyfp = db.Column(db.String(3))
    countyns = db.Column(db.String(8))
    geoid = db.Column(db.String(5))
    name = db.Column(db.String(100))
    namelsad = db.Column(db.String(100))
    lsad = db.Column(db.String(2))
    classfp = db.Column(db.String(2))
    mtfcc = db.Column(db.String(5))
    csafp = db.Column(db.String(3))
    cbsafp = db.Column(db.String(5))
    metdivfp = db.Column(db.String(5))
    funcstat = db.Column(db.String(1))
    aland = db.Column(db.BigInteger)
    awater = db.Column(db.BigInteger)
    intptlat = db.Column(db.String(11))
    intptlon = db.Column(db.String(12))

class CaliforniaPlaces(db.Model):
    __tablename__ = 'California_Places'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    geom = db.Column(Geometry('MULTIPOLYGON', 4326, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    statefp = db.Column(db.String(2))
    placefp = db.Column(db.String(5))
    placens = db.Column(db.String(8))
    geoid = db.Column(db.String(7))
    name = db.Column(db.String(100))
    namelsad = db.Column(db.String(100))
    lsad = db.Column(db.String(2))
    classfp = db.Column(db.String(2))
    pcicbsa = db.Column(db.String(1))
    pcinecta = db.Column(db.String(1))
    mtfcc = db.Column(db.String(5))
    funcstat = db.Column(db.String(1))
    aland = db.Column(db.BigInteger)
    awater = db.Column(db.BigInteger)
    intptlat = db.Column(db.String(11))
    intptlon = db.Column(db.String(12))


class OSMCentralCATrail(db.Model):
    __tablename__ = 'OSM_Central_CA_Trails'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    geom = db.Column(Geometry('MULTILINESTRING', 4326, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    full_id = db.Column(db.String(254))
    osm_id = db.Column(db.String(254))
    osm_type = db.Column(db.String(254))
    access = db.Column(db.String(254))
    highway = db.Column(db.String(254))
    name = db.Column(db.String(254))
    tiger_cfcc = db.Column(db.String(254))
    tiger_coun = db.Column(db.String(254))
    tiger_name = db.Column(db.String(254))
    tiger_revi = db.Column(db.String(254))
    tracktype = db.Column(db.String(254))
    surface = db.Column(db.String(254))
    tiger_sour = db.Column(db.String(254))
    bicycle = db.Column(db.String(254))
    motor_vehi = db.Column(db.String(254))
    motorcar = db.Column(db.String(254))
    motorcycle = db.Column(db.String(254))
    tiger_tlid = db.Column(db.String(254))
    foot = db.Column(db.String(254))
    path = db.Column(db.String(200))
    uc = db.Column(db.String(80))
    layer = db.Column(db.String(100))



class POI(db.Model):
    __tablename__ = 'POI'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    geom = db.Column(Geometry('MULTIPOLYGON', 4326), index=True)
    location = db.Column(db.String(80))
    desc = db.Column(db.String(80))

class Roads(db.Model):
    __tablename__ = 'roads'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    geom = db.Column(Geometry('MULTILINESTRING', 4326), index=True)
    full_id  = db.Column(db.String(80))
    osm_id = db.Column(db.String(80))
    osm_type = db.Column(db.String(80))
    bicycle = db.Column(db.String(80))
    foot = db.Column(db.String(80))
    highway = db.Column(db.String(80))
    name = db.Column(db.String(80))
    surface = db.Column(db.String(80))
    

# class Roads(db.Model):
#     __tablename__ = 'roads'

#     id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
#     geom = db.Column(Geometry('MULTILINESTRING', 4326), index=True)
#     fid = db.Column(db.BigInteger)
#     prefix = db.Column(db.String(80))
#     name = db.Column(db.String(80))
#     suffix = db.Column(db.String(80))
#     full_name = db.Column(db.String(80))
#     alias = db.Column(db.String(80))
#     route = db.Column(db.String(80))
#     road_type = db.Column(db.String(80))
#     func_class = db.Column(db.String(80))
#     l_cmnty_co = db.Column(db.String(80))
#     r_cmnty_co = db.Column(db.String(80))
#     l_zip = db.Column(db.BigInteger)
#     r_zip = db.Column(db.BigInteger)
#     from_l_add = db.Column(db.BigInteger)
#     to_l_addre = db.Column(db.BigInteger)
#     from_r_add = db.Column(db.BigInteger)
#     to_r_addre = db.Column(db.BigInteger)
#     low_addres = db.Column(db.BigInteger)
#     high_addre = db.Column(db.BigInteger)
#     maint_by = db.Column(db.String(80))
#     surface = db.Column(db.String(80))
#     road_numbe = db.Column(db.String(80))
#     road_seg = db.Column(db.String(80))
#     map_number = db.Column(db.String(80))
#     map_coord = db.Column(db.String(80))
#     one_way = db.Column(db.String(80))
#     length = db.Column(db.Numeric)
#     minutes = db.Column(db.BigInteger)
#     f_zlev = db.Column(db.BigInteger)
#     t_zlev = db.Column(db.BigInteger)
#     _class = db.Column('class', db.BigInteger)
#     speed = db.Column(db.BigInteger)
#     shape_len = db.Column(db.Numeric)
#     shape__len = db.Column(db.Numeric)

# class Testtab(db.Model):
#     __tablename__ = 'testtab'

#     id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
#     testf1 = db.Column(db.String(30))
#     testf2 = db.Column(db.String(30))
