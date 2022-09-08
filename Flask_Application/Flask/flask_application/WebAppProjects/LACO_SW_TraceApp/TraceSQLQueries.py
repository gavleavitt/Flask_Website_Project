import flask_application
from flask_application import db
import geojson
from geojson import Feature, Point, Polygon, FeatureCollection, MultiLineString
from flask_application.WebAppProjects.LACO_SW_TraceApp import DomainLookUps
from flask_application import lacotraceSes
from sqlalchemy import text

def getSubWaterSheds(lnglatList):
    latlngStr = ""
    length = len(lnglatList)
    # watershedLayer = "la_co_subwatersheds"
    watershedLayer = "subwatershedstrace"
    for c, i in enumerate(lnglatList):
        newPT = f"ST_Transform(ST_SetSRID(ST_Point({i[0]}, {i[1]}), 4326), 2229)"
        latlngStr += newPT
        if (c + 1) != length:
            latlngStr += ","
    sql =f"""
WITH pttcollect AS (SELECT ST_Collect(
		ARRAY[{latlngStr}]) AS geom)
SELECT
    ST_AsGeoJSON(st_transform(sw.geom, 4326)) AS geom, sw.val AS id
FROM
    {watershedLayer} AS sw, pttcollect AS pts
WHERE
    ST_Intersects(sw.geom, pts.geom)
    """
    # resultDict['Outlets'].append(Feature(geometry=Point(geojsonGeom), properties=propDict))
    resList = []
    # Query DB
    # results = db.session.execute(sql)
    with lacotraceSes() as session:
        results = session.execute(sql)
    for i in results:
        # Load postgres subwatershed geom query result into geojson format
        # resDict[i.id] = {}
        # resDict[i.id]['geom'] = geojson.loads(i.geom)
        # resDict[i.id]['watershed'] = i.watershed
        propDict = {"factype":"subwatersheds"}
        # flask_application.logger.debug(i.id)
        resList.append(Feature(geometry=Polygon(geojson.loads(i.geom)), properties=propDict))
    return resList

def getUnionedSubWaterSheds(lnglatList):
    latlngStr = ""
    length = len(lnglatList)
    watershedLayer = "subwatershedstrace"
    # Loop over list of inlet lon/lats building out a list of postgis points transformed into 2229
    for c, i in enumerate(lnglatList):
        newPT = f"ST_Transform(ST_SetSRID(ST_Point({i[0]}, {i[1]}), 4326), 2229)"
        latlngStr += newPT
        # If there is not another record add a comma
        if (c + 1) != length:
            latlngStr += ","
    sql =f"""
WITH pttcollect AS (SELECT ST_Collect(
		ARRAY[{latlngStr}]) AS geom)
SELECT
    ST_AsGeoJSON(st_union(st_transform(sw.geom, 4326))) AS geom
FROM
    {watershedLayer} AS sw, pttcollect AS pts
WHERE
    ST_Intersects(sw.geom, pts.geom)
    """
    # resDict = {}
    res = []
    # Query DB
    # results = db.session.execute(sql)
    with lacotraceSes() as session:
        results = session.execute(sql)
    # results = lacotraceSes.execute(sql)
    flask_application.logger.debug(f"Unioned suberwatersheds length is: {results.rowcount}")
    for i in results:
        res.append(geojson.loads(i.geom))
    return res
    # for c, i in enumerate(results):
    #     # Load postgres subwatershed geom query result into geojson format
    #     resDict[c] = {}
    #     resDict[c]['geom'] = geojson.loads(i.geom)
    #     # resDict[i.id]['watershed'] = i.watershed
    #     # flask_application.logger.debug(i.geom)
    # return resDict

def TraceNetwork(lon, lat, directionSQL):
    # Raw sql statement, used since PG_Routing doesnt have SQLAlchemy ORM support
    # flask_application.logger.debug(directionSQL)
    sql = ("""
    SELECT
    	node.id as id, node.the_geom as geom, GeometryType(node.the_geom) as geomtype
    INTO TEMP TABLE sp
    FROM
    	storm_network_vertices_pgr as node
    WHERE
    	st_intersects(ST_Snap(ST_Transform(ST_SetSRID(ST_Point(:lon, :lat), 4326),2229),node.the_geom, 500), node.the_geom)
    ORDER BY
    	node.the_geom <-> ST_Transform(ST_SetSRID(ST_Point(:lon, :lat), 4326),2229)
    LIMIT 1;

    SELECT sp.id, nodes.*  INTO TEMP TABLE traceresults from sp, pgr_drivingDistance(
            :directionSQL,
            sp.id, 999999, true) AS nodes;

    SELECT
    	mh.uuid, st_asgeojson(st_transform(mh.geom, 4326)) as geojson, mh.factype as factype,  tr.cost as cost, dwgno, NULL as size, facid as facid, CAST(material as text) as material, CAST(stnd_plan as text) as subtype, GeometryType(mh.geom) as geomtype
    FROM
    	maintenanceholes mh, traceresults as tr
    WHERE
    	(mh.node_fk = tr.node)
    UNION
    select
    	i.uuid, st_asgeojson(st_transform(i.geom, 4326)) as geojson, i.factype as factype, tr.cost as cost, dwgno, NULL as size, facid as facid, NULL as material, CAST(stnd_plan as text) as subtype, GeometryType(i.geom) as geomtype
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
    	gm.uuid, st_asgeojson(st_transform(gm.geom, 4326)) as geojson, gm.factype as factype,  tr.cost as cost, NULL as dwgno, CAST(diameter_h as text) as size, facid as facid,CAST(material as text) as material, CAST(subtype as text) as subtype, GeometryType(gm.geom) as geomtype
    FROM
    	gravitymains gm, traceresults as tr
    WHERE
    	(gm.edge_fk = tr.edge)
    UNION
    SELECT
    	l.uuid, st_asgeojson(st_transform(l.geom, 4326)) as geojson, l.factype as factype,  tr.cost as cost, dwgno, CAST(diameter_height as text) as size, facid as facid, CAST(material as text) as material, CAST(subtype as text) as subtype, GeometryType(l.geom) as geomtype
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
    # flask_application.logger.debug(sql)
    # Lists to hold results
    # results = db.session.execute(sql, {"lat": lat, "lon": lon, "directionSQL": directionSQL})
    # results = lacotraceSes.execute(sql, {"lat": lat, "lon": lon, "directionSQL": directionSQL})
    with lacotraceSes() as session:
        results = session.execute(sql, {"lat": lat, "lon": lon, "directionSQL": directionSQL})
    # if returnType == "geojson":
    resultDict = {'startpoint': [], "Inlets": [], "Outlets": [], "Maintenance Holes": [], "Gravity Mains": [],
                  "Laterals": []}
    # Execute raw SQL query with parameters

    # startpoint = None
    id = 1
    for i in results:
        # Load st_asgeojson query results as geojson data
        geojsonGeom = geojson.loads(i.geojson)
        # Populate properties for each feature
        propDict = {}
        propDict['factype'] = i.factype
        if i.size:
            propDict['size_in'] = i.size
        else:
            propDict['size_in'] = "Unknown"
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
        propDict['pipelength_ft'] = i.cost
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
            resultDict['startpoint'].append(Feature(geometry=Point(geojsonGeom), properties=propDict))
        else:
            propDict['facsubtype'] = i.subtype
        id += 1
    return resultDict

def queryNearestEdges(blockList):
    blockCords = []
    # Parse request to a list
    for i in blockList:
        # Convert request coordinates to floats as nested lists, convert to floats to help avoid injection
        blockCords.append([float(i.split(",")[0]), float(i.split(",")[1])])
    # flask_application.logger.debug(blockCords)
    # Issue postgis request to get edge IDs to give -1 cost, flagging them as impassable
    # See https://gis.stackexchange.com/questions/193023/pgrouting-how-to-temporarily-increase-some-edges-cost-without-affecting-concur
    # Format into SQL statement with a temp table
    # Create SQL expression to find nearest edges, build out expression in raw text
    nearestEdgeSQL = """
            CREATE TEMP TABLE pts(geom geometry);
            INSERT INTO pts VALUES
            """
    # Used to track if the block coordinate is the last in the list
    blockCount = len(blockCords) - 1
    for c, i in enumerate(blockCords):
        nearestEdgeSQL += f"\n(St_transform(ST_SetSRID(ST_Point({i[0]}, {i[1]}), 4326),2229))"
        if c < blockCount:
            # Add each block coordinate to SQL text as a VALUE
            nearestEdgeSQL += ","
        else:
            # Last line of temp table input
            nearestEdgeSQL += ";"
    nearestEdgeSQL += """
    SELECT
    	network.id AS edgeid,
    	ST_Distance(pts.geom, network.geom) AS dist
    from
    	pts
    CROSS JOIN LATERAL (
    	SELECT
    		storm_network.id,
    		storm_network.geom
    	FROM
    		storm_network
    	ORDER BY
    		storm_network.geom <-> pts.geom
    	LIMIT 1
    ) AS network
     """
    # flask_application.logger.debug(nearestEdgeSQL)
    # execute query to get nearest edge id for each input
    # edgeresults = db.session.execute(nearestEdgeSQL)
    with lacotraceSes() as session:
        edgeresults  = session.execute(nearestEdgeSQL)
    # edgeresults = lacotraceSes.execute(nearestEdgeSQL)
    #  Get results of query and build SQL expression of edgeIDs, (#,#,etc)
    edgeIDs = "("
    for i in edgeresults:
        edgeIDs += f"{i.edgeid},"
    # Remove trailing comma
    edgeIDs = edgeIDs[:-1]
    # close out expression
    edgeIDs += ")"
    return edgeIDs
