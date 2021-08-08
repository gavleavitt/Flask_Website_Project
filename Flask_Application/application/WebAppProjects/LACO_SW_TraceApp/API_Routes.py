from flask import Blueprint, request, jsonify, Response
from application import application, Session, db
import geojson
from geojson import Feature, FeatureCollection, MultiLineString, Point

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
    coords = {"lat":lat, "lon":lon}
    coord = f"{lat},{lon}"
    application.logger.debug(f"Lat,lon: {lat},{lon}")
    upstreamSQL = "'SELECT id, source, target, -1 as cost, reverse_cost FROM storm_network'"
    downstreamSQL = "'SELECT id, source, target, cost, -1 as reverse_cost FROM storm_network'"
    if str(request.args.get("direction")) == "upstream":
        directionSQL = upstreamSQL
    elif str(request.args.get("direction")) == "downstream":
        directionSQL = downstreamSQL
    else:
        return Response(status=400)
    # Raw sql statment, used since PG_Routing doesnt have SQLAlchemy ORM support
    sql = ("""
    -- Snap input coordinates to nearest network node
with sc AS (
	SELECT
		node.id as id, node.the_geom as geom
	from 
		storm_network_vertices_pgr as node
	where
		st_intersects(ST_Snap(ST_Transform(ST_SetSRID( ST_Point(:coord), 4326),2226),node.the_geom, 100), node.the_geom)
	ORDER BY 
		node.the_geom <-> ST_Transform(ST_SetSRID( ST_Point(:cord), 4326),2226)
	LIMIT 1
)
SELECT sc.id, i.uuid as inlet_uuid, ST_AsGeoJSON(i.geom) as inletgeom, mh.uuid as mh_uuid, ST_AsGeoJSON(mh.geom) as mhgeom,
ol.uuid as outlet_uuid, ST_AsGeoJSON(ol.geom) as outletgeom,
lat.uuid as lat_uuid, ST_AsGeoJSON(lat.geom) as latgeom, gm.uuid as gm_uuid, ST_AsGeoJSON(gm.geom) as gmgeom,
fm.uuid as fm_uuid, ST_AsGeoJSON(fm.geom) as fmgeom,
nodes.* FROM sc, pgr_drivingDistance(
        :directionSQL,
        sc.id, 999999, true) AS nodes
LEFT join 
	storm_network as sn
ON 
	(nodes.edge = sn.id)
LEFT join
	inlets i
ON 
	(nodes.node = i.node_fk)
LEFT join
	maintenanceholes mh
ON 
	(nodes.node = mh.node_fk)
LEFT join
	outlets ol
ON 
	(nodes.node = ol.node_fk)
LEFT join
	laterals lat 
ON 
	(sn.uuid = lat.uuid)
LEFT join
	gravitymainssplit gm
on
	(sn.uuid = gm.uuid)
LEFT join
	forced_mains fm
on
	(sn.uuid = fm.uuid)
    """)

    # Lists to hold point and line results
    pointfeatures = []
    linefeatures =[]
    results = db.session.execute(sql, {"coord": coord, "direction":directionSQL})
    startpoint = None
    for i in results:
        propDict = {}
        if i.cost == 0.0:
            # The snapped point will have a cost of 0 and all geoms will be null besides startgeom
            propDict['type'] = "start"
            geom = i.startgeom
            geojsonGeom = geojson.loads(geom)
            startpoint = Feature(geometry=Point(geojsonGeom), properties=propDict)
            break
        if i.inletgeom or i.mhgeom or i.olgeom:
        # Record is a point feature, populate point features list
            if i.inletgeom:
                propDict['id'] = i.inlet_uuid
                propDict['type'] = "inlet"
                geom = i.inletgeom
            elif i.mhgeom:
                propDict['id'] = i.mh_uuid
                propDict['type'] = "manhole"
                geom = i.mhgeom
            elif i.olgeom:
                propDict['id'] = i.outlet_uuid
                propDict['type'] = "outlet"
                geom = i.outletgeom
            else:
                propDict = None
                geom = None
            propDict['cost'] = i.cost
            geojsonGeom = geojson.loads(geom)
            pointfeatures.append(Feature(geometry=Point(geojsonGeom), properties=propDict))
        # Populate line features, only one should always be populated
        if i.gmgeom:
            propDict['id'] = i.gm_uuid
            propDict['type'] = "gravitymain"
            geom = i.gmgeom
        elif i.latgeom:
            propDict['id'] = i.lat_uuid
            propDict['type'] = "lateral"
            geom = i.latgeom
        elif i.fmgeom:
            propDict['id'] = i.fm_uuid
            propDict['type'] = "forcedmain"
            geom = i.fmgeom
        else:
            propDict = None
            geom = None
        geojsonGeom = geojson.loads(geom)
        linefeatures.append(Feature(geometry=MultiLineString(geojsonGeom), properties=propDict))
    # Format json response, will have nested goejson data
    response = {"startpoint": startpoint, "lines": linefeatures, "points": pointfeatures}
    return reponse