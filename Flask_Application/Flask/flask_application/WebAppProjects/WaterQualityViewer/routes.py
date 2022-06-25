from flask_application.WebAppProjects.WaterQualityViewer import functionsWaterQual, DBQueriesWaterQuality
from flask import render_template, Blueprint


sbcWaterQuality_BP = Blueprint('sbcWaterQuality_BP', __name__,
                        template_folder='templates',
                        static_folder='static')

@sbcWaterQuality_BP.route("/sbcwaterqualityviewer")
@sbcWaterQuality_BP.route("/sbcwaterquality")
def sbcWaterQualityMap():
    """
    Function to handle webpage requests of the Santa Barbara Ocean Water Quality web page.
    Kicks off functions to get beach test results and returns a Jinja rendered HTML page with the
    beach results passed into the template

    Returns
    -------
    Jinja Rendered HTML webpage
       Leaflet webpage with the beaches and water quality reports passed in a variables.

    """
    beachresults = functionsWaterQual.handleBeaches()
    beachqual = beachresults["waterqual"]
    recentrec = beachresults["recent"]
    standards = DBQueriesWaterQuality.getStandards()
    return render_template("WaterQualityViewer/SBCWaterQualityMap.html", beachgeojson=beachqual, standards=standards,
                           recentdate=recentrec)