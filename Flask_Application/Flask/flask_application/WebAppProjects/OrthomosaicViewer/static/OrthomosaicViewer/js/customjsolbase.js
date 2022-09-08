//popup:https://openlayers.org/en/latest/examples/popup.html
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

/**
 * Add a click handler to hide the popup.
 * @return {boolean} Don't follow the href.
 */
closer.onclick = function () {
  overlay.setPosition(undefined);
  closer.blur();
  return false;
};

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
// List to hold imagery raster tiles
var srcList = []
// get mission extents feature collection, url is provided by server
// Consider adding option that skips geom, dont need geometry: skipGeometry=true
fetch(dataURL)
// Get response and convert to json
.then(response => response.json())
// process response json data
.then(data => {
  // var vectorSource = new ol.source.Vector()
  // const features = new ol.format.GeoJSON().readFeatures(data);
  // vectorSource.addFeatures(features);
    // Doesnt work:
    // features: new ol.format.GeoJSON().readFeatures(data)
    // features: new ol.format.GeoJSON().readFeatures(
    //   data, {dataProjection:"EPSG:4326"}),
    // features: new ol.format.Collection data,
    // Works:
    // url: 'http://geo.leavitttesting.local:5000/collections/ortho_mission_extents/items?f=json',
    // format: new ol.format.GeoJSON(),
  // });
  // create vector layer to hold geojson vector source, hide in switcher
  // const vectorLayer = new ol.layer.Vector({
  //   source: vectorSource,
  //   title:"Imagery Extents",
  //   // projection: 'EPSG:4326'
  //   // displayInLayerSwitcher: false,
  //   // style: hiddenPolygon,
  // });
  // map.addLayer(vectorLayer);
  // Loop over each response in the Feature Collection response
  data.features.forEach((item, i) => {
    // get presigned cogURL, this is dynamic from server
    var cogURL = item.properties.URL
    // Get the item, which is a GeoJSON Feature
    var geojsonObject = item
    // Contruct vector source using the geojson Feature
    // const vectorSource = new ol.source.Vector({
    //   features: new ol.format.GeoJSON().readFeatures(geojsonObject)
    // });
    // // create vector layer to hold geojson vector source, hide in switcher
    // // Not defining the style makes it empty which is desired here
    // const vectorLayer = new ol.layer.Vector({
    //   source: vectorSource,
    //   displayInLayerSwitcher: false,
    //   style: hiddenPolygon,
    // });
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
      // new ol.layer.Group({
      //       openInLayerSwitcher: true,
      //       title: item.properties["Mission Name"] + "<br><span>" + item.properties["Mission Date"].substring(0,10) + " - " + item.properties["GSD"] + " in/px" +"</span>",
      //       layers: [rasterTile]
      // })
    // )
  });
  // Extent imagery group with newly populated list
  imageryGroup.getLayers().extend(srcList)
  // map.getLayers().extend(srcList);
  }
);
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
        // Add event listener to added button
        // see https://www.nickang.com/2018-03-06-add-event-listener-for-loop-problem-in-javascript/
        // console.log("Adding event listener")
        // console.log(`[rid=${item["id"]}]`)
        // var sel = null
        // var sel = document.querySelector(`[rid="${item["id"]}"]`);
        // console.log(sel);
        // if (sel){
        //   console.log("sel exists!")
        //   sel.addEventListener("click", function(){
        //     console.log(item["id"]);
        //   });
        // } else {
        //   console.log("Item not found!")
        // }
      });
      // Get all elements with the rid property, this will be all dynamically generated buttons
      var sel = document.querySelectorAll('[rid]');
      // Loop over each popup button adding an event listener which allows user to toggle only showing a single orthomosaic
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
// https://developers.arcgis.com/openlayers/layers/display-a-popup/
// taken from: https://codesandbox.io/s/cog-forked-dqreb?file=/main.js:1418-1704
// map.on("singleclick", (evt) => {
//   const coordinate = evt.coordinate;
//   const hdms = ol.coordinate.toStringHDMS(ol.proj.toLonLat(coordinate));
//   content.innerHTML = '<p>You clicked here:</p><code>' + hdms + '</code>';
//   overlay.setPosition(coordinate);
// });


// Add control inside the map
// var ctrl = new ol.control.LayerSwitcher({
//   // collapsed: false,
//   // mouseover: true
// });
// Add layer switcher
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
