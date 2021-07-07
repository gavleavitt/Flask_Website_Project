from application import app, application, auth
from flask import Blueprint, Response, request
import os
from application.WebAppProjects.StravaActivityViewer import WebHookFunctionsStrava, DBQueriesStrava, StravaAWSS3

stravaActDashAPI_BP = Blueprint('stravaActDashAPI_BP', __name__,
                        template_folder='templates',
                        static_folder='static')



@stravaActDashAPI_BP.route("/webhookcallback", methods=['GET', 'POST'])
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
    res = WebHookFunctionsStrava.handleSubCallback(request)
    application.logger.debug("Returning code!")
    if res:
        return res
    else:
        return Response(status=400)

# @stravaActDashAPI_BP.route("/stravaroutes", methods=['GET'])
# def stravaActAPI():
#     actLimit = int(request.args.get("actlimit"))
#     res = DBQueriesStrava.getStravaMaskedActGeoJSON(actLimit)
#     return res

@stravaActDashAPI_BP.route("/getstravastreamurl", methods=['GET'])
def getsteamS3url():
    """
    Returns a presigned url, granting temporary access to a Strava Activity Stream CSV. CSVs are not shared directly
    with the public to limit S3 Bucket requests.
    """
    actID = str(request.args.get("actID"))
    # print(f"csvname is: {actID}")
    res = StravaAWSS3.create_presigned_url(actID)
    return res

@stravaActDashAPI_BP.route("/getstravatopojsonurl", methods=['GET'])
def getstravatopojsonurl():
    """
    Returns a presigned url, granting temporary access to the TopoJSON file. The file is not shared directly
    with the public to limit S3 Bucket requests.
    """
    res = StravaAWSS3.create_presigned_url("activitiesTopoJSON")
    return res
