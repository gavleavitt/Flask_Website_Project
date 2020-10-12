# from stravalib.client import Client
from application.stravalib.client import Client
import os
import time
import pickle
from application import app


def gettoken():
    """
    Loads API access token for user if valid, otherwise uses stored refresh token to generate a new access token.

    Returns
    -------
    client. Stravalib model client object. Contains access token to strava API for the user.
    """
    client = Client()
    with open(os.path.join(app.root_path, 'access_token.pickle'), 'rb') as f:
        access_token = pickle.load(f)
    print(f"Access token is {access_token}")
    # https://medium.com/analytics-vidhya/accessing-user-data-via-the-strava-api-using-stravalib-d5bee7fdde17
    if time.time() > access_token['expires_at']:
        print('Token has expired, will refresh')
        refresh_response = client.refresh_access_token(client_id=os.getenv("STRAVA_CLIENT_ID"),
                                                       client_secret=os.getenv("STRAVA_CLIENT_SECRET"),
                                                       refresh_token=access_token['refresh_token'])
        access_token = refresh_response

        with open(os.path.join(app.root_path, 'access_token.pickle'), 'wb') as f:
            pickle.dump(refresh_response, f)
        print('Refreshed token saved to file')

        client.access_token = refresh_response['access_token']
        client.refresh_token = refresh_response['refresh_token']
        client.token_expires_at = refresh_response['expires_at']
    else:
        print(f"Token is valid, expires at {time.localtime(access_token['expires_at'])}")
        client.access_token = access_token['access_token']
        client.refresh_token = access_token['refresh_token']
        client.token_expires_at = access_token['expires_at']
    return client