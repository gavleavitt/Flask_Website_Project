#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the models for tables in the Postgres AWS RDS that are used for SQLAlchemy ORM.
These models get there base declarative state from the flask_sqlalchemy import and application created
in the init module.

Created on Fri May 22 01:09:08 2020

@author: Gavin Leavitt
"""
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Integer, String
from sqlalchemy.schema import FetchedValue
from geoalchemy2.types import Geometry
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
import pytz
from datetime import datetime

Base = declarative_base()




class gpstracks(Base):
    __tablename__ = 'gpstracks'

    id = Column(Integer, primary_key=True)
    timestamp_epoch = Column(DateTime())
    timeutc = Column(DateTime())
    date = Column(Date())
    startstamp = Column(DateTime())
    gpsid = Column(Integer())
    androidid = Column(String(30))
    serial = Column(String(30))
    profile = Column(String(30))
    length = Column(Float())
    timezone = Column(String(30))
    geom = Column(Geometry('Linestring', 4326, from_text='ST_GeomFromEWKT', name='geometry'))


    def builddict(self):
        """
        Formats data in a GeoJSON friendly format, removes troublesome columns and formats datetime fields using .isoformat()
        :return: Dictionary with attribute data
        """
        removedictlist = ['_sa_instance_state', 'geom']
        dateCol = ["timestamp_epoch", "timeutc", "date", "startstamp"]
        res_dict = self.__dict__
        for i in removedictlist:
            res_dict.pop(i, None)
        for i in dateCol:
            res_dict[i] = res_dict[i].isoformat()
        return res_dict

class gpsPointModel(Base):
    __tablename__ = 'gpstrackerpoints'

    id = Column(Integer, primary_key=True)
    lat = Column(Float())
    lon = Column(Float())
    satellites = Column(Integer())
    altitude = Column(Float())
    speed = Column(Float())
    accuracy = Column(Float())
    direction = Column(Integer())
    provider = Column(String(30))
    timestamp_epoch = Column(DateTime())
    timeutc = Column(DateTime())
    date = Column(Date())
    startstamp = Column(DateTime())
    battery = Column(Integer())
    androidid = Column(String(30))
    serial = Column(String(30))
    profile = Column(String(30))
    hhop = Column(Float())
    vdop = Column(Float())
    pdop = Column(Float())
    activity = Column(String(30))
    travelled = Column(Float())
    nearestroad = Column(String(30))
    dist_nearestroad = Column(Float())
    nearesttrail = Column(String(30))
    dist_nearesttrail = Column(Float())
    AOI = Column(String(30))
    city = Column(String(30))
    county = Column(String(30))
    timezone = Column(String(30))
    method = Column(String(30))
    geom = Column(Geometry('POINT', 4326, from_text='ST_GeomFromEWKT', name='geometry'))


    def getLocalTime(self, tz):
        """
        Converts the database Datetime to local time using the provided time zone.

        Parameters
        ----------
        tz: String. tz database formatted time zone.
        -------

        Returns
        -------
        result : Str. Iso formatted time in input timezone

        """

        # tz = pytz.timezone("US/Pacific")
        # print(datetime.fromisoformat(self.startstamp))
        # print(datetime.fromisoformat(self.startstamp).replace(tzinfo=tz))

        # Create date time object with timezone set to UTC:
        utcTime = datetime.fromisoformat(self.timeutc).replace(tzinfo=pytz.utc)
        # Set to PST and return
        # print(utcTime.astimezone(tz))
        return utcTime.astimezone(pytz.timezone(tz)).isoformat()
    
    def builddict(self):
        """
        Formats data in a GeoJSON friendly format, removes troublesome columns and formats datetime fields using .isoformat()
        :return: Dictionary with attribute data
        """
        removedictlist = ['_sa_instance_state', 'geom']
        dateCol = ["timestamp_epoch", "timeutc", "date", "startstamp"]
        res_dict = self.__dict__
        for i in removedictlist:
            res_dict.pop(i, None)
        for v in dateCol:
            if type(res_dict[v]) != "str":
                res_dict[v] = res_dict[v].isoformat()
        res_dict["timeLocal"] = self.getLocalTime(self.timezone)
        # print(self.getPSTTime())
        return res_dict

class CACounty(Base):
    __tablename__ = 'CA_Counties'

    id = Column(Integer, primary_key=True, server_default=FetchedValue())
    geom = Column(Geometry('MULTIPOLYGON', 4326, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    statefp = Column(String(2))
    countyfp = Column(String(3))
    countyns = Column(String(8))
    geoid = Column(String(5))
    name = Column(String(100))
    namelsad = Column(String(100))
    lsad = Column(String(2))
    classfp = Column(String(2))
    mtfcc = Column(String(5))
    csafp = Column(String(3))
    cbsafp = Column(String(5))
    metdivfp = Column(String(5))
    funcstat = Column(String(1))
    aland = Column(BigInteger)
    awater = Column(BigInteger)
    intptlat = Column(String(11))
    intptlon = Column(String(12))

class CaliforniaPlaces(Base):
    __tablename__ = 'California_Places'

    id = Column(Integer, primary_key=True, server_default=FetchedValue())
    geom = Column(Geometry('MULTIPOLYGON', 4326, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    statefp = Column(String(2))
    placefp = Column(String(5))
    placens = Column(String(8))
    geoid = Column(String(7))
    name = Column(String(100))
    namelsad = Column(String(100))
    lsad = Column(String(2))
    classfp = Column(String(2))
    pcicbsa = Column(String(1))
    pcinecta = Column(String(1))
    mtfcc = Column(String(5))
    funcstat = Column(String(1))
    aland = Column(BigInteger)
    awater = Column(BigInteger)
    intptlat = Column(String(11))
    intptlon = Column(String(12))


class OSMCentralCATrail(Base):
    __tablename__ = 'OSM_Central_CA_Trails'

    id = Column(Integer, primary_key=True, server_default=FetchedValue())
    geom = Column(Geometry('MULTILINESTRING', 4326, from_text='ST_GeomFromEWKT', name='geometry'), index=True)
    full_id = Column(String(254))
    osm_id = Column(String(254))
    osm_type = Column(String(254))
    access = Column(String(254))
    highway = Column(String(254))
    name = Column(String(254))
    tiger_cfcc = Column(String(254))
    tiger_coun = Column(String(254))
    tiger_name = Column(String(254))
    tiger_revi = Column(String(254))
    tracktype = Column(String(254))
    surface = Column(String(254))
    tiger_sour = Column(String(254))
    bicycle = Column(String(254))
    motor_vehi = Column(String(254))
    motorcar = Column(String(254))
    motorcycle = Column(String(254))
    tiger_tlid = Column(String(254))
    foot = Column(String(254))
    path = Column(String(200))
    uc = Column(String(80))
    layer = Column(String(100))

class AOI(Base):
    __tablename__ = 'AOI'

    id = Column(Integer, primary_key=True, server_default=FetchedValue())
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)
    location = Column(String(80))
    desc = Column(String(80))
    privacy = Column(String(50))

class Roads(Base):
    __tablename__ = 'roads'

    id = Column(Integer, primary_key=True, server_default=FetchedValue())
    geom = Column(Geometry('MULTILINESTRING', 4326), index=True)
    full_id  = Column(String(80))
    osm_id = Column(String(80))
    osm_type = Column(String(80))
    bicycle = Column(String(80))
    foot = Column(String(80))
    highway = Column(String(80))
    name = Column(String(80))
    surface = Column(String(80))

