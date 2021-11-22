from flask import render_template, Blueprint, url_for
from application import app

lacoSWTraceapp_BP = Blueprint('lacoSWTraceapp_BP', __name__,
                        template_folder='templates',
                        static_folder='static')

@lacoSWTraceapp_BP.route("/laco-sw-trace-app")
# @lacoSWTraceapp_BP.route("/app")
@app.route("/laco-sw-trace-app", subdomain ='apps')
def lacountyswtraceappviewer():
    return render_template("LACO_SW_TraceApp/laco_sw_traceapp.html")