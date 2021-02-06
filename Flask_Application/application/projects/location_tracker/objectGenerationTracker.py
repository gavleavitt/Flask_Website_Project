#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 19:29:11 2020

@author: Gavin Leavitt
"""

from application.projects.location_tracker import DBQueriesTracker as trackerFunc
from application.projects.location_tracker import OverPassAPI as OPA
from application.projects.location_tracker.modelsTracker import gpsPointModel, gpstracks
from application import application
from application import script_config as dbconfig
from application import Session
import time
from datetime import datetime
import pytz

def handleTrackerPOST(data):
    """

    Parameters
    ----------
    data

    Returns
    -------

    """
    session = Session()
    newObjDict = {}
    # Create instance of a gps track
    trackRecord = gpsTrackObj(data)
    # Check if there has been movement, if so add to new object dictionary, otherwise no entry will be made
    if trackRecord["activity"] == "Yes":
        newObjDict["track"] = trackRecord["model"]
    # Add new gps record object to new objects dictionary
    newObjDict["gpspoint"] = newGPSRecord(data, trackRecord["activity"])
    # Iterate over new objdict, can allow building out so many things can be committed to db
    # This allows for empty models to be skipped
    newObjs = []
    for obj in newObjDict.keys():
        newObjs.append(newObjDict[obj])
    # Add new objects to session and commit them
    session.add_all(newObjs)
    session.commit()
    session.close()


def gpsTrackObj(data):
    """
    Return activity status and a new track record if movement has been detected.
    This is a higher level function for generating a new track object and calls on helper functions residing within the functions module. 
    Movement status is based on whether or not the gps record has moved > 3 m, or 10 feet. 

    Parameters
    ----------
    data : Dict
        Dictionary of POST JSON data.

    Returns
    -------
    data: Dict
        Dict containing the gps track object (to be inserted into DB) and activity status (yes/no).

    """
    # Extract lat and lon from POST data
    coordinates = f"{data['Longitude']} {data['Latitude']}"
    # print("Converting time types!")
    # Convert time formats from POST data
    timeDict = convertTime(data['Timestamp'], data['Start_timestamp'], data['Time_Zone'])
    tracks = handleTracks(coordinates, data['Provider'])
    # print(f"!! tracks result is: {tracks}")
    if tracks["activity"] == "Yes":
        model = gpstracks(timestamp_epoch=timeDict['Timestamp_e'], timeutc=data['Time_UTC'], date=timeDict["Date"],
                          startstamp=timeDict['Timestart'], androidid=data['Android_ID'],
                          serial=data['Serial'], profile=data['Profile'], length=tracks['length'], gpsid=None,
                          geom=tracks['Linestring'], timezone=data['Time_Zone'])
    else:
        model = None
    return {"model": model, "activity": tracks["activity"]}


def newGPSRecord(data, actStatus):
    """
    

    Parameters
    ----------
    data : Dict
        Dictionary of POST JSON data.
    actStatus : String
        Activity status, yes/no.

    Returns
    -------
    model: Object
        gpsdatmodel object containing data to be inserted into DB.

    """
    geomData = (f"SRID={dbconfig.settings['srid']};POINT({data['Longitude']} {data['Latitude']})")
    queryData = handleTrackerQueries(geomData, data['Latitude'], data['Longitude'], data['Profile'].replace("+", " "))
    timeDict = convertTime(data['Timestamp'], data['Start_timestamp'], data['Time_Zone'])
    model = gpsPointModel(lat=data['Latitude'], lon=data['Longitude'], satellites=int(data['Satellites']),
                        altitude=float(data['Altitude']), speed=float(data['Speed']),
                        accuracy=data['Accuracy'].split(".")[0], direction=data['Direction'].split(".")[0],
                        provider=data['Provider'], timestamp_epoch=timeDict['Timestamp_e'], timeutc=data['Time_UTC'],
                        date=timeDict['Date'], startstamp=timeDict['Timestart'], battery=data['Battery'].split(".")[0],
                        androidid=data['Android_ID'], serial=data['Serial'], profile=data['Profile'].replace("+", " "),
                        hhop=stringToNone((data['hdop'])),
                        vdop=stringToNone((data['vdop'])),
                        pdop=stringToNone((data['pdop'])),
                        activity=actStatus, travelled=data['Dist_Travelled'].split(".")[0], AOI=queryData['AOI'],
                        city=queryData['city'], county=queryData['county'], nearestroad=queryData['road'],
                        dist_nearestroad=queryData['dist_road'], nearesttrail=queryData['trail'],
                        dist_nearesttrail=queryData['dist_trail'], method=queryData["method"], geom=geomData)
    return model

#TODO:
# Update documentation to include OSM queries
def handleTrackerQueries(geomData, lat, lon, profile):
    """
    Takes Flask API HTTP POST GPS data and issues pre-defined SQLAlchemy database query functions.
    Data is returned in a dict format that is prepared for insertion into the gps activity database table.

    Parameters
    ----------
    geomdat : String
        WKT representation of the incoming GPS point coordinates.

        *I created this before I understood  how to better work with coordinates in handleTrackerQueries,
        this can possibly be improved in the future but is functional for now.

    Returns
    -------
    res : dictionary
        dictionary with results of database handleTrackerQueries, with the following keys:
            AOI, City, county, road, dist_road, trail, and dist_trail.
        Empty result values are returned as None, a database friendy format.

    """
    # Build a dict with DB query results
    res = {}
    # Get AOI if inside one
    res["AOI"] = trackerFunc.AOIIntersection(geomData)

    try:
        osmWayDict = OPA.handleNearestOSMWays(lat=lat, lon=lon, type=profile)
        osmAreaIntersectDict = OPA.getOSMLocation(lat=lat, lon=lon)
        res['road'] = osmWayDict['Road'][0]
        res["dist_road"] = osmWayDict['Road'][1]
        res['city'] = osmAreaIntersectDict["place"]
        res['county'] = osmAreaIntersectDict["county"]
        res["trail"] = osmWayDict['Route'][0]
        res["dist_trail"] = osmWayDict['Route'][1]
        res["method"] = "Overpass"
    except Exception as e:
        application.logger.debug(f"OSM query failed with the error {e}, failing over to Postgres queries!", exc_info=True)
        # Fail over to Postgres method
        res['city'] = trackerFunc.cityIntersection(geomData)
        res["county"] = trackerFunc.countyIntersection(geomData)
        roadInfo = trackerFunc.getNearestRoad(geomData)
        res["road"] = roadInfo["street"]
        res["dist_road"] = roadInfo["distance"]
        # Check if the AOI intersection returned a result in the AOI list, if so calcuate the nearest trail and distance to
        # trail
        if res["AOI"] in dbconfig.settings["AOI_Outdoors"]:
            outdoors = trackerFunc.getNearestTrail(geomData)
            res["trail"] = outdoors['trail']
            res['dist_trail'] = outdoors['trail_distance']
        else:
            res['trail'], res['dist_trail'] = None, None
        res["method"] = "GeoAlchemy"
    return res


def handleTracks(coordinate2, locationType):
    """
    Determines if the incoming record is the first of the day, which returns no activity, then determines if movement
    has occurred between the incoming record and most recent record for the day. Movement is determined if the distance
    is greater than 3m, or 10ft, between points.
    Returns a dict of movement status and a linestring, if movement has occurred, for the trackrecord model and
    insertion into postgres.

    Parameters
    ----------
    coordinate2 : string
        Incoming gps point in the form of "lon lat".
    locationType: string. States if coordinate came from GPS or from cellular network triangulation.
    Returns
    -------
    dict
        keys:
            "activty":movement status as "Yes" or "No"
            "Linestring": Only created if movement status is "Yes". Contains the WKT string representation of
            "LINESTRING" for input in PostGIS
                model geometry column

    """
    record = trackerFunc.getPathPointRecords()
    # print(f"Record result is: {record}")
    # check if a previous record exists, if not then this is the first record of the day and no movement could have
    # occurred
    if record != None:
        # Convert keys to list
        recid = list(record.keys())
        # Reverse sort keys, list[0] is the key, gpsdat id, of the most recent record
        recid.sort(reverse=True)
        # Format data to be sent to geoalchemy functions as WKT
        # Previous record, pulled from postgres and formatted in WKT
        coor1_Q_str = f"POINT({record[recid[0]]['lon']} {record[recid[0]]['lat']})"
        # Incoming record
        coor2_Q_str = f"POINT({coordinate2})"
        dist = trackerFunc.getDist(coor1_Q_str, coor2_Q_str)
        # print(f"Movement distance is: {dist}")
        #TODO:
        # dist > 100
        if (dist > 10 and locationType != 'network') or dist > 100:
            # print("Movement!")
            # Movement greater than 10m, returns dictionary with linestring formmated WKT record and activity type
            return {
                'Linestring': f'SRID={dbconfig.settings["srid"]};'
                              f'LINESTRING({record[recid[0]]["lon"]} {record[recid[0]]["lat"]}, {coordinate2})',
                "activity": "Yes", "length": dist}
        else:
            return {"activity": "No"}
    else:
        # No previous record, first of the day thus no movement, or no movement greater than 10 feet since last record
        # print("No movement!")
        return {"activity": "No"}

def stringToNone(x):
    """
    Evaluates incoming value to convert empty strings, '', into None types.
    Postgres/SQLAlchemy doesn't handle empty strings well when inputting data into a int or float column.

    Parameters
    ----------
    x : String
        String to be inserted into DB.

    Returns
    -------
    x : String
        String or None value.

    """

    if x == '':
        return None
    else:
        return x


def convertTime(timestamp_e, timestart, timeZone):
    """
    Converts times that are received in the http POST into a dict of datetimes. Postgres always stores datetimes in UTC,
    for this reason records will be converted to local time when they are requested.

    Parameters
    ----------
    timestamp_e : str. UTC Time(since epoch)
        timestamp for the current record.
    timestart : str. UTC Time(since epoch)
        start timestamp of the current recording session.
    timeZone: str. tz database formatted time zone.
    Returns
    -------
    result : dict{} with keys "timestamp_e","timestart", "Date", "timeLocal"
    """

    # timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp_e)))
    # start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestart)))
    # date_today = time.strftime('%Y-%m-%d', time.localtime(int(timestamp_e)))

    # Set timezone to localtime from POST request
    tz = pytz.timezone(timeZone)
    # Convert utc timestamp string (seconds since epoch) to a datetime object then replace timezone with utc
    # Trying to use replace with the variable timeZone resulted in the datetime being set to the wrong time,
    # the datetime object would be set to local time at the UTC time, instead of offset
    utcTime = datetime.utcfromtimestamp(int(timestamp_e)).replace(tzinfo=pytz.utc)
    # Set UTC time to local time zone and return iso string format
    timeLocal = utcTime.astimezone(tz).isoformat()
    # Convert timestamp and start times into UTC datetime objects
    timestamp = datetime.utcfromtimestamp(int(timestamp_e))
    start_time = datetime.utcfromtimestamp(int(timestart))
    # print("Times converted!")

    return {'Timestamp_e': timestamp, 'Timestart': start_time, 'Date': start_time, 'timeLocal': timeLocal}
