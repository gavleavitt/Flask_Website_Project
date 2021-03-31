from flask import Blueprint, request, jsonify, Response
from application.util.flaskAuth.authentication import auth

stravaActDashAPI_Admin_BP = Blueprint('stravaActDashAPI_Admin_BP', __name__,
                        template_folder='templates',
                        static_folder='static')

@stravaActDashAPI_Admin_BP.route("/addactivity", methods=['POST'])
@auth.login_required(role='admin')
def addactivity():
    actID = int(request.form['actID'])
    return Response(status=200)