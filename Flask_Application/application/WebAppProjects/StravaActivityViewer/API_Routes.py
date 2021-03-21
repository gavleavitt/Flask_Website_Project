from application import app, application
from flask import Blueprint, Response, request
import os

stravaActDashAPI_BP = Blueprint('stravaActDashAPI', __name__,
                        template_folder='templates',
                        url_prefix='/api/v1/tracker',
                        static_folder='static')


@app.route(os.environ.get("strava_callback_url"), methods=['GET', 'POST'])
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

@app.route("/api/v0.1/stravaroutes", methods=['GET'])
def stravaActAPI():
    actLimit = int(request.args.get("actlimit"))
    res = DBQueriesStrava.getStravaMaskedActGeoJSON(actLimit)
    return res

@app.route("/api/v0.1/getstravastreamurl", methods=['GET'])
def getsteamS3url():
    actID = str(request.args.get("actID"))
    # print(f"csvname is: {actID}")
    res = StravaAWSS3.create_presigned_url(actID)
    return res

@app.route("/api/v0.1/getstravatopojsonurl", methods=['GET'])
def stravaTopoJSON():
    res = StravaAWSS3.create_presigned_url("activitiesTopoJSON")
    return res
