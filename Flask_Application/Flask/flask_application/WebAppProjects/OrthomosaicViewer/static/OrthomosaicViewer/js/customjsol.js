//popup:https://openlayers.org/en/latest/examples/popup.html
// Popup example plugin, switch to?
// http://raw.githack.com/walkermatt/ol-popup/master/examples/scroll.html
const container = document.getElementById('popup');
const content = document.getElementById('popup-content');
const closer = document.getElementById('popup-closer');
var visible = true
var popID = 0
// Create overlay that wraps the popup html element and interacts with map
const overlay = new ol.Overlay({
  element: container,
  autoPan: {
    animation: {
      duration: 250,
    },
  },
});

function zoomTo(rid){
  // Zoom to event of target layer
  // Get ID value assigned to layer
  // Get all layers in imagery group
  var layers = imageryGroup.getLayers()
  layers.forEach((item, i) => {
    // Find layer associated with popup button
    if (item.A['id'] == rid){
      // Get extent of layer
      var extent = item.A["extent"]
      // Set map view based on extent
      map.getView().fit(extent);
    }
  });
};

function showThisLayerBtn(rid){
    // Loop over all layers in imagery group, turning off visibiltiy if not equal to current rid
    var lyrs = imageryGroup.getLayers()
    lyrs.forEach((item, i) => {
      if (item.A.rid !=rid){
        item.setVisible(false)
      } else {
        item.setVisible(true)
        var extent = item.A["extent"]
        // Set map view based on extent
        map.getView().fit(extent);
      }
    });
};

function closeModal(){
  document.getElementById('infoModal').style.display= "none";
}

function popupListener(btn){
  // console.log("clicked!");
  // console.log(btn);
  var rid = btn.target.getAttribute("rid")
 if (btn.target.getAttribute("btntype")=="toggleDisplay"){
   // console.log("Clicked display toggle!")
   showThisLayerBtn(rid)
 } else if (btn.target.getAttribute("btntype")=="ZoomTo") {
   // console.log("Clicked Zoom To!")
    zoomTo(rid)
 } else if (btn.target.getAttribute("btntype")=="NewWindow") {
   window.open(`${window.location}/${rid}`)
 }
}

function popupinfo(item){
  // Format Info popup window
  // console.log(item);
  var infoModal = document.getElementById('infoModal');
  infoModal.style.display = "block";
  var modalHeader = document.getElementById('modalHeader')
  modalHeader.innerHTML = ""
  if (item.raster == true){
    modalHeader.innerHTML += `<span class='popup-header'>Drone Orthomosaic - ${item["Mission Name"].replace("_"," ")}</span>`
    modalHeader.innerHTML +=`</b><br>Collection Date: ${item["Mission Date"].substring(0,10)}`
    modalHeader.innerHTML += `<br>GSD: ${Math.round((item["GSD"]*10))/10} (in/px)`
    modalHeader.innerHTML += `<br>Flight Elevation: ${item["Mission Elevation"]}`
    modalHeader.innerHTML += `<br>Altitude Flight Type: ${item["Altitude Flight Type"]}`
    // modalHeader.innerHTML += `<br>Actions:`
    modalHeader.innerHTML += `<br><div class="popbtngrp"><button rid=${item["id"]} id="zoomTo" class="action_btns"><i class="bi bi-square"></i><span class="btntxt">Zoom</span></button><button rid=${item["id"]} id="toggleDisplayPop" class="action_btns"><i class="bi bi-eye-fill"></i><span class="btntxt">Toggle</span></button><button rid=${item["id"]} id="newWindow" class="action_btns"><i class="bi bi-arrow-up-right-square-fill"></i><span rid=${item["id"]} class="btntxt">New Window</span></button></div>`
    // Add event listeners to popup buttons
    document.getElementById("newWindow").addEventListener("click", function(e){
      // Open new window
      window.open(`${window.location}/${item["id"]}`)
    })
    // TODO: build out to toggle just the selected layer on, already have logic for, consider building into a function to be called here and in other location
    // document.getElementById("toggleDisplayPop").addEventListener("click", showThisLayerBtn);
    document.getElementById("toggleDisplayPop").addEventListener("click", function(e){
      var rid = e.target.attributes.rid.value;
      showThisLayerBtn(rid);
    });
    document.getElementById("zoomTo").addEventListener("click", function(e){
      zoomTo(e.target.attributes.rid.value)
      // console.log("Zoomto!")
      // // Zoom to event of target layer
      // // Get ID value assigned to layer
      // var rid = e.target.attributes.rid.value
      // // Get all layers in imagery group
      // var layers = imageryGroup.getLayers()
      // layers.forEach((item, i) => {
      //   // Find layer associated with popup button
      //   if (item.A['id'] == rid){
      //     // Get extent of layer
      //     var extent = item.A["extent"]
      //     // Set map view based on extent
      //     map.getView().fit(extent);
      //   }
      // });
    });
  }
  else{
    modalHeader.innerHTML += `<span class='popup-header'>${item.title}</span>`
  }
  // Check if 3D view available, add link if so
  document.getElementById('infoClose').addEventListener("click", closeModal)
  window.addEventListener('click', function(event) {
      infoModal.style.display = "none";
  });
  overlay.setPosition(undefined);
  closer.blur();
  // window.onclick = function(event) {
  //   if (event.target == infoModal) {
  //     infoModal.style.display = "none";
  //   }
  // }
}
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
    title: item.properties["Mission Name"].replace("_"," ") + "<br><span>" + item.properties["Mission Date"].substring(0,10) + " - " + item.properties["GSD"] + " in/px" +"</span>",
    // Set rid as object property, will be usually to toggle visibility on and off
    rid: item.properties["id"],
    // Set properties from vector layer soruce
    properties: item.properties,
    extent: extent,
    raster: true
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
const visiblePolygon = new ol.style.Style({
  stroke: new ol.style.Stroke({
    // color: 'rgba(0, 0, 0, 0)',
    color: 'blue',
    width: 1,
  }),
  fill: new ol.style.Fill({
    color: 'rgba(0, 0, 0, 0)',
  }),
});
const hiddenPolygon = new ol.style.Style({
  stroke: new ol.style.Stroke({
    color: 'rgba(0, 0, 0, 0)',
    // color: 'blue',
    // width: 1,
  }),
  fill: new ol.style.Fill({
    color: 'rgba(0, 0, 0, 0)',
  }),
});
// Group layer to hold imagery layers
const imageryGroup =  new ol.layer.Group({
      openInLayerSwitcher: true,
      title: "Imagery",
      layers: [],
      raster: false
    })
// Create openlayers map with popup overlay, basemap, and empty imagery group layer
var map = new ol.Map({
  overlays: [overlay],
  target: 'viewDiv',
  layers: [
    new ol.layer.Tile({
      title: "OpenStreetMap",
      raster: false,
      source: new ol.source.OSM()
    }),
    imageryGroup
  ],
  view: new ol.View({
    // projection: projection,
    center: ol.proj.fromLonLat([-119.919715, 34.437206]),
    // center: [34.437206, -119.919715],
    zoom: 12
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
  displayInLayerSwitcher: true,
  style: visiblePolygon,
});
// create a hidden vector layer using the vector source, this ensures that popups always work
const hiddenVectorLayer = new ol.layer.Vector({
  source: vectorSource,
  title:"Imagery Extents Hidden",
  id: "extentsCollectionHidden",
  // projection: 'EPSG:4326'
  displayInLayerSwitcher: false,
  style: hiddenPolygon,
});
// console.log(vectorLayer.getSource())
// Returns infinity values in log, but running in browser works properly, consider passing values into set view function, may be a async task
// see https://stackoverflow.com/a/30122616
// console.log(await vectorLayer.getSource().getExtent())
// see: https://stackoverflow.com/a/32592280
// taken from: https://stackoverflow.com/a/30020449
// var extent = features[0].getGeometry().getExten0t().slice(0);
// features.forEach(function(feature){ ol.extent.extend(extent,feature.getGeometry().getExtent())});
// console.log(extent);
map.addLayer(vectorLayer);
map.addLayer(hiddenVectorLayer);
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
    });
  } else {
    console.log(data)
    console.log("Single item!")
    var coord = data.geometry.coordinates[0];
    var extent = new ol.extent.boundingExtent(coord)
    var extTrans = ol.proj.transformExtent(extent , 'EPSG:4326', 'EPSG:3857')
    // Input is a single Feature instead of collection, handle differently
    var rasterTile = createWebGLTile(data, extTrans)
    srcList.push(rasterTile)
    map.getView().fit(extTrans);
    // Zoom to extent of item
  }
  // Extent imagery group with newly populated list
  imageryGroup.getLayers().extend(srcList)
  // Click event handler, populates popup and additional event handlers
  map.on("click", (evt) => {
    var pixel = evt.pixel;
    var features = [];
    // Get list of all orthos
    var orthos = imageryGroup.getLayers()
    // Empty list to hold all layers which are toggled on
    var toggledOn = []
    orthos.forEach((item, i) => {
      // Check if feature is rendered, turned on, add to list if so
      if (item.rendered == true){
        console.log(`Feature ${item.A.id} is enabled`)
        toggledOn.push(item.A.id)
      }
    });

    console.log(orthos)
    // https://openlayers.org/en/latest/apidoc/module-ol_Map-Map.html#forEachFeatureAtPixel
    // Loop over each feature clicked getting properties and push to list
    map.forEachFeatureAtPixel(pixel, function(feature, layer) {
      // Use the hidden vector layer to get attributes as it will always be "visible" to this function
      if (layer.A.title =="Imagery Extents Hidden"){
        console.log(feature.A.id)
        console.log(toggledOn)
        // only add features to the list which also have a ortho toggled on
        if (toggledOn.includes(feature.A.id)){
          features.push(feature.getProperties());
        }
      }
    });
    var newContent = ""
    // Reset innerhtml
    content.innerHTML = ""
    // Dynamically build popup html
    if (features.length > 0){
       newContent += "<span class='popup-header'>Drone Orthomosaic(s)</span>"
      // const header = document.createElement("span")
      // header.className="popup-header"
      // const headerText = document.createTextNode("Drone Orthomosaic(s)")
      // header.appendChild(headerText)
      features.forEach((item, i) => {
        // TODO fix,using += on innerhtml writes over previous listeners, need to write logic to append html elements
        popID += 1
        newContent += `<div class="popupItem"><br><b><span class="popupItemName">Name: ${item["Mission Name"].replace("_"," ")}</span></b><br>Date: ${item["Mission Date"].substring(0,10)}<br>GSD: ${Math.round((item["GSD"]*10))/10} (in/px)`
        newContent += `<div class="popbtngrp"><button btnType="ZoomTo" rid=${item["id"]} id="zoomTo_${popID}" class="popupbtns"><i class="bi bi-square"></i><span class="btntxt"></span></button><button btnType="toggleDisplay" rid=${item["id"]} id="toggleDisplay_${popID}" class="popupbtns"><i class="bi bi-eye-fill"></i><span class="btntxt"></span></button><button btnType="NewWindow" rid=${item["id"]} id="newWindow_${popID}" class="popupbtns"><i class="bi bi-arrow-up-right-square-fill"></i><span rid=${item["id"]} class="btntxt"></span></button></div>`
        // Check if 3D view available, add link if so
        if (item["3DMesh"]){
          newContent += `<br><a href=${window.location}/mesh/${item["id"]}></a>`
        }
        newContent += "</div>"
        content.innerHTML = newContent

        // TODO: apply button functions to each button on each loop
        // console.log(document.querySelector(`button[rid='${item["id"]}'][btnType="Toggle"]`))
        // document.querySelector(`button[rid='${item["id"]}'][btnType="Toggle"]`).addEventListener("click", showThisLayerBtn);
        // console.log(document.getElementById(`toggleDisplay`))
        // document.getElementById(`toggleDisplay_${popID}`).addEventListener("click", showThisLayerBtn);
        // Get all elements with the rid property, this will be all dynamically generated buttons
        // var sel = document.querySelectorAll('[rid]');
        // Loop over each popup button adding an event listener which allows user to toggle only showing a single orthomosaic
        // sel.forEach((item, i) => {
        //   item.addEventListener("click", showThisLayerBtn);
        // });
      });
      console.log(content);
      content.addEventListener("click", popupListener)
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
  oninfo: function(e){popupinfo(e.A)}
});
map.addControl(switcher);
var button = $('<div class="toggleVisibility" title="show/hide Orthos">')
  .text("Show/hide Orthos")
  .click(function() {
    // TODO: add a global variable to track if all layers are set to inactive or active, toggle status and visibility using this variable
    // var a = map.getLayers().getArray();
    var a = map.getAllLayers()
    a.forEach((item, i) => {
      // if (item.getVisible() && item.A.title!="OpenStreetMap" && item.A.title!="Imagery Extents"){
      if (visible == true && item.A.raster==true){
        item.setVisible(false)
      } else {
        item.setVisible(true)
      }
    });
    if (visible == true){
      visible = false
    } else {
      visible = true
    }
    console.log(map)
  });
switcher.setHeader($('<div>').append(button).get(0))
