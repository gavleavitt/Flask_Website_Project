#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 16:24:43 2020

@author: user
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, distinct, create_engine, or_, Column, String, Integer, Date, Boolean, ForeignKey, BigInteger, Float, Interval
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func as sqlfunc
import geojson
from geojson import Point, Feature, FeatureCollection, LineString
import os

engine = create_engine(os.environ.get("DBCON"))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class beaches(Base):
    __tablename__ = 'Beaches'

    id = Column(Integer, primary_key=True)
    BeachName = Column(String)

class waterQualityMD5(Base):
    __tablename__ = 'water_qual_md5'

    id = Column(Integer, primary_key=True)
    pdfdate = Column(Date)
    insdate = Column(Date)
    md5 = Column(String)
    pdfName = Column(String)


class stateStandards(Base):
    __tablename__ = "StateStandards"

    id = Column(Integer, primary_key=True)
    Name = Column(String)
    StandardMPN = Column(String)

class waterQuality(Base):
    __tablename__ = "Water_Quality"

    id = Column(Integer, primary_key=True)
    TotColi = Column(Integer)
    FecColi = Column(Integer)
    Entero = Column(Integer)
    ExceedsRatio = Column(String)
    BeachStatus = Column(String)
    beach_id = Column(Integer, ForeignKey("Beaches.id"))
    md5_id = Column(Integer, ForeignKey("water_qual_md5.id"))
    resample = Column(String)

    beach_rel = relationship(beaches, backref="Water_Quality")
    hash_rel = relationship(waterQualityMD5, backref="Water_Quality")

class strava_activities(Base):
    __tablename__ = "strava_activities"

    id = Column(Integer, primary_key=True)
    actID = Column(BigInteger)
    upload_id = Column(String(50))
    name = Column(String(255))
    distance = Column(Float)
    moving_time = Column(Interval)
    elapsed_time = Column(Interval)
    total_elevation_gain = Column(Float)
    elev_high = Column(Float)
    elev_low = Column(Float)
    type = Column(String(50))
    start_date = Column(Date)
    start_date_local = Column(Date)
    timezone = Column(String(50))
    utc_offset = Column(Float)
    start_latlng = Column(String(100))
    end_latlng = Column(String(100))
    start_latitude = Column(Float)
    start_longitude = Column(Float)
    achievement_count = Column(Integer)
    pr_count = Column(Integer)
    private = Column(String(50))
    gear_id = Column(String(50))
    average_speed = Column(Float)
    max_speed = Column(Float)
    average_watts = Column(Float)
    kilojoules = Column(Float)
    description = Column(String(255))
    workout_type = Column(String(100))
    calories = Column(Float)
    geom = Column(Geometry(geometry_type='LINESTRINGM', srid=4326, from_text = 'ST_GeomFromEWKT',  name='geometry',
                           dimension=3))
    def builddict(self):
        """
        Formats data in a GeoJSON friendly format, removes troublesome columns and formats datetime fields using .isoformat()
        :return: Dictionary with attribute data
        """
        removedictlist = ['_sa_instance_state', 'geom']
        dateCol = ["start_date", "start_date_local"]
        durCol = ["moving_time", "elapsed_time"]
        res_dict = self.__dict__
        for i in removedictlist:
            res_dict.pop(i, None)
        for v in dateCol:
            res_dict[v] = res_dict[v].isoformat()
        for h in durCol:
            res_dict[h] = res_dict[h].seconds
        # for item in res_dict.keys():
        #     if res_dict[item] is None:
        #         res_dict[item] = ''
        return res_dict

def getwaterqual():
    records = session.query(distinct(waterQuality.md5_id)) \
        .join(beaches) \
        .join() \
        .order_by(waterQualityMD5.insdate)

def getStravaActGeoJSON(actLimit):
    query = session.query(sqlfunc.ST_AsGeoJSON(strava_activities.geom), strava_activities).limit(actLimit)
    features = []
    for row in query:
        # Build a dictionary of the attribute information
        prop_dict = row[1].builddict()
        # Take ST_AsGeoJSON() result and load as geojson object
        geojson_geom = geojson.loads(row[0])
        # print(row[0])
        # geojson_geom = LineString(row[0])
        # Build the feature and add to feature list
        features.append(Feature(geometry=geojson_geom, properties=prop_dict))
    # Build the feature collection result
    feature_collection = FeatureCollection(features)
    # print(feature_collection)
    return feature_collection
