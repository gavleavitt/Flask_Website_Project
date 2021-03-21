from application import app
from flask import render_template, Blueprint

stravaActDash_BP = Blueprint('stravaActDash_BP', __name__,
                        template_folder='templates',
                        url_prefix='/webapps',
                        static_folder='static')

@stravaActDash_BP.route("/stravamap")
@stravaActDash_BP.route("/strava")
@stravaActDash_BP.route("/stravadashboard")
@stravaActDash_BP.route("/stravaviewer")
def stravaprojmap():
    return render_template("public/maps/Strava_Map_Dashboard.html")

@stravaActDash_BP.route("/maps/stravamaptesting")
def stravatestingmap():
    return render_template("public/maps/Strava_Map_Dashboard_Testing.html")