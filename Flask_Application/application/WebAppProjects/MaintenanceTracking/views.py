from flask.views import View, MethodView
from functools import wraps
from application import login_manager
from flask_login import current_user
from application.WebAppProjects.MaintenanceTracking import models
from application.util.APIAuth import user_required
from sqlalchemy import and_, or_
from application import app, db, logger, apiPrefix
from flask import jsonify, request, Response, abort
import json
import re
from application.util.ErrorHandling import exception_handler




# see https://stackoverflow.com/questions/31669864/date-in-flask-url
# for using date range in url


class stravaRequest(MethodView):
    """
    Process all records between two provided dates and provide a summary of information.
    """
    pass
    # Get Strava credentials
    # req = request.getjson()
    # Get username from session


class apiMethod(MethodView):
    """

    """

    def __init__(self):
        self.dbModel = self.model

    # see https://stackoverflow.com/questions/59272322/flask-methodview-with-decorators-is-giving-error
    # Add decorators to rest API
    ###TODO enable flask login required
    decorators = [exception_handler, user_required]

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
        if 'limit' in reqDict:
            query = query.limit(int(reqDict['limit']))
        # Return formatted query, this query may be added to before being used to call on the database
        return query

    def formatMultiResponse(self, query):
        """
        Issues query to database and serializes results into json.

        Serialization is dependant on the sqlathanor module, consider using Marshmellow or find a
        native, sqlalchemy, or flask function to convert the query results into a dictionary.
        @param query: SQLAlchemy query. Dynamically generated SQLAlchemy query.
        @return: JSON. Query results.
        """
        query = query.all()
        res = []
        if not query:
            return Response(status=404)
        for i in query:
            # Convert each object result to a dictionary and add to result list
            res.append(i.to_dict())
        # Convert list of dictionaries to json response
        return jsonify(res)

    def get(self, rec_id):
        """
        Executes a SELECT/retrieve call on the database using the input SQLAlchemy Model.

        This method is called by GET method views, allowing the control of inputs as required by the API.

        @param rec_id: Int. Record to be updated.
        @param model: SQLAlchemy Model of database table.
        @param idField: String. Optional.
        @param dynamicQuery:
        @return: JSON formatted response.
        """

        # Convert request to a dictionary
        reqDict = request.args.to_dict()
        logger.debug(reqDict)

        # Build query with optional request parameters, if provided
        if reqDict:
            query = self.buildQuery(model=self.dbModel, query=self.dbModel.query, reqDict=reqDict)
        # Check if record ID is none
        elif rec_id is None:
            # No record ID given, return all records
            query = self.dbModel.query
        # Return specific record
        else:
            # Filter by record ID and idField given
            query = self.dbModel.query.filter((getattr(self.dbModel, self.idField)) == rec_id)
        # Get results of query and serialize them into json response
        return self.formatMultiResponse(query)

    def postData(self, model, content):
        """
        Converts POST data into a create/insert call on the database. Each key in the content dictionary is checked
        against the model before being used to set attributes.
        @param model:
        @param content: Dict.
        @return: HTTP Response 201.
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

    def post(self):
        """
        POST request view, inserts the requested part install record into the database.
        @return: Response Code
        """
        # content = request.get_json(force=True)
        # logger.debug(content)
        # Test SQLAthanor de-serialization:
        # Turn request JSON dict into a model, drop extra keys
        deSerialModel = self.dbModel.new_from_dict(request.get_json(),
                                                       error_on_extra_keys = False,
                                                       drop_extra_keys = True)
        # Iterate over request dict keys and values
        # for key, value in content.items(content):
        #     # Check if object has an attribute matching the content update key
        #     if hasattr(self.dbModel(), key):
        #         # Set the object attribute value based on the key:value pair, this allows for updating only
        #         # certain values within the object
        #         setattr(self.dbModel(), key, value)
        # db.session.add(self.dbModel())
        db.session.add(deSerialModel)
        # Commit updates to database
        db.session.commit()
        logger.debug(f"Added a new record to {self.dbModel}: \n {deSerialModel.to_dict()}")
        return Response(status=201)

    def delete(self, rec_id):
        """
        Delete request view, allows deleting a single record.
        @param rec_id: Int. Asset record to be returned
        @return: Response Code.
        """
        if rec_id:
            self.dbModel.query.filter_by(id=rec_id).delete()
        else:
            return Response(status=404)

    def put(self, rec_id):
        """
        Executes an UPDATE request on the input SQLAlchemy Model.

        @param rec_id: Int. Record to be updated.
        @return: Response code.
        """
        # Get content
        content = request.get_json(force=True)
        # Query record
        query = self.model.query.filter_by(id=rec_id).first()
        # Check if any records match
        if query:
            # Iterate over request dict keys and values
            for key, value in content.items():
                # Check if object has an attribute matching the content update key
                if hasattr(query, key):
                    # Set the object attribute value based on the key:value pair, this allows for updating only
                    # certain values within the object
                    setattr(query, key, value)
            # Commit updates to database
            db.session.commit()
            return Response(status=200)
        # Resource not found
        else:
            return Response(status=404)

##TODO build out API to add/edit after market part/accessory installs
class PartInstallRecAPI(apiMethod):
    """
    API for CRUD operations on aftermarket part install information.
    """
    model = models.installs
    idField = 'id'

    # def post(self):
    #     """
    #     POST request view, inserts the requested part install record into the database.
    #     @return: Response Code
    #     """
    #     content = request.get_json(force=True)
    #     # Check if assetFK matches an existing asset
    #     asset = models.Asset.query.filter_by(id=content['assetfk']).first()
    #     # check if maintFK matches an existing maintenance record
    #     maintRec = models.maintRecord.query.filter_by(id=content['maintfk']).first()
    #     if asset and maintRec:
    #         # Create part install record
    #         return self.postData(self.model, content)
    #     else:
    #         # Asset or maintrec dont exist, return 404
    #         return Response(status=404)

class MaintRecAPI(apiMethod):
    """
    API class
    """
    model = models.maintRecord
    idField = 'id'

    # def post(self):
    #     """
    #     POST request view, inserts the requested maintenance record into the database.
    #     @return: Response Code
    #     """
    #     content = request.get_json(force=True)
    #     # Check if assetFK matches an existing asset
    #     asset = models.Asset.query.filter_by(id=content['assetfk']).first()
    #     if asset:
    #         # Create maintenance record
    #         return self.postData(self.model, content)
    #     else:
    #         # Asset doesn't exist, return 404
    #         return Response(status=404)


class AssetRecAPI(apiMethod):
    """
    API for CRUD operations on asset information.
    """
    model = models.Asset
    idField = 'id'

    # def post(self):
    #     """
    #     POST request view, inserts the requested asset record into the database.
    #     @return: Response Code
    #     """
    #     content = request.get_json()
    #     # logger.debug(f"{request.path} Received post request: {content}")
    #     # Get ownerfk
    #     ownerFK = models.Owner.query.filter_by(username=content['username']).first()
    #     if ownerFK:
    #         # Add fk to content Dict
    #         content['ownerfk'] = ownerFK.id
    #         return self.postData(self.model, content)
    #     else:
    #         return Response(status=404)


##TODO build out API to query Strava for distance ridden since maintenance/part install

