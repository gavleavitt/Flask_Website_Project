import overpass
from shapely.geometry import shape, LineString, Point
from shapely.ops import nearest_points
import shapely.wkt
from pyproj import Transformer
import pyproj
from shapely.geometry import Point
from shapely.ops import transform


def getNearestWay(query, project, inputCoord):
    """

    @param query:
    @param project:
    @param inputCoord:
    @return:
    """
    lineStringDict = {}
    for i in query.features:
        # Transform from WGS 1984 to the projection, this avoids getting degrees in results
        shape = transform(project, LineString(i["geometry"]["coordinates"]))
        # Calculate nearest point between the input coordinate and the way geom
        nearestPt = nearest_points(inputCoord, shape)[1]
        # Get the distance to the nearest point from the input coordinate
        distToPt = nearestPt.distance(inputCoord)
        # Build dict with results, OSM IDs are the top level keys
        lineStringDict[i["id"]] = {"name": i["properties"]["name"], "shape": shape, "nearestPt": nearestPt,
                                   "distToPt": distToPt}

    lowestVal = ["", 99999]
    # Get nearest way name by looping over IDs in dict
    for i in lineStringDict.keys():
        if lineStringDict[i]["distToPt"] < lowestVal[1]:
            lowestVal[0] = lineStringDict[i]["name"]
            lowestVal[1] = lineStringDict[i]["distToPt"]
    return lowestVal


def handleNearestOSMWays(lat, lon, type):
    """

    @param lat:
    @param lon:
    @param type:
    @return:
    """
    # see: https://gis.stackexchange.com/a/80898
    # Doc: https://github.com/mvexel/overpass-api-python-wrapper
    # Create overpass API connection, with a timeout time
    api = overpass.API(timeout=15)

    # see: https://shapely.readthedocs.io/en/stable/manual.html#other-transformations
    # Set GCS and projection to be applied: EPSG:3310 NAD83 / California Albers, units are meters
    wgs84 = pyproj.CRS('EPSG:4326')
    calAlb = pyproj.CRS('EPSG:3310')
    # Create transformation object
    project = pyproj.Transformer.from_crs(wgs84, calAlb, always_xy=True).transform

    # transform input coord to PCS, shapely takes coords in X,Y
    inputCoord = transform(project, Point(float(lon), float(lat)))
    # Dict that holds results
    resDict = {}
    # radius list, meters
    radList = (10, 100, 1000, 5000, 10000, 100000)
    for rad in radList:
        # print(f"trying search radius: {rad}")
        # around query
        # req expression : https://gis.stackexchange.com/questions/341746/what-is-a-correct-overpass-turbo-query-for-getting-all-streets-in-a-city

        # Get nearest road, result will always be used:
        roadQ = api.get(f'way["tiger:cfcc"]["name"][!"cycleway"](around:{rad},{lat},{lon})', verbosity='geom')
        # print(f"Len is: {len(roadQ.features)}")
        # Check if a road was found, if not go to the next radius, always want a road result
        if len(roadQ.features) > 0:
            # print("Populating Dict!")
            resDict = {}
            nearestRoad = getNearestWay(roadQ, project, inputCoord)
            resDict["Road"] = nearestRoad
            # print(nearestRoad)
            if type == "Road_Cycling":
                # Same as road query but can include cycling ways, bike paths, etc
                cycleQ = api.get(f'way["highway"]["name"](around:{rad},{lat},{lon})', verbosity='geom')
                nearestRoute = getNearestWay(cycleQ, project, inputCoord)
                resDict["Route"] = nearestRoute
            # elif type in ("MTB", "Walk", "Hike", "Trail"):
            elif type in ['Toro Park','Fort Ord', 'UCSC Trails', 'Soquel Demo','Kern Canyon']:
                # same as road query but can catch all types of named ways
                trailQ = api.get(f'way["name"](around:{rad},{lat},{lon})', verbosity='geom')
                nearestTrail = getNearestWay(trailQ, project, inputCoord)
                resDict["Route"] = nearestTrail
            else:
                resDict["Route"] = [None,None]
            return resDict
    return ["No Nearby Road!", "999999"]


def getOSMLocation(lat, lon):
    """

    @param lat:
    @param lon:
    @return:
    """
    api = overpass.API(timeout=15)

    lat = float(lat)
    lon = float(lon)
    # the default return type, geojson gives invalid returns, use json instead, see here:
    # https://github.com/mvexel/overpass-api-python-wrapper/pull/129

    # Try to query city:
    # print("Querying city")
    place = None
    cityQ = api.get(f'is_in({lat},{lon});area._[admin_level="8"]', responseformat="json")
    for i in cityQ["elements"]:
        place = i['tags']['name']
    # if no city try to get census place
    if not place:
        # print("No city, trying to find cdp")
        cdpQ = api.get(f'is_in({lat},{lon});area._[boundary="census"]', responseformat="json")
        for i in cdpQ["elements"]:
            place = i['tags']['name']
    # Get county:
    # print("Querying county")
    countyQ = api.get(f'is_in({lat},{lon});area._[admin_level="6"]', responseformat="json")
    county = ""
    for i in countyQ["elements"]:
        county = i['tags']['name']
    # Get state:
    # print("Querying state")
    stateQ = api.get(f'is_in({lat},{lon});area._[admin_level="4"]', responseformat="json")
    state = ""
    for i in stateQ["elements"]:
        state = i['tags']['name']
    # print(place)
    # print(county)
    # print(state)
    res = {"place": place, "county": county, "state": state}

    return res
