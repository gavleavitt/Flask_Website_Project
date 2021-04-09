from flask import render_template, Blueprint, url_for
from application.util.flaskAuth.authentication import auth

stravaActDash_BP = Blueprint('stravaActDash_BP', __name__,
                        template_folder='templates',
                        static_folder='static')

@stravaActDash_BP.route("/stravamap")
@stravaActDash_BP.route("/strava")
@stravaActDash_BP.route("/stravadashboard")
@stravaActDash_BP.route("/stravaviewer")
def stravaActivityViewerDashboard():
    # return render_template("StravaActivityViewer/StravaActivityViewerDashboard.html", topojsonurl=url_for(".getstravatopojsonurl"))
    return render_template("StravaActivityViewer/StravaActivityViewerDashboard.html")

@stravaActDash_BP.route("/admin")
@auth.login_required(role='admin')
def stravaActivityAdmin():
    return render_template("StravaActivityViewer/StravaActivityViewerAdminControls.html")
# @stravaActDash_BP.route("/maps/stravamaptesting")
# def stravatestingmap():
#     return render_template("public/maps/Strava_Map_Dashboard_Testing.html")