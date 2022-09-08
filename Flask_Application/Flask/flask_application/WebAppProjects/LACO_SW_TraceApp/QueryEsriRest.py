import requests
import geojson
from geojson import FeatureCollection
import json
from flask_application import application
from arcgis2geojson import arcgis2geojson
import time
import sys
from fileinput import FileInput

class featureServReq:
    """

    """
    def __init__(self, baseurl, geojson, fields, esriInputGeomType, relationship):
        # Map/Feature server baseurl
        self.baseurl = baseurl
        # server query url
        self.queryUrl = baseurl + "/query"
        # Set input geometry type
        self.type = esriInputGeomType
        # Set selection type
        self.rel = relationship
        # Set input and output spatial references
        self.inSR = 4326
        self.outSR = 4326
        # Set output geometry format, some REST servers error out if geojson is used, use json instead
        self.outGeom = "json"
        self.spatialRef = relationship
        # Set output fields as a comma separated string
        self.outFields = ",".join(fields)
        # self.outFields = "*"
        # Set request to return geometry
        self.returnGeom = "true"
        # Set geosjon formatted data, this attribute is not used in the request
        self.geojson = geojson
        # build esri geometry for request
        self.queryGeom = self.buildEsriPolygon(self.geojson)
        # SQL where clause to return all, not sure if actually needed
        self.where = "1=1"
        # Get max record limit of the server
        self.limit = self.getFeatureLimit()

    def handlePagination(self, resDict, params):
        """

        @param resDict:
        @param params: Dict. Request parameters
        @return: Nested dict with pagination offset as keys and json response (dict) as values
        """
        # Result limit, updated if additional queries are needed
        resLimit = 0
        # Check if additional records, 'exceededTransferLimit' will be in keys if results longer than 1000
        while 'exceededTransferLimit' in resDict[resLimit].keys():
             # Increment result limit by server response record limit
            resLimit += self.limit
            # flask_application.logger.debug(f"Querying using resLimit {resLimit}")
            # Add record offset to query the next batch of records
            params['resultOffset'] = resLimit + 1
            # flask_application.logger.debug(f"Querying additional results with an offset of {params['resultOffset']}")
            # Issue query with offset applied
            resp = requests.post(self.queryUrl, data=params)
            # Add additional results to object
            resDict[resLimit] = json.loads(resp.text)
            # Check if result length is less than limit, if so stop querying and return result
            # The 'exceededTransferLimit' response will always be true if more than 1000 results can be returned,
            # even if on last pagination result
            if len(resDict[resLimit]) < resLimit:
                return resDict

    def buildEsriPolygon(self, geojsonFeats):
        """
        Takes input list of geojson polygons and converts them into esri polygon geometry. The returned JSON string dump
        can be used to query a ESRI Feature Server REST API.

        @param geojsonFeats: List of geojson polygon formatted objects
        @return: JSON string of formatted esripolygon
        """
        # esri polygon request format to be populated
        esriPolygon = {"hasZ": "false", "hasM": "false", "rings":[], "spatialReference": 4326}
        # Loop over geojson list
        for i in geojsonFeats:
            # geojson has one nested list, esri geometry doesnt follow this specification, drill in 1 list
            esriPolygon["rings"].append(i["geometry"]["coordinates"][0])
        # Dump dict into json formatted string
        return json.dumps(esriPolygon)

    def getFeatureLimit(self):
        """
        Gets server request limit, this value is used for handling pagination.
        @return: Int. Server record limit
        """
        # Add json result format to parameters
        params = {"f": "json"}
        # Get feature limit
        respJSON = requests.get(self.baseurl, params).json()
        # Extract and return max record count
        return int(respJSON['maxRecordCount'])

    def combineFeatureCollections(self, dict):
        # Check if dict is 1 entry, if so no formatting required
        if len(dict.keys()) == 1:
            return dict[0]
        else:
            featureList = []
            # Iterate over each feature collection object
            for i in dict.keys():
                # iterate over each feature in collection
                for k in dict[i]['features']:
                    # Create geojson feature for entry
                    featureList.append(k)
            # Return a feature collection
            return FeatureCollection(featureList)

    def queryFeaturesGeoJSON(self):
        resJSON = self.queryFeaturesJSON()
        # Convert Esri JSON results to geojson
        resGeoJSON = {}
        for k in resJSON.keys():
            # Convert esri JSON to raw, string, geojson
            rawGeo = arcgis2geojson(resJSON[k])
            resGeoJSON[k] = rawGeo
        return self.combineFeatureCollections(resGeoJSON)

    def queryFeaturesJSON(self):

        #  Set query parameters
        params = {
            "geometryType": self.type,
            "geometry": self.queryGeom,
            "inSR": self.inSR,
            "spatialRel": self.spatialRef,
            "returnGeometry": self.returnGeom,
            "outFields": self.outFields,
            "outSR": self.outSR,
            "returnTrueCurves": "false",
            # "Where": self.where,
            "f": self.outGeom
        }
        # Issue POST request, POST is used instead of GET since GET has an argument limit and POST doesn't
        resp = requests.post(self.queryUrl, data=params)
        # Build dict to hold request results
        resJSON = {}
        # Load result json response
        resJSON[0] = json.loads(resp.text)
        # Handle additional results, if any
        resJSON = self.handlePagination(resJSON, params)
        # Return results
        return resJSON

    def queryFeaturesOIDs(self):
        # Set parameters for query
        params = {
            "geometryType": self.type,
            "returnIdsOnly": "true",
            "geometry": self.queryGeom,
            "inSR": self.inSR,
            "spatialRel": self.spatialRef,
            # "returnGeometry": "false",
            # "outFields": self.outFields,
            # "outSR": self.outSR,
            "f": self.outGeom
        }
        # Send POST request, use in place of GET due to size of request
        resp = requests.post(self.queryUrl, data=params)
        # Convert response to text
        resJSON = json.loads(resp.text)
        # Extract objectIDs from request and return
        return resJSON['objectIds']