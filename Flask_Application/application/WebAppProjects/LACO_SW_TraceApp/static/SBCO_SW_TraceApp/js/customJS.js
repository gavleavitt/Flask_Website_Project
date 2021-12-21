/*jshint esversion: 6 */
// Set global variables
var btnActive = "inactive";
var userLat = null;
var userlon = null;
var serverResponse = null;
var map = null;
var view = null;
var blockBtn = "inactive"
var blockList = []
var layerListCalls = []
var gravMainsTileURL = "https://vectortileservices3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/gravity_mains_vector_tile_layer/VectorTileServer/tile/{z}/{y}/{x}.pbf"
const USERBOOKMARK_KEY = "arcgis-local-bookmarks";
// var activeLayerIDs = []
var layerObj = null;
// var selectionLayer = null
// var resultslayer = null
function getExtents(obj){
  extents = []
  Object.values(obj).forEach((item) => {
    item.queryExtent().then((response) => {
      extents.push(response.extent)
    });
  });
  return extents
};
function calculateExtents(extents){
  console.log(extents)
};
function addToLocalBKStorage(bks){
  const rawBookmarks = bks.bookmarks.map(({ active, extent, name, thumbnail }) => ({ active, extent, name, thumbnail }));
  const localData = localStorage.setItem(USERBOOKMARK_KEY, JSON.stringify(rawBookmarks));
}
// function addToLocalBKStorage(bks, presetuids){
//   // TODO: remove default bookmarks from bks variable before mapping
//   // bks.bookmarks.forEach((e, i) => {
//   // Remove preset bookmarks from bks.bookmarks object
//   // console.log(bks)
//   // removeList = []
//   // bks.bookmarks.items.forEach((e,i)=> {
//   //   if (presetuids.includes(e.uid)) {
//   //     removeList.push(i)
//   //   }
//   // })
//      bks.boomarks.items.splice(presetuids.length)
//   // const rawBookmarks = bks.bookmarks.map(({ active, extent, name, thumbnail }) => ({ active, extent, name, thumbnail }));
//   const rawBookmarks = userBKs.bookmarks.map(({ active, extent, name, thumbnail }) => ({ active, extent, name, thumbnail }));
//   console.log(userBKs)
//   // const localData = localStorage.setItem(BOOKMARK_KEY, JSON.stringify(rawBookmarks));
//   // console.log(JSON.stringify(rawBookmarks))
// }

require(["esri/config", "esri/Map", "esri/layers/VectorTileLayer", "esri/views/MapView", "esri/layers/TileLayer", "esri/Graphic", "esri/layers/GraphicsLayer", "esri/layers/WebTileLayer", "esri/layers/GeoJSONLayer", "esri/symbols/SimpleMarkerSymbol", "esri/renderers/UniqueValueRenderer", "esri/renderers/SimpleRenderer", "esri/widgets/LayerList", "esri/layers/GroupLayer", "esri/rest/support/Query", "esri/widgets/Search", "esri/layers/FeatureLayer", "esri/widgets/Bookmarks", "esri/widgets/Expand","esri/layers/TileLayer", "esri/symbols/CIMSymbol", "esri/layers/support/LabelClass", "esri/layers/MapImageLayer", "esri/Basemap", "esri/rest/support/Query", "esri/geometry/Extent", "esri/geometry/Point", "esri/widgets/Locate","esri/portal/Portal","esri/identity/OAuthInfo","esri/identity/IdentityManager","esri/portal/PortalQueryParams", "esri/layers/Layer", "esri/widgets/Print", "esri/widgets/FeatureTable","esri/widgets/TableList", "esri/widgets/FeatureTable/Grid/support/ButtonMenu"],
  function (esriConfig, Map, VectorTileLayer, MapView, TileLayer, Graphic, GraphicsLayer, WebTileLayer, GeoJSONLayer, SimpleMarkerSymbol, UniqueValueRenderer, SimpleRenderer, LayerList, GroupLayer, Query, Search, FeatureLayer, Bookmarks, Expand, TileLayer, CIMSymbol, LabelClass, MapImageLayer, Basemap, Query, Extent, Point, Locate, Portal, OAuthInfo, esriId, PortalQueryParams, Layer, Print, FeatureTable, TableList, ButtonMenu) {

      // https://developers.arcgis.com/javascript/latest/sample-code/widgets-layerlist-actions/
      function defineActions(event) {
        // For some reason this gets called multiple times and each call only shows the top level layer item
        // Only use the first call, else skip
        if (layerListCalls.indexOf(event.item.title) > -1) {
             return false;
        } else {
          // Event call hasnt been handled yet, add to list and process
             layerListCalls.push(event.item.title);
        }
        if (event.item.title == "Trace Results"){
          event.item.open = true
          event.item.children.forEach((item, i) => {
            item.open = true
            // console.log(item.title)
            layerListCalls.push(item.title)
            item.actionsSections = [
                [
                  {
                    // This allows the user to turn the table on
                    title: "Show table",
                    className: "esri-icon-table",
                    id: `${item.title}`,
                    // type: "toggle"
                    type: "button"
                  }
                ]
              ];
          });
        }
      }

      // function addTables(obj, layerList, groupLayer){
      //   console.log(groupLayer)
      //   Object.keys(obj).forEach((e)=>{
      //     // Check if table is in table list and is defined
      //     if (e !== undefined && layerList.includes(e)){
      //       // Create feature table object
      //       const featureTable = new FeatureTable({
      //         view: view, // The view property must be set for the select/highlight to work
      //         layer: obj[e],
      //         title: e,
      //         // container: "tableDiv"
      //       });
      //       // Query layer list entry that matches the feature layer
      //       // document.querySelectorAll
      //     }
      //   });
      // };

      function getActiveLayerIDs(){
        // Get list of IDs of all layers in the map
        activeLayerIDs = []
        map.layers.forEach((item, i) => {
            activeLayerIDs.push(item.id)
          }
        );
        return activeLayerIDs
      };

      function buildResultsDisplay(geojsonlyr, calciteWindowID, titleText){
        // Check if geojson layer exits, skip if not
        if (geojsonlyr !== undefined){
          // empty object to hold results
          var results = new Object();
          // New blank query to be populated with settings
          query = new Query();
          // Set where clause
          query.where = `factype = '${titleText}'`;
          // Set output fields
          // query.outFields = [ "factype", "id", "facsubtype", "facid", "linearpipefeetfromstart", "uuid"];
          query.outFields = ["*"]
          // Return feature geometry
          query.returnGeometry = true;
          // Query features within geojson layer, async
          geojsonlyr.queryFeatures(query)
          .then(function(response){
              // Get object of results
              // Get record count
              results.count = Object.keys(response.features).length
              features = response.features;
              results.f
              // Update accordian title to show Count
              document.getElementById(calciteWindowID).setAttribute("heading", `${titleText} (${results.count})`);
              // Remove disabled status
              document.getElementById(calciteWindowID).removeAttribute("disabled");
              document.getElementById("DownloadCSV").removeAttribute("disabled");
              document.getElementById("DownloadGeoJSON").removeAttribute("disabled");
              totalLen = 0
              // Loop over each feature in result
              features.forEach((result, index)=>{
                // Pull out attributes
                attr = result.attributes;
                // Create a calcite pick list item to hold record result
                item = document.createElement("calcite-pick-list-item");
                // Set label (title) to facid
                item.setAttribute("label", attr.facid);
                // Set value key to index value
                item.setAttribute("value", index);
                // Add to service results
                // type = `Inlet Type: ${attr[facsubtype]}`;
                // Set asset type text
                // type = `Type: ${attr.facsubtype}`;
                // bulild out description text based on asset type
                if (["Inlets", "Maintenance Holes"].includes(attr.factype)){
                  description = `Type: ${attr.facsubtype}`;
                } else {
                  size =  `Size: ${attr.size}`;
                  material = `Material: ${attr.material}`
                  pipeLen = (parseFloat(attr.linearpipefeetfromstart)).toFixed(1)
                  totalLen += pipeLen
                  description = size + "\n" + material  + "\n" + `Pipe Length (ft): ${pipeLen}`;
                }
                var newNode = document.createElement('div');
                // Add description text to calcite item
                item.setAttribute("description", description);
                // Set the feature's uuid as an attribute to be called later
                item.setAttribute("uuid", attr.uuid);
                // Add event listener to calcite item to open and zoom to popup
                item.addEventListener("click", function(){
                  // Get the clicked feature's uuid
                  uuid = this.getAttribute("uuid")
                  // networklayer.layers.items.forEach(i=>console.log(i.title))
                  // Iterate over each layer in the network group and query its features to find the matching UUID
                  // flatten layers in network layer, pulls out nested layers
                  let flatNetwork = map.layers.flatten(function(item){
                    return item.layers || item.sublayers;
                  });
                  console.log(flatNetwork)
                  flatNetwork.forEach((e,i)=> {
                  // networklayer.layers.items.forEach((e,i)=> {
                    // console.log(e);
                    // Create an empty query
                    if (e.declaredClass == "esri.layers.FeatureLayer"){
                      let query = e.createQuery();
                      // Set where parameter, query matching uuid
                      query.where = `uuid = '${uuid}'`;
                      // query.returnGeometry = true;
                      // query.returnQueryGeometry = true;
                      // Execute query, async, and process results
                      e.queryFeatures(query)
                        .then((res)=>{
                          // Check if result has any features
                          if (res.features.length >0){
                            feat = res.features[0]
                            // check if result is a point or polyline feature, if polyline calculate its midpoint and replace result geometry with the point
                            if (res.geometryType == "polyline"){
                              feat.geometry = feat.geometry.extent.center
                            }
                            view.popup.open({
                              // fetchFeatures: true, // <- fetch the selected features (if any)
                              location:feat.geometry,
                              features: [feat],
                            });
                            view.goTo(feat.geometry)
                          }
                        });
                    }

                  })
                });
                // Append new calcite item to existing results panel
                document.getElementById(calciteWindowID).appendChild(item);
              });
              // TODO: Update results display with total length, depending on if lateral or main
            });
            //
          } else {
            // Result is not populated, set empty results and disable calcite ollapsible
            // console.log("Setting empty results")
            document.getElementById(calciteWindowID).setAttribute("heading", titleText);
            document.getElementById(calciteWindowID).setAttribute("disabled", "");
            document.getElementById("DownloadCSV").setAttribute("disabled", "");
            document.getElementById("DownloadGeoJSON").setAttribute("disabled", "");
          }
        }

      // esriConfig.apiKey = "AAPK5f601af9967543d6bc498db5a6b0f84bpHLpA-1hb11KUYm2IfzgmzBATsNlgD24Rjueqj2sKqaVsz3d6vU-6-l1yb-0YTi3";
      esriConfig.apiKey = "AAPKbf2fbfc0f4f5469d8520ecee766989aaFU4P9UKZIP2TvrGoyjZRYQleJ6QWxf-ZOQgBBaGjor0zJkHYCEH701bI8oJYzxB4";
      // console.log("Loading vector tiles!");
      // Set empty layer to hold user selection graphics
      var selectionLayer = new GraphicsLayer();
      // Create group layer to hold trace results
      var resultslayer = new GroupLayer();

      const gravityMainsVTL = new VectorTileLayer({
        // title: "Gravity Mains",
        title:"Gravity Mains",
        // Hide from layer list
        listMode: "hide",
        // url: "https://vectortileservices3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/Gravity_Mains_VTL/VectorTileServer",
        url:  "https://vectortileservices3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/GravityMains_VTL/VectorTileServer",
        minScale: 2311162.217155,
        // maxScale: 25000,
        maxScale: 15000
      });
      // Set featurelayers (consider imagelayers instead) to display the storm drain network
      const gravitymainsFeatures = new FeatureLayer({
        title: "Gravity Mains",
        url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/GravityMains_Simplify_2ft/FeatureServer/0",
        listMode: "hide",
        // minScale: 25000,
        minScale: 15000,
        popupTemplate: popupGM,
        renderer: gravityMainsCIM,
        // labelingInfo: [gravityMainsLabels]
      });
      const lateralFeatures = new FeatureLayer({
        title: "Laterals",
        url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/Laterals/FeatureServer/0",
        minScale: 25000,
        popupTemplate: popupLat
      });

      const inletFeatures = new FeatureLayer({
        title: "Inlets",
        // url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/inlets_wgs84/FeatureServer/0",
        url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/Inlets_SHP/FeatureServer/0",
        minScale: 15000,
        popupTemplate: popupIN
      });
      const mhFeatures = new FeatureLayer({
        title: "Maintenance Holes",
        url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/maintenanceholes/FeatureServer/0",
        minScale: 15000,
        popupTemplate: popupMH
      });

       const olFeatures = new FeatureLayer({
        title: "Outlets",
         url: "https://services3.arcgis.com/NfAw5Z474Q8vyMGv/arcgis/rest/services/outlets/FeatureServer/0",
         minScale: 15000
       });

       // Add ancillary data layer as MapImageLayers
       // const laCoParcels = new FeatureLayer({
       // Use image layer instead, data are requested from server as a raster file instead of vector data
       const laCoParcels = new MapImageLayer({
         title: "LA County Parcels",
         // url: "https://public.gis.lacounty.gov/public/rest/services/LACounty_Cache/LACounty_Parcel/MapServer/0",
         url: "https://public.gis.lacounty.gov/public/rest/services/LACounty_Cache/LACounty_Parcel/MapServer",
         minscale: 15000,
         // Not visible by default
         visible: false,
         listMode: "hide",
         // sublayers: [{
         //   id: 0,
         //   labelsVisible: true,
         //   labelingInfo: parcelLabeling
         // }]
       })
       const laCoParcelsSearch = new FeatureLayer({
        title: "LA County Parcels",
        url: "https://public.gis.lacounty.gov/public/rest/services/LACounty_Cache/LACounty_Parcel/MapServer/0",
        listMode: "hide",
       })

       const laCoCities = new MapImageLayer({
       // const laCoCities = new FeatureLayer({
         title: "LA County Cities",
         // url: "https://public.gis.lacounty.gov/public/rest/services/LACounty_Dynamic/Political_Boundaries/MapServer/19",
         url: "https://public.gis.lacounty.gov/public/rest/services/LACounty_Dynamic/Political_Boundaries/MapServer/",
         // url: "https://dpw.gis.lacounty.gov/dpw/rest/services/PW_Open_Data/MapServer",
         sublayers: [{
           id: 19,
           renderer: cityBorder,
           title: "LA County Cities"
           // labelsVisible: true,
           // labelingInfo: cityLabel,
         }]
         // labelingInfo: cityLabel,
         // renderer: cityBorder
       })

       const laCoBoundary = new MapImageLayer({
       // const laCoBoundary = new FeatureLayer({
         title: "LA County Boundary",
         url: "https://dpw.gis.lacounty.gov/dpw/rest/services/PW_Open_Data/MapServer",
         // url: "https://dpw.gis.lacounty.gov/dpw/rest/services/PW_Open_Data/MapServer/13",
         sublayers: [{
           id: 13,
           renderer: countyBorder,
           title: "LA County Boundary"
         }]
       })

       const riversChannels = new MapImageLayer({
       // const riversChannels = new FeatureLayer({
         title: "Major Rivers and Channels",
         // url: "https://dpw.gis.lacounty.gov/dpw/rest/services/dynamicLayers/MapServer/1",
         url: "https://dpw.gis.lacounty.gov/dpw/rest/services/dynamicLayers/MapServer",
         visible: false,
         sublayers: [{
           id: 1,
         }]
       })

       const watersheds = new MapImageLayer({
       // const watersheds = new FeatureLayer({
         title: "Watersheds",
         url: "https://dpw.gis.lacounty.gov/dpw/rest/services/dynamicLayers/MapServer",
         visible: false,
         sublayers: [{
           id: 0,
           title: "Watersheds"
         }]
       })

       // Add featurelayer for parcels which are traced, this featurelayer will not be displayed directly, instead it will be called with a active filter based on the trace query
       // This is done as a workaround for queries which exceed the server's feature limit
       const laCoParcelsFilter = new FeatureLayer({
         title: "Possible Source Parcels",
         url: "https://public.gis.lacounty.gov/public/rest/services/LACounty_Cache/LACounty_Parcel/MapServer/0",
         renderer: parcelFilterBorder,
         labelingInfo: parcelFilterLabel,
         popupTemplate: popupfilteredparcels
       })

       gravityMainsGrouped = new GroupLayer({
         id: "gmgroup",
         title: "Gravity Mains",
         layers: [gravitymainsFeatures,gravityMainsVTL],
         visibilityMode: "inherited"
       })

       parcelsGrouped = new GroupLayer({
         id:"parcelgroup",
         title: "LACO Parcels",
         visible: false,
         layers: [laCoParcels, laCoParcelsSearch],
         visibilityMode: "inherited"
       })
       // Add group layer for the network reference data
      const networklayer = new GroupLayer({
          id: "networklayer",
          title: "Storm Network",
          layers: [lateralFeatures, gravityMainsGrouped, inletFeatures, mhFeatures, olFeatures]
          // layers: [lateralFeatures, gravitymainsFeatures, inletFeatures, mhFeatures, olFeatures]
        });

        // Add group data for the ancillary data
        const ancilData = new GroupLayer({
          id: "AncilGroup",
          title: "Ancillary Data",
          layers: [laCoCities, laCoBoundary, riversChannels, watersheds, parcelsGrouped],
          visible: true
        })


      // Add customized esri topo basemap as a vector tile layer using its AGOL ID
      // Doesnt appear to render properly in print tool, removed for now
      // const customVTL = new VectorTileLayer({
      //   portalItem: {
      //     id: "3fa74fed129c4276ac3bf41eefdad6ac",
      //     title: "Basemap"
      //   }
      // });
      //
      // // create basemap object from vector tile layer
      // const custombasemap = new Basemap({
      //   baseLayers: [
      //     customVTL,
      //   ],
      //   title: "Basemap"
      // });

      // Init map with the custom vector basemap
      const map = new Map({
        basemap: "arcgis-topographic", // Basemap layer service
        // Custom edited basemap
        // basemap: custombasemap,
        layers: [networklayer, ancilData] // vector tile layer
      });
      // Create mapview using the map
      const view = new MapView({
        map: map,
        center: [-118.167416, 34.00], // Longitude, latitude
        zoom: 8, // Zoom level
        container: "viewDiv", // Div element
      });

      // Use default popup templates, as set in the featurelayer on AGOL
      view.popup.defaultPopupTemplateEnabled = true;
      // Add window for viewing current zoom scale
      // Move zoom to buttom left
      // view.ui.move("zoom", "bottom-right");
      view.ui.move("zoom", "manual");
      view.ui.add(vScale, {
        index: 0,
        // position: 'bottom-right'
        position: 'manual'
      });
      let existingData = [];
      // Get existing user bookmarks
      const userBookmarks = localStorage.getItem(USERBOOKMARK_KEY);
      // console.log(existingBookmarks)
      if (userBookmarks) {
        parsedBookmarks = JSON.parse(userBookmarks);
        // existingData.push(...presetBks)
        // Combine user bookmarks with preset bookmarks
        // combinedBookmarks = parsedBookmarks.concat(presetBks);
        presetLength = presetBks.length
      } else {
        parsedBookmarks = presetBks
      }
      // Create bookmarks widget
      const bookmarks = new Bookmarks({
        view: view,
        // allows bookmarks to be added, edited, or deleted
        editingEnabled: true,
        bookmarks: parsedBookmarks
      });
      // Get array of uids associated with the preset BKs
      // presetList = bookmarks.bookmarks.items.slice(0,presetLength)
      // presetuids = []
      // presetList.forEach((e)=>{
      //   presetuids.push(e.uid);
      // })

      // Create an expand widget containing the bookmarks widget
      const bkExpand = new Expand({
         view: view,
         content: bookmarks,
         expanded: false,
         container: document.createElement("bkExpand"),
       });
       // Add expand widget to UI
      view.ui.add(bkExpand, "top-right", 0);
      console.log(bookmarks.bookmarks);
      console.log(bookmarks)

      // See: https://codepen.io/kellyhutchins/pen/ExjPGQe
      // https://odoe.net/blog/custom-bookmarks-in-your-arcgis-js-api-apps
      // https://odoe.net/blog/custom-bookmarks-in-your-arcgis-js-api-apps
      view.when(function () {
        bookmarks.bookmarks.on("change", function (evt) {
          evt.added.forEach(function (e) {
            addToLocalBKStorage(bookmarks)
          });
          evt.removed.forEach(function (e) {
            addToLocalBKStorage(bookmarks)
          });
          evt.moved.forEach(function (e) {
            addToLocalBKStorage(bookmarks)
          })
        });
    })
    //   view.when(function () {
    //     bookmarks.bookmarks.on("before-remove", function (evt) {
    //       if (presetuids.includes(evt.item.uid)){
    //         evt.preventDefault();
    //       }
    //       })
    //     bookmarks.bookmarks.on("before-add", function (evt) {
    //       if (presetuids.includes(evt.item.uid)){
    //         evt.preventDefault();
    //       }
    //     })
    //     bookmarks.bookmarks.on("before-change", function (evt) {
    //       if (presetuids.includes(evt.item.uid)){
    //         evt.preventDefault();
    //       }
    //     })
    //     bookmarks.bookmarks.on("change", function (evt) {
    //       evt.added.forEach(function (e) {
    //         addToLocalBKStorage(bookmarks, presetuids)
    //       });
    //       evt.removed.forEach(function (e) {
    //         addToLocalBKStorage(bookmarks, presetuids)
    //       });
    //       evt.moved.forEach(function (e) {
    //         addToLocalBKStorage(bookmarks, presetuids)
    //       })
    //     });
    // });

       // Create search widget using the map view as the source
       // see https://developers.arcgis.com/javascript/latest/sample-code/widgets-search-multiplesource/
       const searchWidget = new Search({
         view: view,
         autoSelect: true,
         sources: [
           {
             layer:inletFeatures,
             searchFields: ["eqnum","uuid", "dwgno"],
             name: "Inlets"
           },
           {
             layer:mhFeatures,
             searchFields: ["eqnum","uuid","dwgno","jhsrc", "name"],
             name: "Maintenance Holes"
           }, {
             layer:gravitymainsFeatures,
             searchFields: ["eqnum","uuid","dwgno","jhsrc", "name", "pmnum"],
             name: "Gravity Mains"
           }, {
             layer:lateralFeatures,
             searchFields: ["eqnum","uuid","dwgno","jhsrc", "name"],
             name: "Laterals"
           }, {
             layer:olFeatures,
             searchFields: ["eqnum","uuid","dwgno", "name", "outfall_id"],
             name: "Laterals"
           },
           {
             layer:laCoParcelsSearch,
             searchFields: ["AIN","APN"],
             name: "Parcels"
           }
         ]
       });
       // Add search widget to ui
       view.ui.add(searchWidget, {
         position: "top-right",
         index: 2
       });

      view.ui.add("traceDiv", "top-left");

      layerList = new LayerList({
        view: view,
        listItemCreatedFunction: defineActions
      });
      layerList.on("trigger-action", (event) => {
        // Clear out any existing tables
        document.getElementById("tableDiv").innerHTML = ""
        try {
          const featureTable = new FeatureTable({
            view: view, // The view property must be set for the select/highlight to work
            layer: layerObj[event.action.id],
            title: event.action.id,
            container: "tableDiv",
            id: "table"
          });
        }
        catch(e){
          console.log("Table error")
        }
        // Display table container
        document.getElementById("tableContainer").style.display = "flex"
        // Add event listener to close table container
        document.getElementById("closeTab").addEventListener("click", function(){
          document.getElementById("tableContainer").style.display = "none"
        })
        // see: https://developers.arcgis.com/javascript/latest/sample-code/sandbox/?sample=widgets-featuretable-popup-interaction
        // add pop interactions to feature table
        // if (event.action.value == true){
        //
        //
        //   // Turn off any other tables
        // } else {
        //   console.log("turn table off")
        //   document.getElementById("tableContainer").style.display = "none"
        //   // document.getElementById("tableDiv").innerHTML = ""
        // }
        // Create table using event id
      })

      view.ui.add(layerList, "top-right", 3);

      let locateWidget = new Locate({
        view: view,   // Attaches the Locate button to the view
        container: document.createElement("locateWidget"),
        graphic: new Graphic({
          symbol: { type: "simple-marker" }  // overwrites the default symbol used for the
          // graphic placed at the location of the user when found
        })
      });

      // Add locate widget
      view.ui.add(locateWidget, {
        position: "manual",
        index: 0
      });
      // Add print widget
      const print = new Print({
        view: view,
        templateOptions: {
          legendEnbaled: false,
          attributionEnabled: false
        },
        printServiceUrl:
           "https://utility.arcgisonline.com/arcgis/rest/services/Utilities/PrintingTools/GPServer/Export%20Web%20Map%20Task"
      });
      const printExpand = new Expand({
         view: view,
         content: print,
         expanded: false,
         container: document.createElement("printExpand"),
         mode:"auto"
       });
       // Add expand widget to UI
      view.ui.add(printExpand);


      // const tabList = new Expand({
      //    view: view,
      //    content: "",
      //    expanded: false,
      //    container: document.createElement("tabList"),
      //    mode:"auto"
      //  });


      // const attrTab new FeatureTable({
      //   view: view, // The view property must be set for the select/highlight to work
      //   layer: featureLayer,
      //   container: "tableDiv"
      // })
      // // Attribuet Table expand
      // const attrTabExpand = new Expand({
      //    view: view,
      //    content: attrTab,
      //    expanded: false,
      //    container: document.createElement("attrTabExpand"),
      //    mode:"auto"
      //  });
      //  view.ui.add(attrTabExpand);


      // Watch scale/zoom changes, update current scale display
      view.watch('scale', function(evt){
        document.getElementById('vScale').innerHTML = '1:' + evt.toFixed(2);
      });

      view.on("click", (event) => {
        // console.log("click event: ", event);
        console.log("x(lon):", event.mapPoint.x.toFixed(2));
        console.log("y(lat):", event.mapPoint.y.toFixed(2));
        // esriTilequery([event.mapPoint.longitude, event.mapPoint.latitude], gravMainsTileURL)
        document.getElementById("NoSelAlert").removeAttribute('active');
        console.log(blockBtn);
        // Check if selection button is active
        if (btnActive === "active"){
          // Disable popups, stops popup window when selecting a new start location
          view.popup.autoOpenEnabled = false;
          // Set global variables of user's selection:
          userLong = event.mapPoint.longitude;
          userLat = event.mapPoint.latitude;
          // Remove existing selection layer
          map.remove(selectionLayer);
          view.graphics.remove(selectionLayer);
          console.log("Selection is active!");
          // Create selection poinot graphic at the user's selection location
          const selectionpoint = new Graphic({
            title:"Start Point",
            geometry: {
               type: "point",
               longitude: event.mapPoint.longitude,
               latitude: event.mapPoint.latitude
             },
             symbol: selectionMarkerSymbol
          });
          // Add graphic to GraphicsLayer
          selectionLayer = new GraphicsLayer({
            id: "selectionLayer",
            title: "Selected Start Point",
            graphics: [selectionpoint]
          });
          // Add GraphicsLayer to map
          map.add(selectionLayer);
          // Set bottom back to inactive
          btnActive = null;
        }
        // Active block button logic
        if (blockBtn==="active"){
          view.popup.autoOpenEnabled = false;
          // Add block lnglat array
          // blockList.push({"lng":event.mapPoint.longitude,"lat":event.mapPoint.latitude})
          blockList.push([event.mapPoint.longitude,event.mapPoint.latitude])
          console.log("Block selection active!")
          // Create a graphic point at the block location
          const blockPoint = new Graphic({
            title:"Block Points",
            geometry: {
               type: "point",
               longitude: event.mapPoint.longitude,
               latitude: event.mapPoint.latitude
             },
             symbol: blockingMarkerSymbol
          });
          // If blocking layer doesn't exist in the map, create it
          if (!getActiveLayerIDs().includes("blockingLayer")){
            blockingLayer = new GraphicsLayer({
              id: "blockingLayer",
              title: "Selected Block Points"
            });
            // Add layer to map
            map.add(blockingLayer);
          }
          // Add new block point to blocking layer
          blockingLayer.graphics.add(blockPoint);
        }
        // Re-enable popups, if disabled for button usage
        view.popup.autoOpenEnabled = true;
      });

      // Add event listener for cursor movement, change cursor if selection is active
      document.addEventListener("pointermove", function(){
        if ((btnActive === "active") ||(blockBtn === "active")){
          // console.log("crosshair cursor active!")
          // Set crosshair cursor
          document.body.style.cursor = "crosshair";
          // Disable popups
          view.popup.autoOpenEnabled = false;
        } else {
            document.body.style.cursor = "default";
            view.popup.autoOpenEnabled = true;
            // Enable popups
          }
      });
      // Add listener to selection button
      document.getElementById("selBtn").addEventListener("click", function(){
        // console.log("selection active!");
        userLat = null;
        userlon = null;
        btnActive = "active";
        blockBtn = "inactive";
        // clear existing user selection location
        if (getActiveLayerIDs().includes("selectionLayer")){
          map.remove(selectionLayer);
          view.graphics.remove(selectionLayer);
        }
      });
      // Add event listener to flow block button
      document.getElementById("block-Btn").addEventListener("click", function(){
        // console.log("Block selection active!");
        blockBtn = "active";
        btnActive = "inactive";
      });
      // Create clear button funtionality
      document.getElementById("clearBtn").addEventListener("click", function(){
              // console.log("Clearing results!")
              // Remove results and selection layers from the map and view
              map.remove(selectionLayer);
              map.remove(resultslayer);
              view.graphics.remove(selectionLayer);
              view.graphics.remove(resultslayer);
              // Clear out feature tables
              document.getElementById("tableDiv").innerHTML = ""
              document.getElementById("tableContainer").style.display = "none"
              // Check if blocking layer exists, if so remove it from map and graphics
              if (getActiveLayerIDs().includes("blockingLayer")){
                // console.log("Map has blocking points!")
                map.remove(blockingLayer);
                view.graphics.remove(blockingLayer);
              }
              // Close any open popups
              view.popup.close();
              // Close out any alerts
              document.getElementById("NoSelAlert").removeAttribute('active');
              document.getElementById("NoResultAlert").removeAttribute('active');
              // Reset user lng/lat
              userLat = null;
              userlon = null;
              btnActive = "inactive";
              blockBtn = "inactive";
              blockList = [];
              // inletResults, outletResults, mhResults, gmResults, latResults = null;
              // Hide results window
              document.getElementById("results-grp").style.display = "none";
              // Get list of results to remove, using their calcite attribute
              document.querySelectorAll("calcite-pick-list-item").forEach(e => e.remove());
            }
          )

      document.getElementById("submitBtn").addEventListener("click", function(){
            // Close out any alerts
            document.getElementById("NoSelAlert").removeAttribute('active');
            document.getElementById("NoResultAlert").removeAttribute('active');
            // clear out any layerlist call information
            layerListCalls = []
            btnActive = "inactive";
            blockBtn = "inactive";
            // Clear out existing graphic layers
            map.remove(resultslayer);
            // Check if a point has been clicked, if not return message
            if (userLat === null){
              //Turn alert on
              document.getElementById("NoSelAlert").setAttribute('active','');
              return;
            }
            // Get the active radio selection to determine flow direction
            radioGrp = document.querySelector('#directionGrp');
            traceDirection = radioGrp.querySelectorAll(":checked")[0].defaultValue;
            // Set server request URL
            // var url = new URL('http://leavittmapping.com/api/v1/trace/lacostormwater');
            // var url = new URL('http://api.leavitttesting133.com:5000/api/v1/trace/lacostormwater');
            // Set query parameters
            var params = {"latitude":userLat, "longitude":userLong, "direction":traceDirection};
            // Check if parcel filter opton has been selected, set param
            if (document.getElementById("parcel-btn").hasAttribute("checked")){
              params["parcels"] = "true"
            } else {
              params["parcels"] = "false"
            };
            // Create GET querly string based on parameters
            searchQuery = new URLSearchParams(params)
            // if blocklist exists, add each to query parameters
            if (blockList.length > 0){
              blockList.forEach((item, i) => {
                // Add to GET query parameters, key value is repeated for each item
                searchQuery.append('blocklnglats',item)
              });
            }
            console.log(traceurl)
            console.log(JSON.stringify(traceurl))
            // Add GET parameters to GET request string
            traceurl.search = searchQuery.toString();
            console.log(traceurl)
            console.log(JSON.stringify(traceurl))
            // Set Query active text to active
            document.querySelector('#query-text').style.display = "block";
            // Issue Async request
            fetch(traceurl, {method: "GET",
              mode: 'cors'})
            .then(r => {
              console.log("waiting on fetch")
              // Returns data as json, I think this has to be done in a .then statement
              return r.json();
            })
            // Pass result json data into a generic function
            .then(function(data){
              console.log("handling fetch{}")
              // Change variable name
              serverResponse = data
              // Object to hold ArcGIS JS API geojson formatted layers, reset on every server request
              layerObj = {}
              function addGeoJson(geojson, title, popupTemplate){
                // Takes geojson result features returned from server and brings them in as object URLs since the GeoJSONLayer function expects a seperate URL
                // for each layer, not one URL for all
                // check if geojson result is populated, if so process
                if (geojson['features'].length > 0) {
                  // Make a blob object of geojson formatted data
                  const blob = new Blob([JSON.stringify(geojson)], {type: "application/json"});
                  // Make a temporary URL that points to the client-side stored previously created blob feature
                  const url  = URL.createObjectURL(blob);
                  // Create a GeoJSON layer using provided popupTemplate and previously set renderer template
                  const result = new GeoJSONLayer({
                    url:url,
                    title:title,
                    renderer:resultsrenderer,
                    popupTemplate: null,
                    id: `${title}-resultslayer`
                    // popupTemplate: popupTemplate
                  });
                  // Add new geojson layer to result layerObj
                  layerObj[title] = result;
                }
              }

              // Process geojson result layers provided by server
              addGeoJson(data['Gravity Mains'], 'Gravity Mains', null)
              addGeoJson(data['Laterals'], 'Laterals', null)
              addGeoJson(data['Inlets'], 'Inlets', null)
              addGeoJson(data['startpoint'], 'Start Point', null)
              addGeoJson(data['Outlets'], 'Outlets', null)
              addGeoJson(data['Maintenance Holes'], 'Maintenance Holes',null)
              // Process parcel OID results, if provided in request
              if ("parcels" in data){
                // Convert results into string SQL statement
                sql = 'OBJECTID IN ('
                // Iterate over each OID in list, buildng out string
                data['parcels'].forEach((item, i) => {
                  sql += `${item},`
                });
                // Remove last comma and add right ) to complete statement
                sql = sql.substring(0,sql.length-1)
                sql += ")"
                // let parcelQuery = laCoParcelsFilter.createQuery();
                // parcelQuery.where = sql
                // parcelQuery.outFields = ["APN"]
                // parcelQuery.returnGeometry = true;
                // laCoParcelsFilter.queryFeatures(parcelQuery)
                // .then(function(response){
                //   console.log(response)
                // });
                // Filter results parcel layer, this is a seperate layer than the ancillary parcels dataset
                laCoParcelsFilter.definitionExpression = sql
                // Add filtered parcel layer to map by adding it to the results layer object
                layerObj['Filtered Parcels'] = laCoParcelsFilter;
              }
              // Check if suberwatersheds were included in response, if so add to map
              if ("subwatersheds" in data){
                addGeoJson(data['subwatersheds'], "Subwatersheds", null)
              }

              // Add results as a group layer
              resultslayer = new GroupLayer({
                id: "resultslayer",
                title: "Trace Results",
                // Add all layerobj values as layers
                layers: Object.values(layerObj)
              });
              // Add group layer to map
              map.add(resultslayer);
            //   resultslayer
            //   .when(()=>{
            //     console.log(resultslayer)
            //   }
            // )
            // Array to hold promises
            var extents = []
            // Iterate over each geojson feature layer
            Object.values(layerObj).forEach((item)=>{
              // Push each query promise to array
              extents.push(item.queryExtent())
              // item.queryExtent().then((response) => {
                // extents.push(response.extent)
                // console.log(response.extent)
                // });
            });
            // Process extents after the promises have resolved
            Promise.all(extents).then((values) => {
              // Clone first extent to build out a properly formatted extent object
              totalExtent = values[0].extent.clone()
              // Iterate over extents, unioning them to the next result, this will expand the extent to include all results
              values.forEach((item) => {
                // Check if values are within normal WGS ranges, some layers appear to be in a web mercator
                if (item.extent.xmax > -190 && item.extent.xmax < 80 && item.extent.ymax > -90 && item.extent.ymax < 90){
                  totalExtent.union(item.extent)
                }
              });
              // Expand extent by 35% to ensure it covers the area
              totalExtent.expand(1.35)
              // Set the view to the new extent
              view.goTo(totalExtent)
            });
            // addTables(layerObj, ["Gravity Mains","Outlets","Inlets","Maintenance Holes"], resultslayer)
            // const tableList = new TableList({
            //     map: map, // get access to the map which has the collection of tables
            //     selectionEnabled: true,
            //     listItemCreatedFunction: createActions // call createActions function to set ActionToggle and ActionButton
            //   });
            // console.log(tableList);
            // const tableExpand = new Expand({
            //     view: view,
            //     content: tableList,
            //     container: document.createElement("tableExpand"),
            //     expandIconClass: "esri-icon-table",
            //     // group: "top-right"
            //   });
            //   view.ui.add(tableExpand, "manual")


            // Set Query text to inactive
            document.querySelector('#query-text').style.display = "none";
            // Replace base html item with itself, this will remove any existing event listeners from previous runs
            document.getElementById("DownloadCSV").outerHTML = document.getElementById("DownloadCSV").outerHTML
            document.getElementById("DownloadGeoJSON").outerHTML = document.getElementById("DownloadGeoJSON").outerHTML
            // Add event listener to downlaod CSV button
            document.getElementById("DownloadCSV").addEventListener("click", function(){
              createCSV(data)
            });
            // Add event listener to downlaod GeoJSON button
            document.getElementById("DownloadGeoJSON").addEventListener("click", function(){
              createGeoJSONZIP(data)
            });

            // Set total linear pipe feet, broken up by mains and laterals

            // Build out Calcite block results window
            buildResultsDisplay(layerObj['Gravity Mains'], 'GM-Window', 'Gravity Mains')
            buildResultsDisplay(layerObj['Laterals'], 'Lat-Window', 'Laterals')
            buildResultsDisplay(layerObj['Inlets'], 'InletsWindow', 'Inlets')
            buildResultsDisplay(layerObj['Outlets'], 'OutletsWindow', 'Outlets')
            buildResultsDisplay(layerObj['Maintenance Holes'], 'MH-Window', 'Maintenance Holes')
            // Set result group to display
            document.getElementById("results-grp").style.display = "block";
             })
          // Catch server error and display alert
          .catch(error =>{
            console.log(error)
            console.log("Server request error!")
            // Set query text to error
            document.querySelector('#query-text').style.display = "none";
            document.getElementById("NoResultAlert").setAttribute('active','')
          });
      });
      document.getElementById("upstream-btn").addEventListener("click", function(){
        // Trigger if upstream button is pressed, allow user to select parcel return
        console.log("Upstream clicked!")
        document.getElementById("parcel-label").style.display = "block";
      });

      document.getElementById("downstream-btn").addEventListener("click", function(){
        // Trigger if downstream button is pressed, hide parcel option and set it to inative
        console.log("Downstream clicked!")
        document.getElementById("parcel-label").style.display = "none";
        document.getElementById("parcel-btn").removeAttribute("checked");
      });
      // document.getElementById("toolloader").removeAttribute('active');
  });
;
