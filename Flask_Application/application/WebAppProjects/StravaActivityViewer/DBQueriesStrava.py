from application.WebAppProjects.StravaActivityViewer.modelsStrava import athletes, sub_update, strava_activities, \
    strava_activities_masked, strava_gear, AOI, webhook_subs
from datetime import datetime
from application import application, Session
from application.util.ErrorEmail import errorEmail
from sqlalchemy import func as sqlfunc
import geojson
from geojson import Feature, FeatureCollection, MultiLineString
import topojson as tp
import re


def updateSubId(subId, verifytoken):
    """
    Updates webhook subscriptions table with the new subscription id provided by Strava then updates all athletes
    with the new subID foreign key.
    @param subId: Int. Webhook subscription ID provided by Strava API
    @param verifytoken: String. Script generated verification token
    @return: Nothing. Database is updated
    """
    session = Session()
    try:
        application.logger.debug(f"Updating record with the following token: {verifytoken}")
        # Update recently created record which only has the verify token populated
        # application.logger.debug(session.query(webhook_subs.verify_token == verifytoken).first())
        insQ = session.query(webhook_subs).filter(webhook_subs.verify_token == verifytoken).update(
            {webhook_subs.sub_id: subId,
             webhook_subs.activesub: "Yes"})
        session.commit()
        # Get the primary key from the new webhook subscription
        record = session.query(webhook_subs).filter(webhook_subs.verify_token == verifytoken).first()
        # Update all athletes with the new subscription entry foreign key
        session.query(athletes).update({athletes.sub_id: record.id})
        session.commit()
        session.close()
    except Exception as e:
        application.logger.debug(f"Update Strava athlete sub Id failed with the exception: {e}")
        errorEmail.sendErrorEmail(script=updateSubId.__name__, exceptiontype=e.__class__.__name__, body=e)


def getAthleteList():
    """
    Gets list of athlete IDs from database.

    Returns
    -------
    List. Athlete IDs (int) stored in database.
    """
    session = Session()
    query = session.query(athletes).all()
    athleteList = []
    for i in query:
        athleteList.append(i.athlete_id)
    session.close()
    return athleteList


def getActiveSubID():
    """
    Gets the active Strava webhook subscription ID from the database.
    @return: Int. Active subscription ID
    """
    session = Session()
    query = session.query(webhook_subs).filter(webhook_subs.activesub == "Yes").first()
    session.close()
    if query:
        return int(query.sub_id)


def getSubIdList():
    """
    Gets list of subscription webhook IDs from database.
    Check if used, likely can delete
    Returns
    -------
    List. Subscription webhook IDs (Int) stored in database.
    """
    session = Session()
    query = session.query(athletes).all()
    subIdList = []
    for i in query:
        subIdList.append(i.sub_id)
    session.close()
    return subIdList


def insertSubUpdate(content):
    """

    Inserts Strava webhook subscription data into Postgres database. This information will be used to get full activity
    information from another query.

    Parameters
    ----------
    content. Subscription Update object of Strava webhook update generated by Stravalib

    Returns
    -------
    Nothing. Updates database.
    """
    # Verify is activity title is in update data, if not set to None. Some activities may have empty titles.
    if "title" in content.updates.keys():
        title = content.updates['title']
        application.logger.debug(f"Title of new activity is {title}")
    else:
        title = None
    session = Session()
    insert = sub_update(aspect=content.aspect_type, event_time=datetime.fromtimestamp(content.event_time.timestamp),
                        object_id=content.object_id, object_type=content.object_type, owner_id=content.owner_id,
                        subscription_id=content.subscription_id,
                        update_title=title)
    session.add(insert)
    session.commit()
    session.close()
    application.logger.debug(f"New webhook update has been added to Postgres!")


def updateExistingActivity(update):
    """
    Updates existing activity in database, currently only handles activity title updates.

    @param update: Stravalib update instance
    @return: Nothing.
    """
    # Get object ID
    objectID = update.object_id
    # Get new activity title, if applicable
    newTitle = update.updates['title']
    session = Session()
    # use SQL alchemy to update existing feature title
    session.query(strava_activities).filter(strava_activities.actID == objectID). \
        update({strava_activities.name: newTitle})
    session.commit()
    session.close()


def insertOriginalAct(actDict):
    """
    Inserts new activity into database, POSTed by Strava webhook update or by manually triggering process activity
    event route.

    Parameters
    ----------
    actDict. Dict. Generated by StravaWebHook.handle_sub_update() or by getStravaActivities.processActs().

    Returns
    -------
    Nothing. Data are inserted into Postgres/PostGIS.
    """
    insert = strava_activities(actID=actDict['actId'], upload_id=actDict['upload_id'], name=actDict['name'],
                               distance=actDict['distance'], moving_time=actDict['moving_time'],
                               elapsed_time=actDict['elapsed_time'],
                               total_elevation_gain=actDict['total_elevation_gain'],
                               elev_high=actDict['elev_high'], elev_low=actDict['elev_low'], type=actDict['type'],
                               start_date=actDict['start_date'], start_date_local=actDict['start_date_local'],
                               timezone=actDict['timezone'], utc_offset=actDict['utc_offset'],
                               start_latlng=actDict['start_latlng'], end_latlng=actDict['end_latlng'],
                               start_latitude=actDict['start_latitude'], start_longitude=actDict['start_longitude'],
                               achievement_count=actDict['achievement_count'], pr_count=actDict['pr_count'],
                               private=actDict['private'], gear_id=actDict['gear_id'],
                               average_speed=actDict['average_speed'], max_speed=actDict['max_speed'],
                               average_watts=actDict['average_watts'], kilojoules=actDict['kilojoules'],
                               description=actDict['description'], workout_type=actDict['workout_type'],
                               calories=actDict['calories'], device_name=actDict['device_name'],
                               manual=actDict['manual'], athlete_id=actDict['athlete_id'],
                               type_extended=actDict['type_extended'], avgtemp=actDict['average_temp'],
                               has_heartrate=actDict['has_heartrate'], average_cadence=actDict["average_cadence"],
                               average_heartrate=actDict['average_heartrate'], max_heartrate=actDict['max_heartrate'],
                               geom=actDict['geom_wkt'])
    session = Session()
    session.add(insert)
    session.commit()
    session.close()
    application.logger.debug(f"New webhook update for activity {actDict['actId']} has been added to Postgres!")


def createStravaPublicActTopoJSON():
    """
    Creates a in memory TopoJSON file containing all database stored Strava Activities. This file will be uploaded to a
    S3 Bucket, replacing the existing file. A pre-generated file is used to speed up response time, as generating the
    file may take a few seconds. This function is called whenever a new subscription update adds a new activity to the
    database or when triggered on the admin page.

    Returns
    -------
    In memory TopoJSON file.
    """
    # Create Postgres connection
    session = Session()
    # Query geom as GeoJSON and other attribute information
    query = session.query(sqlfunc.ST_AsGeoJSON(strava_activities_masked.geom, 5),
                          strava_activities.name,
                          strava_activities.actID,
                          strava_activities.type,
                          strava_activities.distance,
                          strava_activities.private,
                          strava_activities.calories,
                          strava_activities.start_date,
                          strava_activities.elapsed_time,
                          strava_activities.moving_time,
                          strava_activities.average_watts,
                          strava_activities.start_date_local,
                          strava_activities.total_elevation_gain,
                          strava_activities.average_speed,
                          strava_activities.max_speed,
                          strava_activities.type_extended,
                          strava_activities.has_heartrate,
                          strava_activities.average_cadence,
                          strava_activities.max_heartrate,
                          strava_activities.average_heartrate,
                          strava_gear.gear_name) \
        .join(strava_activities_masked.act_rel) \
        .join(strava_activities.gear_rel, isouter=True) \
        .order_by(strava_activities.start_date.desc())
    features = []
    for row in query:
        # Build a dictionary of the attribute information
        propDict = {"name": row.name, "actID": row.actID, "type": row.type, "distance": round(row.distance),
                    "private": row.private, "calories": round(row.calories),
                    "startDate": row.start_date_local.isoformat(),
                    "elapsed_time": row.elapsed_time.seconds, "total_elevation_gain": round(row.total_elevation_gain),
                    "average_speed": round(row.average_speed, 1), "max_speed": row.max_speed,
                    "gear_name": row.gear_name,
                    "type_extended": row.type_extended, "moving_time": row.moving_time.seconds,
                    "average_watts": row.average_watts, "has_heartrate": row.has_heartrate,
                    "average_cadence": row.average_cadence, "max_heartrate": row.max_heartrate,
                    "average_heartrate": row.average_heartrate}
        # Take ST_AsGeoJSON() result and load as geojson object
        geojsonGeom = geojson.loads(row[0])
        # Build the feature and add to feature list
        features.append(Feature(geometry=MultiLineString(geojsonGeom), properties=propDict))
    session.close()
    # Build the feature collection result
    feature_collection = FeatureCollection(features)
    # Create local topoJSON file of geoJSON Feature Collection. Don't create a topology, doesn't matter for a polyline
    # and prequantize the data, this reduces file size at the cost of processing time.
    # prequantize 1e7 is used over default, 1e6, to avoid errors in which data were placed in the South Pacific Ocean
    return tp.Topology(feature_collection, topology=False, prequantize=10000000).to_json()


def processActivitiesPublic(recordID):
    """
    Processes Strava activity by simplifying geometry and removing private areas. This prepares the activity to be
    shared publicly on a Leaflet map. These functions greatly reduce the number of vertices, reducing JSON file size,
    and process the data to be topoJSON friendly, preventing geometries from failing to be converted.

    SQLAlchemy and GeoAlchemy2 ORM queries are used to do the following:

    1.  Create a common table expression(CTE) to select privacy zones geometry. This expression selects AOI polygons
        flagged as privacy zones, combines them into a single multi-part polygon contained inside a geometry.
        collection(ST_Collect), extracts the multi-polygon from the collection(ST_CollectionExtract), and transforms
        (ST_transform) the geometry to the projected coordinate system geometricProj. This CTE is used to create a
        single multi-part polygon containing all privacy zones. This ensures that ST_Difference only calculates the
        difference between each activity and the privacy zones only once. If the privacy zones are not combined, then
        the difference between each privacy zone record and the activity would be calculated, resulting in duplicated
        results.

        Using a projected coordinate allows for faster geometric calculations and allows for meters to be used in
        PostGIS function parameters which use the geometry's units.
    2. Select strava_activities activity linestring geometry based on Record ID and transform(ST_Transform) to
        geometricProj.
    3. Snap activity linestrings to a 0.0001m grid (ST_SnapToGrid, variant 3). This solves a non-node intersection error
        when running ST_Difference. See this thread: https://gis.stackexchange.com/q/50399 for explanation for this
        problem and solution.
    4. Calculate difference(ST_Difference) between activity linestring and privacy zone CTE result. ST_Difference
        subtracts geometry B from A, removing the vertices from A that are within B and segments that touch B.
    5. Snap activity linestring vertices to a 5m grid(ST_SnapToGrid, variant 3). This removes some messy areas by
        combining and removing excess vertices while also reducing resulting geometry memory/file size. This also solves
        geometric errors when exporting data to a topoJSON format. However, resulting linestring geometries have a
        step-shaped appearance resembling the grid.
    6. Simplify activity linestring with a 15m tolerance(ST_Simplify). This further removes messy areas and bends in
        the linestring by removing vertices to create longer straight line segments. This provides large reductions in
        resulting geometry memory/file sizes and mitigates the step-shaped results created by ST_SnapToGrid.
    7. Convert linestrings to multi-linestrings(ST_Multi). Geometries in the strava_activities table are stored as
        linestrings since activity data provided by Strava are contiguous and don't need to be stored in a multi-part
        format. However, ST_Difference may create multi-linestrings that must be stored as such, so all geometries
        are converted to this format.
    8. Fix any invalid activity linestring geometries(ST_MakeValid) that were generated during prior processing.
    9. Transform activity linestring geometry(ST_Transform) back into WGS 1984, SRID 4326. WGS 1984 is best for database
        storage and required for display in Leaflet.
    10. Convert linestring geometry representation to Extended Well Known Binary(ST_AsEWKB). This ensures that data can
        be be easily inserted into the strava_activities_masked table.
    11. Query Activity ID of strava_activities record. Will be inserted as a foreign in strava_activities_masked table.

    Parameters
    ----------
    recordID. Int. Strava activity record ID.

    Returns
    -------
    Nothing. Data are processed and committed to PostgresSQL/PostGIS database.
    """
    session = Session()
    # Simplification tolerance in geometry's units, which is meters here. Higher values more aggressively simplify
    # geometries
    simplifyFactor = 15
    # Projected coordinate system SRID to transform geometries into. WGS84 UTM 10N is used since most
    # activities are in within its zone in California.
    geometricProj = 32610
    # SRID of final data product, WGS 1984, to be used in Leaflet
    webSRID = 4326
    # Grid snapping grid size geometry's units, which is meters here. Larger values mean larger cells and greater
    # vertex snapping
    gridSnap = 5
    # See https://gis.stackexchange.com/a/90271, fixes non-noded intersection error
    nonNodedSnap = 0.0001
    # Extract polygons from geometry collection
    collectionExtract = 3
    # Create CTE to query privacy zone polygons, combine them, extract polygons, and transform to geometricProj
    privacy_cte = session.query(sqlfunc.ST_Transform(sqlfunc.ST_CollectionExtract(sqlfunc.ST_Collect(AOI.geom),
                                                                                  collectionExtract),
                                                     geometricProj).label("priv_aoi")).filter(AOI.privacy == "Yes").cte(
        "privacy_aoi")

    if recordID == "All":
        privacyClipQuery = session.query(strava_activities.actID, sqlfunc.ST_AsEWKB(
            sqlfunc.ST_Transform(
                sqlfunc.ST_MakeValid(
                    sqlfunc.ST_Multi(
                        sqlfunc.ST_Simplify(
                            sqlfunc.ST_SnapToGrid(
                                sqlfunc.ST_Difference(
                                    sqlfunc.ST_SnapToGrid(sqlfunc.ST_Transform(
                                        strava_activities.geom, geometricProj), nonNodedSnap), privacy_cte.c.priv_aoi)
                                , gridSnap),
                            simplifyFactor),
                    )), webSRID)))
    else:
        privacyClipQuery = session.query(strava_activities.actID, sqlfunc.ST_AsEWKB(
            sqlfunc.ST_Transform(
                sqlfunc.ST_MakeValid(
                    sqlfunc.ST_Multi(
                        sqlfunc.ST_Simplify(
                            sqlfunc.ST_SnapToGrid(
                                sqlfunc.ST_Difference(
                                    sqlfunc.ST_SnapToGrid(sqlfunc.ST_Transform(strava_activities.geom, geometricProj),
                                                          nonNodedSnap), privacy_cte.c.priv_aoi)
                                , gridSnap),
                            simplifyFactor),
                    )), webSRID))) \
            .filter(strava_activities.actID == recordID)
    # Iterate over query to process data, add data to strava_activities_masked instance, and add instance to session
    for i in privacyClipQuery:
        session.add(strava_activities_masked(actID=i[0], geom=i[1]))
    session.commit()
    session.close()


def formatPointResponse(point):
    """
    Takes single St_AsText(ST_DumpPoint) record and formats as a lon,lat string
    @param point: Well-Known Text representation of a Point Geometry
    @return: String. Single point formatted in lon,lat
    """
    # Use regular expression to replace ",", "POINT", and "'" with a empty space, ""
    res = re.sub("|,|POINT|'|", "", str(point))
    # Replace spaces with commas and double single parentheses with empty space, couldn't get RegEX to work for this
    res = res.replace(" ", ",").replace("((", "").replace("))", "")
    # listRes = res.split(",")
    return res


def getIntersectingPoints(wktStr):
    """
    Takes an EWKT string of a Strava Activity Stream's latlngs and returns a list of float points which reside within
    the privacy areas.
    @param wktStr: String. EWKT representation of Strava Activity Stream latlngs
    @return: List of strings. Points are returned as WGS 1984 coordinate strings in the format lon,lat
    """
    # geometricProj = 32610
    collectionExtract = 3
    # Open session
    session = Session()
    # Get coordinates from within privacy zones
    try:
        # Create a labled common table expression to query privacy zones geometries collected into a single multi-polygon
        privacy_cte = session.query(
            sqlfunc.ST_CollectionExtract(
                sqlfunc.ST_Collect(AOI.geom), collectionExtract).label("ctelab")).filter(
            AOI.privacy == "Yes").cte()
        # points_cte = session.query(sqlfunc.ST_DumpPoints(sqlfunc.st_geomfromewkt(wktStr)))
        # Take provided EWKT string and convert to GeoAlchemy geometry
        # lineString = sqlfunc.ST_GeomFromEWKT(wktStr)
        # application.logger.debug(f"Geoalchemy Geom is: \n{dir(lineString)}")
        # Get a list of points from the linestring which fall inside the privacy zone
        # ST_DumpPoints provides a point geometry per iterative loop which is converted to a text representation using As_Text
        pointQuery = session.query(sqlfunc.ST_AsText(
            sqlfunc.ST_DumpPoints(sqlfunc.ST_Intersection(sqlfunc.ST_GeomFromEWKT(wktStr), privacy_cte.c.ctelab)).geom))
        # pointQuery = session.query(sqlfunc.ST_AsText(
        #     sqlfunc.ST_DumpPoints(sqlfunc.ST_Intersection(sqlfunc.ST_GeomFromEWKT(wktStr),
        #     privacy_cte.c.ctelab)).geom)).filter(privacy_cte.c.ctelab.
        #     ST_Intersects(sqlfunc.ST_GeomFromEWKT(wktStr)))
        coordinateList = []
        for i in pointQuery:
            # application.logger.debug(f"Point query response is: {i}")
            # strip out the WKT parts of the coordinates, only want list of [lon,lat]
            coordinateList.append(formatPointResponse(i))
    finally:
        session.close()
    return coordinateList


def removeActivityFromDB(actID):
    """
    Removes a activity from the original and public activities database tables.

    @param actID: Int. Strava Activity ID
    @return: Nothing.
    """
    # Open session
    session = Session()
    # Delete from masked table
    session.query(strava_activities_masked).filter(strava_activities_masked.actID == actID).delete()
    # Delete from original DB table
    session.query(strava_activities).filter(strava_activities.actID == actID).delete()
    # Commit changes
    session.commit()
    # Close session
    session.close()


def checkActID(actID):
    """
    Checks if the provided actID is already within the database.

    @param actID: Int. Strava Activity ID
    @return: String. "True" or "False" depending if record exists in databse
    """
    # Open session
    session = Session()
    # Query database
    record = session.query(strava_activities.actID == actID).first()
    session.close()
    return record


def checkAthleteAndSub(athID, subID):
    """
    Checks if provided athlete and subscription ID are in the database with an active subscription status
    @param athID: Int. Strava athlete ID
    @param subID: Int. Strava Webhook Subscription ID
    @return: Object Instance. Instance of Athletes Model with results
    """
    # Open session
    session = Session()
    # Query database
    record = session.query(athletes). \
        join(webhook_subs). \
        filter(athletes.athlete_id == athID, webhook_subs.sub_id == subID, webhook_subs.activesub == "Yes").first()
    session.close()
    return record


def setWebhookInactive(subID):
    """
    Sets provided subscription to inactive status
    @param subID: Int.
    @return: Nothing
    """
    # Open session
    session = Session()
    # Set active status to No
    session.query(webhook_subs).filter(webhook_subs.sub_id == subID).update({webhook_subs.activesub: "No"})
    # Commit changes
    session.commit()
    # Close out session
    session.close()


def checkathleteID(athID):
    """
    Checks if the provided actID is already within the database.

    @param actID: Int. Strava Activity ID
    @return: String. "True" or "False" depending if record exists in databse
    """
    # Open session
    session = Session()
    # Query database
    record = session.query(athletes.athlete_id == athID).first()
    session.close()
    return record


def insertVerifyToken(token):
    """
    Inserts the provided generated token into database.
    @param token: String. Strava verify token generated in script.
    @return: Nothing
    """
    # Open session
    session = Session()
    # Create new record
    newRec = webhook_subs(verify_token=token)
    # Add new record to session
    session.add(newRec)
    session.commit()
    session.close()


def checkVerificationToken(token):
    """
    Verifies that the provided verification token is in the database. Used as part Strava Webhook subscription callback
    verification and setup process. Only needed on setup, further POST requests won't contain the token.
    @param token: String. Strava verify token generated in script
    @return: Instance of webhook sub model if exists, None otherwise
    """
    # Open session
    session = Session()
    # Query database, get most recent record in case the token is in the database multiple times
    record = session.query(webhook_subs.verify_token == token).order_by(webhook_subs.id.desc()).first()
    session.close()
    if record:
        return record


def deleteVerifyTokenRecord(token):
    """
    Deletes script generated Strava webhook verification token from database, called when an existing webhook is removed
    @param token: String. Strava verify token generated in script
    @return: Nothing
    """
    # Open session
    session = Session()
    session.query(webhook_subs).filter(webhook_subs.verify_token == token).delete()
    session.commit()
    session.close()
