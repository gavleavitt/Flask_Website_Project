from flask import render_template, Blueprint, url_for
from flask_application import app, application

lacoSWTraceapp_BP = Blueprint('lacoSWTraceapp_BP', __name__,
                        template_folder='templates',
                        static_folder='static')

# @lacoSWTraceapp_BP.route("/app")
@app.route("/laco-sw-trace-app")
@lacoSWTraceapp_BP.route("/laco-sw-trace-app")
def lacountyswtraceappviewer():
    # Check if production or development mode
    if application.config['ENV'] == "development":
        # apiURL = f"http://api.{app.config['SERVER_NAME'] + url_for('lacoSWTraceapp_API_BP.handletracerequest')}"
        apiURL = f"http://localhost:5000{url_for('lacoSWTraceapp_API_BP.handletracerequest')}"
    else:
        apiURL = f"https://www.leavittmapping.com{url_for('lacoSWTraceapp_API_BP.handletracerequest')}"
    # apiURL = url_for('lacoSWTraceapp_API_BP.handletracerequest')
    application.logger.debug(apiURL)
    return render_template("LACO_SW_TraceApp/laco_sw_traceapp.html", apiURL = apiURL)
    # return render_template("LACO_SW_TraceApp/laco_sw_traceapp.html", apiURL = f"http://api.{app.config['SERVER_NAME'] + url_for('lacoSWTraceapp_API_BP.handletracerequest')}")

@app.route("/laco-sw-trace-app-protected")
@lacoSWTraceapp_BP.route("/laco-sw-trace-app-protected")
def lacountyswtraceappprotectedviewer():
    # Check if production or development mode
    if application.config['ENV'] == "development":
        # apiURL = f"http://api.{app.config['SERVER_NAME'] + url_for('lacoSWTraceapp_API_BP.handletracerequest')}"
        apiURL = f"http://localhost:5000{url_for('lacoSWTraceapp_API_BP.handletracerequest')}"
    else:
        apiURL = f"https://www.leavittmapping.com{url_for('lacoSWTraceapp_API_BP.handletracerequest')}"
    # apiURL = url_for('lacoSWTraceapp_API_BP.handletracerequest')
    application.logger.debug(apiURL)
    return render_template("LACO_SW_TraceApp/laco_sw_traceapp_protected.html", apiURL = apiURL)
    # return render_template("LACO_SW_TraceApp/laco_sw_traceapp.html", apiURL = f"http://api.{app.config['SERVER_NAME'] + url_for('lacoSWTraceapp_API_BP.handletracerequest')}")