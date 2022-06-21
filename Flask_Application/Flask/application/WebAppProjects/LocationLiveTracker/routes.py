from flask import render_template, Blueprint
from application.util.flaskAuth.authentication import auth

liveTracker_BP = Blueprint('liveTracker_BP', __name__,
                        template_folder='templates',
                        # url_prefix='/webapps',
                        static_folder='static')

@liveTracker_BP.route("/dashboards/livetracker")
@liveTracker_BP.route("/livetracker")
@liveTracker_BP.route("/liveviewer")
@liveTracker_BP.route("/tracker")
@liveTracker_BP.route("/viewer")
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
    return render_template("LocationLiveTracker/LocationLiveTrackerDashboard.html")