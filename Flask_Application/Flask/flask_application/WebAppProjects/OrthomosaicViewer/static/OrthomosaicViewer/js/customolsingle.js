// Group layer to hold imagery layers
const imageryGroup =  new ol.layer.Group({
      openInLayerSwitcher: true,
      title: "Imagery",
      layers: []
})

// Create openlayers map with popup overlay, basemap, and empty imagery group layer
var map = new ol.Map({
  // overlays: [overlay],
  target: 'viewDiv',
  layers: [
    new ol.layer.Tile({
      title: "Open Street Map",
      source: new ol.source.OSM()
    }),
    imageryGroup
  ],
  view: new ol.View({
    // projection: projection,
    center: ol.proj.fromLonLat([-119.919715, 34.437206]),
    // center: [34.437206, -119.919715],
    zoom: 17
  })
  // view: source.getView()
});
// Create vector source using the OGC API url for feature extents
const vectorSource = new ol.source.Vector({
  url: dataURL,
  // Format data as geojson
  format: new ol.format.GeoJSON(),
})
// create a vector layer using the vector source
const vectorLayer = new ol.layer.Vector({
  source: vectorSource,
  title:"Imagery Extents",
  id: "extentsCollection",
  // projection: 'EPSG:4326'
  // displayInLayerSwitcher: false,
  style: hiddenPolygon,
});
map.addLayer(vectorLayer);
fetch(dataURL)
// Get response and convert to json
.then(response => response.json())
// process response json data
.then(data => {
  // Loop over each response in the Feature Collection response
  data.features.forEach((item, i) => {
    // get presigned cogURL, this is dynamic from server
    var cogURL = item.properties.URL
    // Get the item, which is a GeoJSON Feature
    var geojsonObject = item
    // Get the geotiff source using the URL provided in the geojson Feature
    var rasterSource = new ol.source.GeoTIFF({
      sources: [
        {
          url: item.properties.URL,
          // Set to value that doesnt exist, this is desirable since setting black, 0, causes large JPG artifacts around the border of the image which have values that not
          // exactly 0,0,0. Setting to 255 instead causes some full white values to dispear instead, creating holes.
          // Setting to 256 effectively turns off nodata
          // nodata: 256,
          nodata: 0,
          // bands: [1,2,3],
        },
      ],
      // COG is not in RGB, convert to RGB
      convertToRGB: true,
    });
    // Convert geotiff into WebGLTile, requried for COG to work properly
    var rasterTile = new ol.layer.WebGLTile({
      source: rasterSource,
      displayInLayerSwitcher: true,
      title: item.properties["Mission Name"] + "<br><span>" + item.properties["Mission Date"].substring(0,10) + " - " + item.properties["GSD"] + " in/px" +"</span>",
      // Set rid as object property, will be usually to toggle visibility on and off
      rid: item.properties["id"]
    });
    // Push a list of group layers to imagery group layer, this is done such that the extent polygon, with attributes, are grouped together with the raster layers
    srcList.push(rasterTile)
  });
  // Extent imagery group with newly populated list
  imageryGroup.getLayers().extend(srcList)
  // map.getLayers().extend(srcList);
  }
);
