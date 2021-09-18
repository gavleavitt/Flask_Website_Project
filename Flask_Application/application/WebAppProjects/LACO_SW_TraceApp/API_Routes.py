from flask import Blueprint, request, jsonify, Response, make_response
from application import application, Session, db
import geojson
from geojson import Feature, FeatureCollection, MultiLineString, Point
from application.WebAppProjects.LACO_SW_TraceApp import DomainLookUps
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
    returnType = request.args.get("returnType")
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
    # Raw sql statement, used since PG_Routing doesnt have SQLAlchemy ORM support
    sql = ("""
SELECT 
	node.id as id, node.the_geom as geom, GeometryType(node.the_geom) as geomtype
INTO TEMP TABLE sp
FROM
	storm_network_vertices_pgr as node
WHERE
	st_intersects(ST_Snap(ST_Transform(ST_SetSRID(ST_Point(:lon, :lat), 4326),2229),node.the_geom, 100), node.the_geom)
ORDER BY 
	node.the_geom <-> ST_Transform(ST_SetSRID(ST_Point(:lon, :lat), 4326),2229)
LIMIT 1;

SELECT sp.id, nodes.*  INTO TEMP TABLE traceresults from sp, pgr_drivingDistance(
        :directionSQL,
        sp.id, 999999, true) AS nodes;
		
SELECT
	mh.uuid, st_asgeojson(st_transform(mh.geom, 4326)) as geojson, mh.factype as factype,  tr.cost as cost, "DWGNO" as dwgno, NULL as size, "JHSRC" as facid, CAST("MATERIAL" as text) as material, CAST("STND_PLAN" as text) as subtype, GeometryType(mh.geom) as geomtype
FROM 
	maintenanceholes mh, traceresults as tr
WHERE
	(mh.node_fk = tr.node)
UNION
select 
	i.uuid, st_asgeojson(st_transform(i.geom, 4326)) as geojson, i.factype as factype, tr.cost as cost, dwgno, NULL as size, eqnum as facid, NULL as material, CAST(stnd_plan as text) as subtype, GeometryType(i.geom) as geomtype
FROM 
	inlets i, traceresults as tr
WHERE
	(i.node_fk = tr.node)
UNION
select 
	ol.uuid, st_asgeojson(st_transform(ol.geom, 4326)) as geojson, ol.factype as factype, tr.cost as cost, dwgno, CAST(diameter_h as text) as size, outfall_id as facid, CAST(material as text) as material, CAST(cross_sect as text) as subtype, GeometryType(ol.geom) as geomtype 
FROM 
	outlets ol, traceresults as tr
WHERE
	(ol.node_fk = tr.node)
UNION
SELECT
	gm.uuid, st_asgeojson(st_transform(gm.geom, 4326)) as geojson, gm.factype as factype,  tr.cost as cost, NULL as dwgno, CAST(diameter_h as text) as size, eqnum as facid,CAST(material as text) as material, CAST(subtype as text) as subtype, GeometryType(gm.geom) as geomtype
FROM 
	gravitymainssplit gm, traceresults as tr
WHERE
	(gm.edge_fk = tr.edge)
UNION
SELECT
	l.uuid, st_asgeojson(st_transform(l.geom, 4326)) as geojson, l.factype as factype,  tr.cost as cost, "DWGNO" as dwgno, CAST("DIAMETER_H" as text) as size, "JHSRC" as facid, CAST("MATERIAL" as text) as material, CAST("SUBTYPE" as text) as subtype, GeometryType(l.geom) as geomtype  
FROM 
	laterals l, traceresults as tr
WHERE
	(l.edge_fk = tr.edge)
UNION
SELECT
	NULL as uuid, st_asgeojson(st_transform(sp.geom, 4326)) as geojson, 'startpoint' as factype,  '0' as cost, NULL as dwgno, NULL as size, NULL as facid, NULL as material, NULL as subtype, GeometryType(sp.geom) as geomtype
FROM
	sp
    """)

    # Lists to hold results
    results = db.session.execute(sql, {"lat": lat, "lon": lon, "directionSQL": directionSQL})
    # if returnType == "geojson":
    resultDict = {'startpoint': None, "Inlets": [], "Outlets": [], "Maintenance Holes": [], "Gravity Mains": [],
                  "Laterals": []}
    # Execute raw SQL query with parameters

    startpoint = None
    id = 1
    for i in results:
        # Load st_asgeojson query results as geojson data
        geojsonGeom = geojson.loads(i.geojson)
        # Populate properties for each feature
        propDict = {}
        propDict['factype'] = i.factype
        if i.size:
            propDict['size'] = i.size
        else:
            propDict['size'] = "Unknown"
        propDict['dwgno'] = i.dwgno
        if i.dwgno:
            propDict['dwgno'] = i.dwgno
        else:
            propDict['dwgno'] = "Unknown"
        # if i.material:
        #     propDict['material'] = i.material
        # else:
        #     propDict['material'] = "Unknown"
        propDict['id'] = id
        if not i.facid:
            propDict['facid'] = "Unknown"
        else:
            propDict['facid'] = i.facid
        propDict['linearpipefeetfromstart'] = i.cost
        propDict['uuid'] = i.uuid
        propDict['facsubtype'] = "Unknown"
        propDict['material'] = "Unknown"
        if i.factype == "Inlets":
            propDict['facsubtype'] = DomainLookUps.inletPlanLookUp(str(i.subtype))
            resultDict['Inlets'].append(Feature(geometry=Point(geojsonGeom), properties=propDict))
        elif i.factype == "Outlets":
            propDict['material'] = DomainLookUps.gravityMainsMaterialLookup(str(i.material))
            resultDict['Outlets'].append(Feature(geometry=Point(geojsonGeom), properties=propDict))
        elif i.factype == "Maintenance Holes":
            propDict['facsubtype'] = DomainLookUps.maintenanceHolePlanLookUp(str(i.subtype))
            resultDict['Maintenance Holes'].append(Feature(geometry=Point(geojsonGeom), properties=propDict))
        elif i.factype == "Gravity Mains":
            propDict['material'] = DomainLookUps.gravityMainsMaterialLookup(str(i.material))
            resultDict['Gravity Mains'].append(Feature(geometry=MultiLineString(geojsonGeom), properties=propDict))
        elif i.factype == "Laterals":
            propDict['material'] = DomainLookUps.gravityMainsMaterialLookup(str(i.material))
            resultDict['Laterals'].append(Feature(geometry=MultiLineString(geojsonGeom), properties=propDict))
        elif i.factype == "startpoint":
            startpoint = Feature(geometry=Point(geojsonGeom), properties=propDict)
            resultDict['startpoint'] = startpoint
        else:
            propDict['facsubtype'] = i.subtype
        id += 1
    # jsonify response

    response = jsonify({"startpoint": FeatureCollection(resultDict['startpoint']),
        "Inlets": FeatureCollection(resultDict["Inlets"]),
        "Outlets":FeatureCollection(resultDict["Outlets"]),
        "Maintenance Holes": FeatureCollection(resultDict["Maintenance Holes"]),
        "Gravity Mains": FeatureCollection(resultDict["Gravity Mains"]),
        "Laterals": FeatureCollection(resultDict["Laterals"])})
    # else:
    #     # write csv to memory as string
    #     csvObject = io.StringIO
    #     # Make csv writer
    #     csvWriter = csv.writer(csvObject)
    #     # write header row
    #     headerList = ["factype", "facsubtype", "facid", "material", "size", "dwgno", "uuid", "cost"]
    #     csvWriter.writerow(headerList)
    #     # write query results to csv
    #     for i in results:
    #         csvWriter.writerow([i.factype, i.facsubtype, i.facid,i.material, i.size, i.dwgno, i.uuid, i.cost])
    #     # See: https://stackoverflow.com/a/26998089
    #
    #
    #     #
    #     # cw.writerows(csvList)
    #     response = make_response(csvObject.getvalue())
    #     response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    #     response.headers["Content-type"] = "text/csv"
    # Add header to allow CORS
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response