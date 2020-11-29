"""
This Module contains the domain URL routes served by Flask that will be visited directly by a user in a browser.
API routes accessed by scripts are not included in this module. 

@author: Gavin Leavitt
"""

from application import app
from flask import render_template
from application.projects.water_quality import functionsWaterQual, DBQueriesWaterQuality
from application.flaskAuth.authentication import auth

@app.route("/")
@app.route("/main")
def index():
    return render_template("public/index.html")

@app.route("/resume")
def resume():
    return render_template("public/resume.html")

@app.route("/about")
def about():
    return render_template("public/aboutme.html")

@app.route("/contact")
def contact():
    return render_template("public/contactme.html")

@app.route("/templatetesting")
def template():
    return render_template("public/projects/project-template.html")

@app.route("/maps/stravamap")
@app.route("/stravamap")
@app.route("/strava")
def stravaprojmap():
    return render_template("public/maps/Strava_Map_Dashboard.html")

@app.route("/maps/stravamaptesting")
def stravatestingmap():
    return render_template("public/maps/Strava_Map_Dashboard_Testing.html")

@app.route("/maps/sbcoceanwaterquality")
@app.route("/waterquality")
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
@app.route("/dashboards/livetracker")
@app.route("/livetracker")
@auth.login_required(role='viewer')
def liveGPS():
    """
    This HTML document contains Javascript to poll other APIs in this application, allowing for dynamic
    data that updates automatically, so no data is passed through here.

    Returns
    -------
    HTML webpage
        Renders the live mobile GPS webpage and sends to the user.

    """
    return render_template("private/livertracker_dashboard.html")

@app.route("/projects/sbcoceanquality")
def waterqualproj():
    return render_template("public/projects/project-Water-Quality.html")

@app.route("/projects/livetrackingdashboard")
def livetrackingdash():
    return render_template("public/projects/project-Live-Tracking-Dashboard.html")

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

@app.route("/projects/stravamap")
def stravaactivitymap():
    return render_template("public/projects/project-Strava-Activities.html")
