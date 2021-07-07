from flask import Blueprint, request, Response
from application.util.flaskAuth.authentication import auth
from application.WebAppProjects.StravaActivityViewer import DBQueriesStrava, APIFunctionsStrava, OAuthStrava, StravaAWSS3
import os
from application import application
import logging
import secrets

stravaActDashAPI_Admin_BP = Blueprint('stravaActDashAPI_Admin_BP', __name__,
                        template_folder='templates',
                        static_folder='static')

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
                    APIFunctionsStrava.singleActivityProcessing(client, actID)
                # elif actionType == "Delete":
                #     application.logger.debug(f"Fully deleting the activity {actID}, if it exists")
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
                #     application.logger.debug(f"Removing the activity stream {actID}")
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
        response = client.create_subscription(client_id=os.getenv("STRAVA_CLIENT_ID"),
                                              client_secret=os.getenv("STRAVA_CLIENT_SECRET"),
                                              callback_url=os.getenv('FULL_STRAVA_CALLBACK_URL'),
                                              verify_token=verifytoken)
        application.logger.debug(f"New sub id is {response.id}, updating database")
        # Update database with new sub id
        DBQueriesStrava.updateSubId(response.id, verifytoken)
        application.logger.debug(f"New sub id {response.id} has been added to the database")
        return Response(status=200)
    except Exception as e:
        application.logger.debug(f"Webhook creation process failed with the error {e}")
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
    # Create topojson file
    application.logger.debug(f"Received request to bulk process!")


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
#         # Get application access credentials
#         # client = stravaAuth.gettoken()
#         # application.logger.debug("Client loaded with tokens!")
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
#     Lists application webhook subscriptions. Manually visited,
#
#     Requires admin level access.
#
#     Returns
#     -------
#     String. Message with webhook subscription IDs.
#     """
#     # Get application access credentials
#     client = stravaAuth.gettoken()
#     subIDs = StravaWebHook.listStravaSubIds(client)
#     return f"Webhook subscriptions IDs are {subIDs}"
#
