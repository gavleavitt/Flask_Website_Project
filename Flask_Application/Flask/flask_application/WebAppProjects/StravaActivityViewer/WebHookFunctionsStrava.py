import os
from flask_application import application
from flask_application.util import errorEmail
from flask_application.WebAppProjects.StravaActivityViewer import OAuthStrava, DBQueriesStrava, APIFunctionsStrava, StravaAWSS3
import json
from threading import Thread
from flask import Response

def handleSubUpdate(client, updateContent):
    """
    Handles Strava webhook subscription update. This function is called by a valid Strava POST request to the webhook
    subscription callback URL.

    Parameters
    ----------
    client. Stravalib model client object. Contains access token to strava API for the user.
    updateContent. Dict. POST request JSON data formatted by Flask as a dict.

    Returns
    -------
    Nothing. Data are inserted into Postgres/PostGIS.
    """

    # Parse update information into a model using stravalib
    update = client.handle_subscription_update(updateContent)
    # Verify that the athlete(s) and subscription ID contained in the message are in Postgres
    if DBQueriesStrava.checkAthleteAndSub(update.owner_id, update.subscription_id):
        application.logger.debug("Sub update from Strava appears valid")
        # Insert subscription update message details into Postgres
        DBQueriesStrava.insertSubUpdate(update)
        # Verify that the update is a activity creation event
        if update.aspect_type == "create" and update.object_type == "activity":
            application.logger.debug("This is a activity create event, creating thread to process activity")
            try:
                # Create a thread to handle async processing of the activity and its derivatives
                # Threading allows the activity to long process with a quick 200 code to be sent to the Strava API
                Thread(target=APIFunctionsStrava.singleActivityProcessing, args=(client, update.object_id)).start()
            except Exception as e:
                application.logger.error(f"Creating a thread to process new activity failed with in the error: {e}")
                errorEmail.sendErrorEmail(script="Webhook Activity Threading", exceptiontype=e.__class__.__name__, body=e)
        elif update.aspect_type == "update" and update.object_type == "activity":
            application.logger.debug("This is a activity update event, updating existing record")
            # Update existing activity title
            DBQueriesStrava.updateExistingActivity(update)
        else:
            # Write logic to handle delete events
            application.logger.debug("Sub update message contains an delete event, skipping request")
            pass
    else:
        application.logger.debug("POST request is invalid, user ID or subscription ID don't match those in database!")

def handleSubCallback(request):
    """
    Handles requests to Strava subscription callback URL.

    GET:
        Webhoook Subscription Creation Process:
            CallbackURL is sent a GET request containing a challenge code. This code is sent back to requester to verify
            the callback.

             The initial request to create a new webhook subscription is then provided with verification and
             the new subscription ID.
    POST:
        Webhook subscription update message. Sent when a activity on a subscribed account is created, updated, or deleted,
        or when a privacy related profile setting is changed.

        All update messages are inputted into Postgres.

        Currently, only activity creation events are handled, additional development is needed to handle other events.

    Returns
    -------
    GET request:
        JSON, echoed Strava challenge text.
    POST request:
        Success code if data are successfully added to Postgres/PostGIS. Strava must receive a 200 code in response to
        POST.
    """
    application.logger.debug(f"Request to Strava callback url. Request is: {request}")
    # Check if request is a GET callback request, part of webhook subscription process
    if request.method == 'GET':
        application.logger.debug("Got a GET callback request from Strava to verify webhook. Request args are: "
                                 f"{request.args}")
        # Extract challenge and verification tokens
        callBackContent = request.args.get("hub.challenge")
        callBackVerifyToken = request.args.get("hub.verify_token")
        # Form callback response as dict
        callBackResponse = {"hub.challenge": callBackContent}
        # Check if verification tokens match, i.e. if GET request is from Strava
        if callBackVerifyToken and DBQueriesStrava.checkVerificationToken(callBackVerifyToken):
            application.logger.debug(f"Strava callback verification succeeded, "
                                     f" responding with the challenge code"
                                     f" message: {callBackResponse}")
            # Verification succeeded, return challenge code as dict
            # Using Flask Response API automatically converts it to JSON with HTTP 200 success code
            return callBackResponse
        else:
            # Verification failed, raise error
            application.logger.error(f"Strava verification token doesn't match!")
            raise ValueError('Strava token verification failed, no match found.')
    # POST request containing webhook subscription update message, new activity or other change to Strava account
    elif request.method == 'POST':
        application.logger.debug("New activity incoming! Got a POST callback request from Strava")
        try:
            # Convert JSON body to dict
            callbackContent = json.loads(request.data, strict=False)
            application.logger.debug("JSON content has been extracted")
            application.logger.debug(f"Update content is {callbackContent}")
            # flask_application.logger.debug(f"Update content dir is {dir(callbackContent)}")
            # Call function to handle update message and process new activity, if applicable
            # Get flask_application access credentials
            client = OAuthStrava.getAuth()
            handleSubUpdate(client, callbackContent)
            application.logger.debug("Inserted webhook update and activity details into postgres tables!")
            return Response(status=200)
        except Exception as e:
            application.logger.error(f"Strava subscription update failed with the error {e}")
