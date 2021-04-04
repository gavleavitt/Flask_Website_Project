from application import app, application, auth
from flask import Blueprint, Response, request
import os
from application.WebAppProjects.StravaActivityViewer import WebHookFunctionsStrava, DBQueriesStrava, StravaAWSS3

stravaActDashAPI_BP = Blueprint('stravaActDashAPI_BP', __name__,
                        template_folder='templates',
                        static_folder='static')



@stravaActDashAPI_BP.route(os.environ.get("STRAVA_CALLBACK_URL"), methods=['GET', 'POST'])
def subCallback():
    """
    Strava subscription callback URL.

    Returns
    -------
    GET request:
        JSON, echoed Strava challenge text.
    POST request:
        Success code if data are successfully added to Postgres/PostGIS. Strava must receive a 200 code in response to
        POST.
    """
    application.logger.debug("Got a callback request!")
    WebHookFunctionsStrava.handleSubCallback(request)
    application.logger.debug("Returning success code!")
    return Response(status=200)

@stravaActDashAPI_BP.route("/stravaroutes", methods=['GET'])
def stravaActAPI():
    actLimit = int(request.args.get("actlimit"))
    res = DBQueriesStrava.getStravaMaskedActGeoJSON(actLimit)
    return res

@stravaActDashAPI_BP.route("/getstravastreamurl", methods=['GET'])
def getsteamS3url():
    actID = str(request.args.get("actID"))
    # print(f"csvname is: {actID}")
    res = StravaAWSS3.create_presigned_url(actID)
    return res

@stravaActDashAPI_BP.route("/getstravatopojsonurl", methods=['GET'])
def getstravatopojsonurl():
    res = StravaAWSS3.create_presigned_url("activitiesTopoJSON")
    return res


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
