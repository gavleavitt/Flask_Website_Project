from datetime import datetime, timedelta, date
from application.models_Strava import athletes, sub_update, strava_activities
from application import app, stravaAuth, DB_Queries_Strava, application
import geojson
import logging
import time
remove_keys = ['guid', 'external_id', 'athlete',
               'location_city', 'location_state', 'location_country',
               'kudos_count', 'comment_count',
               'athlete_count', 'photo_count', 'total_photo_count', 'map', 'trainer', 'commute', 'manual',
               'gear', 'device_watts', 'has_kudoed', 'best_efforts',
               'segment_efforts', 'splits_metric', 'splits_standard', 'weighted_average_watts',
               'suffer_score', 'has_heartrate', 'average_heartrate', 'max_heartrate', 'average_cadence',
               'average_temp', 'device_name', 'embed_token', 'trainer',
               'photos', 'instagram_primary_photo', 'partner_logo_url', 'partner_brand_tag', 'from_accepted_tag',
               'segment_leaderboard_opt_out', 'highlighted_kudosers', 'laps']


def getListIds(client, days):
    """
    Gets a list of all Strava Activity IDs since days ago from Strava API. The api appears to limit requests if too many
    activities are queried too fast.

    Parameters
    ----------
    client. Stravalib model client object. Contains access token to strava API for the user.

    Returns
    -------
    List. List of int IDs of all strava activities for the user.
    """
    # use current time and timedelta to calculate previous time
    after = datetime.today() - timedelta(days=days)
    # after = datetime(year=2019, month=8, day=1)
    actList = []
    # Get all activities since after time
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
    Dict. Full ta
    lar and coordinate information formatted to be inserted into Postgres/PostGIS.
    """

    # Set logger to suppress debug errors, these messages aren't important and pollute the console
    Log = logging.getLogger()
    Log.setLevel('ERROR')
    # Stream data to get from activity streams
    types = ['time', 'latlng']
    # get activity details as a dictionary
    act = client.get_activity(actId).to_dict()
    # Get starttime and conver to datetime object
    starttime = datetime.fromisoformat(act['start_date'])
    # get the activity stream details for the activity id
    stream = client.get_activity_streams(actId, types=types)
    latlng = stream['latlng'].data
    time = stream['time'].data
    linestringdat = []
    wktList = []
    # Iterate over time and latlng streams, combining them into a list containing sublists with lat, lng, UTC time
    for i in range(0, len(latlng)):
        # create new entry, swapping the lat, lon to lon, lat then append time as datetime UTC (time is provded as time
        # since start of the activity and is converted to datetime)
        newEntry = [latlng[i][1], latlng[i][0], (starttime + timedelta(seconds=time[i])).timestamp()]
        # append data as list
        linestringdat.append(newEntry)
        # Take newEntry list and create a string with a space delimiter between list items, add to list of wkt
        # This formats data to be friendly with geoalchemy ST_GeomFromEWKT
        wktList.append(" ".join(str(v) for v in newEntry))
        # print(wktList)
    # Format entire list to be friendly with geoalchemy ST_GeomFromEWKT
    sep = ", "
    wktstr = f"SRID=4326;LINESTRINGM({sep.join(wktList)})"
    # add lat, lng, UTC time as geom key to dict
    act['geom'] = linestringdat
    act['actId'] = actId
    act['geom_wkt'] = wktstr
    # Iterate over dict keys, removing unnecessary keys
    for key in list(act.keys()):
        if key in remove_keys:
            del (act[key])
    return act

def processActs(days):
    """
    Handle issuing functions to download and insert Strava activities since days ago. This is used to grab Strava
    activities manually that are not within a webhook update and to download all existing activities in preparation
    for webhook to provide updates. Currently this is used to download activities as the webhook is developed, once
    fully functional this function should not be needed.

    Parameters
    ----------
    days. Int. How many days back to download Strava Activites

    Returns
    -------
    String. Provides details about which activities were processed.
    """
    client = stravaAuth.gettoken()
    listIds = getListIds(client, days)
    for actId in listIds:
        print(f"Working on activity {actId}")
        try:
            actDict = getFullDetails(client, actId)
            DB_Queries_Strava.insertAct(actDict)
            DB_Queries_Strava.maskandInsertAct(actId)
        except Exception as e:
            print(f"Strava download/insert failed with the error {e}")
            application.logger.error(f"Strava activity {actId} failed to parse properly!")
            application.logger.error(e)
        print(f"Finished working on activity {actId}")
        time.sleep(1)
    return f"Success, finished working on ActIDs {listIds}"
