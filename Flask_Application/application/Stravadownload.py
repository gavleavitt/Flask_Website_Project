# from stravaio import strava_oauth2
# from stravaio import StravaIO
from stravalib.client import Client
from dotenv import load_dotenv
import requests
import os
import time
load_dotenv()

# strava_oauth2(client_id=os.getenv("STRAVA_CLIENT_ID"), client_secret=os.getenv("STRAVA_CLIENT_SECRET"))
# client = StravaIO(access_token=os.getenv("STRAVA_ACCESS_TOKEN"))
print("Running!")


def stravaAuth():
    # https://github.com/hozn/stravalib
    client = Client()
    authorize_url = client.authorization_url(client_id=os.getenv("STRAVA_CLIENT_ID"),
                                             redirect_uri='http://localhost:5000/authorized',
                                             scope=['read_all','profile:read_all','activity:read_all'])

    # Extract the code from your webapp response
    code = requests.get('code') # or whatever your framework does
    token_response = client.exchange_code_for_token(client_id=os.getenv("STRAVA_CLIENT_ID"), client_secret=os.getenv("STRAVA_CLIENT_SECRET"), code=code)
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    expires_at = token_response['expires_at']

    # Now store that short-lived access token somewhere (a database?)
    client.access_token = access_token
    # You must also store the refresh token to be used later on to obtain another valid access token
    # in case the current is already expired
    client.refresh_token = refresh_token

    # An access_token is only valid for 6 hours, store expires_at somewhere and
    # check it before making an API call.
    client.token_expires_at = expires_at

    if time.time() > client.token_expires_at:
        refresh_response = client.refresh_access_token(client_id=os.getenv("STRAVA_CLIENT_ID"), client_secret=os.getenv("STRAVA_CLIENT_SECRET"),
            refresh_token=client.refresh_token)
        access_token = refresh_response['access_token']
        refresh_token = refresh_response['refresh_token']
        expires_at = refresh_response['expires_at']
    return client
def getatth(client):
    athlete = client.get_athlete()
    return athlete