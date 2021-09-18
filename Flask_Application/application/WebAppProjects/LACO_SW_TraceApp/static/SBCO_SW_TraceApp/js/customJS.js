/*jshint esversion: 6 */
var btnActive = null;
var userLat = null;
var userlon = null;
var geojsonData = null;
var map = null;
var view = null;
// var layerObj = null;
// var selectionLayer = null
// var resultslayer = null
require(["esri/config", "esri/Map", "esri/layers/VectorTileLayer", "esri/views/MapView", "esri/layers/TileLayer", "esri/Graphic", "esri/layers/GraphicsLayer", "esri/layers/WebTileLayer", "esri/layers/GeoJSONLayer", "esri/symbols/SimpleMarkerSymbol", "esri/renderers/UniqueValueRenderer", "esri/renderers/SimpleRenderer", "esri/widgets/LayerList", "esri/layers/GroupLayer", "esri/rest/support/Query"],
  function (esriConfig, Map, VectorTileLayer, MapView, TileLayer, Graphic, GraphicsLayer, WebTileLayer, GeoJSONLayer, SimpleMarkerSymbol, UniqueValueRenderer, SimpleRenderer, LayerList, GroupLayer, Query) {
      esriConfig.apiKey = "AAPK5f601af9967543d6bc498db5a6b0f84bpHLpA-1hb11KUYm2IfzgmzBATsNlgD24Rjueqj2sKqaVsz3d6vU-6-l1yb-0YTi3";
      console.log("Loading vector tiles!");

      var selectionLayer = new GraphicsLayer();
      var resultslayer = new GroupLayer();

      const gravitymainstiles = new VectorTileLayer({
        title: "Gravity Mains",
        url: "https://vectortileservices3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/LACO_GravityMains_VTL/VectorTileServer"
      });

      const lateraltiles = new VectorTileLayer({
        title: "Laterals",
        url: "https://vectortileservices3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/Laterals/VectorTileServer"
      });

      const inlettiles = new VectorTileLayer({
          title: "Inlets",
          url: "https://vectortileservices3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/Inlets/VectorTileServer",
          minScale: 15000
         });

      const mhtiles = new VectorTileLayer({
           title: "Maintenance Holes",
           url: "https://vectortileservices3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/MaintenanceH_oles/VectorTileServer",
           minScale: 15000
          });

      const ottiles = new VectorTileLayer({
            title: "Outlets",
            url: "https://vectortileservices3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/Outlets/VectorTileServer",
            minScale: 15000
           });


      const networklayer = new GroupLayer({
          id: "networklayer",
          title: "Storm Network",
          layers: [gravitymainstiles, lateraltiles, inlettiles, mhtiles, ottiles]
        });

      const map = new Map({
        basemap: "arcgis-topographic", // Basemap layer service
        layers: [networklayer] // vector tile layer
      });
      const view = new MapView({
        map: map,
        center: [-118.167416, 33.784257], // Longitude, latitude
        zoom: 13, // Zoom level
        container: "viewDiv", // Div element
      });

      const selectionMarkerSymbol = {
         type: "simple-marker",
         style: "x",
         color: "blue",
         size:"20px",
         outline: {
             color: "blue", // White
             width: "10px"
         }
      };

      view.ui.add("traceDiv", "top-left");

      view.on("click", (event) => {
        // console.log("click event: ", event);
        // console.log("x:", event.mapPoint.longitude.toFixed(5));
        // console.log("y:", event.mapPoint.latitude.toFixed(5));
        // console.log("x:", event.mapPoint.x.toFixed(2));
        // console.log("y:", event.mapPoint.y.toFixed(2));
        document.getElementById("NoSelAlert").removeAttribute('active');
        // Set global variables of user's selection:
        userLong = event.mapPoint.longitude;
        userLat = event.mapPoint.latitude;
        if (btnActive === "active"){
          map.remove(selectionLayer);
          view.graphics.remove(selectionLayer);
          console.log("Selection is active!");
          const selectionpoint = new Graphic({
            title:"Start Point",
            geometry: {
               type: "point",
               longitude: event.mapPoint.longitude,
               latitude: event.mapPoint.latitude
             },
             symbol: selectionMarkerSymbol
          });
          selectionLayer = new GraphicsLayer({
            id: "selectionLayer",
            title: "Selected Start Point",
            graphics: [selectionpoint]
          });
          // selectionLayer.add(selectionpoint);
          map.add(selectionLayer);
          btnActive = null;
        }
          document.addEventListener("pointermove", function(){
            if (btnActive === "active"){
              document.body.style.cursor = "crosshair";
            } else {
                document.body.style.cursor = "default";
              }
          });
      });
      document.getElementById("selBtn").addEventListener("click", function(){
        console.log("selection active!");
        userLat = null;
        userlon = null;
        btnActive = "active";
      });



      document.getElementById("clearBtn").addEventListener("click", function(){
              console.log("Clearing results!")
              map.remove(selectionLayer);
              map.remove(resultslayer);
              view.graphics.remove(selectionLayer);
              view.graphics.remove(resultslayer);
              view.popup.close();
              document.getElementById("NoSelAlert").removeAttribute('active');;
              document.getElementById("NoResultAlert").removeAttribute('active')
              userLat = null;
              userlon = null;
              btnActive = null;
              // inletResults, outletResults, mhResults, gmResults, latResults = null;
              // Hide results window
              document.getElementById("results-grp").style.display = "none";
              // Get list of results to remove, using their calcite attribute
              document.querySelectorAll("calcite-pick-list-item").forEach(e => e.remove());
              // removeList = document.querySelectorAll("calcite-pick-list-item").forEach(e => e.remove());
              // for (let i = 0; i < removeList.length; i++) {
              //   removeList[i].remove();
              // }}
            }
          )

      layerList = new LayerList({
        view
      });

      view.ui.add(layerList, "top-right");

      document.getElementById("submitBtn").addEventListener("click", function(){
            // Clear out existing graphic layers
            map.remove(selectionLayer);
            map.remove(resultslayer);
            // Check if a point has been clicked, if not return message
            if (userLat === null){
              //Turn alert on
              console.log("No selection!");
              // document.getElementById("NoSelAlert").classList.add("is-active");
              document.getElementById("NoSelAlert").setAttribute('active','');
              return;
            }
            document.getElementById("NoSelAlert").removeAttribute('active');
            // Get coordinates from user selection
            // Get the active radio selection to determine flow direction
            radioGrp = document.querySelector('#directionGrp');
            traceDirection = radioGrp.querySelectorAll(":checked")[0].defaultValue;
            // console.log(userLat)
            // console.log(userLong)
            // console.log(traceDirection)
            var url = new URL('http://api.leavitttesting.com:5000/api/v1/trace/lacostormwater');
            // var url = new URL('/api/v1/trace/lacostormwater')
            var params = {"latitude":userLat, "longitude":userLong, "direction":traceDirection};
            url.search = new URLSearchParams(params).toString();
            // console.log(url);
            // Set Query text to active
            document.querySelector('#query-text').style.display = "block";
            // Issue Async request
            fetch(url, {method: "GET",
              mode: 'cors'})
            .then(r => {
              // Returns data
              return r.json();
            })
            .then(function(data){

              // Object to hold ArcGIS JS API geojson formatted layers
              layerObj = {}
              function addGeoJson(geojson, title, popupTemplate){
                // Takes geojson result features returned from server and brings them in as object URLs since the GeoJSONLayer function expects a seperate URL
                // for each layer, not one URL for all
                // Check if the GeoJSON has results, if not skip it
                if (geojson['features'].length > 0){
                  // Make a blob object of geojson formatted data
                  const blob = new Blob([JSON.stringify(geojson)], {type: "application/json"});
                  // Make a temporary URL that points to the client-side store previously created blob feature
                  const url  = URL.createObjectURL(blob);
                  // Create a GeoJSON layer using provided popupTemplate and previously set renderer
                  const result = new GeoJSONLayer({
                    url:url,
                    title:title,
                    renderer:lineResultRenderer,
                    popupTemplate: popupTemplate
                  });
                  // Add new geojson layer to layerObj
                  layerObj[title] = result;
                }
              }
              // Process geojson result layers provided by server
              addGeoJson(data['Gravity Mains'], 'Gravity Mains', popupGM)
              addGeoJson(data['Laterals'], 'Laterals', popupLat)
              addGeoJson(data['Inlets'], 'Inlets', popupInlet)
              addGeoJson(data['startpoint'], 'Start Point', null)
              addGeoJson(data['Outlets'], 'Outlets', popupOutlet)
              addGeoJson(data['Maintenance Holes'], 'Maintenance Holes', popupMH)

              // Add results as a group layer
              resultslayer = new GroupLayer({
                id: "resultslayer",
                title: "Trace Results",
                layers: Object.values(layerObj)
              });
              // Add group layer to map
              map.add(resultslayer);
              // Zoom to extent of gravity mains result, can't zoom to extent of group layer
              layerObj['Gravity Mains'].queryExtent().then((response) => {
                view.goTo(response.extent);
              });
              // Set Query text to inactive
              document.querySelector('#query-text').style.display = "none";
              document.getElementById("DownloadCSV").addEventListener("click", function(){
                createCSV(data)
              });

              function buildResultsDisplay(geojsonlyr, calciteWindowID, titleText){
                //  Get count of features in geojson layer
                // if (datalyr['features'].length > 0){
                console.log(titleText);
                console.log(geojsonlyr)
                if (geojsonlyr !== undefined){
                  console.log("Populating data!");
                  var results = new Object();
                  query = new Query();
                  query.where = `factype = '${titleText}'`;
                  query.outFields = [ "factype", "id", "facsubtype", "facid"];
                  query.returnGeometry = true;
                  geojsonlyr.queryFeatures(query)
                  .then(function(response){
                      // Get object of results
                      // Get record count
                      results.count = Object.keys(response.features).length
                      console.log(results.count)
                      features = response.features;
                      // Update accordian title to show Count
                      document.getElementById(calciteWindowID).setAttribute("heading", `${titleText} (${results.count})`)
                      // Loop over each feature in result
                      features.forEach((result, index)=>{
                        attr = result.attributes;
                        item = document.createElement("calcite-pick-list-item");
                        item.setAttribute("label", attr.facid);
                        item.setAttribute("value", index);
                        // Add to service results
                        // type = `Inlet Type: ${attr[facsubtype]}`;
                        type = `${titleText} Type: ${attr.facsubtype}`;
                        if (["Inlets, Maintenance Holes"].includes(titleText)){
                          console.log(titleText)
                          description = type;
                        } else {
                          size =  `Size: ${attr.size}`;
                          material = `Material: ${attr.material}`
                          description = type + "\n" + size + "\n" + material;
                        }
                        item.setAttribute("description", description);
                        item.addEventListener("click", function(){
                          // const target = event.target;
                          // const resultId = target.getAttribute("value");
                          view.popup.open({
                            features: [result],
                            location: result.geometry
                          });
                          view.goTo(result.geometry)
                        });
                        // Append to existing results panel
                        console.log(calciteWindowID)
                        document.getElementById(calciteWindowID).appendChild(item);
                      });
                    });
                  } else {
                    console.log("Setting empty results")
                    document.getElementById(calciteWindowID).setAttribute("heading", titleText)
                  }
                }


              buildResultsDisplay(layerObj['Gravity Mains'], 'GM-Window', 'Gravity Mains')
              buildResultsDisplay(layerObj['Laterals'], 'Lat-Window', 'Laterals')
              buildResultsDisplay(layerObj['Inlets'], 'InletsWindow', 'Inlets')
              buildResultsDisplay(layerObj['Outlets'], 'OutletsWindow', 'Outlets')
              buildResultsDisplay(layerObj['Maintenance Holes'], 'MH-Window', 'Maintenance Holes')
              // Set result group to display
              document.getElementById("results-grp").style.display = "block";
               })
            .catch(error =>{
              console.log(error)
              console.log("Server request error!")
              // Set query text to error
              document.querySelector('#query-text').style.display = "none";
              document.getElementById("NoResultAlert").setAttribute('active','')
            });
      });
  });
;
