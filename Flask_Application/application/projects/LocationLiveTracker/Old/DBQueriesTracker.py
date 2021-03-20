#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains PostgresSQL database query functions that are called by the functions and authentication modules.

Created on Mon May 25 17:40:53 2020

@author: Gavin Leavitt


"""
from application.projects.location_tracker import models_tracker, db
import pytz
from application.models_tracker import gpsdatmodel, gpstracks, AOI, CaliforniaPlaces, CACounty
from application import functions as func
# from application import script_config as dbconfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, distinct
from application.models_tracker import gpsdatmodel as gpsdat
from sqlalchemy import func as sqlfunc
from datetime import datetime
from flask.json import jsonify
import geojson
from geojson import Point, Feature, FeatureCollection, LineString
# from geoalchemy2.shape import to_shape
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
import os
