"""
This Module contains the domain URL routes served by Flask that will be visited directly by a user in a browser.
API routes accessed by scripts are not included in this module. 

@author: Gavin Leavitt
"""

from application import application, app
from flask import render_template
from application import functions as func
from application import DB_Queries as DBQ
from application import getStravaActivities
from application import DB_Queries_Strava
from application.authentication import auth

@app.route("/")
def index():
    return render_template("public/index.html")


@app.route("/main")
def main():
    return render_template("public/index.html")


@app.route("/dashboards/livetracker")
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


@app.route("/maps/sbcoceanwaterquality")
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
    beachresults = func.handleBeaches()
    beachqual = beachresults["waterqual"]
    recentrec = beachresults["recent"]
    standards = DBQ.getStandards()
    return render_template("public/maps/Water_Qual_Map.html", beachgeojson=beachqual, standards=standards,
                           recentdate=recentrec)



@app.route("/projects/sbcoceanquality")
def waterqualproj():
    return render_template("public/projects/project-Water-Quality.html")


@app.route("/projects/livetrackingdashboard")
def livetrackingdash():
    return render_template("public/projects/project-Live-Tracking-Dashboard.html")


@app.route("/templatetesting")
def template():
    return render_template("public/projects/project-template.html")


@app.route("/resume")
def resume():
    return render_template("public/resume.html")


@app.route("/about")
def about():
    return render_template("public/aboutme.html")


@app.route("/projects/sanitarysewertraceapp")
def sanitarysewertrace():
    return render_template("public/projects/project-Sanitary-Sewer-Trace.html")


@app.route("/projects/sanitaryewerstormdrainbuildout")
def sanitarysewerstormdrainbuildout():
    return render_template("public/projects/project-Sanitary-Sewer-Storm-Drain-Builtout.html")


@app.route("/projects/streetlightpolepermitting")
def streetlightpolepermitting():
    return render_template("public/projects/project-Streetlight-Pole-Permitting.html")


@app.route("/projects/dashboardsmaps")
def dashboardsmaps():
    return render_template("public/projects/project-Operations-Dashboards-Maps.html")


@app.route("/contact")
def contact():
    return render_template("public/contactme.html")


@app.route("/maps/stravamap")
def stravaprojmap():
    # activityData = DB_Queries_Strava.getStravaActGeoJSON(20)
    # activityData = DB_Queries_Strava.getStravaMaskedActGeoJSON(30)
    return render_template("public/maps/Strava_Map.html")

