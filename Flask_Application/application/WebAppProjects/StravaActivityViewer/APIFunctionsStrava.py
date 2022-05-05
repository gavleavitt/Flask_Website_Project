from datetime import datetime, timedelta
import logging, os, csv
from io import StringIO
from application import application, errorEmail
from application.WebAppProjects.StravaActivityViewer import DBQueriesStrava, StravaAWSS3, OAuthStrava
import time
import requests

def singleActivityProcessing(client, actID):
    """
    Processes a single Strava Activity by placing the full activity in the database, making a simplified and masked public
    version, and by creating a privacy masked stream CSV which is added to a S3 Bucket. Finally a TopoJSON of the
    public activities is generated and uploaded to the S3 Bucket.

    @param client: stravalib client instance with valid access token
    @param actID: Int. ID of Strava Activity to be processed
    @return: Email. Message states if process was successful or failed
    """

    try:
        # Wait 45 minutes before processing update, this allows time for user to update any ride details before they
        #  are processed, in particular changing details uploaded from Wahoo
        # Check if in development mode, if not wait 45 minutes
        if application.config['ENV'] != "development":
            time.sleep(2700)
        application.logger.debug("Getting full activity details")
        # Get all activity details for newly created activity, including stream data
        activity = getFullDetails(client, actID)
        application.logger.debug("Inserting activity details")
        # Insert original, non-masked, coordinates and attribute details into Postgres/PostGIS
        DBQueriesStrava.insertOriginalAct(activity['act'])
        # Calculate masked, publicly sharable, activities and insert into Postgres masked table
        application.logger.debug("Processing and inserting masked geometries")
        DBQueriesStrava.processActivitiesPublic(activity["act"]["actId"])
        # Handle CSV stream processing
        generateAndUploadCSVStream(client, actID, activity)
        # Create topojson file
        topoJSON = DBQueriesStrava.createStravaPublicActTopoJSON()
        # Upload topoJSON to AWS S3
        StravaAWSS3.uploadToS3(topoJSON)
        # Send success email
        errorEmail.sendSuccessEmail("Webhook Activity Update", f'The strava activity: {activity["act"]["actId"]}'
                                                               f' has been processed, the activity can be'
                                                               f' viewed on Strava at: '
                                                               f'https://www.strava.com/activities/{activity["act"]["actId"]}')
        application.logger.debug("Strava activity has been processed!")
    except Exception as e:
        application.logger.error(f"Handling and inserting new webhook activity inside a thread failed with the error {e}")
        errorEmail.sendErrorEmail(script="Webhook Activity Threaded Task Update", exceptiontype=e.__class__.__name__, body=e)
        # Raise another exception, this will signal the route function to return an error 500
        raise()

def generateAndUploadCSVStream(client, actID, activity=None):
    """
    Generates and uploads a privacy zone masked Strava Stream CSV.

    @param client: stravalib client instance with valid access token
    @param actID: Int. Activity ID of Strava activity to process
    @param activity: Dictionary. Optional. Dictionary of full Strava Activity details, generated if not provided
    @return: Nothing. Uploads file to S3 Bucket
    """
    if not activity:
        # Get all activity details for newly created activity, including stream data
        activity = getFullDetails(client, actID)
    # Create in-memory buffer csv of stream data
    csvBuff = StravaAWSS3.writeMemoryCSV(activity["stream"])
    # Get WKT formatted latlng stream data
    wktStr = formatStreamData(activity["stream"])
    # application.logger.debug(f"wktSTR is: \n {wktStr}")
    # Get list of coordinates which cross privacy areas, these will be removed from the latlng stream CSV data
    removeCoordList = DBQueriesStrava.getIntersectingPoints(wktStr)
    # application.logger.debug(f"Remove cord list is: \n {removeCoordList}")
    # Trim/remove rows from latlng CSV stream which have coordinates that intersect the privacy areas
    trimmedMemCSV = trimStreamCSV(removeCoordList, csvBuff)
    # Upload trimmed buffer csv to AWS S3 bucket
    StravaAWSS3.uploadToS3(trimmedMemCSV, activity["act"]["actId"])

def getListIds(client, days):
    """
    Gets a list of all Strava Activity IDs since (days) ago from Strava API.

    Parameters
    ----------
    client. Stravalib model client object. Contains access token to strava API for the user.
    days. Int. How many days to look back, queries all activities since this calculated date.

    Returns
    -------
    List. List of int IDs of all strava activities for the user.
    """
    # use current datetime and timedelta to calculate previous datetime
    after = datetime.today() - timedelta(days=days)
    # after = datetime(year=2019, month=8, day=1)
    actList = []
    # Get all activities since after time and add to list
    acts = client.get_activities(after=after)
    for i in acts:
        actList.append(i.id)
    return actList


def getFullDetails(client, actId):
    """
    Gets the full details of Strava activities using get_activity() to query flat data and get_activity_streams() to get
    GPS coordinates and times. Coordinates are formatted to be inserted in PostGIS following ST_GeomFromEWKT.

    Parameters
    ----------
    client. Stravalib model client object. Contains access token to strava API for the user.
    actId. Int. Activity ID.

    Returns
    -------
    Dict. Activity and coordinate information formatted to be inserted into Postgres/PostGIS.
    """

    # Set logger to suppress debug errors, these messages aren't important and pollute the console
    Log = logging.getLogger()
    Log.setLevel('ERROR')
    # Stream data to get from activity streams
    types = ['time', 'latlng', 'altitude', 'velocity_smooth', 'grade_smooth', "distance", "heartrate", "cadence", "temp"]
    # Get activity details as a dictionary, stravalib method no longer works properly
    # act = client.get_activity(actId).to_dict()
    headers = {f"Authorization": f"Bearer {client.access_token}"}
    act = requests.get(f"https://www.strava.com/api/v3/activities/{actId}", headers=headers).json()
    # Get the activity stream details for the activity id
    stream = client.get_activity_streams(actId, types=types)
    # Get athlete ID directly from API call, instead of digging into the nested result provided by get_activity
    athId = client.get_athlete().id
    # Extract latlng and time information from activity stream
    latlng = stream['latlng'].data
    time = stream['time'].data
    lineStringData = []
    wktList = []
    # Iterate over time and latlng streams, combining them into a list containing sublists with lat, lng, time
    for i in range(0, len(latlng)):
        # Create new entry, swapping (lat, lon) to (lon, lat) then append time, provided as time since start of activity
        ## as datetime UTC (time is provided as time
        ## since start of the activity and is converted to datetime)
        # newEntry = [latlng[i][1], latlng[i][0], (starttime + timedelta(seconds=time[i])).timestamp()]
        newEntry = [latlng[i][1], latlng[i][0], time[i]]
        # Append data as nested list
        lineStringData.append(newEntry)
        # Take newEntry list and create a string with a space delimiter between list items, add to list of wkt
        # This formats data to be friendly with geoalchemy ST_GeomFromEWKT
        wktList.append(" ".join(str(v) for v in newEntry))
        # print(wktList)
    # Format entire list to be friendly with geoalchemy ST_GeomFromEWKT
    sep = ", "
    wktStr = f"SRID=4326;LINESTRINGM({sep.join(wktList)})"
    # Add lat, lng, time as geom key to dict
    act['geom'] = lineStringData
    act['actId'] = actId
    act['geom_wkt'] = wktStr
    # Add athlete id to dict
    act['athlete_id'] = athId
    # Extend type to account for mtb and road rides
    act['type_extended'] = None
    # Calculate type of riding activity, using GearIDs
    if act['gear_id'] in ["b4317610", "b2066194"]:
        act['type_extended'] = "Mountain Bike"
    elif act['gear_id'] == "b5970935":
        act['type_extended'] = "Road Cycling"
    elif act['type'] == "Walk":
        act['type_extended'] = "Walk"
    elif act['type'] == "Run":
        act['type_extended'] = "Run"
    elif act['type'] == "Hike":
        act['type_extended'] = "Walk"
    # Wahoo Bolt provides additional data, check if populated, if not set to null
    wahooList = ["average_temp", "has_heartrate", "max_heartrate", "average_heartrate", "average_cadence"]
    for i in wahooList:
        if act[i] == "":
            act[i] = None
    # List of dictionary keys to remove, these are null or uninteresting
    remove_keys = ['guid', 'external_id', 'athlete', 'location_city', 'location_state', 'location_country',
                   'kudos_count', 'comment_count', 'athlete_count', 'photo_count', 'total_photo_count', 'map',
                   'trainer', 'commute', 'gear', 'device_watts', 'has_kudoed', 'best_efforts',
                   'segment_efforts', 'splits_metric', 'splits_standard', 'weighted_average_watts',
                   'suffer_score',
                   'embed_token', 'trainer', 'photos', 'instagram_primary_photo', 'partner_logo_url',
                   'partner_brand_tag', 'from_accepted_tag', 'segment_leaderboard_opt_out', 'highlighted_kudosers',
                   'laps']
    # Iterate over dict keys, removing unnecessary/unwanted keys
    for key in list(act.keys()):
        if key in remove_keys:
            del (act[key])
    return {"act": act, "stream": stream}

def formatStreamData(stream):
    """
    Formats Strava Activity Stream latlng data into a EWKT string. The string is constructed using string manipulation,
    consider finding a library which can convert a list of coordinates into EWKT or WKT.

    @param stream: Strava Activity Stream with latlng data
    @return: String. EWKT representation of Strava Activity Stream data.
    """
    # Pull out latlngs
    latlng = stream['latlng'].data
    # Format first part of EWKT LINESTRING String, in 4326, WGS1984
    wktStr = f"SRID=4326;LINESTRING("
    #  Iterate over latlng records
    for c, i in enumerate(latlng):
        # Split based on comma
        lat, lng = latlng[c].split(",")
        # Make string of new long lat value
        newEntry = f"{lng} {lat},"
        # newEntry = f"{lat} {lng},"
        # Add new record to existing string
        wktStr += newEntry
    # Remove last comma
    wktStr = wktStr[:-1]
    # Close out wktStr
    wktStr += ")"
    return wktStr

def trimStreamCSV(coordList, memCSV):
    """
    Trims out all records from the Strava stream CSV that fall within privacy zones, ensuring that the stream data do
    not contain reveal locations within sensitive areas. Coordinates are included in the stream data such that they
    can be used to draw point markers on the map on chart mouseover

    @param coordList: List. Coordinates which fall within privacy zones
    @param memCSV: StringIO CSV. Contains original, unaltered activity stream details
    @return: StringIO CSV. Memory CSV with sensitive locations removed
    """

    # see https://stackoverflow.com/a/41978062
    # Reset seek to 0 for memory CSV, after writing it the file pointer is still at the end and must be reset
    memCSV.seek(0)
    # Open original memory csv with a reader
    reader = csv.reader(memCSV)
    # Create new memory CSV to hold results
    trimmedMemOutput = StringIO()
    # Create csv writer on memory csv
    trimmedWriter = csv.writer(trimmedMemOutput)
    # Iterate over original CSV
    for c, row in enumerate(reader):
        # Write header row
        if c == 0:
            trimmedWriter.writerow(row)
        else:
            # split row into [lat, lng]
            coord = row[1].split(",")
            # Check if lat or long exist in the coordinate list
            latCheck = any(coord[0] in x for x in coordList)
            lngCheck = any(coord[1] in x for x in coordList)
            # If neither lat or long are within a privacy zone, write the entire row into the trimmed csv
            if not latCheck or not lngCheck:
                # Not within privacy zone, write CSV
                trimmedWriter.writerow(row)
            # else:
            #     application.logger.debug(f"Coordinates: {coord[0]},{coord[1]} are within a privacy zone!")
    return trimmedMemOutput

def getAthlete(client):
    athlete = client.get_athlete()
    return athlete

def deleteSingleActivity(actID):
    """
    Deletes a single Strava activity from database and removes S3 file

    @param actID: Int. Strava Activity ID
    @return: Nothing
    """
    application.logger.debug(f"Deleting activity {actID}")
    # Delete activity from database
    DBQueriesStrava.removeActivityFromDB(actID)
    # Delete from S3
    # Get bucket details from environmental variable
    bucket = os.getenv("S3_TRIMMED_STREAM_BUCKET")
    application.logger.debug(f"Removing {actID} from S3 bucket")
    StravaAWSS3.deleteFromS3(bucket, "trimmedCSV", actID)
    # # Create new topojson file
    # application.logger.debug(f"Ge")
    # topoJSON = DBQueriesStrava.createStravaPublicActTopoJSON()
    # # Upload topoJSON to AWS S3
    # StravaAWSS3.uploadToS3(topoJSON)