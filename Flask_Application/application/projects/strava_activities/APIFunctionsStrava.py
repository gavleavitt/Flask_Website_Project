from datetime import datetime, timedelta
# from application.projects.strava_activities import OAuthStrava, DBQueriesStrava, StreamDataAWSS3
# from application import application
import logging
import csv
from io import StringIO

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
    # Get activity details as a dictionary
    act = client.get_activity(actId).to_dict()

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

    @param stream:
    @return:
    """
    # Pull out latlngs
    latlng = stream['latlng'].data
    wktStr = f"SRID=4326;LINESTRING("
    for c, i in enumerate(latlng):
        lat, lng = latlng[c].split(",")
        newEntry = f"{lat} {lng},"
        wktStr += newEntry
    # Remove last comma
    wktStr = wktStr[:-1]
    # Close out wktStr
    wktStr += ")"
    return wktStr

def trimStreamCSV(coordList, memCSV):
    """

    @param coordList:
    @param memCSV:
    @return:
    """

    # see https://stackoverflow.com/a/41978062
    # Reset seek to 0 for memory CSV, after writing it the file pointer is still at the end
    memCSV.seek(0)
    reader = csv.reader(memCSV)
    # Create new memory CSV to hold results
    trimmedMemOutput = StringIO()
    trimmedWriter = csv.writer(trimmedMemOutput)

    for c, row in enumerate(reader):
        # Write header
        if c == 0:
            trimmedWriter.writerow(row)
        else:
            # print(row)
            # # split row into [lat, lng]
            coord = row[1].split(",")
            # Check if lat or long exist in the coordinate list
            latCheck = any(coord[0] in x for x in coordList)
            lngCheck = any(coord[1] in x for x in coordList)
            if not latCheck or not lngCheck:
                trimmedWriter.writerow(row)
    return trimmedMemOutput

def getAthlete(client):
    athlete = client.get_athlete()
    return athlete

