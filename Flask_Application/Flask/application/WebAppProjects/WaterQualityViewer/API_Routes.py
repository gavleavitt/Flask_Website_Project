from application.WebAppProjects.WaterQualityViewer import functionsWaterQual, DBQueriesWaterQuality
from flask import render_template, Blueprint, request

sbcWaterQualityAPI_BP = Blueprint('sbcWaterQualityAPI_BP', __name__,
                        template_folder='templates',
                        static_folder='static')


@sbcWaterQualityAPI_BP.route("getbeachhistory", methods=['GET'])
def getWaterQualityHistory():
    beachName = str(request.args.get("beachName"))
    return DBQueriesWaterQuality.getBeachResults(beachName)