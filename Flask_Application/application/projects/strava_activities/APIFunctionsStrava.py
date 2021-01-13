from datetime import datetime, timedelta
# from application.projects.strava_activities import OAuthStrava, DBQueriesStrava, StreamDataAWSS3
# from application import application
import logging

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
    types = ['time', 'latlng', 'altitude', 'velocity_smooth', 'grade_smooth']
    # Get activity details as a dictionary
    act = client.get_activity(actId).to_dict()
    # Get starttime and convert to datetime object
    # starttime = datetime.fromisoformat(act['start_date'])
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
    # List of dictionary keys to remove, these are null or uninteresting
    remove_keys = ['guid', 'external_id', 'athlete', 'location_city', 'location_state', 'location_country',
                   'kudos_count', 'comment_count', 'athlete_count', 'photo_count', 'total_photo_count', 'map',
                   'trainer', 'commute', 'gear', 'device_watts', 'has_kudoed', 'best_efforts',
                   'segment_efforts', 'splits_metric', 'splits_standard', 'weighted_average_watts',
                   'suffer_score', 'has_heartrate', 'average_heartrate', 'max_heartrate', 'average_cadence',
                   'average_temp', 'embed_token', 'trainer', 'photos', 'instagram_primary_photo', 'partner_logo_url',
                   'partner_brand_tag', 'from_accepted_tag', 'segment_leaderboard_opt_out', 'highlighted_kudosers',
                   'laps']
    # Iterate over dict keys, removing unnecessary/unwanted keys
    for key in list(act.keys()):
        if key in remove_keys:
            del (act[key])
    return {"act": act, "stream": stream}

# def processActs(days):
#     """
#     Handle issuing functions to download and insert Strava activities since days ago. This is used to grab Strava
#     activities manually that are not within a webhook update and to download all existing activities in preparation
#     for webhook to provide updates. Currently this is used to download activities as the webhook is developed, once
#     fully functional this function should not be needed.
#
#     Parameters
#     ----------
#     days. Int. How many days back to download Strava Activites
#
#     Returns
#     -------
#     String. Provides details about which activities were processed.
#     """
#     client = OAuthStrava.getAuth()
#     listIds = getListIds(client, days)
#     count = 0
#     print(f"Length of ID list is {len(listIds)}")
#     waitTime = 960
#     for actId in listIds:
#         for attempt in range(3):
#             try:
#                 print(f"\nWorking on activity {actId}")
#                 actDict = getFullDetails(client, actId)
#                 if actDict['manual'] == "true":
#                     application.logger.error(f"Activity {actId} is a manual entry, attempting to break loop to skip")
#                     break
#                 else:
#                     DBQueriesStrava.insertAct(actDict)
#                     DBQueriesStrava.maskandInsertAct(actId)
#             except Exception as e:
#                 # print(f"Strava download/insert failed with the error {e}")
#                 application.logger.error(f"Strava activity {actId} failed to parse properly, possible API"
#                                          f"timeout, waiting {waitTime} seconds to try again.")
#                 application.logger.error(e)
#                 time.sleep(waitTime)
#             else:
#                 break
#         print(f"Finished working on activity {actId}")
#         count += 1
#         print(f"{count} out of {len(listIds)} activities processed")
#     return f"Success, finished working on ActIDs {listIds}"

def getAthlete(client):
    athlete = client.get_athlete()
    return athlete

