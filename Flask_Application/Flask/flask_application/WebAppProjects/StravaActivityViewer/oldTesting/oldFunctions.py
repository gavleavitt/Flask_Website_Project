# from stravaio import strava_oauth2
# from stravaio import StravaIO
from stravalib.client import Client
from dotenv import load_dotenv
import requests
import os
import time
# load_dotenv()
#
# # strava_oauth2(client_id=os.getenv("STRAVA_CLIENT_ID"), client_secret=os.getenv("STRAVA_CLIENT_SECRET"))
# # client = StravaIO(access_token=os.getenv("STRAVA_ACCESS_TOKEN"))
# print("Running!")

#
# def simplifyandMaskAllActivities():
#     """
#     Calculate difference, keep only different sections
#     Do a separate query to select everything that didn't have an intersection with privacy areas.
#     Use collect to combine these datasets
#     create a new table with both datasets
#     remain activity ID throughout the process to be used for joining attribute data
#     Convert to UTM 10N 32610
#     Returns
#     -------
#     """
#     session = createSession()
#     print("creating queries")
#     # Simplify tolerence, in meters.
#     simplifyFactor = 12
#     proj = 32610
#     collectionInt = 2
#     # get all act IDs from original database
#     stravaIDs = session.query(strava_activities.actID)
#     allID = []
#     for i in stravaIDs:
#         allID.append(i.actID)
#     # Privacy geometries CTE
#     privateAOI = session.query(AOI.geom.label("priv_aoi")).filter(AOI.privacy == "Yes").cte("privacy_aoi")
#
#     # CTE query to query the geometries and act IDs of all records in original table
#     stravaSimp = session.query(strava_activities.geom.label("trans_geom"),
#                                (strava_activities.actID.label("strava_id"))).cte("simp_cte")
#
#     # Query first uses ST_Difference to split the linestrings by their intersections with the AOI polygons, I don't
#     # entirely understand what this function does since it doesn't appear to follow the official description of
#     # returning just geom B-A, it appears to return B-A and A. Next geom A is removed using a filter based on
#     # ST_Intersects, which removes geom A, including areas with no intersection with geom B, I don't understand why
#     # this combination of functions removes geom A that doesn't intersect geom B, however these data will be selected
#     # again later.
#     # Next the filtered data are transformed into UTM 10N (srid 32610) such that the data are in meters, not degrees,
#     # and passed into ST_SimplifyPreserveTopology. This smooths data within the smoothing tolerance without breaking
#     # any topology, the tolerance is in the geometry's units which makes more sense in meters. After smoothing the data
#     # are transformed back into WGS 1984 (srid 4326).
#     # Activity IDs are also queried to keep track of which records were used in this process
#     maskedQuery = session.query(stravaSimp.c.strava_id,
#                                 sqlfunc.ST_AsEWKB(sqlfunc.ST_CollectionExtract(sqlfunc.ST_MakeValid(sqlfunc.ST_Multi(
#                                     sqlfunc.ST_Transform(
#                                         sqlfunc.ST_Simplify(
#                                             sqlfunc.ST_Transform(
#                                                 sqlfunc.ST_Difference(
#                                                     stravaSimp.c.trans_geom, privateAOI.c.priv_aoi), proj),
#                                             simplifyFactor),
#                                         4326))), collectionInt))) \
#         .filter(sqlfunc.ST_Intersects(stravaSimp.c.trans_geom, privateAOI.c.priv_aoi))
#     allFeatures = []
#     differenceIds = []
#     print("Working on masked query")
#     for row in maskedQuery:
#         differenceIds.append(row.strava_id)
#         allFeatures.append([row[0], row[1]])
#         # geojson_geom = geojson.loads(row[1])
#         # features.append(Feature(geometry=geojson_geom))
#     # print(f"Len of differenceIDs list is {len(differenceIds)}")
#     # print(differenceIds)
#     nonIntersectQueryList = list(set(allID) - set(differenceIds))
#     # Query geoms in nonIntersectqueryList
#     print("Finished masked query, working on non-intersect query")
#     nonIntersectQuery = session.query(strava_activities.actID, sqlfunc.ST_AsEWKB(
#         (sqlfunc.ST_CollectionExtract(sqlfunc.ST_MakeValid(sqlfunc.ST_Multi(
#             sqlfunc.ST_Transform(sqlfunc.ST_SimplifyPreserveTopology(sqlfunc.ST_Transform(strava_activities.geom, proj),
#                                                                      simplifyFactor), 4326))), collectionInt)))).filter(
#         strava_activities.actID.in_(nonIntersectQueryList))
#     # print(nonIntersectQuery)
#     for row in nonIntersectQuery:
#         # print(f"working on non-intersecting actID {row[0]}")
#         # differenceIds.append(row.strava_id)
#         allFeatures.append([row[0], row[1]])
#
#     # print(f"Length of all feature list with all linestrings added is {len(allFeatures)}")
#     print("Non-intersect query complete, adding all features to session")
#     for item in allFeatures:
#         insert = strava_activities_masked(actID=item[0], geom=item[1])
#         session.add(insert)
#         # print(f"Activity {item[0]} has been added to session!")
#     print("All initial data added to session, committing!")
#     session.commit()
#     print("Checking for invalid geometries")
#     # invalidGeom = session.query(strava_activities_masked.actID, sqlfunc.ST_AsEWKB(strava_activities_masked.geom)). \
#     #     filter(sqlfunc.ST_IsValid(strava_activities_masked.geom) == 'false')
#     session.close()
#     print("All entries committed to database!")
#
#
# def findInvalid():
#     session = createSession()
#     collectionInt = 2
#     invalidGeom = session.query(strava_activities_masked.actID). \
#         filter(~sqlfunc.ST_IsValid(strava_activities_masked.geom))
#     invalidList = []
#     for i in invalidGeom:
#         invalidList.append(i.actID)
#     print(f"Invalid list is {invalidList}")
#     print(len(invalidList))
#
#
# def fixInvalid():
#     session = createSession()
#     collectionInt = 2
#     session.query(strava_activities_masked).filter(~sqlfunc.ST_IsValid(strava_activities_masked.geom)). \
#         update({strava_activities_masked.geom: sqlfunc.ST_CollectionExtract(sqlfunc.ST_MakeValid(
#         strava_activities_masked.geom), collectionInt)}, synchronize_session="fetch")
#     session.commit()
#     session.close()
#
# def maskandInsertAct(actId):
#     """
#
#     Parameters
#     ----------
#     actId
#
#     Returns
#     -------
#
#     """
#     session = createSession()
#     collectionInt = 2
#     # Simplfy tolerence, in meters.
#     simplifyFactor = 12
#     # Projection srid to use for simplify, UTM 10N
#     proj = 32610
#     # Privacy geometries CTE
#     privateAOI = session.query(AOI.geom.label("priv_aoi")).filter(AOI.privacy == "Yes").cte("privacy_aoi")
#
#     # CTE query to query the geometry of new actID
#     stravaGeom = session.query(strava_activities.geom.label("trans_geom"),
#                                (strava_activities.actID.label("strava_id"))).filter(
#         strava_activities.actID == actId).cte("simp_cte")
#
#     # Query first uses ST_Difference to split the linestrings by their intersections with the AOI polygons, I don't
#     # entirely understand what this function does since it doesn't appear to follow the official description of
#     # returning just geom B-A, it appears to return B-A and A. Next geom A is removed using a filter based on
#     # ST_Intersects, which removes geom A, including areas with no intersection with geom B, I don't understand why
#     # this combination of functions removes geom A that doesn't intersect geom B, however these data will be selected
#     # again later.
#     # Next the filtered data are transformed into UTM 10N (srid 32610) such that the data are in meters, not degrees,
#     # and passed into ST_SimplifyPreserveTopology. This smooths data within the smoothing tolerance without breaking
#     # any topology, the tolerance is in the geometry's units which makes more sense in meters. After smoothing the data
#     # are transformed back into WGS 1984 (srid 4326) then returned as EWKT to be inserted into new table.
#     maskedQuery = session.query(stravaGeom.c.strava_id, sqlfunc.ST_AsEWKT(sqlfunc.ST_Multi(sqlfunc.ST_Transform(
#         sqlfunc.ST_Simplify(
#             sqlfunc.ST_Transform(sqlfunc.ST_Difference(stravaGeom.c.trans_geom, privateAOI.c.priv_aoi), proj),
#             simplifyFactor), 4326)))).filter(sqlfunc.ST_Intersects(stravaGeom.c.trans_geom, privateAOI.c.priv_aoi))
#     # Iterate over masked query result, add results to Postgres, should only ever be 1 empty at a time
#     queryLen = 0
#     for row in maskedQuery:
#         insert = strava_activities_masked(actID=row[0], geom=row[1])
#         session.add(insert)
#         flask_application.logger.debug(f"Activity ID {row[0]} had an intersection with a privacy AOI, masked linestring has "
#                                  f"been added to session")
#         queryLen += 1
#     # Check if masked query returned anything, if return is empty then the activity didn't intersect a privacy zone
#     # Perform a separate query without ST_Difference or ST_Intersects
#     if queryLen == 0:
#         nonIntersectQuery = session.query(strava_activities.actID,
#                                           sqlfunc.ST_AsEWKT(sqlfunc.ST_Multi(sqlfunc.ST_Transform(
#                                               sqlfunc.ST_Simplify(
#                                                   sqlfunc.ST_Transform(strava_activities.geom, proj), simplifyFactor),
#                                               4326)))).filter(
#             strava_activities.actID == actId)
#         for row in nonIntersectQuery:
#             insert = strava_activities_masked(actID=row[0], geom=row[1])
#             session.add(insert)
#             flask_application.logger.debug(
#                 f"Activity ID {row[0]} had no intersections with a privacy AOI, linestring has been added to session")
#     session.commit()
#     session.close()
#     flask_application.logger.debug(
#         f"Activity ID {actId} has been committed to Postgres")
#
# def getStravaMaskedActTopoJSON(actLimit):
#     startTime = time.time()
#     session = createSession()
#     query = session.query(strava_activities_masked.geom,
#                           strava_activities.name,
#                           strava_activities.actID,
#                           strava_activities.type,
#                           strava_activities.distance,
#                           strava_activities.private,
#                           strava_activities.calories,
#                           strava_activities.start_date,
#                           strava_activities.elapsed_time,
#                           strava_activities.start_date_local,
#                           strava_activities.total_elevation_gain,
#                           strava_activities.average_speed,
#                           strava_activities.max_speed,
#                           strava_activities.type_extended,
#                           strava_gear.gear_name) \
#         .join(strava_activities_masked.act_rel) \
#         .join(strava_activities.gear_rel, isouter=True) \
#         .order_by(strava_activities.start_date.desc()) \
#         .limit(actLimit)
#     features = []
#     print("Iterating over query!")
#     for row in query:
#         # Build a dictionary of the attribute information
#         propDict = {"name": row.name, "actID": row.actID, "type": row.type, "distance": round(row.distance),
#                     "private": row.private, "calories": round(row.calories),
#                     "startDate": row.start_date_local.isoformat(),
#                     "elapsed_time": row.elapsed_time.seconds, "total_elevation_gain": round(row.total_elevation_gain),
#                     "average_speed": row.average_speed, "max_speed": row.max_speed, "gear_name": row.gear_name,
#                     "type_extended": row.type_extended}
#         shapelyGeom = to_shape(row[0])
#         test = mapping(shapelyGeom)
#         obj = Feature(geometry=test, properties=propDict)
#
#         # shapelyGeom = to_shape(row[0])
#         # # Take ST_AsGeoJSON() result and load as geojson object
#         # geojsonGeom = geojson.loads(row[0])
#         # # Build the feature and add to feature list
#         # # features.append(Feature(geometry=geojsonGeom, properties=propDict))
#         # shapelyObj = shape(geojsonGeom)
#         # shapelyObj.name = propDict['name']
#         # print(shapelyObj.name)
#         features.append(obj)
#     topo = tp.Topology(features, topology=False).to_json()
#     session.close()
#     # Build the feature collection result
#     feature_collection = FeatureCollection(features)
#     # print(f"Process took {time.time() - startTime} to finish!")
#     # topotest = tp.Topology(feature_collection, topology=False, prequantize=True)
#     # topo = tp.Topology(feature_collection)
#     # topo = tp.Topology(feature_collection, topology=False, prequantize=True).to_json()
#     # print(dir(topotest))
#     # print(topotest._invalid_geoms)
#     # print(topotest.options)
#     print(f"Process took {time.time() - startTime} to finish!")
#     return topo
#     # return feature_collection
#
# def processActivitiesPublic(recordID):
#     """
#
#     Parameters
#     ----------
#     recordID
#
#     Returns
#     -------
#
#     """
#     session = createSession()
#     # Is_Valid returns a multi-geometry result, regardless of input, set ST_CollectionExtract to extract linestrings, 2.
#     collectionInt = 2
#     simplifyFactor = 15
#     geometricProj = 32610
#     webSRID = 4326
#     gridSnap = 3
#     if recordID == "All":
#         privacyClipQuery = session.query(strava_activities.actID, sqlfunc.ST_AsEWKB(
#             sqlfunc.ST_MakeValid(
#                 sqlfunc.ST_Multi(
#                     sqlfunc.ST_Transform(
#                         sqlfunc.ST_Intersection(
#                             sqlfunc.ST_Simplify(
#                                 sqlfunc.ST_SnapToGrid(
#                                     sqlfunc.ST_Transform(strava_activities.geom, geometricProj), gridSnap),
#                                 simplifyFactor),
#                             sqlfunc.ST_Transform(privacy_clip_poly.geom, geometricProj)), webSRID)))))
#
#     # if recordID == "All":
#     #     privacyClipQuery = session.query(strava_activities.actID, sqlfunc.ST_AsEWKB(sqlfunc.ST_CollectionExtract(
#     #         sqlfunc.ST_MakeValid(
#     #             sqlfunc.ST_Multi(
#     #                 sqlfunc.ST_Transform(
#     #                     sqlfunc.ST_Intersection(
#     #                         sqlfunc.ST_Simplify(
#     #                             sqlfunc.ST_SnapToGrid(
#     #                                 sqlfunc.ST_Transform(strava_activities.geom, geometricProj), gridSnap),
#     #                             simplifyFactor),
#     #                         sqlfunc.ST_Transform(privacy_clip_poly.geom, geometricProj)), webSRID))), collectionInt)))
#     else:
#         privacyClipQuery = session.query(strava_activities.actID, sqlfunc.ST_AsEWKB(sqlfunc.ST_CollectionExtract(
#             sqlfunc.ST_MakeValid(
#                 sqlfunc.ST_Multi(
#                     sqlfunc.ST_Transform(
#                         sqlfunc.ST_Intersection(
#                             sqlfunc.ST_Simplify(
#                                 sqlfunc.ST_SnapToGrid(
#                                     sqlfunc.ST_Transform(strava_activities.geom, geometricProj), gridSnap),
#                                 simplifyFactor),
#                             sqlfunc.ST_Transform(privacy_clip_poly.geom, geometricProj)), webSRID))), collectionInt))) \
#             .filter(strava_activities.actID == recordID)
#     print("Processing query!")
#     for i in privacyClipQuery:
#         session.add(strava_activities_masked(actID=i[0], geom=i[1]))
#     print("Committing query!")
#     # session.commit()
#     print("All done!")
#     session.close()

# def getStravaPublicActTopoJSON(actLimit):
#     startTime = time.time()
#     session = createSession()
#     query = session.query(sqlfunc.ST_AsGeoJSON(strava_activities_masked.geom, 7),
#                           strava_activities.name,
#                           strava_activities.actID,
#                           strava_activities.type,
#                           strava_activities.distance,
#                           strava_activities.private,
#                           strava_activities.calories,
#                           strava_activities.start_date,
#                           strava_activities.elapsed_time,
#                           strava_activities.start_date_local,
#                           strava_activities.total_elevation_gain,
#                           strava_activities.average_speed,
#                           strava_activities.max_speed,
#                           strava_activities.type_extended,
#                           strava_gear.gear_name) \
#         .join(strava_activities_masked.act_rel) \
#         .join(strava_activities.gear_rel, isouter=True) \
#         .order_by(strava_activities.start_date.desc()) \
#         .limit(actLimit)
#     features = []
#     print("Iterating over query!")
#     for row in query:
#         # Build a dictionary of the attribute information
#         propDict = {"name": row.name, "actID": row.actID, "type": row.type, "distance": round(row.distance),
#                     "private": row.private, "calories": round(row.calories),
#                     "startDate": row.start_date_local.isoformat(),
#                     "elapsed_time": row.elapsed_time.seconds, "total_elevation_gain": round(row.total_elevation_gain),
#                     "average_speed": row.average_speed, "max_speed": row.max_speed, "gear_name": row.gear_name,
#                     "type_extended": row.type_extended}
#         # Take ST_AsGeoJSON() result and load as geojson object
#         geojsonGeom = geojson.loads(row[0])
#         # Build the feature and add to feature list
#         features.append(Feature(geometry=geojsonGeom, properties=propDict))
#     session.close()
#     # Build the feature collection result
#     feature_collection = FeatureCollection(features)
#     print(f"Process took {time.time() - startTime} to finish!")
#     # prequant = True makes it less than 1MB, but adds time!
#     topoResult = tp.Topology(feature_collection, topology=False, prequantize=True).to_json()
#     print(f"Process took {time.time() - startTime} to finish!")
#     return topoResult
#     # return feature_collection


# def getStravaMaskedActGeoJSON(actLimit):
#     startTime = time.time()
#     session = createSession()
#     query = session.query(sqlfunc.ST_AsGeoJSON(strava_activities_masked.geom, 5).label("geom"),
#                           strava_activities.name,
#                           strava_activities.actID,
#                           strava_activities.type,
#                           strava_activities.distance,
#                           strava_activities.private,
#                           strava_activities.calories,
#                           strava_activities.start_date,
#                           strava_activities.elapsed_time,
#                           strava_activities.start_date_local,
#                           strava_activities.total_elevation_gain,
#                           strava_activities.average_speed,
#                           strava_activities.max_speed,
#                           strava_activities.type_extended,
#                           strava_gear.gear_name) \
#         .join(strava_activities_masked.act_rel) \
#         .join(strava_activities.gear_rel, isouter=True) \
#         .order_by(strava_activities.start_date.desc()) \
#         .limit(actLimit)
#     features = []
#     print("Iterating over query!")
#     for row in query:
#         # Build a dictionary of the attribute information
#         propDict = {"name": row.name, "actID": row.actID, "type": row.type, "distance": round(row.distance),
#                     "private": row.private, "calories": round(row.calories),
#                     "startDate": row.start_date_local.isoformat(),
#                     "elapsed_time": row.elapsed_time.seconds, "total_elevation_gain": round(row.total_elevation_gain),
#                     "average_speed": row.average_speed, "max_speed": row.max_speed, "gear_name": row.gear_name,
#                     "type_extended": row.type_extended}
#         # Take ST_AsGeoJSON() result and load as geojson object
#         geojsonGeom = geojson.loads(row[0])
#         # Build the feature and add to feature list
#         features.append(Feature(geometry=geojsonGeom, properties=propDict))
#         # features.append(Feature(geometry=geojsonGeom))
#     session.close()
#     # Build the feature collection result
#     feature_collection = FeatureCollection(features)
#     # print(f"Process took {time.time() - startTime} to finish!")
#     print(f"Process took {time.time() - startTime} to finish!")
#     return feature_collection