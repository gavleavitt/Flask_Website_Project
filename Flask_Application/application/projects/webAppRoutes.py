@projectPages_BP.route("/maps/stravamap")
@projectPages_BP.route("/stravamap")
@projectPages_BP.route("/strava")
def stravaprojmap():
    return render_template("public/maps/Strava_Map_Dashboard.html")

@projectPages_BP.route("/maps/stravamaptesting")
def stravatestingmap():
    return render_template("public/maps/Strava_Map_Dashboard_Testing.html")

@projectPages_BP.route("/maps/sbcoceanwaterquality")
@projectPages_BP.route("/waterquality")
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
@projectPages_BP.route("/dashboards/livetracker")
@projectPages_BP.route("/livetracker")
@projectPages_BP.route("/liveviewer")
@projectPages_BP.route("/tracker")
@projectPages_BP.route("/viewer")
@projectPages_BP.login_required(role='viewer')
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