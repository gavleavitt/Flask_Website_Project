from application import app
from flask import render_template, Blueprint


projectPages_BP = Blueprint('projectPages_BP', __name__,
                        template_folder='templates',
                        url_prefix='/projectpages',
                        static_folder='static')


@projectPages_BP.route("/sbcoceanquality")
def sbcwaterquality():
    return render_template("project-SBC-Water-Quality/project-SBC-Water-Quality.html")

@projectPages_BP.route("/livetrackingdashboard")
def livetrackingdash():
    return render_template("project-Live-Tracking-Dashboard/project-Live-Tracking-Dashboard.html")

@projectPages_BP.route("/sanitarysewertraceapp")
def sanitarysewertrace():
    return render_template("project-Sanitary-Sewer-Trace/project-Sanitary-Sewer-Trace.html")

@projectPages_BP.route("/sanitaryewerstormdrainbuildout")
def sanitarysewerstormdrainbuildout():
    return render_template("project-Sanitary-Sewer-Storm-Drain-Builtout/project-Sanitary-Sewer-Storm-Drain-Builtout.html")

@projectPages_BP.route("/streetlightpolepermitting")
def streetlightpolepermitting():
    return render_template("project-Streetlight-Pole-Permitting/project-Streetlight-Pole-Permitting.html")

@projectPages_BP.route("/dashboardsandmaps")
def dashboardsandmaps():
    return render_template("project-Operations-Dashboards-Maps/project-Operations-Dashboards-Maps.html")

@projectPages_BP.route("/stravamapserverside")
def stravaserversideprocessing():
    return render_template("project-Strava-Activities-Server-Side/project-Strava-Activities-Server-Side.html")

@projectPages_BP.route("/lacostormwatertrace")
def lacostormwatertrace():
    return render_template("project-LA-County-Stormwater-Trace/project-LA-County-Stormwater-Trace.html")
