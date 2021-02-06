#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:25:08 2020

@author: Gavin Leavitt

"""
from datetime import datetime
from geojson import Point, Feature, FeatureCollection
from application import script_config as dbconfig
from application.projects.location_tracker.modelsTracker import gpsPointModel, gpstracks, AOI, CaliforniaPlaces, CACounty
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func as sqlfunc
from application import Session
from application import application
import os
import pytz
import geojson


# def createSession():
#     engine = create_engine(os.environ.get("DBCON"))
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session

#TODO:
# Re-do the documentation for this function, out of date for new datetime query function
def getTrackerFeatCollection(datatype, reclimit):
    """
    handleTrackerQueries PostgreSQL using SQLAlchemy and GeoAlchemy functions, returns data formatted as a geoJSON feature collection.
    All stored attribute information are returned along with the geometries. gpstracks are returned for the current day,
    using the pytz library to set the today date to the US/Pacific timezone, instead of using the system clock. This
    enables the map to be accurate for the west coast, where most of the usage of the app will take place.

    Parameters
    ----------
    datatype: String. Type of data being queried, points or tracks
    reclimit: Int. Number of gpspoints to return

    Returns
    -------
    GeoJSON Feature Collection of datatype parameter containing all stored attribute information.

    """
    session = Session()
    if datatype == "gpspoints":
        # Query using GeoAlchemy PostGIS function to get geojson representation of geometry and regular query to get
        # tabular data
        query = session.query(sqlfunc.ST_AsGeoJSON(gpsPointModel.geom), gpsPointModel).order_by(gpsPointModel.id.desc()).\
            limit(reclimit)
    elif datatype == "gpstracks":

        newestRecordTime = session.query(gpsPointModel.timezone, gpsPointModel.timeutc). \
            order_by(gpsPointModel.timeutc.desc()).limit(1).all()
        recTZ = []
        recDateTime = []
        for row in newestRecordTime:
            recTZ.append(row.timezone)
            recDateTime.append(row.timeutc)

        # Set time to UTC time zone:
        # utcTime = recDateTime[0].replace(tzinfo=recTZ[0])
        # application.logger.debug(f"Queried time is: {recDateTime[0]}")
        utcTime = recDateTime[0].replace(tzinfo=pytz.utc)
        # application.logger.debug(f"UTC time is: {utcTime }")
        localTime = utcTime.astimezone(recTZ[0])
        # application.logger.debug(f"Local time time is: {localTime}")
        startofDayLocal = localTime.replace(hour=0, minute=0, second=0, microsecond=0)
        # Convert to startofDayLocal to UTC time
        # application.logger.debug(f"Start of day in local is: {startofDayLocal}")
        startofDayUTC = startofDayLocal.astimezone(pytz.utc)
        # application.logger.debug(f"Start of day in UTC is: {startofDayUTC}")

        # Query using GeoAlchemy PostGIS function to get geojson representation of geometry and regular query to get
        # tabular data
        # Since all records are recorded in PST, they will always be -8 from UTC so the date in postgres may be a day
        # ahead of the local time, use >= to account for this
        # query = session.query(sqlfunc.ST_AsGeoJSON(gpstracks.geom), gpstracks).filter_by(date=todaydate)
        query = session.query(sqlfunc.ST_AsGeoJSON(gpstracks.geom), gpstracks).filter(gpstracks.timeutc >= startofDayUTC)
    features = []
    for row in query:
        # Build a dictionary of the attribute information
        prop_dict = row[1].builddict()
        # Take ST_AsGeoJSON() result and load as geojson object
        geojson_geom = geojson.loads(row[0])
        # Build the feature and add to feature list
        features.append(Feature(geometry=geojson_geom, properties=prop_dict))
    session.close()
    # Build the feature collection result
    feature_collection = FeatureCollection(features)
    return feature_collection


def getDist(coordinate1, coordinate2):
    """
    Get the distance between the newest incoming point and the most recent previously recorded
    point, distance is reported as meters by default by ST_DistanceSphere.

    Parameters
    ----------
    coordinate:1 String
        WKT representation of the most recently recorded GPS point coordinates.
    coordinate2: String
        WKT representation of the incoming GPS point coordinates.

    Returns
    -------
    dist : Float
        Distance in meters between the newest and most recent recorded points.

    """
    session = Session()
    # Geoalchemy ORM expression
    res = session.query(
        sqlfunc.ST_DistanceSphere(sqlfunc.ST_GeomFromText(coordinate1), sqlfunc.ST_GeomFromText(coordinate2)))
    # coordinate1 = coordinate1
    # res = db.session.query(sqlfunc.ST_DistanceSphere(coordinate1,coordinate2))
    dist = None
    for i in res:
        # Make sure the data comes through as a float, not a ORM object
        dist = float(i[0])
        # Round off number, don't need high precision
        dist = round(dist, 1)
    session.close()
    return dist


def getPathPointRecords():
    """
    Gets the most recently recorded GPS point, used to check for movement and to generate a GPS track. This entire function may not be needed
    and can likely be combined with "getrecords".

    Returns a dictionary with a single top level key and a nested dictionary of record details, kept logic for multiple top level keys in
    case I need to build this function out.

    Parameters
    ----------
    Returns
    -------
    res_dict : Dictionary
       Results of gps point query with details as keys.

    """

    session = Session()
    # records = session.query(gpsdatmodel.id, gpsdatmodel.lat, gpsdatmodel.lon, gpsdatmodel.geom, gpsdatmodel.timeutc,
    #                         gpsdatmodel.date). \
    #     filter(gpsdatmodel.getLocalTime() >= dateTime). \
    #     order_by(gpsdatmodel.timeutc.desc()).limit(1).all()
    records = session.query(gpsPointModel.id, gpsPointModel.lat, gpsPointModel.lon, gpsPointModel.geom,
                            gpsPointModel.timeutc, gpsPointModel.date). \
        order_by(gpsPointModel.timeutc.desc()).limit(1).all()
    res_dict = {}
    row_count = 0
    for row in records:
        row_count += 1
    if row_count > 0:
        for row in records:
            res_dict[row.id] = {"id": row.id, "lat": row.lat, "lon": row.lon, "utc": row.timeutc, "date": row.date,
                                "geom": row.geom}
        session.close()
        return res_dict
    else:
        session.close()
        return None


def AOIIntersection(geomdat):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the AOI PostGIS table and returns a string of results.

    The AOI table contains hand digitized locations of interest.

    Currently only single POI results are returned, however this will change as POIs are added.

    Parameters
    ----------
    geomdat : String
        WKT representation of the incoming GPS point coordinates.

    Returns
    -------
    result : String
        AOI results as a string with individual results comma seperated or None in case
            of empty result.
        A comma seperated string is returned for easier processing and insertion into
        dictionary created by the handleTrackerQueries function.

    """
    session = Session()
    # SQLAlchemy and GeoAlchemy SQL query
    query = session.query(AOI).filter(AOI.geom.ST_Intersects(geomdat))
    # Get the size of the result, used for building out the string result.
    query_count = 0
    for i in query:
        query_count += 1

    if query_count > 0:
        result = ""
        count = 0
        # Iterate over SQL Alchemy result object, if greater than 1 result build out with comma seperation.
        for POI in query:
            if count > 0:
                # result object columns can be individually called with their column names, only want location info.
                result += "," + POI.location
                count += 1
            else:
                result += POI.location
                count += 1
    else:
        session.close()
        return None
    session.close()
    return result


def cityIntersection(geomdat):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the city PostGIS table and returns a string of results.

    Parameters
    ----------
    geomdat : String
        WKT representation of the incoming GPS point coordinates.

    Returns
    -------
    result : String
        String of intersecting city or None if empty result.
        Should only ever be a single result but logic is included in case of multiple
        records returned.

    """
    session = Session()
    query = session.query(CaliforniaPlaces).filter(CaliforniaPlaces.geom.ST_Intersects(geomdat))
    query_count = 0
    for i in query:
        query_count += 1
        # Logic to create a comma separted string of all results in case multiple cities
    # are returned, this should not happen under normal circumstances
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
        session.close()
        return None
    session.close()
    return result


def countyIntersection(geomdat):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the county PostGIS table and returns a string of results.

    Parameters
    ----------
    geomdat : String
        WKT representation of the incoming GPS point coordinates.

    Returns
    -------
    TYPE
        String of intersecting city or None if empty result.
        Should only ever be a single result but logic is included in case of multiple
        records returned.

    """

    session = Session()
    query = session.query(CACounty).filter(CACounty.geom.ST_Intersects(geomdat))

    query_count = 0
    for i in query:
        query_count += 1
        # Logic to create a comma separted string of all results in case multiple counties
    # are returned, this should not happen under normal circumstances
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
        session.close()
        return "Out of State!"
    session.close()
    return result


def getNearestRoad(coordinate):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the roads PostGIS table and returns a dictionary of nearest road
    and distance to road in feet.

    SQL expression is in raw form until it can be converted to SQLAlchemy format.

    Query uses bounding box index location (<-> in SQL) to get candiate roads (40 records) then passes the results into the
    ST_DistanceSphere function to get the nearest road. ST_DistanceSphere assumes the data are in WGS 84 and returns distance in meters.

    The bounding box index calculations are fast but not entirely accurate, this method is useful for creating a smaller
    list of results to run more costly ST_DistanceSphere calculations on.

    Parameters
    ----------
    coordinate: String
        WKT representation of the incoming GPS point coordinates.


    Returns
    -------
    result : dictionary
        dictionary with the keys: "street" and "distance".
            street:
                String of nearest street
            distance:
                Distance in feet to nearest road
        Results should never be empty, no matter how far away nearest road is.

    """

    sql = text("""WITH nearestcanidates AS (
    SELECT
        roads.name,
        roads.geom
    FROM
        	roads AS roads
    WHERE
        roads.name IS NOT NULL
    ORDER BY
        	roads.geom <-> (ST_GeomFromText(:param, 4326))
    LIMIT 40)

    SELECT 
        nearestcanidates.name,
        ST_DistanceSphere(
                nearestcanidates.geom,
                ST_GeomFromText(:param, 4326)
                ) AS distance
    FROM
        nearestcanidates
    ORDER BY
        distance
    LIMIT 1""")

    session = Session()
    # Execute database query using the coordinates as a variable.
    # print(f"Going to run query with coordinate: {coordinate}")
    query = session.execute(sql, {"param": coordinate})
    result = {}
    query_count = 0
    # Build out dict with each result in query
    for dat in query:
        result["street"] = dat[0]
        # Convert meters (default unit of postgis function) to feet
        result["distance"] = dat[1] * 3.28
        query_count += 1
    if query_count == 0:
        result['street'], result['distance'] = None, None
    session.close()
    return result


def getNearestTrail(coordinate):
    """
    Issues a SQLAlchemy/GeoAlchemy intersection query against the trails PostGIS table and returns a dictionary of nearest trail
    and distance to trail in feet. Trails with name "Unknown" are excluded from results.

    SQL expression is in raw form until it can be converted to SQLAlchemy format.

    Query uses bounding box index location (<-> in SQL) to get candiate roads (40 records) then passes the results into the
    ST_DistanceSphere function to get the nearest road. ST_DistanceSphere assumes the data are in WGS 84 and returns distance in meters.

    The bounding box index calculations are fast but not entirely accurate, this method is useful for creating a smaller
    list of results to run more costly ST_DistanceSphere calculations on.

    Parameters
    ----------
    coordinate: String
        WKT representation of the incoming GPS point coordinates.

    Returns
    -------
    result : dictionary
        dictionary with the keys: "trail" and "trail_distance"
            street:
                String of nearest trail
            distance:
                Distance in feet to nearest trail

    Results should never be empty, no matter how far nearest trail is.
    """
    # Raw SQL query with triple quotes to maintain formatting, see function comments for descripton
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
    session = Session()
    query = session.execute(sql, {"param": coordinate})
    result = {}
    query_count = 0
    for dat in query:
        result["trail"] = dat[0]
        result["trail_distance"] = dat[1]
        query_count += 1
    if query_count == 0:
        result['trail'], result['trail_distance'] = None, None
    session.close()
    return result
