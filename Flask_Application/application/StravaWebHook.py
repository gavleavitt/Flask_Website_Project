from stravalib.client import Client
import os
from application import application, script_config, getStravaActivities, errorEmail
from application import DB_Queries_Strava as DQS


def create_Strava_Webhook(client):
    """
    Creates new Strava webhook subscription. Client information and client generated token are pulled from environmental
    variables and the callback URL is set to a dedicated callback address on the application.

    If subscription is successful, a subscription ID will be provided by Strava and this ID will be inserted into
    Postgres.

    Returns
    -------
    Integer. Strava subscription id

    """
    try:
        # kick off process to create new webhook
        # callback URL needs to be a HTTP url, not HTTPS, so the elastic beanstalk base environment URL is provided
        # as all calls to leavittmapping.com are redirected to HTTPS, consider making HTTP only mapping to domain.
        application.logger.debug(f"Attempting to create a new Strava webhook subscription with the values: client id: "
                              f"{os.getenv('STRAVA_CLIENT_ID')} client_secret: {os.getenv('STRAVA_CLIENT_SECRET')}"
                              f"callback url: {(script_config.htttpSiteIndex + script_config.strava_callback_url)} and the "
                              f"verify token: {os.getenv('STRAVA_VERIFY_TOKEN')}")
        response = client.create_subscription(client_id=os.getenv("STRAVA_CLIENT_ID"),
                                   client_secret=os.getenv("STRAVA_CLIENT_SECRET"),
                                   callback_url=(script_config.htttpSiteIndex + script_config.strava_callback_url),
                                   verify_token=os.getenv("STRAVA_VERIFY_TOKEN"))
    except Exception as e:
        # Something broke, log error and quit, should timeout request to Strava
        application.logger.error(f"Create subscription function failed with the error {e}")
        quit()
    # Update database with sub id
    application.logger.debug(f"Response id is {response.id}")
    DQS.updateSubId(response.id)
    return response.id

# def subCallback(client, callbackContent):
#     response = client.handle_subscription_callback(callbackContent, verify_token=os.getenv("STRAVA_VERIFY_TOKEN"))
#     return response
def handle_sub_update(client, updateContent):
    """
    Handles Strava webhook subscription update. This function is called by a valid Strava POST request to Strava Callback
    URL.

    Parameters
    ----------
    client. Stravalib model client object. Contains access token to strava API for the user.
    updateContent. Dict. POST request JSON data formatted by Flask as Dict.

    Returns
    -------
    Nothing. Data are inserted into Postgres/PostGIS.
    """

    # Parse update information into a model
    update = client.handle_subscription_update(updateContent)
    application.logger.debug(f"Update model is {update}")
    application.logger.debug(f"Update model dir is {dir(update)}")
    # Iterate over update model, should only be 1 object
    for i in update:
        application.logger.debug(f"Update content is {i}")
        application.logger.debug(f"Update dir content is {dir(i)}")
        # Verify that info is from Strava and has correct content, and
        if update.owner_id in DQS.getAthleteList() and update.subscription_id in DQS.getSubIdList():
            application.logger.debug("Sub update from Strava appears valid")
            # Insert subscription update message details into Postgres
            DQS.insertSubUpdate(i)
            # Verify that the update is a activity creation event
            if i.aspect_type == "create" and i.object_type == "activity":
                application.logger.debug("This is a activity create event, inserting update event data")
                try:
                    application.logger.debug("Getting full activity details")
                    # Get activity details for newly created activity
                    activity = getStravaActivities.getFullDetails(client, i.object_id)
                    application.logger.debug("Inserting activity details")
                    # Insert activity details into Postgres/PostGIS
                    DQS.insertAct(activity)
                    # Calculate masked activities and insert into Postgres masked table
                    DQS.maskandInsertAct(activity.actId)
                except Exception as e:
                    application.logger.error(f"Handling and inserting new webhook activity failed with the error {e}")
                    errorEmail.senderroremail(script="Webhook Activity Update", exceptiontype=e.__class__.__name__, body=e)
            else:
                # Write logic to handle update and delete events
                application.logger.debug("Sub update message contains an update or delete event, skipping request")
                pass
def listStravaSubIds(client):
    """
    Lists webhook subscriptions registered with Strava, response is provided by Strava.

    Parameters
    ----------
    client. Stravalib model client object. Contains access token to strava API for the user.

    Returns
    -------
    List. List of webhook subscriptions (int) registered with Strava.
    """
    Ids = client.list_subscriptions(os.getenv('STRAVA_CLIENT_ID'), os.getenv('STRAVA_CLIENT_SECRET'))
    idList = []
    for i in Ids:
        idList.append(i.id)
    return idList

def deleteStravaSubIds(client):
    """

    Delete webhook subscriptions registered with Strava. Subscriptions IDs are requested from Strava then used to
    unregister.

    Parameters
    ----------
    client. Stravalib model client object. Contains access token to strava API for the user.

    Returns
    -------
    List. List of IDs (int) that were unregistered.
    """
    # Get list of webhook subscriptions
    Ids = client.list_subscriptions(os.getenv('STRAVA_CLIENT_ID'), os.getenv('STRAVA_CLIENT_SECRET'))
    idList = []
    for i in Ids:
        idList.append(i.id)
    # Iterate over sub IDs, deleting subscriptions
    for v in idList:
        client.delete_subscription(v, os.getenv('STRAVA_CLIENT_ID'),os.getenv('STRAVA_CLIENT_SECRET'))
    return idList