#
#     # private_aoi = session.query(AOI.geom).filter(AOI.privacy == "Yes").subquery()
#     # query = session.query(sqlfunc.ST_Difference(strava_activities.geom, private_aoi)).order_by(strava_activities.id.desc()).limit(actLimit)
#     # query = session.query(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom))
#
#
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom)), strava_activities).order_by(strava_activities.id.desc()).limit(5)
#     # query = session.query(strava_activities).filter(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom)).limit(20).all()
#     # query = session.query(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom)).filter(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom)).limit(
#     #     20).all()
#
#     # query = session.query(sqlfunc.ST_AsEWKT(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom))).limit(20)
#     # query = session.query(sqlfunc.ST_AsEWKT(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom))).limit(20)
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom))).limit(20)
#     # strava_act = session.query(strava_activities.geom).limit(20).subquery()
#     # query = session.query(sqlfunc.ST_Intersection(strava_act, AOI.geom))
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom))).filter(
#     #     sqlfunc.ST_Disjoint(strava_activities.geom, AOI.geom)).limit(20)
#
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom))).filter(
#     #     sqlfunc.ST_Overlaps(strava_activities.geom, AOI.geom)).limit(20)
#
#     # query = session.query(sqlfunc.ST_AsGeoJSON(strava_activities.geom)).filter(sqlfunc.ST_Disjoint(strava_activities.geom, AOI.geom)).limit(20)
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_activities.geom, query_ins))).limit(20)
#     # query = session.qeury()
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Multi(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom)))).limit(20)
#     # query_ins = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Intersection(strava_activities.geom, AOI.geom))).limit(20)
#     # query = session.qeury()
#     # query = session.query(sqlfunc.ST_AsText(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom))).limit(20)
#     # query = session.query(sqlfunc.ST_AsGeoJSON(strava_activities.geom), (sqlfunc.ST_Difference(strava_activities.geom, AOI.geom))).limit(20)
#     # query = session.query(sqlfunc.ST_AsGeoJSON(strava_activities.geom)).filter(strava_activities.geom == sqlfunc.ST_Difference(strava_activities.geom, AOI.geom)).limit(20)
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom))).limit(20)
#     # query = session.query(strava_activities).filter(sqlfunc.AsEWKB((sqlfunc.ST_Difference(strava_activities.geom, AOI.geom)))).limit(20)
#
#
#
#
# # on.query(strava_activities.geom.ST_Union().label("actunion")).order_by(strava_activities.id.desc()).limit(20).subquery()
#     # union = session.query(strava_activities.geom.ST_Union().label("actunion")).limit(20).subquery()
#     # query = session.query(sqlfunc.ST_AsGeoJSON(
#     #     sqlfunc.ST_Difference(union.c.actunion, AOI.geom)))
#     # for row in query:
#     #     print(row)
#
#
#     # # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(sqlfunc.ST_Union(strava_activities.geom), sqlfunc.ST_Union(AOI.geom)))).limit(30)
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom))).filter(
#     #     sqlfunc.ST_Intersects(strava_activities.geom, AOI.geom))
#     # strava_act = session.query(strava_activities.geom).order_by(strava_activities.id.desc()).limit(20).label("desc_act")
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Intersection(strava_act, private_aoi)))
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Intersection(strava_activities.geom, ((AOI.geom).filter((AOI.privacy == "Yes")))))).limit(20)
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Intersection(strava_activities.geom, AOI.geom)), AOI).filter(AOI.privacy == "Yes").limit(20)
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Intersection(strava_activities.geom, AOI.geom)))
#     # query = session.query(AOI.geom).join(private_aoi).filter()
#
#     #Selects the correct geoms!
#     # query = session.query(sqlfunc.ST_AsGeoJSON(AOI.geom)).filter(AOI.privacy == "Yes")
#
#
#     # for i in strava_act:
#     #     print(i)
#     # query = session.query(sqlfunc.ST_Difference(strava_activities.geom, AOI.geom)).limit(20)
#     # query = session.query(sqlfunc.ST_AsGeoJSON(AOI.geom))
#
#     # act_inters = session.query(sqlfunc.ST_AsText(sqlfunc.ST_Intersection(strava_lim.c.geom, private_aoi.c.geom))).cte("act_inters")
#     # print(f"!!! {act_inters}")
#     # print(dir(act_inters))
#     # print(dir(act_inters.c))
#     # print(act_inters.c.__str__)
#     # act_inters = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Intersection(strava_lim.c.geom, private_aoi.c.geom))).cte("act_inters")
#
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_lim.c.geom, sqlfunc.ST_GeomFromGeoJSON(act_inters.c))))
#
#
#     # query = session.query(sqlfunc.ST_Difference(strava_activities.geom, private_aoi),
#     #                       sqlfunc.ST_AsGeoJSON(strava_activities.geom),
#     #                       strava_activities).order_by(strava_activities.id.desc()).limit(actLimit)
#
#     # query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_activities.geom, private_aoi),
#     #                                            strava_activities)).order_by(strava_activities.id.desc()).limit(actLimit)
#
#     # sqlfunc.ST_Difference(strava_activities.geom, private_aoi),
#     #                   sqlfunc.ST_AsGeoJSON(strava_activities.geom),
#     #                   strava_activities).order_by(strava_activities.id.desc()).limit(actLimit)
#     # use https://postgis.net/docs/ST_Difference.html
#     # query = session.query(sqlfunc.ST_AsGeoJSON(strava_activities.geom),
#     #                       strava_activities).order_by(strava_activities.id.desc()).limit(actLimit)
#
#     # Issue GeoAlchemy queries
#
#     print("Issuing query!")
#     # privateAoi_Q = session.query(sqlfunc.ST_AsText(AOI.geom)).filter(AOI.privacy == "Yes")
#     # privateAoi_Q = session.query(AOI).filter(AOI.privacy == "Yes")
#     # privateAoi_Q = session.query(sqlfunc.ST_Collect(AOI.geom).label("collect")).filter(AOI.privacy == "Yes").one()
#     # stravaActs_Q = session.query(sqlfunc.ST_Collect(strava_activities.geom)).order_by(strava_activities.id.desc()).limit(20)
#     # privateAoi_Q = session.query(sqlfunc.ST_Collect(AOI.geom).label("collect")).filter(AOI.privacy == "Yes")
#     # privateAoi_Q = session.query(sqlfunc.ST_AsGEOJSON(AOI.geom)).filter(AOI.privacy == "Yes")
#     privateAoi_Q = session.query(AOI).filter(AOI.privacy == "Yes")
#     stravaActs_Q = session.query(strava_activities).order_by(strava_activities.id.desc()).limit(20)
#     # Covert to shapely shape object
#     print("Converting to shapely!")
#     # print(type(privateAoi_Q.geom))
#     featAoi = []
#     stravaAct = []
#     # print(dir(privateAoi_Q))
#     # featAoi = to_shape(privateAoi_Q.geom)
#     # for i in privateAoi_Q:
#     #     featAoi.append(to_shape(i.collect))
#     for i in privateAoi_Q:
#         featAoi.append(to_shape(i.geom))
#     for h in stravaActs_Q:
#         stravaAct.append(to_shape(h.geom))
#     # print(featAoi)
#     # print(stravaAct)
#     print("Converting activites to multi-line string")
#     multiAct = MultiLineString(stravaAct)
#     print("Performing union on AOI polygons")
#     multiAoi = cascaded_union(featAoi)
#     print("Calculating differences")
#     diff = multiAct.difference(multiAoi)
#     print("Differences calculated, loading into geojson")
#     test = geojson.loads(mapping(diff))
#     print(dir(test))
#
#
#
#     # Select everything that doesn't intersect a privacy POI polygon
#     # print(dir(private_aoi))
#     # return previously queried data, works!
#     # stravaReturn = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Transform(strava_simp.c.geom_simp, 4326)))
#
#     # print(dir(strava_simp.id))
#     # calc and return difference, which will drop activities that don't intersect the AOIs
#     # stravaReturn = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_simp.c.geom_simp, private_aoi.c.priv_aoi)), strava_activities.id).filter(
#     #     sqlfunc.ST_Intersects(strava_simp.c.geom_simp, private_aoi.c.priv_aoi))
#
#     # stravaReturn = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Transform(sqlfunc.coalesce(sqlfunc.ST_Difference(strava_simp.c.geom, private_aoi.c.priv_aoi)), 4326)), strava_activities.id).filter(
#     #     sqlfunc.ST_Intersects(strava_simp.c.geom, private_aoi.c.priv_aoi))
#     # strava_simp = session.query(sqlfunc.ST_SimplifyPreserveTopology(sqlfunc.ST_Transform(sqlfunc.ST_Collect(strava_activities.geom), 32610), 3).label("geom_simp"), strava_activities.id).group_by(strava_activities.id).limit(4)
#
#     # strava_simp = session.query(
#     #     sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Transform(sqlfunc.ST_SimplifyPreserveTopology(sqlfunc.ST_Transform(sqlfunc.ST_Collect(strava_activities.geom), 32610), 3), 4326))).limit(3)
#
#
#     # Returns 3 smoothed lines, try to get working with collect
#     # strava_simp = session.query(
#     #     sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Transform(sqlfunc.ST_SimplifyPreserveTopology(sqlfunc.ST_Transform(strava_activities.geom, 32610), 3), 4326)), strava_activities.id).limit(3)
#
#     # trying to get transformed geom out as labeled part of CTE
#     # strava_simp = session.query(
#     #     sqlfunc.ST_Transform(sqlfunc.ST_SimplifyPreserveTopology(sqlfunc.ST_Transform(strava_activities.geom, 32610), 3), 4326).label("trans_geom"),
#     #     strava_activities.id).limit(3).cte("simp_cte")
#     # takes previous and creates one multi-string with all geom
#     # stravaReturn = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Collect(strava_simp.c.trans_geom)))
#
#     # try to get diffence from strava_simp
#
#     # stravaDiff = session.query((strava_simp.c.strava_id).label("diff_id"),
#     #                            (sqlfunc.ST_Difference(strava_simp.c.trans_geom, private_aoi.c.priv_aoi)).label("strava_diff")).\
#     #     filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi)).cte("difference")
#     # stravaReturn = session.query(stravaDiff.c.strava_diff).join(stravaDiff.c.strava_diff, stravaDiff.c.diff_id != strava_simp.c.strava_id)
#
#     # Using case
#     # stravaReturn = session.query(strava_simp.c.strava_id, sqlfunc.ST_AsGeoJSON(
#     #     sqlfunc.ST_Transform(case([sqlfunc.ST_Difference(strava_simp.c.trans_geom, private_aoi.c.priv_aoi) == None, strava_simp.c.trans_geom]), 4326))).filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi))
#     #
#     # # private_aoi = session.query((sqlfunc.ST_Transform(AOI.geom, 32610)).filter(AOI.privacy == "Yes").label("priv_aoi")).cte("private_aoi")
#     # private_aoi = session.query(
#     #     sqlfunc.ST_Transform(AOI.geom, 32610).label("priv_aoi")).filter(AOI.privacy == "Yes").cte("privacy_aoi")
#     #
#     # strava_simp = session.query(
#     #     sqlfunc.ST_SimplifyPreserveTopology(sqlfunc.ST_Transform(strava_activities.geom, 32610), 3).label("trans_geom"),
#     #     (strava_activities.id).label("strava_id")).limit(5).cte("simp_cte")
#     # Returns everything, with geometries split at intersection
#     # stravaReturn = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Transform(sqlfunc.ST_Difference(strava_simp.c.trans_geom,private_aoi.c.priv_aoi), 4326)))
#
#     # Works!!!! However need to modify to also return things which don't intersect the AOI at all
#     # stravaReturn = session.query(sqlfunc.ST_AsGeoJSON(
#     #     sqlfunc.ST_Transform(sqlfunc.ST_Difference(strava_simp.c.trans_geom, private_aoi.c.priv_aoi), 4326))).filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi))
#     # # Works, missing data, but retain ID throughout!
#     # stravaReturn = session.query(strava_simp.c.strava_id, sqlfunc.ST_AsGeoJSON(
#     #     sqlfunc.ST_Transform(sqlfunc.ST_Difference(strava_simp.c.trans_geom, private_aoi.c.priv_aoi), 4326))).filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi))
#     #
#
#     # trying different methods
#     # stravaReturn = session.query(sqlfunc.ST_AsGeoJSON(
#     #     sqlfunc.ST_Transform(sqlfunc.Coalesce(sqlfunc.ST_Difference(strava_simp.c.trans_geom, private_aoi.c.priv_aoi), strava_simp.c.trans_geom), 4326))).filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi))
#     # stravaReturn = session.query(sqlfunc.ST_AsGeoJSON(
#     #     sqlfunc.ST_Transform((sqlfunc.ST_Difference(sqlfunc.Coalesce(strava_simp.c.trans_geom, strava_simp.c.trans_geom), private_aoi.c.priv_aoi)), 4326))).filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi))
#
#     # Works, missing data, but retain ID throughout!
#     # stravaReturn = session.query(strava_simp.c.strava_id, sqlfunc.ST_AsGeoJSON(
#     #     sqlfunc.ST_Transform(sqlfunc.ST_Difference(strava_simp.c.trans_geom, private_aoi.c.priv_aoi), 4326))).\
#     #     filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi))
#
#     # # Works, missing data, but retain ID throughout!
#     # stravaReturn = session.query(strava_simp.c.strava_id, sqlfunc.ST_AsGeoJSON(
#     #     sqlfunc.ST_Transform(sqlfunc.Coalesce(sqlfunc.ST_Difference(strava_simp.c.trans_geom, private_aoi.c.priv_aoi), strava_simp.c.trans_geom), 4326))).\
#     #     filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi))
#
#
#     # stravaReturn = session.query(strava_simp.c.strava_id, sqlfunc.ST_AsGeoJSON(
#     #     sqlfunc.ST_Transform(sqlfunc.ST_Difference(strava_simp.c.trans_geom, private_aoi.c.priv_aoi), 4326)))\
#     #     .filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi))
#
#     # try: https://gis.stackexchange.com/questions/250674/postgis-st-difference-similar-to-arcgis-erase
#     # try: https://gis.stackexchange.com/questions/187406/how-to-use-st-difference-and-st-intersection-in-case-of-multipolygons-postgis?rq=1
#     # stravaReturn = session.query(strava_simp.c.strava_id, sqlfunc.ST_AsGeoJSON(
#     #     sqlfunc.ST_Transform(sqlfunc.Coalesce(sqlfunc.ST_Difference(strava_simp.c.trans_geom, private_aoi.c.priv_aoi),strava_simp.c.trans_geom), 4326)))\
#     #     .filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi)).join(strava_simp, strava_activities.id)
#
#
#     # private_aoi = session.query((sqlfunc.ST_Transform(AOI.geom, 32610)).filter(AOI.privacy == "Yes").label("priv_aoi")).cte("private_aoi")
#     # private_aoi = session.query((AOI.geom).label("priv_aoi")).filter(AOI.privacy == "Yes").cte("privacy_aoi")
#     #
#     # strava_simp = session.query((strava_activities.geom).label("trans_geom"),
#     # (strava_activities.id.label("strava_id"))).limit(5).cte("simp_cte")
#
#     # stravaReturn = session.query(strava_simp.c.strava_id, sqlfunc.ST_AsGeoJSON
#     #     (sqlfunc.ST_Difference(strava_simp.c.trans_geom, private_aoi.c.priv_aoi)))\
#     #     .filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi))
#
#     # stravadiff = session.query(
#     #     (strava_simp.c.strava_id).label("diff_ids"),
#     #     (sqlfunc.ST_Difference(strava_simp.c.trans_geom, private_aoi.c.priv_aoi)).label("diff_geom")
#     # ).filter(sqlfunc.ST_Intersects(strava_simp.c.trans_geom, private_aoi.c.priv_aoi)).cte("strava_diff")
#
#     # stravaReturn = session.query(stravadiff.c.diff_ids, sqlfunc.ST_AsGeoJSON(stravadiff.c.diff_geom)).join(strava_simp, stravadiff.c.diff_ids != strava_simp.c.strava_id)
#
# TODO:
###### Gives me limited, desc, activites within privacy areas using CTE and multiple queries
# private_aoi = session.query(AOI.geom).filter(AOI.privacy == "Yes").cte("private_aoi")
# strava_lim = session.query(strava_activities.geom).order_by(strava_activities.id.desc()).limit(20).cte("strava_lim")
# query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Intersection(strava_lim.c.geom, private_aoi.c.geom)))
#


# Create a union of activities:
# private_aoi = session.query(sqlfunc.ST_Union(AOI.geom).filter(AOI.privacy == "Yes")).cte("private_aoi")
# Returns CTE of AOI with only privacy zones

# Based on: https://gis.stackexchange.com/questions/213851/more-on-cutting-polygons-with-polygons-in-postgis
# and on: https://stackoverflow.com/questions/22287328/geoalchemy2-find-a-set-of-geometry-items-that-doesnt-intersect-with-a-separate
# very slow, consider using shapely, follow: https://towardsdatascience.com/install-shapely-on-windows-72b6581bb46c to install
# on windows
# just using pip seems to work well on linux
# private_aoi = session.query(AOI.geom).filter(AOI.privacy == "Yes").cte("private_aoi")
# strava_lim = session.query(strava_activities.geom).order_by(strava_activities.id.desc()).limit(100).cte("stravalim")
# query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_lim.c.geom, private_aoi.c.geom))).filter(
#     sqlfunc.ST_Intersects(strava_lim.c.geom, private_aoi.c.geom))
# private_aoi = session.query(sqlfunc.ST_Collect(AOI.geom).filter(AOI.privacy == "Yes").label("aoicol")).cte("private_aoi")
# strava_lim = session.query(sqlfunc.ST_Collect(strava_activities.geom).label("stravaact")).order_by(strava_activities.id.desc()).limit(5).cte("stravalim")
# # strava_lim = session.query(sqlfunc.ST_Collect(strava_activities.geom).order_by(strava_activities.id.desc()))
# # strava_lim = session.query(sqlfunc.ST_Collect((strava_activities.geom).order_by(strava_activities.id.desc()).label("stravalim"))).cte("stravalim")
# print(strava_lim)
# query = session.query(sqlfunc.ST_AsGeoJSON(sqlfunc.ST_Difference(strava_lim.c.stravaact, private_aoi.c.aoicol))).filter(
#     sqlfunc.ST_Intersects(strava_lim.c.stravaact, private_aoi.c.aoicol))

# query = session.query(sqlfunc.ST_AsGeoJSON(strava_activities.geom))