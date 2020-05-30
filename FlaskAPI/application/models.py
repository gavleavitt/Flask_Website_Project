#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 01:09:08 2020

@author: user
"""
from application import app
from application import db
from sqlalchemy import ARRAY, BigInteger, Boolean, CheckConstraint, Column, Date, DateTime, Float, Integer, Numeric, String, Table, Text, Time, TEXT
from sqlalchemy.schema import FetchedValue
from geoalchemy2.types import Geometry
from geoalchemy2 import Geometry
from flask_sqlalchemy import SQLAlchemy

class gpsdatmodel(db.Model):
    __tablename__ = 'gpsapidattest'

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



class CaliforniaPlace(db.Model):
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



t_geography_columns = db.Table(
    'geography_columns',
    db.Column('f_table_catalog', db.String),
    db.Column('f_table_schema', db.String),
    db.Column('f_table_name', db.String),
    db.Column('f_geography_column', db.String),
    db.Column('coord_dimension', db.Integer),
    db.Column('srid', db.Integer),
    db.Column('type', db.Text)
)



t_geometry_columns = db.Table(
    'geometry_columns',
    db.Column('f_table_catalog', db.String(256)),
    db.Column('f_table_schema', db.String),
    db.Column('f_table_name', db.String),
    db.Column('f_geometry_column', db.String),
    db.Column('coord_dimension', db.Integer),
    db.Column('srid', db.Integer),
    db.Column('type', db.String(30))
)



class Gpsdatum(db.Model):
    __tablename__ = 'gpsdata'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    gpstime = db.Column(db.DateTime(True))
    lat = db.Column(db.Float(53))
    lon = db.Column(db.Float(53))
    elevation = db.Column(db.Float)
    accuracy = db.Column(db.Float)
    bearing = db.Column(db.Float)
    speed = db.Column(db.Float)
    satellites = db.Column(db.Integer)
    provider = db.Column(db.String(10))
    hdop = db.Column(db.Float)
    vdop = db.Column(db.Float)
    pdop = db.Column(db.Float)
    geoidheight = db.Column(db.Float)
    ageofdgpsdata = db.Column(db.String(15))
    dgpsid = db.Column(db.String(10))
    activity = db.Column(db.String(40))
    battery = db.Column(db.Integer)
    phone = db.Column(db.String(40))
    inserttime = db.Column(db.Time)
    gpstimelocal = db.Column(db.Time)
    city = db.Column(db.String(30))
    county = db.Column(db.String(30))
    poi = db.Column(db.String(30))
    road = db.Column(db.String(30))
    dist_nearestroad = db.Column(db.Float)
    trail = db.Column(db.String(30))
    dist_nearesttrail = db.Column(db.Float)
    geom = db.Column(Geometry('POINT', 4326))



class MocoRoad(db.Model):
    __tablename__ = 'moco_roads'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    geom = db.Column(Geometry('MULTILINESTRING', 4326), index=True)
    fid = db.Column(db.BigInteger)
    prefix = db.Column(db.String(80))
    name = db.Column(db.String(80))
    suffix = db.Column(db.String(80))
    full_name = db.Column(db.String(80))
    alias = db.Column(db.String(80))
    route = db.Column(db.String(80))
    road_type = db.Column(db.String(80))
    func_class = db.Column(db.String(80))
    l_cmnty_co = db.Column(db.String(80))
    r_cmnty_co = db.Column(db.String(80))
    l_zip = db.Column(db.BigInteger)
    r_zip = db.Column(db.BigInteger)
    from_l_add = db.Column(db.BigInteger)
    to_l_addre = db.Column(db.BigInteger)
    from_r_add = db.Column(db.BigInteger)
    to_r_addre = db.Column(db.BigInteger)
    low_addres = db.Column(db.BigInteger)
    high_addre = db.Column(db.BigInteger)
    maint_by = db.Column(db.String(80))
    surface = db.Column(db.String(80))
    road_numbe = db.Column(db.String(80))
    road_seg = db.Column(db.String(80))
    map_number = db.Column(db.String(80))
    map_coord = db.Column(db.String(80))
    one_way = db.Column(db.String(80))
    length = db.Column(db.Numeric)
    minutes = db.Column(db.BigInteger)
    f_zlev = db.Column(db.BigInteger)
    t_zlev = db.Column(db.BigInteger)
    _class = db.Column('class', db.BigInteger)
    speed = db.Column(db.BigInteger)
    shape_len = db.Column(db.Numeric)
    shape__len = db.Column(db.Numeric)



t_raster_columns = db.Table(
    'raster_columns',
    db.Column('r_table_catalog', db.String),
    db.Column('r_table_schema', db.String),
    db.Column('r_table_name', db.String),
    db.Column('r_raster_column', db.String),
    db.Column('srid', db.Integer),
    db.Column('scale_x', db.Float(53)),
    db.Column('scale_y', db.Float(53)),
    db.Column('blocksize_x', db.Integer),
    db.Column('blocksize_y', db.Integer),
    db.Column('same_alignment', db.Boolean),
    db.Column('regular_blocking', db.Boolean),
    db.Column('num_bands', db.Integer),
    db.Column('pixel_types', db.ARRAY(TEXT())),
    db.Column('nodata_values', db.ARRAY(Float(precision=53))),
    db.Column('out_db', db.Boolean),
    db.Column('extent', Geometry(from_text='ST_GeomFromEWKT', name='geometry')),
    db.Column('spatial_index', db.Boolean)
)



t_raster_overviews = db.Table(
    'raster_overviews',
    db.Column('o_table_catalog', db.String),
    db.Column('o_table_schema', db.String),
    db.Column('o_table_name', db.String),
    db.Column('o_raster_column', db.String),
    db.Column('r_table_catalog', db.String),
    db.Column('r_table_schema', db.String),
    db.Column('r_table_name', db.String),
    db.Column('r_raster_column', db.String),
    db.Column('overview_factor', db.Integer)
)



class SpatialRefSy(db.Model):
    __tablename__ = 'spatial_ref_sys'
    __table_args__ = (
        db.CheckConstraint('(srid > 0) AND (srid <= 998999)'),
    )

    srid = db.Column(db.Integer, primary_key=True)
    auth_name = db.Column(db.String(256))
    auth_srid = db.Column(db.Integer)
    srtext = db.Column(db.String(2048))
    proj4text = db.Column(db.String(2048))



class Testtab(db.Model):
    __tablename__ = 'testtab'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    testf1 = db.Column(db.String(30))
    testf2 = db.Column(db.String(30))

#
##    def __init__(self, id, lat, lon, satellites, altitude, speed, accuracy, direction, provider,
##                 timestamp_epoch, timeutc, date, startstamp, battery, androidid, serial, profile,hdop, vdop, pdop,travelled,geom):
##        self.id = id
##        self.lat = lat
##        self.lon = lon
##        self.satellites = satellites
##        self.altitude = altitude
##        self.speed = speed
##        self.accuracy = accuracy
##        self.direction = direction
##        self.provider = provider
##        self.timestamp_epoch = timestamp_epoch
##        self.timeutc = timeutc
##        self.date = date
##        self.startstamp = startstamp
##        self.battery = battery
##        self.androidid = androidid
##        self.serial = serial
##        self.profile = profile
##        self.hdop = hdop
##        self.vdop = vdop
##        self.pdop = pdop
##        self.travelled = travelled
##        self.geom = geom
#        
#    def __repr__(self):
#        return f"<GPS entry {self.timeutc}>"
# 
#"""
#Auto generated models using flask-sqlacodegen on database.
#"""   
#class AllStravaActivity(db.Model):
#    __tablename__ = 'All_Strava_Activities'
#
#    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
#    geom = Geometry('MULTILINESTRING', 4326, from_text='ST_GeomFromEWKT', name='geometry')
#    ActName = db.Column(db.String)
#    Date = db.Column(db.Date)
#    Filename = db.Column(db.String)
#    ActType = db.Column(db.String)
#    Bike = db.Column(db.String)
#    Elapsed_Ti = db.Column(db.Integer)
#    Distance = db.Column(db.Float(53))
#    layer = db.Column(db.String)
#    path = db.Column(db.String)
#
#
#
#class CACounty(db.Model):
#    __tablename__ = 'CA_Counties'
#
#    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
#    geom = Geometry('MULTIPOLYGON', 4326, from_text='ST_GeomFromEWKT', name='geometry')
#    statefp = db.Column(db.String(2))
#    countyfp = db.Column(db.String(3))
#    countyns = db.Column(db.String(8))
#    geoid = db.Column(db.String(5))
#    name = db.Column(db.String(100))
#    namelsad = db.Column(db.String(100))
#    lsad = db.Column(db.String(2))
#    classfp = db.Column(db.String(2))
#    mtfcc = db.Column(db.String(5))
#    csafp = db.Column(db.String(3))
#    cbsafp = db.Column(db.String(5))
#    metdivfp = db.Column(db.String(5))
#    funcstat = db.Column(db.String(1))
#    aland = db.Column(db.BigInteger)
#    awater = db.Column(db.BigInteger)
#    intptlat = db.Column(db.String(11))
#    intptlon = db.Column(db.String(12))
#
#
#
#class CaliforniaPlace(db.Model):
#    __tablename__ = 'California_Places'
#
#    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
#    geom = Geometry('MULTIPOLYGON', 4326, from_text='ST_GeomFromEWKT', name='geometry')
#    statefp = db.Column(db.String(2))
#    placefp = db.Column(db.String(5))
#    placens = db.Column(db.String(8))
#    geoid = db.Column(db.String(7))
#    name = db.Column(db.String(100))
#    namelsad = db.Column(db.String(100))
#    lsad = db.Column(db.String(2))
#    classfp = db.Column(db.String(2))
#    pcicbsa = db.Column(db.String(1))
#    pcinecta = db.Column(db.String(1))
#    mtfcc = db.Column(db.String(5))
#    funcstat = db.Column(db.String(1))
#    aland = db.Column(db.BigInteger)
#    awater = db.Column(db.BigInteger)
#    intptlat = db.Column(db.String(11))
#    intptlon = db.Column(db.String(12))
#
#
#
#class OSMCentralCATrail(db.Model):
#    __tablename__ = 'OSM_Central_CA_Trails'
#
#    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
#    geom = Geometry('MULTILINESTRING', 4326, from_text='ST_GeomFromEWKT', name='geometry')
#    full_id = db.Column(db.String(254))
#    osm_id = db.Column(db.String(254))
#    osm_type = db.Column(db.String(254))
#    access = db.Column(db.String(254))
#    highway = db.Column(db.String(254))
#    name = db.Column(db.String(254))
#    tiger_cfcc = db.Column(db.String(254))
#    tiger_coun = db.Column(db.String(254))
#    tiger_name = db.Column(db.String(254))
#    tiger_revi = db.Column(db.String(254))
#    tracktype = db.Column(db.String(254))
#    surface = db.Column(db.String(254))
#    tiger_sour = db.Column(db.String(254))
#    bicycle = db.Column(db.String(254))
#    motor_vehi = db.Column(db.String(254))
#    motorcar = db.Column(db.String(254))
#    motorcycle = db.Column(db.String(254))
#    tiger_tlid = db.Column(db.String(254))
#    foot = db.Column(db.String(254))
#    path = db.Column(db.String(200))
#    uc = db.Column(db.String(80))
#    layer = db.Column(db.String(100))
#
#
#
#class POI(db.Model):
#    __tablename__ = 'POI'
#
#    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
#    geom = Geometry('MULTIPOLYGON', 4326, from_text='ST_GeomFromEWKT', name='geometry')
#    location = db.Column(db.String(80))
#    desc = db.Column(db.String(80))
#
#
#
#t_geography_columns = db.Table(
#    'geography_columns',
#    db.Column('f_table_catalog', db.String),
#    db.Column('f_table_schema', db.String),
#    db.Column('f_table_name', db.String),
#    db.Column('f_geography_column', db.String),
#    db.Column('coord_dimension', db.Integer),
#    db.Column('srid', db.Integer),
#    db.Column('type', db.Text)
#)
#
#
#
#t_geometry_columns = db.Table(
#    'geometry_columns',
#    db.Column('f_table_catalog', db.String(256)),
#    db.Column('f_table_schema', db.String),
#    db.Column('f_table_name', db.String),
#    db.Column('f_geometry_column', db.String),
#    db.Column('coord_dimension', db.Integer),
#    db.Column('srid', db.Integer),
#    db.Column('type', db.String(30))
#)
#
#
#
#class Gpsdatum(db.Model):
#    __tablename__ = 'gpsdata'
#
#    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
#    gpstime = db.Column(db.DateTime(True))
#    lat = db.Column(db.Float(53))
#    lon = db.Column(db.Float(53))
#    elevation = db.Column(db.Float)
#    accuracy = db.Column(db.Float)
#    bearing = db.Column(db.Float)
#    speed = db.Column(db.Float)
#    satellites = db.Column(db.Integer)
#    provider = db.Column(db.String(10))
#    hdop = db.Column(db.Float)
#    vdop = db.Column(db.Float)
#    pdop = db.Column(db.Float)
#    geoidheight = db.Column(db.Float)
#    ageofdgpsdata = db.Column(db.String(15))
#    dgpsid = db.Column(db.String(10))
#    activity = db.Column(db.String(40))
#    battery = db.Column(db.Integer)
#    phone = db.Column(db.String(40))
#    inserttime = db.Column(db.Time)
#    gpstimelocal = db.Column(db.Time)
#    city = db.Column(db.String(30))
#    county = db.Column(db.String(30))
#    poi = db.Column(db.String(30))
#    road = db.Column(db.String(30))
#    dist_nearestroad = db.Column(db.Float)
#    trail = db.Column(db.String(30))
#    dist_nearesttrail = db.Column(db.Float)
#    geom = Geometry('POINT', 4326, from_text='ST_GeomFromEWKT', name='geometry')
#
#
#
#class MocoRoad(db.Model):
#    __tablename__ = 'moco_roads'
#
#    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
#    geom = Geometry('MULTILINESTRING', 4326, from_text='ST_GeomFromEWKT', name='geometry')
#    fid = db.Column(db.BigInteger)
#    prefix = db.Column(db.String(80))
#    name = db.Column(db.String(80))
#    suffix = db.Column(db.String(80))
#    full_name = db.Column(db.String(80))
#    alias = db.Column(db.String(80))
#    route = db.Column(db.String(80))
#    road_type = db.Column(db.String(80))
#    func_class = db.Column(db.String(80))
#    l_cmnty_co = db.Column(db.String(80))
#    r_cmnty_co = db.Column(db.String(80))
#    l_zip = db.Column(db.BigInteger)
#    r_zip = db.Column(db.BigInteger)
#    from_l_add = db.Column(db.BigInteger)
#    to_l_addre = db.Column(db.BigInteger)
#    from_r_add = db.Column(db.BigInteger)
#    to_r_addre = db.Column(db.BigInteger)
#    low_addres = db.Column(db.BigInteger)
#    high_addre = db.Column(db.BigInteger)
#    maint_by = db.Column(db.String(80))
#    surface = db.Column(db.String(80))
#    road_numbe = db.Column(db.String(80))
#    road_seg = db.Column(db.String(80))
#    map_number = db.Column(db.String(80))
#    map_coord = db.Column(db.String(80))
#    one_way = db.Column(db.String(80))
#    length = db.Column(db.Numeric)
#    minutes = db.Column(db.BigInteger)
#    f_zlev = db.Column(db.BigInteger)
#    t_zlev = db.Column(db.BigInteger)
#    _class = db.Column('class', db.BigInteger)
#    speed = db.Column(db.BigInteger)
#    shape_len = db.Column(db.Numeric)
#    shape__len = db.Column(db.Numeric)
#
#
#
#t_raster_columns = db.Table(
#    'raster_columns',
#    db.Column('r_table_catalog', db.String),
#    db.Column('r_table_schema', db.String),
#    db.Column('r_table_name', db.String),
#    db.Column('r_raster_column', db.String),
#    db.Column('srid', db.Integer),
#    db.Column('scale_x', db.Float(53)),
#    db.Column('scale_y', db.Float(53)),
#    db.Column('blocksize_x', db.Integer),
#    db.Column('blocksize_y', db.Integer),
#    db.Column('same_alignment', db.Boolean),
#    db.Column('regular_blocking', db.Boolean),
#    db.Column('num_bands', db.Integer),
#    db.Column('pixel_types', db.ARRAY(TEXT())),
#    db.Column('nodata_values', db.Float(53)),
#    db.Column('out_db', db.Boolean),
#    db.Column('extent', Geometry(from_text='ST_GeomFromEWKT', name='geometry')),
#    db.Column('spatial_index', db.Boolean)
#)
#
#
#
#t_raster_overviews = db.Table(
#    'raster_overviews',
#    db.Column('o_table_catalog', db.String),
#    db.Column('o_table_schema', db.String),
#    db.Column('o_table_name', db.String),
#    db.Column('o_raster_column', db.String),
#    db.Column('r_table_catalog', db.String),
#    db.Column('r_table_schema', db.String),
#    db.Column('r_table_name', db.String),
#    db.Column('r_raster_column', db.String),
#    db.Column('overview_factor', db.Integer)
#)
#
#
#
#class SpatialRefSy(db.Model):
#    __tablename__ = 'spatial_ref_sys'
#    __table_args__ = (
#        db.CheckConstraint('(srid > 0) AND (srid <= 998999)'),
#    )
#
#    srid = db.Column(db.Integer, primary_key=True)
#    auth_name = db.Column(db.String(256))
#    auth_srid = db.Column(db.Integer)
#    srtext = db.Column(db.String(2048))
#    proj4text = db.Column(db.String(2048))
#
#
#
#class Testtab(db.Model):
#    __tablename__ = 'testtab'
#
#    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
#    testf1 = db.Column(db.String(30))
#    testf2 = db.Column(db.String(30))
#  