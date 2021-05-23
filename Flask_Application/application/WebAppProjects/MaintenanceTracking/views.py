from flask.views import View, MethodView
from functools import wraps
from application import login_manager
from flask_login import current_user
from application.WebAppProjects.MaintenanceTracking import models
from application.util.flaskLogin.models import User
from application import app, db, logger, apiPrefix
from flask import jsonify, request, Response
import json
from application.util.ErrorHandling import exception_handler
# Pluggable views
# https://flask.palletsprojects.com/en/2.0.x/views/
# see https://stackoverflow.com/a/19376449
# for using flask login with pluggable view

def user_required(f):
    """

    @param f:
    @return:
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        if not current_user.is_authenticated():
            return login_manager.unauthorized()
            # or, if you're not using Flask-Login
            # return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorator

class apiMethod(MethodView):
    """

    """
    def postData(self):
        pass

    def getData(self, rec_id, model, resultName):
        """
        Executes an GET request on the input SQLAlchemy Model.

        @param rec_id: Int. Record to be updated.
        @param model: SQLAlchemy Model of database table.
        @param resultName: String. Name of JSON array to be returned.
        @return: JSON formatted response.
        """
        if rec_id is None:
            # No record ID given, return all records
            query = model.query.all()
            # see https://stackoverflow.com/a/35958717
            res = []
            for i in query:
                # Convert each object result to a dictionary and add to result list
                res.append(i.to_dict())
            return jsonify({resultName:res})
        else:
            # Return just the requested record, if it exists
            res = model.query.filter_by(id=rec_id).first()
            if res:
                return res.to_json()
            else:
                return Response(status=404)
    def deleteData(self, model):
        pass

    def putData(self, rec_id, model, content):
        """
        Executes an UPDATE request on the input SQLAlchemy Model.

        @param rec_id: Int. Record to be updated.
        @param model: SQLAlchemy Model of database table.
        @param content: Dict. JSON PUT request body converted to a dict.
        @return: Response code.
        """
        # Query record
        query = model.query.filter_by(id=rec_id).first()
        # Check if any records match
        if query:
            # Iterate over request dict keys and values
            for key, value in content.items():
                # Check if object has an attribute matching the content update key
                if hasattr(query,key):
                    # Set the object attribute value based on the key:value pair, this allows for updating only
                    # certain values within the object
                    setattr(query, key, value)
            # Commit updates to database
            db.session.commit()
            return Response(status=200)
        # Resource not found
        else:
            return Response(status=404)

    # def getOwnerFK(self, userName):
    #     return loginModels.User.filter_by(userName=userName).first()

class AssetRecAPI(apiMethod):
    """
    API for CRUD operations on asset information.
    """
    def post(self):
        """
        POST request view, inserts the requested asset record into the database.
        @return: Response Code
        """
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
    def put(self, rec_id):
        """
        PUT request view, allows updating individual asset records.
        @param rec_id: Int. Asset record to be updated
        @return: Response Code
        """
        # Get content, even if request isn't set to json
        content = request.get_json(force=True)
        # Set asset model as the model to receive update
        return self.putData(rec_id, models.Asset, content)

    def get(self, rec_id):
        """
        GET request view, allows selecting one or all records
        @param rec_id: Int. Asset record to be returned
        @return: JSON. Requested record(s).
        """
        return self.getData(rec_id, models.Asset, "Assets")

class maintRecAPI(apiMethod):
    """

    """
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