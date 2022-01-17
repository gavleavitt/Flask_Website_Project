class esriPolygon():
    polygon = {"hasZ": "false", "hasM": "false", "rings": [], "spatialReference": 4326}
    def __init__(self, lnglatList):
        self.coords = lnglatList