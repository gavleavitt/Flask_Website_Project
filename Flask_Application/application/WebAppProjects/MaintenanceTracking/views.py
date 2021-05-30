from flask.views import View, MethodView
from functools import wraps
from application import login_manager
from flask_login import current_user
from application.WebAppProjects.MaintenanceTracking import models
from application.util.flaskLogin.models import User
from sqlalchemy import and_, or_
from application import app, db, logger, apiPrefix
from flask import jsonify, request, Response, abort
from application.util.ErrorHandling import exception_handler
import json
import re
from application.util.ErrorHandling import exception_handler
# Pluggable views
# https://flask.palletsprojects.com/en/2.0.x/views/
# see https://stackoverflow.com/a/19376449
# for using flask login with pluggable view

# see https://stackoverflow.com/questions/31669864/date-in-flask-url
# for using date range in url

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
    # see https://stackoverflow.com/questions/59272322/flask-methodview-with-decorators-is-giving-error
    # Add decorators to rest API
    ###TODO enable flask login required
    decorators = [exception_handler]

    ## Helper Functions

    def buildQuery(self, model, query, reqDict):
        """
        Builds a dynamic SQLAlchemy query based on GET request arguments.

        ## see
        # https://treyhunner.com/2018/04/keyword-arguments-in-python/
        # https://www.reddit.com/r/learnpython/comments/7b9qqs/dynamically_generate_sqlalchemy_query_based_on/
        # see https://stackoverflow.com/questions/27810523/sqlalchemy-elegant-way-to-deal-with-several-optional-filters

        @param model:
        @param query:
        @param reqDict:
        @return:
        """
        # Iterate over request dictionary building out query, each iteration will add a filter statement
        for param, value in reqDict.items():
            # Use regex to remove min and max from key name
            reParam = re.sub("max|min", "", param)
            # Use key name to get matching model attribute, this attribute will be used in query against the database
            modelParam = getattr(model, reParam)
            # Apply greater than or less than equal to if the request parameter contained min or max
            if 'min' in param:
                query = query.filter(modelParam >= value)
            elif 'max' in param:
                query = query.filter(modelParam <= value)
            else:
                query = query.filter(modelParam == value)
        # Apply a limit to query
        if reqDict['limit']:
            query = query.limit(int(reqDict['limit']))
        # Return formatted query, this query may be added to before being used to call on the database
        return query

    def formatMultiResponse(self, query):
        query = query.all()
        res = []
        if not query:
            return Response(status=404)
        for i in query:
            # Convert each object result to a dictionary and add to result list
            res.append(i.to_dict())
        return jsonify(res)

    def postData(self, model, content):
        """

        @param model:
        @param content:
        @return:
        """
        newRec = model()
        # Iterate over request dict keys and values
        for key, value in content.items():
            # Check if object has an attribute matching the content update key
            if hasattr(newRec, key):
                # Set the object attribute value based on the key:value pair, this allows for updating only
                # certain values within the object
                setattr(newRec, key, value)
        db.session.add(newRec)
        # Commit updates to database
        db.session.commit()
        return Response(status=201)

    # def getData(self, rec_id, model, idField=None, minDate=None, maxDate=None, workType=None, minCost=None,
    #             maxCost=None, shop=None, minDuration=None, maxDuration=None):
    def getData(self, rec_id, model, idField=None, dynamicQuery=None):
        """
        Executes an GET request on the input SQLAlchemy Model.

        @param rec_id: Int. Record to be updated.
        @param model: SQLAlchemy Model of database table.
        @return: JSON formatted response.
        """
        # Check if record ID is none
        if rec_id is None:
            # No record ID given, return all records
            query = model.query
            # res = self.formatMultiResponse(query)
        # Check if a dynamic query has been generated
        elif dynamicQuery:
            query = dynamicQuery
        # Return specific record or related records
        else:
            # Filter by record ID and idField given
            # pass a dictionary into filter by then unpack it, forming proper request syntax
            # query = model.query.filter_by(**{idField: rec_id})
            query = model.query.filter_by((getattr(model, idField)) == rec_id)
        # Get results of query and serialize them into json response
        return self.formatMultiResponse(query)

    def deleteData(self, rec_id, model):
        # Delete record
        model.query.filter_by(id=rec_id).delete()
        # Commit delete
        db.session.commit()

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

class PartInstallRecAPI(apiMethod):
    pass


class MaintRecAPI(apiMethod):
    """
    API for CRUD operations on maintenance information.
    """
    model = models.maintRecord
    # getName = "MaintenanceRecord"
    # startDate = None
    # endDate = None

    def post(self):
        """
        POST request view, inserts the requested maintenance record into the database.
        @return: Response Code
        """
        content = request.get_json(force=True)
        # Check if assetFK matches an existing asset
        asset = models.Asset.query.filter_by(id=content['assetfk']).first()
        if asset:
            # Create maintenance record
            return self.postData(self.model, content)
        else:
            # Asset doesn't exist, return 404
            return Response(status=404)

    def put(self, rec_id):
        """
        PUT request view, allows updating individual maintenance records.
        @param rec_id: Int. Asset record to be updated
        @return: Response Code
        """
        # Get content, even if request isn't set to json
        content = request.get_json(force=True)
        # Set asset model as the model to receive update
        return self.putData(rec_id, self.model, content)

    def get(self, rec_id):
        """
        GET request view, allows selecting one or all records.

        # Convert arguments to query directly:
        https://stackoverflow.com/questions/19680103/flask-convert-request-args-to-dict
        @param rec_id: Int. Asset record to be returned
        @return: JSON. Requested record(s).
        """
        # Convert request to a dictionary
        reqDict = request.args.to_dict()
        # Build query with optional request parameters
        query = self.buildQuery(model=self.model, query=self.model.query, reqDict=reqDict)
        # Get the query results as a json
        return self.getData(rec_id=rec_id, idField='assetfk', model=self.model, dynamicQuery=query)

    def delete(self, rec_id):
        """
        Delete request view, allows deleting a single record.
        @param rec_id: Int. Asset record to be returned
        @return: Response Code.
        """
        if rec_id:
            return self.deleteData(rec_id, self.model)
        else:
            return Response(status=405)

class AssetRecAPI(apiMethod):
    """
    API for CRUD operations on asset information.
    """
    model = models.Asset
    # getName = "Assets"
    def post(self):
        """
        POST request view, inserts the requested asset record into the database.
        @return: Response Code
        """
        content = request.get_json()
        # logger.debug(f"{request.path} Received post request: {content}")
        # Get ownerfk
        ownerFK = models.Owner.query.filter_by(username=content['username']).first()
        if ownerFK:
            # Add fk to content Dict
            content['ownerfk'] = ownerFK.id
            return self.postData(self.model, content)
        else:
            return Response(status=404)

    def put(self, rec_id):
        """
        PUT request view, allows updating individual asset records.
        @param rec_id: Int. Asset record to be updated
        @return: Response Code
        """
        # Get content, even if request isn't set to json
        content = request.get_json(force=True)
        # Set asset model as the model to receive update
        return self.putData(rec_id, self.model, content)

    def get(self, rec_id):
        """
        GET request view, allows selecting one or all records
        @param rec_id: Int. Asset record to be returned
        @return: JSON. Requested record(s).
        """
        return self.getData(rec_id=rec_id, idField='id', model=self.model)

    def delete(self, rec_id):
        """
        Delete request view, allows deleting a single record.
        @param rec_id: Int. Asset record to be returned
        @return: Response Code.
        """
        if rec_id:
            return self.deleteData(rec_id, self.model)
        else:
            return Response(status=404)

##TODO build out API to add/edit after market part/accessory installs




##TODO build out API to query Strava for distance ridden since maintenance/part install


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