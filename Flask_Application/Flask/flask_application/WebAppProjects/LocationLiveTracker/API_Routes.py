from flask_application import application
from flask import Blueprint, request, jsonify
from flask_application.util.flaskAuth.authentication import auth
from flask_application.WebAppProjects.LocationLiveTracker import DBQueriesTracker, modelsTracker, objectGenerationTracker, OverPassAPI

livetrackerAPI_BP = Blueprint('livetrackerAPI_BP', __name__,
                        template_folder='templates',
                        static_folder='static')


@livetrackerAPI_BP.route("/postgpsdata", methods=['POST'])
@auth.login_required(role='admin')
def handle_gps():
    """
    Handles incoming GPS HTTP POST requests by kicking off the workflow to process ancillary data,
    generate models, and commit new data to the DB.

    Requires admin level access.
    -------
    TYPE
        JSON response code, success or error.

    """
    # print("Hit with a post request!")
    if request.method == 'POST':
        if request.is_json:
            # print("Hit server with POST request and valid json mime type!")
            data = request.get_json()
            # print(data)
            objectGenerationTracker.handleTrackerPOST(data)
            # Return a json success code
            resp = jsonify(success=True)
            return resp
            # return {"message": f"GPS entry {newrecord.date} has been created successfully."}
        else:
            # POST request is not in json, return error
            # print("Got a POST request but the payload isnt in JSON!", file=sys.stdout)
            return {"error": "The request payload is not in JSON format"}


@livetrackerAPI_BP.route("/getpoint", methods=['GET'])
@auth.login_required(role='viewer')
def getPointGeojson():
    """
    Handles HTTP GET requests of GPS points, kicks off the process to generate and return a geoson GPS data point.

    Currently this is hard coded to return only the most recent point.

    Requires at least viewer authentication

    Returns
    -------
    result : geojson
        Geojson representation of the gps point spatial data.

    """
    # print("Hit with a point get request!")
    result = DBQueriesTracker.getTrackerFeatCollection(reclimit=1, datatype="gpspoints")
    return result


@livetrackerAPI_BP.route("/gettracks", methods=['GET'])
@auth.login_required(role='viewer')
def getTrackGeojson():
    """
    Handles HTTP GET requests of GPS tracks, this is hard coded in the DB query helper function to only query the records for the same day.

    Requires at least viewer authentication.

    Returns
    -------
    result :  geojson
        Geojson representation of the gps tracks spatial data

    """
    # print("Hit with a gpstrack get request!")
    result = DBQueriesTracker.getTrackerFeatCollection(reclimit="all", datatype="gpstracks")
    return result
