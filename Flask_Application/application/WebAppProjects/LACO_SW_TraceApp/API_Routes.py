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
    # Coordinates to use in SQL query, must be in x, y / lon, lat
    coord = (lon, lat)
    application.logger.debug(f"Lat,lon: {coord}")
    application.logger.debug(f"ST_Point({coord})")
    upstreamSQL = 'SELECT id, source, target, -1 as cost, reverse_cost FROM storm_network'
    downstreamSQL = 'SELECT id, source, target, cost, -1 as reverse_cost FROM storm_network'
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
		st_intersects(ST_Snap(ST_Transform(ST_SetSRID(ST_Point(:lon, :lat), 4326),2229),node.the_geom, 100), node.the_geom)
	ORDER BY 
		node.the_geom <-> ST_Transform(ST_SetSRID(ST_Point(:lon, :lat), 4326),2229)
	LIMIT 1
)
SELECT sc.id,  ST_AsGeoJSON(st_transform(sc.geom, 4326)) as startgeom, 
i.uuid as inlet_uuid, ST_AsGeoJSON(st_transform(i.geom, 4326)) as inletgeom, 
mh.uuid as mh_uuid, ST_AsGeoJSON(st_transform(mh.geom, 4326)) as mhgeom,
ol.uuid as outlet_uuid, ST_AsGeoJSON(st_transform(ol.geom, 4326)) as outletgeom,
lat.uuid as lat_uuid, ST_AsGeoJSON(st_transform(lat.geom, 4326)) as latgeom, 
gm.uuid as gm_uuid, ST_AsGeoJSON(st_transform(gm.geom, 4326)) as gmgeom,
fm.uuid as fm_uuid, ST_AsGeoJSON(st_transform(fm.geom, 4326)) as fmgeom,
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
    # Execute raw SQL query with parameters
    results = db.session.execute(sql, {"lat": lat, "lon": lon, "directionSQL":directionSQL})
    startpoint = None
    for i in results:
        application.logger.debug(i)
        # Dictionary to hold data for each loop
        propDict = {}
        application.logger.debug(propDict)
        if i.cost == 0.0:
            # The snapped point will have a cost of 0 and all geoms will be null besides startgeom
            # TODO: verify if this is correct, a point with a cost of 0.0 is also the first node
            propDict['factype'] = "start"
            geom = i.startgeom
            geojsonGeom = geojson.loads(geom)
            startpoint = Feature(geometry=Point(geojsonGeom), properties=propDict)
            # break
        if i.inletgeom or i.mhgeom or i.outletgeom:
            application.logger.debug("Non null point geom!")
            # Record is a point feature, populate point features list depending on which geometry is not null
            if i.inletgeom:
                application.logger.debug("Inlet!")
                propDict['id'] = i.inlet_uuid
                propDict['factype'] = "inlet"
                geom = i.inletgeom
            elif i.mhgeom:
                application.logger.debug("MH!")
                propDict['id'] = i.mh_uuid
                propDict['factype'] = "manhole"
                geom = i.mhgeom
            elif i.outletgeom:
                application.logger.debug("Outlet!")
                propDict['id'] = i.outlet_uuid
                propDict['factype'] = "outlet"
                geom = i.outletgeom
            else:
                propDict = None
                geom = None
            # Set the cost property, not currently used
            propDict['cost'] = i.cost
            # Load st_asgeojson result as a geojson object
            geojsonGeom = geojson.loads(geom)
            # Create a point feature using the geometry and properties, append to point features list
            application.logger.debug(propDict)
            pointfeatures.append(Feature(geometry=Point(geojsonGeom), properties=propDict))
        # Populate line features, only one should always be populated
        # A single record can have both a line and a point geom so these are not in a else statement with the prior
        # if statement.
        if i.gmgeom:
            propDict['id'] = i.gm_uuid
            propDict['factype'] = "gravitymain"
            geom = i.gmgeom
        elif i.latgeom:
            propDict['id'] = i.lat_uuid
            propDict['factype'] = "lateral"
            geom = i.latgeom
        elif i.fmgeom:
            propDict['id'] = i.fm_uuid
            propDict['factype'] = "forcedmain"
            geom = i.fmgeom
        else:
            break
            propDict = None
            geom = None
        geojsonGeom = geojson.loads(geom)
        linefeatures.append(Feature(geometry=MultiLineString(geojsonGeom), properties=propDict))
    # Format json response, will have nested goejson data
    lineCollection = FeatureCollection(linefeatures)
    pointsCollection = FeatureCollection(pointfeatures)
    response = jsonify({"startpoint": startpoint, "lines": lineCollection, "points": pointsCollection})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response