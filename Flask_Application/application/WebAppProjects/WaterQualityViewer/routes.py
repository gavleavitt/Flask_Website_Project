from application import app
from flask import render_template, Blueprint


sbcWaterQuality_BP = Blueprint('sbcWaterQuality_BP', __name__,
                        template_folder='templates',
                        url_prefix='/webapps',
                        static_folder='static')



@sbcWaterQuality_BP.route("/maps/sbcoceanwaterquality")
@sbcWaterQuality_BP.route("/waterquality")
def waterQual():
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
    return render_template("public/maps/Water_Qual_Map.html", beachgeojson=beachqual, standards=standards,
                           recentdate=recentrec)