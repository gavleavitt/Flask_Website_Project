from flask.views import View, MethodView
from functools import wraps
from application import login_manager
from flask_login import current_user
from application.WebAppProjects.MaintenanceTracking import models
from application.util.flaskLogin.models import User
from application import app, db, logger, apiPrefix
from flask import jsonify, request, Response
from application.util.ErrorHandling import exception_handler
# Pluggable views
# https://flask.palletsprojects.com/en/2.0.x/views/
# see https://stackoverflow.com/a/19376449
# for using flask login with pluggable view

def user_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not current_user.is_authenticated():
            return login_manager.unauthorized()
            # or, if you're not using Flask-Login
            # return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorator

class apiMethod(MethodView):

    def get(self, rec_id, model):
        if rec_id is None:
            # return all
            return jsonify(model.query.all())
        else:
            return model.filter_by(id=rec_id)

    def delete(self, model):
        pass
    # def getOwnerFK(self, userName):
    #     return loginModels.User.filter_by(userName=userName).first()

class maintRecAPI(apiMethod):

    def post(self):
        # Get request content
        # request.json['abc']
        # content = request.get_json()
        newRec = models.maintRecord()
        # Add record to session
        db.session.add(newRec)
        # Commit record to database
        db.session.commit()
        # Return success
        return Response(status = 201)
    def put(self):
        pass

class AssetRecAPI(apiMethod):
    def post(self):
        content = request.get_json()
        # logger.debug(f"{request.path} Received post request: {content}")
        # Get ownerfk
        ownerFK = models.Owner.query.filter_by(username=content['UserName']).first()
        # logger.debug(f"FK is {ownerFK}")
        newAsset = models.Asset(name=content['AssetName'], modelyear=content['ModelYear'],
                                make=content['MakeName'], model=content['ModelName'], notes=content['Notes'],
                                suspension=content['Suspension'], framesize=content['FrameSize'],
                                wheelsize=content['WheelSize'], type=content['Type'], retailprice=content['RetailPrice'],
                                purchaseprice=content['PurchasePrice'], purchasetype=content['PurchaseType'],
                                purchasesource=content['PurchaseSource'], serial=content['Serial'],
                                ownerfk=ownerFK.id)
        db.session.add(newAsset)
        db.session.commit()
        return Response(status=201)

###TODO enable flask login required:
# maint_view = user_required(maintRecAPI.as_view('maintenance_api'))
# Add maintenance view
# Convert class into a view function, string is the name of the endpoint
# maint_view = maintRecAPI.as_view('maintenance_api')
# # Attach url routes and methods to the view function and register them with the application
# maintAPIPrefix = f'{apiPrefix}/maintenancetracking'
# app.add_url_rule(f'{maintAPIPrefix}/record/', defaults={'user_id': None},
#                  view_func=maint_view, methods=['GET',])
# app.add_url_rule(f'{maintAPIPrefix}/record/', view_func=maint_view, methods=['POST',])
# # Set route to handle requests for specific record IDs
# app.add_url_rule(f'{maintAPIPrefix}/record/<int:record_id>', view_func=maint_view,
#                  methods=['GET', 'PUT', 'DELETE'])

# # Add Asset view
# asset_view = maintRecAPI.as_view('asset_api')
# # Attach url routes and methods to the view function and register them with the application
# app.add_url_rule(f'{maintAPIPrefix}/asset/', defaults={'asset_id': None},
#                  view_func=asset_view, methods=['GET',])
# app.add_url_rule(f'{maintAPIPrefix}/asset/', view_func=asset_view, methods=['POST',])
# # Set route to handle requests for specific record IDs
# app.add_url_rule(f'{maintAPIPrefix}/asset/<int:asset_id>', view_func=asset_view,
#                  methods=['GET', 'PUT', 'DELETE'])

# def register_api(view, endpoint, url, pk='id', pk_type='int'):
#     view_func = view.as_view(endpoint)
#     app.add_url_rule(url, defaults={pk: None},
#                      view_func=view_func, methods=['GET',])
#     app.add_url_rule(url, view_func=view_func, methods=['POST',])
#     app.add_url_rule(f'{url}<{pk_type}:{pk}>', view_func=view_func,
#                      methods=['GET', 'PUT', 'DELETE'])
#
# register_api(UserAPI, 'user_api', '/users/', pk='user_id')