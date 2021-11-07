from flask import Blueprint, request, jsonify, Response, make_response
from application import application, Session, db
import geojson
from geojson import Feature, FeatureCollection, MultiLineString, Point

from application.WebAppProjects.LACO_SW_TraceApp import QueryEsriRest
from application.WebAppProjects.LACO_SW_TraceApp import TraceSQLQueries
import io
import csv

lacoSWTraceapp_API_BP = Blueprint('lacoSWTraceapp_API_BP', __name__,
                        template_folder='templates',
                        static_folder='static')

@lacoSWTraceapp_API_BP.route("/lacostormwater", methods=['GET', 'POST'], subdomain='api')
def handletracerequest():
    # Get coordinates
    # Get lat, y
    lat = float(request.args.get("latitude"))
    # Get lon, x
    lon = float(request.args.get("longitude"))
    # Coordinates to use in SQL query, must be in x, y / lon, lat
    # Check if request included flow block coordinates
    if request.args.getlist("blocklnglats"):
        #  Get request as a list
        reqBlockList = request.args.getlist("blocklnglats")
        # Get edgeIDs nearest to the request coordinates
        edgeIDs = TraceSQLQueries.queryNearestEdges(reqBlockList)
        # application.logger.debug(edgeIDs)
        # Set both flow direction options, correct one will be used in request
        upstreamSQL = f'SELECT id, source, target, -1 as cost,' \
                      f'CASE WHEN id IN {edgeIDs} THEN -1 ELSE reverse_cost END as reverse_cost ' \
                      f'FROM storm_network'
        downstreamSQL = f'SELECT id, source, target, ' \
                        f'CASE WHEN id IN {edgeIDs} THEN -1 ELSE cost END as cost,' \
                        f'-1 as reverse_cost FROM storm_network'
    else:
        # Set both flow direction options, correct one will be used in request
        upstreamSQL = 'SELECT id, source, target, -1 as cost, reverse_cost FROM storm_network'
        downstreamSQL = 'SELECT id, source, target, cost, -1 as reverse_cost FROM storm_network'
    # Set direction SQL based on request parameters
    if str(request.args.get("direction")) == "upstream":
        directionSQL = upstreamSQL
    elif str(request.args.get("direction")) == "downstream":
        directionSQL = downstreamSQL
    else:
        return Response(status=400)
    # Get trace results as a dict
    TraceDict = TraceSQLQueries.TraceNetwork(lon, lat, directionSQL)
    # Create response dictionary
    responseDict = {"startpoint": FeatureCollection(TraceDict['startpoint']),
     "Inlets": FeatureCollection(TraceDict["Inlets"]),
     "Outlets": FeatureCollection(TraceDict["Outlets"]),
     "Maintenance Holes": FeatureCollection(TraceDict["Maintenance Holes"]),
     "Gravity Mains": FeatureCollection(TraceDict["Gravity Mains"]),
     "Laterals": FeatureCollection(TraceDict["Laterals"])}

    # Check if return parcel OIDs was selected
    if request.args.get('parcels') == "true":
        parcelsURL = "https://public.gis.lacounty.gov/public/rest/services/LACounty_Cache/LACounty_Parcel/MapServer/0"
        # buildings = "https://arcgis.gis.lacounty.gov/arcgis/rest/services/DRP/SMMNA_Resources_AGOL_Version/MapServer/177"
        # serviceRestURL = "https://arcgis.gis.lacounty.gov/arcgis/rest/services/DRP/SMMNA_Resources_AGOL_Version/MapServer/177"
        lnglats = []
        # Create a list of point lnglat coordinates from the inlet results
        for k in responseDict["Inlets"]['features']:
            lng = k['geometry']['coordinates'][0]
            lat = k['geometry']['coordinates'][1]
            lnglats.append([lng, lat])
        # Check if any lnglats were returned, if not skip getting subwatersheds
        if len(lnglats) > 0:
            # Get subwatersheds as geojson
            subWaterSheds = TraceSQLQueries.getSubWaterSheds(lnglats)
            # Get unioned/dissolved subwatershed boundary
            # unionGeom = TraceSQLQueries.getUnionedSubWaterSheds(lnglats)
            req = QueryEsriRest.featureServReq(parcelsURL, subWaterSheds, ['APN', 'SitusFullAddress', 'UseType', 'UseDescription'],
                                               "esriGeometryPolygon", "esriSpatialRelIntersects")
            # reqGeom = req.queryFeaturesGeoJSON()
            reqOIDs= req.queryFeaturesOIDs()
            # TODO: Consider querying landuse or zoning information for each building, add to building details
            responseDict["parcels"] = reqOIDs
            responseDict["subwatersheds"] = FeatureCollection(subWaterSheds)
    # Jsonify response
    response = jsonify(responseDict)
    # Add header to allow CORS
    response.headers.add('Access-Control-Allow-Origin', '*')
    # Return nested JSON response
    return response