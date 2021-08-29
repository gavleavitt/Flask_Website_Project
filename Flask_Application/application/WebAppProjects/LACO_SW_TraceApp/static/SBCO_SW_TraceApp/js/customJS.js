/*jshint esversion: 6 */
var btnActive = null;
var userLat = null;
var userlon = null;
var geojsonData = null;
var map = null;
var view = null;
var layerList = null;
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
          minScale: 20000
         });

      const mhtiles = new VectorTileLayer({
           title: "Maintenance Holes",
           url: "https://vectortileservices3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/MaintenanceH_oles/VectorTileServer",
           minScale: 20000
          });

      const ottiles = new VectorTileLayer({
            title: "Outlets",
            url: "https://vectortileservices3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/Outlets/VectorTileServer",
            minScale: 20000
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
        console.log("click event: ", event);
        console.log("x:", event.mapPoint.longitude.toFixed(5));
        console.log("y:", event.mapPoint.latitude.toFixed(5));
        console.log("x:", event.mapPoint.x.toFixed(2));
        console.log("y:", event.mapPoint.y.toFixed(2));
        document.getElementById("NoSelAlert").removeAttribute('active');
        // Set global variables of user's selection:
        userLong = event.mapPoint.longitude;
        userLat = event.mapPoint.latitude;
        if (btnActive === "active"){
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
        // Clear out existing graphic layers
        // if (typeof selectionLayer != "undefined"){
        //   selectionLayer.removeAll();
        // };
        // map.removeLayer(map.getLayer("selectionLayer"));
        // map.removeLayer(map.getLayer("resultslayer"));
        // const removelayers = map.allLayers.find(function(layer) {
        //   return layer.title === "Selected Start Point";
        // });
        const removelayers = map.allLayers.find(function(layer) {
          map.remove(layer.title === "Selected Start Point");
          map.remove(layer.title === "Trace Results");
          // return [layer.title === "Selected Start Point",
          //   layer.title === "Trace Results"]
        });
        map.removeMany(removelayers);
        userLat = null;
        userlon = null;
        btnActive = "active";
      });
      document.getElementById("clearBtn").addEventListener("click", function(){
        map.remove(selectionLayer);
        map.remove(resultslayer);
        view.graphics.remove(selectionLayer);
        view.graphics.remove(resultslayer);
        document.getElementById("NoSelAlert").removeAttribute('active');;
        document.getElementById("NoResultAlert").removeAttribute('active')
        userLat = null;
        userlon = null;
        btnActive = null;
        // Hide results window
        document.getElementById("results-grp").style.display = "none";
        // Get list of results to remove, using their calcite attribute
        removeList = document.querySelectorAll("calcite-pick-list-item");
        for (let i = 0; i < removeList.length; i++) {
          removeList[i].remove();
        }
      });


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
            fetch(url, {method: "GET",
              mode: 'cors'})
            .then(r => {
              // Returns data
              return r.json();
            })
            .then(function(data){
              const lineblob = new Blob([JSON.stringify(data['lines'])], {type: "application/json"});
              const lineurl  = URL.createObjectURL(lineblob);
              const resultLines = new GeoJSONLayer({
                url:lineurl,
                title:"Underground Drainage Results",
                renderer:lineResultRenderer
              });
              const pointblob = new Blob([JSON.stringify(data['points'])], {type: "application/json"});
              const pointurl  = URL.createObjectURL(pointblob);
              const resultpoints = new GeoJSONLayer({
                url:pointurl,
                title: "Structure Results",
                renderer: pointResultRenderer
              });
              const startblob = new Blob([JSON.stringify(data['startpoint'])], {type: "application/json"});
              const starturl  = URL.createObjectURL(startblob);
              const startpoint = new GeoJSONLayer({
                url:starturl,
                title: "Trace Start Point",
                renderer: startrenderer
              });
              resultslayer = new GroupLayer({
                id: "resultslayer",
                title: "Trace Results",
                layers: [resultLines, startpoint, resultpoints]
              });
              map.add(resultslayer);
              resultLines.queryExtent().then((response) => {
                view.goTo(response.extent);
              });
              // Set Query text to inactive
              document.querySelector('#query-text').style.display = "none";
              // query features: https://developers.arcgis.com/javascript/latest/api-reference/esri-layers-GeoJSONLayer.html#queryFeatures
              // See https://developers.arcgis.com/javascript/latest/sample-code/featurelayer-query/
              //###### Inlet results ######
              var inletResults = new Object();
              inletQuery = new Query();
              inletQuery.where = "factype = 'Inlet'";
              inletQuery.outFields = [ "factype", "id", "facsubtype", "facid"];
              resultpoints.queryFeatures(inletQuery)
              .then(function(response){
                  // Get object of results
                  // console.log(response)
                  // console.log(response.features)
                  // Get record count
                  inletResults.count = Object.keys(response.features).length
                  console.log(inletResults.count)
                  features = response.features;
                  // Update accordian title to show Count
                  document.getElementById("InletsWindow").setAttribute("heading", `Inlets (${inletResults.count})`)
                  // Loop over each feature in result
                  features.forEach((result, index)=>{
                    attr = result.attributes;
                    item = document.createElement("calcite-pick-list-item");
                    item.setAttribute("label", attr.facid);
                    item.setAttribute("value", index);
                    // Add to service results
                    // type = `Inlet Type: ${attr[facsubtype]}`;
                    type = `Inlet Type: ${attr.facsubtype}`;
                    // size =  `Inlet Size: ${attr[size]}`;
                    // description = type + "\n" + size;
                    description = type
                    item.setAttribute("description", description);
                    // Add event listenr to pick list item, opens popup for feature
                    // item.addEventListener("click", traceResultClickHandler);
                    // Append to existing results panel
                    document.getElementById("InletsWindow").appendChild(item);
                  });
                });

              // ###### Outlet Results ######
              var outletResults = new Object();
              outletQuery = new Query();
              outletQuery.where = "factype = 'Outlet'";
              outletQuery.outFields = [ "factype", "id", "size", "facid", "material", "facsubtype"];
              resultpoints.queryFeatures(outletQuery)
              .then(function(response){
                // Get object of results
                // console.log(response)
                // console.log(response.features)
                // Get record count
                outletResults.count = Object.keys(response.features).length
                features = response.features;
                // Update accordian title to show Count
                document.getElementById("OutletsWindow").setAttribute("heading", `Outlets (${outletResults.count})`)
                // Loop over each feature in result
                features.forEach((result, index)=>{
                  attr = result.attributes;
                  item = document.createElement("calcite-pick-list-item");
                  item.setAttribute("label", attr.facid);
                  item.setAttribute("value", index);
                  // Add to service results
                  // type = `Inlet Type: ${attr[facsubtype]}`;
                  type = `Inlet Type: ${attr.facsubtype}`;
                  // size =  `Inlet Size: ${attr[size]}`;
                  // description = type + "\n" + size;
                  description = type
                  item.setAttribute("description", description);
                  // Add event listenr to pick list item, opens popup for feature
                  // item.addEventListener("click", traceResultClickHandler);
                  // Append to existing results panel
                  document.getElementById("OutletsWindow").appendChild(item);
                });
               });
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

  // load geojson data as a layer
  // see https://gis.stackexchange.com/questions/373811/create-geojson-layer-based-on-remote-server-request-arcgis-js-api
  // inletQuery.outFields = [ "factype", "id", "POPULATION", "(POPULATION / AREA) as 'POP_DENSITY'" ];
  // inletQuery.outFields = [ "factype", "id", "subfactype", "size", "dwgno", "material", "facid"];
  // Click listener for when user clicks on a result list entry,
  // zooms to feature and opens popup
  // function traceResultClickHandler(event) {
  //   const target = event.target;
  //   const resultId = target.getAttribute("value");
  //
  //   // get the graphic corresponding to the clicked item
  //   const result =
  //     resultId && graphics && graphics[parseInt(resultId, 10)];
  //   if (result) {
  //     view.popup.open({
  //       features: [result],
  //       location: result.geometry
  //     });
  //     // Zoom to feature
  //   }
  // };
