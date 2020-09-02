"""
This Module contains the domain URL routes served by Flask that will be visited directly by a user in a browser.
API routes accessed by scripts are not included in this module. 

@author: Gavin Leavitt
"""

from application import application, app
from flask import render_template
from application import functions as func
from application import DB_Queries as DBQ

@app.route("/")
def index():
    return "Hello world"

@app.route("/about")
def about():
    return "All about Flask"

@app.route("/gps")
def gps():
    return render_template("private/tracker.html")

@app.route("/main")
def main():
    return render_template("public/index.html")

@app.route("/liveviewer")
def liveGPS():
    """
    This HTML document contains Javascript to poll other APIs in this application, allowing for dynamic 
    data that updates automatically, so no data is passed through here.

    Returns
    -------
    HTML webpage
        Renders the live mobile GPS webpage and sends to the user.  

    """
    return render_template("private/tracker_API.html")

@app.route("/SBCOceanWaterQuality")
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
    beachqual = func.handleBeaches()
    standards = DBQ.getStandards()
    return render_template("public/leaflet_map.html", beachgeojson = beachqual, standards=standards)
