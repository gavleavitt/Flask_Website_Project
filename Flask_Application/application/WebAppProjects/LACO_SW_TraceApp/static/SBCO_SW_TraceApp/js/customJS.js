/*jshint esversion: 6 */
var btnActive = null;
var userLat = null;
var userlon = null;
var geojsonData = null;
var map = null;
var view = null;
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
        // Clear out existing graphic layers
        // if (typeof selectionLayer != "undefined"){
        //   selectionLayer.removeAll();
        // };
        // map.removeLayer(map.getLayer("selectionLayer"));
        // map.removeLayer(map.getLayer("resultslayer"));
        // const removelayers = map.allLayers.find(function(layer) {
        //   return layer.title === "Selected Start Point";
        // });
        // const removelayers = map.allLayers.find(function(layer) {
        //   map.remove(layer.title === "Selected Start Point");
        //   map.remove(layer.title === "Trace Results");
        //   // return [layer.title === "Selected Start Point",
        //   //   layer.title === "Trace Results"]
        // });
        //  removeLayers = map.allLayers.find(function(layer){
        //    return layer.title === "Selected Start Point";
        //  })
        // map.removeMany(removelayers);
        // map.allLayers.find(function(layer){
        //   console.log(layer)
        // })
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
            fetch(url, {method: "GET",
              mode: 'cors'})
            .then(r => {
              // Returns data
              return r.json();
            })
            .then(function(data){

              var layerObj = {}

              if (data['Gravity Mains']['features'].length > 0){
                const gmblob = new Blob([JSON.stringify(data['Gravity Mains'])], {type: "application/json"});
                const gmurl  = URL.createObjectURL(gmblob);
                const resultgm = new GeoJSONLayer({
                  url:gmurl,
                  title:"Gravity Mains",
                  renderer:lineResultRenderer,
                  popupTemplate: popupGM
                });
                layerObj['Gravity Mains'] = resultgm;
              }
              const startptblob = new Blob([JSON.stringify(data['startpoint'])], {type: "application/json"});
              const startpturl  = URL.createObjectURL(startptblob);
              const resultstartpt = new GeoJSONLayer({
                url:startpturl,
                title:"Start Point",
                renderer:pointResultRenderer
              });

              if (data['Inlet']['features'].length > 0){
                const inletblob = new Blob([JSON.stringify(data['Inlet'])], {type: "application/json"});
                const inleturl  = URL.createObjectURL(inletblob);
                const resultinlet = new GeoJSONLayer({
                  url:inleturl,
                  title:"Inlets",
                  renderer:pointResultRenderer,
                  popupTemplate: popupInlets
                });
                layerObj['Inlet'] = resultinlet;
              }

              if (data['Outlets']['features'].length > 0){
                const outletblob = new Blob([JSON.stringify(data['Outlets'])], {type: "application/json"});
                const outleturl  = URL.createObjectURL(outletblob);
                const resultoutlet = new GeoJSONLayer({
                  url:outleturl,
                  title: "Outlets",
                  renderer:pointResultRenderer
                });
                layerObj['Outlets'] = resultoutlet;
              }

              if (data['Maintenance Holes']['features'].length > 0){
                const mhblob = new Blob([JSON.stringify(data['Maintenance Holes'])], {type: "application/json"});
                const mhurl  = URL.createObjectURL(mhblob);
                const resultmh = new GeoJSONLayer({
                  url:mhurl,
                  title: "Maintenance Holes",
                  renderer:pointResultRenderer,
                  popupTemplate: popupMHs
                });
                layerObj['Maintenance Holes'] = resultmh;
              }

              if (data['Laterals']['features'].length > 0){
                const latblob = new Blob([JSON.stringify(data['Laterals'])], {type: "application/json"});
                const laturl  = URL.createObjectURL(latblob);
                const resultlat = new GeoJSONLayer({
                  url:laturl,
                  title:"Laterals",
                  renderer:lineResultRenderer,
                  popupTemplate: popupLat
                });
                layerObj['Laterals'] = resultlat;
              }
              resultslayer = new GroupLayer({
                id: "resultslayer",
                title: "Trace Results",
                layers: Object.values(layerObj)
              });
              map.add(resultslayer);
              layerObj['Gravity Mains'].queryExtent().then((response) => {
                view.goTo(response.extent);
              });
              // Set Query text to inactive
              document.querySelector('#query-text').style.display = "none";


              // query features: https://developers.arcgis.com/javascript/latest/api-reference/esri-layers-GeoJSONLayer.html#queryFeatures
              // See https://developers.arcgis.com/javascript/latest/sample-code/featurelayer-query/
              //###### Inlet results ######
              if (data['Inlet']['features'].length > 0){
                var inletResults = new Object();
                inletQuery = new Query();
                inletQuery.where = "factype = 'Inlet'";
                inletQuery.outFields = [ "factype", "id", "facsubtype", "facid"];
                layerObj['Inlet'].queryFeatures(inletQuery)
                .then(function(response){
                    // Get object of results
                    // Get record count
                    inletResults.count = Object.keys(response.features).length
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
                      item.addEventListener("click", function(){
                        const target = event.target;
                        const resultId = target.getAttribute("value");
                        view.popup.open({
                          features: [result],
                          location: result.geometry
                        });

                      });
                      // Append to existing results panel
                      document.getElementById("InletsWindow").appendChild(item);
                    });
                  });
                } else {
                  document.getElementById("InletsWindow").setAttribute("heading", "Inlets")
                }
              // ###### Outlet Results ######
              if (data['Outlets']['features'].length > 0){
                console.log("Outlet results!")
                var outletResults = new Object();
                outletQuery = new Query();
                outletQuery.where = "factype = 'Outlets'";
                outletQuery.outFields = [ "factype", "id", "size", "facid", "material"];
                layerObj['Outlets'].queryFeatures(outletQuery)
                .then(function(response){
                  // Get object of results
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
                    type = `Outlet Type: ${attr.facsubtype}`;
                    size =  `Size: ${attr.size}`;
                    material = `Material: ${attr.material}`
                    description = type + "\n" + size + "\n" + material;
                    item.setAttribute("description", description);
                    // Add event listenr to pick list item, opens popup for feature
                    // item.addEventListener("click", traceResultClickHandler);
                    // Append to existing results panel
                    document.getElementById("OutletsWindow").appendChild(item);
                  });
                });
              } else {
                document.getElementById("OutletsWindow").setAttribute("heading", "Outlets")
              }

              if (data['Maintenance Holes']['features'].length > 0){
                // ###### Maintenance Hole Results ######
                var mhResults = new Object();
                mhQuery = new Query();
                mhQuery.where = "factype = 'Maintenance Holes'";
                mhQuery.outFields = [ "factype", "id", "facid", "facsubtype"];
                layerObj['Maintenance Holes'].queryFeatures(mhQuery)
                .then(function(response){
                  // Get object of results
                  // Get record count
                  mhResults.count = Object.keys(response.features).length
                  features = response.features;
                  // Update accordian title to show Count
                  document.getElementById("MH-Window").setAttribute("heading", `Maintenance Holes (${mhResults.count})`)
                  // Loop over each feature in result
                  features.forEach((result, index)=>{
                    attr = result.attributes;
                    item = document.createElement("calcite-pick-list-item");
                    item.setAttribute("label", attr.facid);
                    item.setAttribute("value", index);
                    // Add to service results
                    // type = `Inlet Type: ${attr[facsubtype]}`;
                    type = `Maintenance Hole Type: ${attr.facsubtype}`;
                    description = type
                    item.setAttribute("description", description);
                    // Add event listenr to pick list item, opens popup for feature
                    // item.addEventListener("click", traceResultClickHandler);
                    // Append to existing results panel
                    document.getElementById("MH-Window").appendChild(item);
                  });
                });
              } else {
                document.getElementById("MH-Window").setAttribute("heading", "Maintenance Holes")
              }

              if (data['Gravity Mains']['features'].length > 0){
                // ###### Gravity Mains Results ######
                var gmResults = new Object();
                gmQuery = new Query();
                gmQuery.where = "factype = 'Gravity Mains'";
                gmQuery.outFields = ["factype", "id", "facid", "size", "material"];
                layerObj['Gravity Mains'].queryFeatures(gmQuery)
                .then(function(response){
                  // Get object of results
                  // Get record count
                  gmResults.count = Object.keys(response.features).length
                  features = response.features;
                  // Update accordian title to show Count
                  document.getElementById("GM-Window").setAttribute("heading", `Gravity Mains (${gmResults.count})`)
                  // Loop over each feature in result
                  features.forEach((result, index)=>{
                    attr = result.attributes;
                    item = document.createElement("calcite-pick-list-item");
                    item.setAttribute("label", attr.facid);
                    item.setAttribute("value", index);
                    // Add to service results
                    // type = `Inlet Type: ${attr[facsubtype]}`;
                    type = `Gravity Main Type: ${attr.facsubtype}`;
                    size = `Size: ${attr.size}`
                    description = type + "\n" + "\n" + size
                    item.setAttribute("description", description);
                    // Add event listenr to pick list item, opens popup for feature
                    // item.addEventListener("click", traceResultClickHandler);
                    // Append to existing results panel
                    document.getElementById("GM-Window").appendChild(item);
                  });
                });
              } else {
                document.getElementById("GM-Window").setAttribute("heading", "Gravity Mains")
              }

              if (data['Laterals']['features'].length > 0){
                // ###### Laterals Results ######
                var latResults = new Object();
                latQuery = new Query();
                latQuery.where = "factype = 'Laterals'";
                latQuery.outFields = [ "factype", "id", "facid", "size", "material"];
                layerObj['Laterals'].queryFeatures(latQuery)
                .then(function(response){
                  // Get object of results
                  // Get record count
                  latResults.count = Object.keys(response.features).length
                  features = response.features;
                  // Update accordian title to show Count
                  document.getElementById("Lat-Window").setAttribute("heading", `Laterals (${latResults.count})`)
                  // Loop over each feature in result
                  features.forEach((result, index)=>{
                    attr = result.attributes;
                    item = document.createElement("calcite-pick-list-item");
                    item.setAttribute("label", attr.facid);
                    item.setAttribute("value", index);
                    // Add to service results
                    // type = `Inlet Type: ${attr[facsubtype]}`;
                    type = `Lateral Type: ${attr.facsubtype}`;
                    size = `Size: ${attr.size}`
                    // material = `Material: ${attr.material}`
                    description = type + "\n" + size
                    item.setAttribute("description", description);
                    // Add event listenr to pick list item, opens popup for feature
                    // item.addEventListener("click", traceResultClickHandler);
                    // Append to existing results panel
                    document.getElementById("Lat-Window").appendChild(item);
                  });
                });
              } else {
                document.getElementById("Lat-Window").setAttribute("heading", "Laterals")
              }
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
