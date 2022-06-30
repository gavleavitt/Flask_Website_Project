from application import application
import os
from application.WebAppProjects.StravaActivityViewer import DBQueriesStrava


def createStravaWebhook(client):
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
        # Kick off process to create new webhook
        #### The following may not be true, HTTPS may work, server was experiencing other problems that may have
        #### interferred in the process, need to test.
        # callback URL needs to be a HTTP url, not HTTPS, so the elastic beanstalk base environment URL is provided
        # as all calls to leavittmapping.com are redirected to HTTPS, consider making HTTP only mapping to domain.
        application.logger.debug(f"Attempting to create a new Strava webhook subscription with the values: client id: "
                                 f"{os.getenv('STRAVA_CLIENT_ID')} client_secret: {os.getenv('STRAVA_CLIENT_SECRET')}"
                                 f"callback url: {(os.getenv('httpSiteIndex') + os.getenv('strava_callback_url'))} "
                                 f"and the verify token: {os.getenv('STRAVA_VERIFY_TOKEN')}")

        response = client.create_subscription(client_id=os.getenv("STRAVA_CLIENT_ID"),
                                              client_secret=os.getenv("STRAVA_CLIENT_SECRET"),
                                              callback_url=(
                                                      os.getenv('httpSiteIndex') + os.getenv('strava_callback_url')),
                                              verify_token=os.getenv("STRAVA_VERIFY_TOKEN"))
        application.logger.debug(f"Response id is {response.id}")
        # Update database with sub id
        DBQueriesStrava.updateSubId(response.id)
        return response.id
    except Exception as e:
        # Something broke, log error
        application.logger.error(f"Create subscription function failed with the error {e}")

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
        client.delete_subscription(v, os.getenv('STRAVA_CLIENT_ID'), os.getenv('STRAVA_CLIENT_SECRET'))
    return idList