from flask import Blueprint, request, Response, redirect, url_for
from flask_application.util.flaskAuth.authentication import auth
from flask_application.WebAppProjects.StravaActivityViewer import DBQueriesStrava, APIFunctionsStrava, OAuthStrava
from flask_application.util.Boto3AWS import StravaAWSS3
import os
from flask_application import application
import secrets
import time
import traceback
import requests
from urllib.parse import urlencode

stravaActDashAPI_Admin_BP = Blueprint('stravaActDashAPI_Admin_BP', __name__,
                                      template_folder='templates',
                                      static_folder='static')

stravaSubUrl = "https://www.strava.com/api/v3/push_subscriptions"
@stravaActDashAPI_Admin_BP.route("/processactivity", methods=['POST'])
@auth.login_required(role='admin')
def processActivity():
    """
    Processes a single Strava Activity, will add/remove the activity and all derivatives, or just the Stream data.
    Called by Strava Activity admin page inputs.
    """
    # Get POST request info
    actID = int(request.form['actID'])
    athID = int(request.form['athID'])
    actionType = str(request.form['actionType'])
    procScope = str(request.form['scope'])
    # Verify that athlete ID is in database
    try:
        if athID in DBQueriesStrava.getAthleteList():
            application.logger.debug(f"Received a valid POST request to process a Strava Activity: {request.form}")
            # Get Strava API access credentials
            client = OAuthStrava.getAuth()
            if procScope == "scopeFullActivity":
                # Process entire activity and all derived products
                # Delete activity, if it exists
                application.logger.debug(f"Fully deleting the activity {actID}, if it exists")
                APIFunctionsStrava.deleteSingleActivity(actID)
                # Add new activity
                if actionType == "Add":
                    application.logger.debug(f"Fully processing the activity {actID}")
                    # Issue activity Update
                    APIFunctionsStrava.singleActivityProcessing(client, actID, "manual")
                # elif actionType == "Delete":
                #     flask_application.logger.debug(f"Fully deleting the activity {actID}, if it exists")
                #     APIFunctionsStrava.deleteSingleActivity(actID)
                else:
                    return Response(status=400)
            elif procScope == "scopeCSV":
                # Delete existing Strava Stream from S3
                application.logger.debug(f"Removing the activity stream {actID}")
                StravaAWSS3.deleteFromS3(os.getenv("S3_TRIMMED_STREAM_BUCKET"), "trimmedCSV", actID)
                if actionType == "Add":
                    # Add new Strava stream
                    application.logger.debug(f"Adding the activity stream {actID}")
                    APIFunctionsStrava.generateAndUploadCSVStream(client, actID)
                # elif actionType == "Remove":
                #     # Delete existing Strava Stream from S3
                #     flask_application.logger.debug(f"Removing the activity stream {actID}")
                #     StravaAWSS3.deleteFromS3(os.getenv("S3_TRIMMED_STREAM_BUCKET"), "trimmedCSV", actID)
                else:
                    return Response(status=200)
            else:
                return Response(status=400)
            return Response(status=200)
        else:
            return Response(status=400)
    except:
        return Response(status=500)


@stravaActDashAPI_Admin_BP.route("/removesubscription", methods=['POST'])
@auth.login_required(role='admin')
def removewebhooksub():
    """
    Removes activate webhook subscription from database and Strava API. SubID is disabled and will no longer be accepted
    by Flask.
    Called by Strava Activity admin page inputs.
    """
    # Get POST request info
    # athID = int(request.form['athID'])
    # subID = int(request.form['subID'])
    # if DBQueriesStrava.checkAthleteAndSub(athID, subID):
    # Get Strava API access credentials
    client = OAuthStrava.getAuth()
    # Send request to Strava to delete webhook subscription
    # Get webhook subID
    subID = DBQueriesStrava.getActiveSubID()
    application.logger.debug(f"Sub ID is: {subID}")
    if subID:
        try:
            application.logger.debug(f"Received request to remove the webhook subscription {subID}")
            client.delete_subscription(subID, os.getenv('STRAVA_CLIENT_ID'), os.getenv('STRAVA_CLIENT_SECRET'))
            # Set active webhook to inactive in database
            DBQueriesStrava.setWebhookInactive(subID)
            application.logger.debug(f"webhook subscription {subID} has been set to inactive")
            return Response(status=200)
        except Exception as e:
            application.logger.error(e)
            return Response(status=400)
    else:
        application.logger.debug("No active webhook subscription to remove in DB, querying Strava API to check if one "
                                 "exists.")
        # Send request to Strava API webhook service to get details of existing subscription
        request = requests.get(stravaSubUrl, data={"client_id":os.getenv("STRAVA_CLIENT_ID"),
                                              "client_secret":os.getenv("STRAVA_CLIENT_SECRET")})
        # Parse to JSON
        r = request.json()[0]
        if r["id"]:
            application.logger.debug("Webhook exists, sending delete request")
            delR = client.delete_subscription(r["id"], os.getenv('STRAVA_CLIENT_ID'), os.getenv('STRAVA_CLIENT_SECRET'))
            application.logger.debug("Existing webhook has been removed!")
        return Response(status=200)

@stravaActDashAPI_Admin_BP.route("/addsubscription", methods=['POST'])
@auth.login_required(role='admin')
def addwebhooksub():
    """
    Adds a new Strava webhook subscription to the database and Strava API. Kicks off callback verification process.
    Called by Strava Activity admin page inputs.
    """
    # Get POST request info
    # athID = int(request.form['athID'])
    # callbackurl = str(request.form['callbackURL'])
    # Generate 14 character verify token string
    verifytoken = secrets.token_hex(7)
    # Insert token into database, will be updated if subID if successful, otherwise row will be deleted
    DBQueriesStrava.insertVerifyToken(verifytoken)
    application.logger.debug(f"New verification token {verifytoken} has been added to database")
    # Get Strava API access credentials
    client = OAuthStrava.getAuth()
    try:
        # Send request to create webhook subscription, will be given the new subscription ID in response
        application.logger.debug(f"Callback url is {os.getenv('FULL_STRAVA_CALLBACK_URL')}")
        # postDat = {"client_id": os.getenv("STRAVA_CLIENT_ID"),
        #            "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
        #            "callback_url": os.getenv('FULL_STRAVA_CALLBACK_URL'),
        #            "verify_token": verifytoken}
        #
        # r = requests.post("https://www.strava.com/api/v3/push_subscriptions", data=postDat)
        # resp = r.json()

        resp = client.create_subscription(client_id=os.getenv("STRAVA_CLIENT_ID"),
                                          client_secret=os.getenv("STRAVA_CLIENT_SECRET"),
                                          # callback_url=os.getenv('FULL_STRAVA_CALLBACK_URL'),
                                          callback_url=os.getenv('FULL_STRAVA_CALLBACK_URL'),
                                          verify_token=verifytoken)
        application.logger.debug(resp)
        # flask_application.logger.debug(f"New sub id is {resp['id']}, updating database")
        application.logger.debug(f"New sub id is {resp.id}, updating database")
        # Update database with new sub id
        # DBQueriesStrava.updateSubId(resp["id"], verifytoken)
        DBQueriesStrava.updateSubId(resp.id, verifytoken)
        # flask_application.logger.debug(f"New sub id {resp['id']} has been added to the database")
        application.logger.debug(f"New sub id {resp.id} has been added to the database")
        return Response(status=200)
    except Exception as e:
        application.logger.debug(f"Webhook creation process failed with the error {e}")
        # logging.error(e, exc_info=True)
        DBQueriesStrava.deleteVerifyTokenRecord(verifytoken)
        return Response(status=400, response=str(e))


@stravaActDashAPI_Admin_BP.route("/generatetopojson", methods=['POST'])
@auth.login_required(role='admin')
def genTopoJSON():
    """
    Generates a new TopoJSON file using all stored Strava activities and uploads to S3 Bucket, replaces existing file.
    Called by Strava Activity admin page inputs.
    """
    # Create topojson file
    application.logger.debug(f"Received request to generate a new TopoJSON")
    topoJSON = DBQueriesStrava.createStravaPublicActTopoJSON()
    # Upload topoJSON to AWS S3
    StravaAWSS3.uploadToS3(topoJSON)
    application.logger.debug(f"New TopoJSON has been generated")
    return Response(status=200)


@stravaActDashAPI_Admin_BP.route("/bulkprocess", methods=['POST'])
@auth.login_required(role='admin')
def bulkprocess():
    """
    """
    #
    application.logger.debug(f"Received request to bulk process!")
    # Get form action parameter
    actionType = str(request.form['actionType'])
    # Strava API request wait time if request limit is exceeded
    waitTime = 960
    application.logger.debug(actionType)
    if actionType == "streamdata-Acts":
        application.logger.debug("Received Admin command to regenerate Strava stream data")
        # Get Client details
        client = OAuthStrava.getAuth()
        # Get all activity IDs
        actIDList = APIFunctionsStrava.getListIds(client, 10000)
        # Loop over IDs
        for i in actIDList:
            for attempt in range(3):
                # Try block to process and upload CSVs, Strava API will timeout after too many requests, wait 16 minutes
                # for the 15 minute API lockout to end before trying again
                try:
                    APIFunctionsStrava.generateAndUploadCSVStream(client, i, activity=None)
                except Exception as e:
                    application.logger.debug(f"Failed on Strava Stream download for activity {i} and upload with the "
                                             f"error: {e}")
                    application.logger.debug((traceback.format_exc()))
                    time.sleep(waitTime)
                else:
                    # CSV has been uploaded, break attempt look and move onto next activity ID
                    break

        return Response(status=200)


@stravaActDashAPI_Admin_BP.route("/authuser", methods=['GET'])
@auth.login_required(role='admin')
def authUser():
    """
    URL for kicking off process for OAuth, user will be redirected Strava's Oauth page before being bounced back to
    this website. Redirection URL will contain parameters for this flask_application and website.
    @return:
    """
    stravaAuthurl = "https://www.strava.com/oauth/authorize?"
    params = {"client_id": os.getenv("STRAVA_CLIENT_ID"),
              "redirect_uri": url_for("stravaActDashAPI_Admin_BP.getauthdetails"),
              "scope": "activity:read_all",
              "response_type": "code"
              }
    paramsEncoded = urlencode(params)
    return redirect(stravaAuthurl + paramsEncoded)


@stravaActDashAPI_Admin_BP.route("/authuserredirected", methods=['GET'])
@auth.login_required(role='admin')
def getauthdetails():
    """
    Handles Strava OAuth redirection. Pulls one-time use code from the redirection and exchanges for access and refresh
    tokens.
    @return: Nothing.
    """
    scopes = request.args.get("scope")
    code = request.args.get("code")
    # Post Code to Strava oauth to get access token for user
    params = {"client_id":os.getenv("STRAVA_CLIENT_ID"), "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
              "code":code,"grant_type":"authorization_code"}
    postR = requests.post("https://www.strava.com/oauth/token", data=params)
    # Get response as dict
    r = postR.json()[0]
    # TODO: Write queries to write to DB
    pass
# @stravaActDashAPI_BP.route("/admin/stravacreatesub", methods=['POST'])
# @auth.login_required(role='admin')
# def handle_Create_Strava_Sub():
#     """
#     URL to handle creation of new webhook subscription. Requires that OAuth access has already been given, consider
#     setting up a flow to prompt user to provide OAuth access and password protect at user role level.
#
#     Requires admin level access to visit.
#
#     Consider for future development:
#     Have page prompt user for OAuth access, process Oauth creds, then create new webhook subscription including new user
#     Maybe use Flask-Login to keep track of who is logged in and Oauth credentials.
#
#     Returns
#     -------
#     String. String containing new webhook subscription ID.
#     """
#     try:
#         # Get flask_application access credentials
#         # client = stravaAuth.gettoken()
#         # flask_application.logger.debug("Client loaded with tokens!")
#         # Handle webhook subscription and response
#         response = StravaWebHook.create_Strava_Webhook(client)
#         return f"Creation of new strava webhook subscription succeeded, new sub id is {response}!"
#     except Exception as e:
#         return f"Creation of new strava webhook subscription failed with the error {e}"
#
# @stravaActDashAPI_BP.route("/admin/listactivesubs", methods=['GET'])
# @auth.login_required(role='admin')
# def liststravasubs():
#     """
#     Lists flask_application webhook subscriptions. Manually visited,
#
#     Requires admin level access.
#
#     Returns
#     -------
#     String. Message with webhook subscription IDs.
#     """
#     # Get flask_application access credentials
#     client = stravaAuth.gettoken()
#     subIDs = StravaWebHook.listStravaSubIds(client)
#     return f"Webhook subscriptions IDs are {subIDs}"
#
