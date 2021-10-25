import requests
import geojson
from geojson import FeatureCollection
import json
from application import application
from arcgis2geojson import arcgis2geojson
import time
class featureServReq:
    def __init__(self, baseurl, geojson, fields, esriInputGeomType, relationship):
        self.baseurl = baseurl
        self.queryUrl = baseurl + "/query"
        self.type = esriInputGeomType
        self.rel = relationship
        self.inSR = 4326
        self.outSR = 4326
        self.outGeom = "json"
        self.spatialRef = relationship
        self.outFields = ",".join(fields)
        # self.outFields = "*"
        self.returnGeom = "true"
        self.geojson = geojson
        self.queryGeom = self.buildEsriPolygon(self.geojson)
        self.where = "1=1"
        # Get max record limit of the server
        self.limit = self.getFeatureLimit()

    def handlePagination(self, resDict, params):
        # Result limit, updated if additional queries are needed
        resLimit = 0
        # Check if additional records, 'exceededTransferLimit' will be in keys if results longer than 1000
        while 'exceededTransferLimit' in resDict[resLimit].keys():
             # Increment result limit by server response record limit
            resLimit += self.limit
            application.logger.debug(f"Querying using resLimit {resLimit}")
            # Add record offset to query the next batch of records
            params['resultOffset'] = resLimit + 1
            application.logger.debug(f"Querying additional results with an offset of {params['resultOffset']}")
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
        esriPolygon = {"hasZ": "false", "hasM": "false", "rings": [[]], "spatialReference": 4326}
        # Drill into geojson data and build out esripolygon geometry dict
        # Loop over every feature in collection
        # application.logger.debug(geojsonFeats)
        for k in geojsonFeats.keys():
            # application.logger.debug(geojsonFeats[k]['geom'])
            for i in geojsonFeats[k]['geom']['coordinates'][0]:
                esriPolygon["rings"][0].append(i)
        # application.logger.debug(esriPolygon)
        application.logger.debug(len(esriPolygon['rings']))
        # Convert esriPolygon dict to json format
        return json.dumps(esriPolygon)

    def getFeatureLimit(self):
        # Get feature limit
        params = {"f": "json"}
        respJSON = requests.get(self.baseurl, params).json()
        return respJSON['maxRecordCount']

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
            # Load as geojson object
            # resGeoJSON[k] = geojson.loads(rawGeo)
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
        # Issue GET request
        # resp = requests.get(self.queryUrl, params=params)
        # Issue POST request, POST is used instead of GET since GET has an argument limit and POST doesn't
        resp = requests.post(self.queryUrl, data=params)
        # Build dict to hold request results
        resJSON = {}
        # Load result json response
        resJSON[0] = json.loads(resp.text)
        # Get count of results
        # application.logger.debug(len(resJSON[resLimit]['features']))
        # Handle additional results, if any
        resJSON = self.handlePagination(resJSON, params)
        # return geojson formatted feature collection
        # return self.combineFeatureCollections(resJSON)
        return resJSON

    def queryFeaturesOIDs(self):
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
        resp = requests.post(self.queryUrl, data=params)
        resJSON = json.loads(resp.text)
        # application.logger.debug(resJSON)
        return resJSON['objectIds']