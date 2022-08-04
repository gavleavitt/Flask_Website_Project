//popup:https://openlayers.org/en/latest/examples/popup.html
// Popup example plugin, switch to?
// http://raw.githack.com/walkermatt/ol-popup/master/examples/scroll.html
const container = document.getElementById('popup');
const content = document.getElementById('popup-content');
const closer = document.getElementById('popup-closer');
// Create overlay that wraps the popup html element and interacts with map
const overlay = new ol.Overlay({
  element: container,
  autoPan: {
    animation: {
      duration: 250,
    },
  },
});
function createWebGLTile(item, extent=Null){
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
    rid: item.properties["id"],
    extent: extent
  });
  return rasterTile;
}
/**
 * Add a click handler to hide the popup.
 * @return {boolean} Don't follow the href.
 */
closer.onclick = function () {
  overlay.setPosition(undefined);
  closer.blur();
  return false;
};
// Style for polygon extents
const hiddenPolygon = new ol.style.Style({
  stroke: new ol.style.Stroke({
    // color: 'rgba(0, 0, 0, 0)',
    color: 'blue',
    width: 1,
  }),
  fill: new ol.style.Fill({
    color: 'rgba(0, 0, 0, 0)',
  }),
});
// Group layer to hold imagery layers
const imageryGroup =  new ol.layer.Group({
      openInLayerSwitcher: true,
      title: "Imagery",
      layers: []
    })
// Create openlayers map with popup overlay, basemap, and empty imagery group layer
var map = new ol.Map({
  overlays: [overlay],
  target: 'viewDiv',
  layers: [
    new ol.layer.Tile({
      title: "OpenStreetMap",
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
  displayInLayerSwitcher: false,
  style: hiddenPolygon,
});
console.log(vectorLayer.getSource())
// Returns infinity values in log, but running in browser works properly, consider passing values into set view function, may be a async task
// see https://stackoverflow.com/a/30122616
console.log(await vectorLayer.getSource().getExtent())
// see: https://stackoverflow.com/a/32592280
// taken from: https://stackoverflow.com/a/30020449
// var extent = features[0].getGeometry().getExten0t().slice(0);
// features.forEach(function(feature){ ol.extent.extend(extent,feature.getGeometry().getExtent())});
// console.log(extent);
map.addLayer(vectorLayer);
// function getBB(coords){
//   vectorSource.once('change',function(e){
//       if(vectorSource.getState() === 'ready') {
//           var extent = vectorSource.getExtent();
//           console.log(extent);
//           map.getView().fit(extent, map.getSize());
//       }
// }
// List to hold imagery raster tiles
var srcList = []
// get mission extents feature collection, url is provided by server
// Consider adding option that skips geom, dont need geometry: skipGeometry=true
fetch(dataURL)
// Get response and convert to json
.then(response => response.json())
// process response json data
.then(data => {
  // Check if input is a feature collection, process all imagery if so
  if(data.type =="FeatureCollection"){
    // Loop over each response in the Feature Collection response
    data.features.forEach((item, i) => {
      // get coordinates from geometry, extract from nested list
      var coords = item.geometry.coordinates[0];
      // get extent, returns in 4326
      var extent = new ol.extent.boundingExtent(coords)
      // Transform extent, need to be 3857, web mercator, or else doesnt work
      var extTrans = ol.proj.transformExtent(extent , 'EPSG:4326', 'EPSG:3857')
      // Generate WebGLTile, only way to load a geotiff
      var rasterTile = createWebGLTile(item, extTrans)
      // Push a list of group layers to imagery group layer, this is done such that the extent polygon, with attributes, are grouped together with the raster layers
      srcList.push(rasterTile)
        // new ol.layer.Group({
        //       openInLayerSwitcher: true,
        //       title: item.properties["Mission Name"] + "<br><span>" + item.properties["Mission Date"].substring(0,10) + " - " + item.properties["GSD"] + " in/px" +"</span>",
        //       layers: [rasterTile]
        // })
      // )
    });
  } else {
    // Input is a single Feature instead of collection, handle differently
    var rasterTile = createWebGLTile(data)
    srcList.push(rasterTile)
  }
  // Extent imagery group with newly populated list
  imageryGroup.getLayers().extend(srcList)
//  http://jsfiddle.net/HarolddP/2wfo5acf/3/
// https://openlayers.org/en/latest/apidoc/module-ol_Map-Map.html#addOverlay
  // const popup = new ol.Overlay.Popup();
  // map.addOverlay(popup);
  // Click event handler, populates popup and additional event handlers
  map.on("click", (evt) => {
    var pixel = evt.pixel;
    var features = [];
    // https://openlayers.org/en/latest/apidoc/module-ol_Map-Map.html#forEachFeatureAtPixel
    // Loop over each feature clicked getting properties and push to list
    map.forEachFeatureAtPixel(pixel, function(feature, layer) {
      features.push(feature.getProperties());
    });
    // Reset innerhtml
    content.innerHTML = ""
    // Dynamically build popup html
    if (features.length > 0){
      content.innerHTML += "<span class='popup-header'>Drone Orthomosaic(s)</span>"
      features.forEach((item, i) => {
        content.innerHTML += `<br><b>Name: ${item["Mission Name"]}</b><br>Date: ${item["Mission Date"].substring(0,10)}<br>GSD: ${Math.round((item["GSD"]*10))/10} (in/px)<br><button rid=${item["id"]} class='layertogglebtn'>Make just this imagery visible</button><br><a href=${window.location}/${item["id"]}>Open just this orthomosaic</a>`
        // Check if 3D view available, add link if so
        if (item["3DMesh"]){
          content.innerHTML += `<br><a href=${window.location}/mesh/${item["id"]}></a>`
        }
      });
      // Get all elements with the rid property, this will be all dynamically generated buttons
      var sel = document.querySelectorAll('[rid]');
      // Loop over each popup button adding an event listener which allows user to toggle only showing a single orthomosaic
      // TODO: attach to icon in popup
      sel.forEach((item, i) => {
        item.addEventListener("click", function(btn){
          // Get rid of clicked button
          var rid = btn.target.getAttribute("rid")
          // Loop over all layers in imagery group, turning off visibiltiy if not equal to current rid
          var lyrs = imageryGroup.getLayers()
          lyrs.forEach((item, i) => {
            if (item.A.rid !=rid){
              item.setVisible(false)
            } else {
              item.setVisible(true)
            }
          });
        });
      });

      const coordinate = evt.coordinate;
      overlay.setPosition(evt.coordinate);
    } else {
      // No extend clicked, hide popup
      overlay.setPosition(undefined);
      // popup.hide();
    }
  });
  });
// http://viglino.github.io/ol-ext/examples/control/map.switcher.html
var switcher = new ol.control.LayerSwitcher({
  target:$(".layerSwitcher").get(0),
  // displayInLayerSwitcher: function (l) { return false; },
  show_progress:true,
  collapsed: false,
  extent: true,
  trash: true,
  // oninfo: function (l) { alert(l.get("title")); }
});
map.addControl(switcher);
var button = $('<div class="toggleVisibility" title="show/hide">')
  .text("Show/hide all")
  .click(function() {
    // TODO: add a global variable to track if all layers are set to inactive or active, toggle status and visibility using this variable
    // var a = map.getLayers().getArray();
    var a = map.getAllLayers()
    a.forEach((item, i) => {
      if (item.getVisible() && item.A.title!="OpenStreetMap"){
        item.setVisible(false)
      } else {
        item.setVisible(true)
      }
    });

    console.log(map)
  });
switcher.setHeader($('<div>').append(button).get(0))
