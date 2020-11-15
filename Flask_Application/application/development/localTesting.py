from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func as sqlfunc
from ..projects.strava_activities.modelsStrava import strava_activities, strava_activities_masked
from ..script_config import dbcon

def createSession():
    engine = create_engine(dbcon)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def simplifyandMaskAllActivities():
    """


    Calculate difference, keep only different sections
    Do a separate query to select everything that didn't have an intersection with privacy areas.
    Use collect to combine these datasets
    create a new table with both datasets
    remain activity ID throughout the process to be used for joining attribute data
    Convert to UTM 10N 32610
    Returns
    -------
    """
    session = createSession()
    print("creating queries")
    # Simplify tolerence, in meters.
    simplify = 10
    proj = 32610
    # get all act IDs from original database
    stravaIDs = session.query(strava_activities.actID)
    allID = []
    for i in stravaIDs:
        allID.append(i.actID)
    # print(f"Length of all query is: {len(allID)}")
    # Privacy geometries CTE
    privateAOI = session.query(AOI.geom.label("priv_aoi")).filter(AOI.privacy == "Yes").cte("privacy_aoi")

    # CTE query to query the geometries and act IDs of all records in original table
    stravaSimp = session.query(strava_activities.geom.label("trans_geom"),
                               (strava_activities.actID.label("strava_id"))).cte("simp_cte")

    # Query first uses ST_Difference to split the linestrings by their intersections with the AOI polygons, I don't
    # entirely understand what this function does since it doesn't appear to follow the official description of
    # returning just geom B-A, it appears to return B-A and A. Next geom A is removed using a filter based on
    # ST_Intersects, which removes geom A, including areas with no intersection with geom B, I don't understand why
    # this combination of functions removes geom A that doesn't intersect geom B, however these data will be selected
    # again later.
    # Next the filtered data are transformed into UTM 10N (srid 32610) such that the data are in meters, not degrees,
    # and passed into ST_SimplifyPreserveTopology. This smooths data within the smoothing tolerance without breaking
    # any topology, the tolerance is in the geometry's units which makes more sense in meters. After smoothing the data
    # are transformed back into WGS 1984 (srid 4326).
    # Activity IDs are also queried to keep track of which records were used in this process
    maskedQuery = session.query(stravaSimp.c.strava_id,
                                sqlfunc.ST_AsEWKT(sqlfunc.ST_Multi(sqlfunc.ST_Transform(
                                    sqlfunc.ST_SimplifyPreserveTopology(sqlfunc.ST_Transform(sqlfunc.ST_Difference(
                                        stravaSimp.c.trans_geom, privateAOI.c.priv_aoi), proj), simplify), 4326)))) \
        .filter(sqlfunc.ST_Intersects(stravaSimp.c.trans_geom, privateAOI.c.priv_aoi))
    allFeatures = []
    differenceIds = []
    print("Working on masked query")
    for row in maskedQuery:
        # print(f"working on {row[0]}")
        differenceIds.append(row.strava_id)
        allFeatures.append([row[0], row[1]])
        # geojson_geom = geojson.loads(row[1])
        # features.append(Feature(geometry=geojson_geom))
    # print(f"Len of differenceIDs list is {len(differenceIds)}")
    # print(differenceIds)
    nonIntersectQueryList = list(set(allID) - set(differenceIds))
    # print(f"Length of non-intersecting list is {len(nonIntersectqueryList)}")
    # print(nonIntersectqueryList)
    # print(queryList)
    # print(f"Length of all feature list with only intersecting linestrings is {len(allFeatures)}")
    # Query geoms in nonIntersectqueryList
    print("Finished masked query, working on non-intersect query")
    nonIntersectQuery = session.query(strava_activities.actID, sqlfunc.ST_AsEWKT(sqlfunc.ST_Multi(sqlfunc.ST_Transform(
        sqlfunc.ST_SimplifyPreserveTopology(sqlfunc.ST_Transform(strava_activities.geom, proj), simplify),
        4326)))).filter(
        strava_activities.actID.in_(nonIntersectQueryList))
    # print(nonIntersectQuery)
    for row in nonIntersectQuery:
        # print(f"working on non-intersecting actID {row[0]}")
        # differenceIds.append(row.strava_id)
        allFeatures.append([row[0], row[1]])

    # print(f"Length of all feature list with all linestrings added is {len(allFeatures)}")
    print("Non-intersect query complete, adding all features to session")
    for item in allFeatures:
        # print(type(item[1]))
        # print(len(item[1]))
        # print(item[1])
        # print(f"working on {item[0]}")
        insert = strava_activities_masked(actID=item[0], geom=item[1])
        session.add(insert)
        # print(f"Activity {item[0]} has been added to session!")
    print("All sessions added, committing!")
    session.commit()
    session.close()
    print("All entries committed to database!")
