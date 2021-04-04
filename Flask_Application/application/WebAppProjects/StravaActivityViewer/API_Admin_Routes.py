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

# @stravaActDashAPI_Admin_BP.route("/removeactivesubscription", methods=['POST'])
# @auth.login_required(role='admin')
# def removetravasubscription():
#     """
#     Deletes application webhook subscriptions. Manually visited, requires admin level access.
#
#     Returns
#     -------
#     String. Message with deleted webhook subscription IDs.
#
#     """
#     # Get application access credentials
#     client = stravaAuth.gettoken()
#     subIDs = StravaWebHook.deleteStravaSubIds(client)
#     return f"Deleted webhook subscriptions with the IDs: {subIDs}"

@stravaActDashAPI_Admin_BP.route("/removesubscription", methods=['POST'])
@auth.login_required(role='admin')
def removewebhooksub():
    # Get POST request info
    athID = int(request.form['athID'])
    subID = int(request.form['subID'])
    if DBQueriesStrava.checkAthleteAndSub(athID, subID):
        # Get Strava API access credentials
        client = OAuthStrava.getAuth()
        # Send request to Strava to delete webhook subscription
        client.delete_subscription(subID, os.getenv('STRAVA_CLIENT_ID'), os.getenv('STRAVA_CLIENT_SECRET'))
        # Set active webhook to inactive in database
        DBQueriesStrava.setWebhookInactive(subID)
        return Response(status=200)
    else:
        return Response(status=400)

@stravaActDashAPI_Admin_BP.route("/addsubscription", methods=['POST'])
@auth.login_required(role='admin')
def addwebhooksub():
    # Get POST request info
    athID = int(request.form['athID'])
    # callbackurl = str(request.form['callbackURL'])
    # Verify that athlete is in database
    if DBQueriesStrava.checkathleteID():
        # Generate 15 character verify token string
        verifytoken = secrets.token_hex(15)
        # Insert token into database, will be updated if subID if successful, otherwise row will be deleted
        DBQueriesStrava.insertVerifyToken(verifytoken)
        # Get Strava API access credentials
        client = OAuthStrava.getAuth()
        try:
            # Send request to create webhook subscription, will be given the new subscription ID in response
            response = client.create_subscription(client_id=os.getenv("STRAVA_CLIENT_ID"),
                                                  client_secret=os.getenv("STRAVA_CLIENT_SECRET"),
                                                  callback_url=os.getenv('FULL_STRAVA_CALLBACK_URL'),
                                                  verify_token=verifytoken)
            application.logger.debug(f"Response id is {response.id}")
            # Update database with new sub id
            DBQueriesStrava.updateSubId(response.id, verifytoken)
        except:
            DBQueriesStrava.deleteVerifyTokenRecord(verifytoken)

@stravaActDashAPI_Admin_BP.route("/generatetopojson", methods=['POST'])
@auth.login_required(role='admin')
def genTopoJSON():
    # Create topojson file
    topoJSON = DBQueriesStrava.createStravaPublicActTopoJSON()
    # Upload topoJSON to AWS S3
    StravaAWSS3.uploadToS3(topoJSON)
    return Response(status=200)