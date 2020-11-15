from application.stravalib.client import Client
import os
import time
import pickle
from application import app

def getAuth():
    """
    Loads API access token for user if valid, otherwise uses stored refresh token to generate a new access token.

    Returns
    -------
    client. Stravalib model client object. Contains access token to strava API for the user.
    """
    # Build empty stravalib client instance
    client = Client()
    # Load access token from the pickle file
    with open(os.path.join(app.root_path, 'projects', 'strava_activities', 'access_token.pickle'), 'rb') as f:
        access_token = pickle.load(f)
    # print(f"Access token is {access_token}")
    # https://medium.com/analytics-vidhya/accessing-user-data-via-the-strava-api-using-stravalib-d5bee7fdde17
    # Check if access token has expired
    if time.time() > access_token['expires_at']:
        print('Token has expired, will refresh')
        # Use client ID, secret, and refresh token to generate a new access token with Strava API
        refresh_response = client.refresh_access_token(client_id=os.getenv("STRAVA_CLIENT_ID"),
                                                       client_secret=os.getenv("STRAVA_CLIENT_SECRET"),
                                                       refresh_token=access_token['refresh_token'])
        # access_token = refresh_response
        # Open Pickle file and update with new access token
        with open(os.path.join(app.root_path, 'access_token.pickle'), 'wb') as f:
            pickle.dump(refresh_response, f)
        print('Refreshed token saved to file')
        # Set new access token in client instance
        client.access_token = refresh_response['access_token']
        # Set refresh token in client instance
        client.refresh_token = refresh_response['refresh_token']
        # Set access token expiration time for client instance
        client.token_expires_at = refresh_response['expires_at']
    # Access token is still valid, set token in client instance
    else:
        print(f"Token is valid, expires at {time.localtime(access_token['expires_at'])}")
        client.access_token = access_token['access_token']
        client.refresh_token = access_token['refresh_token']
        client.token_expires_at = access_token['expires_at']
    return client

# def stravaAuth():
#     """
#     Returns
#     -------
#
#     """
#     # https://github.com/hozn/stravalib
#     client = Client()
#     authorize_url = client.authorization_url(client_id=os.getenv("STRAVA_CLIENT_ID"),
#                                              redirect_uri='http://localhost:5000/authorized',
#                                              scope=['read_all','profile:read_all','activity:read_all'])
#
#     # Extract the code from your webapp response
#     code = requests.get('code') # or whatever your framework does
#     token_response = client.exchange_code_for_token(client_id=os.getenv("STRAVA_CLIENT_ID"), client_secret=os.getenv("STRAVA_CLIENT_SECRET"), code=code)
#     access_token = token_response['access_token']
#     refresh_token = token_response['refresh_token']
#     expires_at = token_response['expires_at']
#
#     # Now store that short-lived access token somewhere (a database?)
#     client.access_token = access_token
#     # You must also store the refresh token to be used later on to obtain another valid access token
#     # in case the current is already expired
#     client.refresh_token = refresh_token
#
#     # An access_token is only valid for 6 hours, store expires_at somewhere and
#     # check it before making an API call.
#     client.token_expires_at = expires_at
#
#     if time.time() > client.token_expires_at:
#         refresh_response = client.refresh_access_token(client_id=os.getenv("STRAVA_CLIENT_ID"), client_secret=os.getenv("STRAVA_CLIENT_SECRET"),
#             refresh_token=client.refresh_token)
#         access_token = refresh_response['access_token']
#         refresh_token = refresh_response['refresh_token']
#         expires_at = refresh_response['expires_at']
#     return client