function menuHover(){
  document.getElementById("menu-icon-img").setAttribute('src', '/static/images/menu-icon-blue.svg')
};

function menuUnhover(){
  document.getElementById("menu-icon-img").setAttribute('src', '/static/images/menu-icon-gray.svg')
};

// function closeMenu(){
//   console.log("Scrolling!")
//   var menu = document.getElementsByClassName("navbarright responsive")
//   if (menu.length){
//     menu.className = "navbarright";
//   }
// }

function closeMenu(){
  var menu = document.getElementById("interactiveBarRight")
  if (menu.className = ("navbarright responsive")){
    menu.className = "navbarright";
  }
};

/* Toggle between adding and removing the "responsive" class to navbarright when the user clicks on the icon */
function navBarFunction() {
  var x = document.getElementById("interactiveBarRight");
  if (x.className === "navbarright") {
    x.className += " responsive";
  } else {
    x.className = "navbarright";
  }
};

function onEachFeatureAct(feature,layer) {
  layer.bindPopup(
    "<div class='spanbotbord'><b>" + feature.properties.name + "</b></div>" +
     // "<div><b><a href=https://www.strava.com/activities/" + feature.properties.actID + ">Strava Activity Page</a></b></div>" +
      "<div><b>Type: " + feature.properties.type + "</b></div>" +
    "<div><b>Date (PST): " + feature.properties.startDate + "</b></div>" +
    "<div><b>Duration: " + convertDuration(feature.properties.elapsed_time) + "</b></div>" +
    "<div><b>Distance (Miles): " + (feature.properties.distance * 0.000621371).toFixed(1) + "</b></div>" +
    "<div><b>Elevation gain (Feet): " + (feature.properties.total_elevation_gain * 3.28084).toFixed(1) + "</b></div>" +
    "<div><b>Calories burned: " + feature.properties.calories + "</b></div>" +
    "<div><b>Average speed (mph): " + (feature.properties.average_speed * 2.23694).toFixed(1) + "</b></div>" +
    "<div><b>Activity ID: " + feature.properties.actID + "</b></div>" +
    privatecheck(feature.properties.private, feature.properties.actID)
  )
};


function privatecheck(privacy, actID) {
  if (privacy == "true"){
    res = "<div><b>Private Activity</b></div>"
  } else {
    res = "<div><b><a href=https://www.strava.com/activities/" + actID + ">Strava Activity Page</a></b></div>"
  }
  return res
};

function convertDuration(seconds){
  var date = new Date(null);
  date.setSeconds(seconds);
  var result = date.toISOString().substr(11, 8);
  return result
};

function geartext(gearname) {
  if (gearname){
    res = "<div><b>Bike: " + gearname + "</b></div>"
    return res
  }
};


var mtb_lineStyle = {
  "color": "#e41a1c",
  "weight": 2,
  "opacity": 0.7,
  "fillColor": "black"
};
var road_lineStyle = {
  "color": "#377eb8",
  "weight": 2,
  "opacity": 0.7,
  "fillColor": "black"
};
var run_lineStyle = {
  "color": "#a65628",
  "weight": 2,
  "opacity": 0.7,
  "fillColor": "black"
};
var walk_lineStyle = {
    "color": "#984ea3",
    "weight": 2,
    "opacity": 0.7,
    "fillColor": "black"
};


// function timeFilterActive(){
//   active = document.querySelectorAll('.active:not(#All)')
//   for (var h = 0; h < active.length; h++) {
//
//   }
// }


// Styles linestyles according to their properties
function actStyle(feature, layer) {
  if (feature.properties.type == "Walk") {
    return walk_lineStyle;
  } else if (feature.properties.type == "Run") {
    return run_lineStyle;
  } else if ((feature.properties.type == "Ride") && (feature.properties.type_extended == "Road Cycling")) {
    return road_lineStyle;
  } else if ((feature.properties.type == "Ride") && (feature.properties.type_extended == "Mountain Bike")) {
    return mtb_lineStyle;
  }
};

// Selects active buttons, excluding the "All" button, and interates over them rebuilding the associated geojson layers
function addActiveLayers(userStartDate = null, userEndDate = null) {
  if (document.getElementById('All').className.includes("active") == true) {
    active = document.querySelectorAll('.filterbtn:not(#All)');
    for (var h = 0; h < active.length; h++) {
      actFilter(active[h].id, userStartDate, userEndDate)
    }
  } else {
    active = document.querySelectorAll('.active-btn:not(#All)');
    for (var h = 0; h < active.length; h++) {
      actFilter(active[h].id, userStartDate, userEndDate)
    }
  }
};

// Helper functions called when user clicks a button, button IDs match the strings
// used in the equality statements
function actFilter(actType, userStartDate = null, userEndDate = null){
  // console.log(actType)
  newRaw = orgActivities.toGeoJSON()
  if ((userStartDate == null) && (userEndDate == null)) {
    displayDate = document.getElementById("display-date").textContent.split(" - ");
    userStartDate = moment(new Date(displayDate[0])).format().slice(0,10)
    userEndDate = moment(new Date(displayDate[0])).format().slice(0,10)
  }
  if (actType=="All") {
    filteredGroup.clearLayers()
    filteredAct = L.geoJson(newRaw, {
        style: actStyle,
        onEachFeature: onEachFeatureAct,
        filter: function(feature, layer) {
          if (feature.properties.startDate.slice(0,10) > userStartDate.slice(0,10)) return true
        }
    });
  } else {
    //console.log(newRaw)
    filteredAct = L.geoJson(newRaw, {
        style: actStyle,
        onEachFeature: onEachFeatureAct,
  			filter: function(feature, layer) {
          if (actType == "Walk") {
            if ((feature.properties.type == "Walk") && (feature.properties.startDate.slice(0,10) > userStartDate.slice(0,10))) return true
          } else if (actType == "Run") {
            if ((feature.properties.type == "Run") && (feature.properties.startDate.slice(0,10) > userStartDate.slice(0,10))) return true
          } else if (actType == "MTB") {
            if ((feature.properties.type_extended == "Mountain Bike") && (feature.properties.startDate.slice(0,10) > userStartDate.slice(0,10))) return true
          } else if (actType == "Road") {
            // if ((feature.properties.type == "Road Cycling") && (feature.properties.startDate.slice(0,10) > userStartDate.slice(0,10))) return true
            if ((feature.properties.type_extended == "Road Cycling") && (feature.properties.startDate.slice(0,10) > userStartDate.slice(0,10))) return true
          }
				}
    });
  }
  filteredGroup.addLayer(filteredAct);
};

// Button coloring and filter behavior, allows user to single and multi-select as well add and remove all
// layers with the "All" button.
// This function is loaded asynchronously after the document has loaded in the activity geojson data
function loadActivityListener() {
  // get div that contains the filter buttons
  var group = document.getElementById("act-filter-group");
  // get all buttons within group
  var btns = group.getElementsByClassName("filterbtn");
  // Iterate over buttons in group adding an click event listener to each
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function(obj) {
      //get active buttons, exluding the All button, this is used to determine if multi-selection is occurring
      active = document.querySelectorAll('.active-btn:not(#All)')
      console.log(active)
      // Check to see if button click target is the "All" button and if any other buttons are also flagged as active,
      // if so remove the active class from these buttons (reverting them to disabled opacity) and set the All button
      // to active and add all activity layers to display
      if ((obj.target.id == "All") && (active.length > 0)) {
        console.log("case A")
        // iterate over buttons flagged as active
        for (var h = 0; h < active.length; h++) {
          // remove active class from buttons, reverting them to disabled opacity
          active[h].className = active[h].className.replace(" active-btn", "");
        }
        // call function to add all activity layers to display
        actFilter("All")
        document.getElementById("All").innerHTML = "Clear all";
        // set "All" button to active
        this.className += " active-btn";
        // change text of "All" to tell user that clicking it will remove all activity layers
        document.getElementById("All").innerHTML = "Clear all";
      // Check if user click target is a button flagged as active
      } else if (obj.target.className.includes("active-btn")) {
        console.log("case B")
        // Remove active class from button, reverting it to the disabled opacity
        this.className = this.className.replace(" active-btn","");
        // If the target was the All button, clear all layers from display
        if (obj.target.id == "All"){
          // change text of "All" to tell user that clicking it will add all activity layers
          document.getElementById("All").innerHTML = "Add all";
          filteredGroup.clearLayers()
        // if user clicks an active button that is not All, remove just that layer from display
        // A dictionary is used for lookup to select the correct layer using the target button's ID value
        } else {
          filteredGroup.clearLayers()
          // Add geojson data for all active buttons
          addActiveLayers()
          document.getElementById("All").innerHTML = "Clear all";
          // filteredGroup.removeLayer(layerGroupDict[obj.target.id]);
        }
      // Check if user click target is NOT the "All" button, but the "All" button is flagged as active
      // Used to determine if a user is selecting activity button when the "All" button is active
      } else if ((!(obj.target.id.includes("All"))) && (document.getElementById("All").className.includes("active-btn"))) {
          console.log("case C")
          // Remove the active flag from the "All" button, reverting to disabled opacity
          document.getElementById("All").className = document.getElementById("All").className.replace(" active-btn", "");
          // change text of "All" to tell user that clicking it will add all activity layers
          document.getElementById("All").innerHTML = "Add all";
          // Set the target button to active
          this.className += " active-btn";
          // Remove all activity layers
          filteredGroup.clearLayers();
          // Add the activity layer associated with the button clicker by the user
          // console.log("Generating a new geojson!")
          actFilter(obj.target.id);
      // Last chase, user is multi-selecting activities, i.e. "All" is disabled and at least one other activity
      // is flagged as active
      } else if ((obj.target.id == "All") && (active.length == 0)) {
        console.log("case D")
        document.getElementById("All").innerHTML = "Clear all";
        this.className += " active-btn";
      } else {
        console.log("case E")
        // Set this activity to active, in addition to other active buttons
        this.className += " active-btn";
        // Add the layer associated with the button clicker by the user.
        // This is added in addition to other active layers
        // console.log("Multi-selecting!")
        actFilter(obj.target.id);
        // console.log(filteredGroup)
      }
    });
  }
};





// function timefiltergeojson(userStartDate, userEndDate) {
//   actLayerGroupfiltered.eachLayer(function(groupLayer) {
//     actLayerGroupfiltered.removeLayer(groupLayer);
//     newraw = groupLayer.toGeoJSON();
//     filteredAct = L.geoJSON(newraw, {
//       style: function(feature, layer) {
//         if (feature.properties.type == "Walk") {
//           return walk_lineStyle;
//         } else if (feature.properties.type == "Run") {
//           return run_lineStyle;
//         } else if ((feature.properties.type == "Ride") && (feature.properties.type_extended == "Road Cycling")) {
//           return road_lineStyle;
//         } else if ((feature.properties.type == "Ride") && (feature.properties.type_extended == "Mountain Bike")) {
//           return mtb_lineStyle;
//         }
//       },
//       onEachFeature: onEachFeatureAct,
//       filter: function (feature, layer) {
//         if (feature.properties.startDate.slice(0,10) > userStartDate.slice(0,10)) return true
//       }
//     }).addTo(map);
//     actLayerGroupfiltered.addLayer(filteredAct);
//   })
// };

// function filterActType(addLayer){
//   actLayerGroupfiltered.addLayer(addLayer);
//   displayDate = document.getElementById("display-date").textContent.split(" - ");
//   userStartDate = moment(displayDate[0]).format().slice(0,10)
//   userEndDate = moment(displayDate[1]).format().slice(0,10)
//   filtergeojson(userStartDate, userEndDate);
// };

// Helper functions called when user clicks a button, button IDs match the strings
// used in the equality statements
// function actFilter(act){
//   if(act=="All"){
//     actLayerGroupfiltered.clearLayers()
//     actLayerGroupfiltered.addLayer(run_act)
//     actLayerGroupfiltered.addLayer(walk_act)
//     actLayerGroupfiltered.addLayer(road_act)
//     actLayerGroupfiltered.addLayer(mtb_act)
//   } else if (act == "MTB") {
//     filterActType(mtb_act)
//   } else if (act == "Road") {
//     filterActType(road_act)
//   } else if (act == "Walk") {
//     filterActType(walk_act)
//   } else if (act == "Run") {
//     filterActType(run_act)
//   }
// };
// Called when date range is changed
// function filtergeojson(userStartDate, userEndDate) {
//   actLayerGroupfiltered.eachLayer(function(groupLayer) {
//     map.removeLayer(groupLayer);
//     newraw = groupLayer.toGeoJSON();
//     L.geoJSON(newraw, {
//       style: function(feature, layer) {
//         if (feature.properties.type == "Walk") {
//           return walk_lineStyle;
//         } else if (feature.properties.type == "Run") {
//           return run_lineStyle;
//         } else if ((feature.properties.type == "Ride") && (feature.properties.type_extended == "Road Cycling")) {
//           return road_lineStyle;
//         } else if ((feature.properties.type == "Ride") && (feature.properties.type_extended == "Mountain Bike")) {
//           return mtb_lineStyle;
//         }
//       },
//       onEachFeature: onEachFeatureAct,
//       filter: function (feature, layer) {
//         if (feature.properties.startDate.slice(0,10) > userStartDate.slice(0,10)) return true
//       }
//     }).addTo(map);
//   })
// };





//consider https://gis.stackexchange.com/questions/192303/leaflet-filter-with-condition
//Re init geojson data on each selection

//https://jsbin.com/hobohah/2/edit?html,js,console,output
// Change style based on user selection

// see https://gis.stackexchange.com/questions/265648/set-feature-styles-dynamically-in-leaflet
// https://jsbin.com/hobohah/2/edit?html,js,console,output
// function filtergeojson(userStartDate, userEndDate) {
//   // console.log(startDate)
//   actLayerGroup.eachLayer(function(groupLayer) {
//     groupLayer.eachLayer(function(layer) {
//       // console.log("Checking date!")
//       // console.log(layer.feature.properties.startDate)
//       // console.log("Sliced string is:")
//       // console.log(layer.feature.properties.startDate.slice(0,10))
//       // console.log("returning original sliced date!")
//       // console.log(startDate.slice(0,10))
//       if (layer.feature.properties.startDate.slice(0,10) > userStartDate.slice(0,10)) {
//         // console.log("Inside if statement!")
//         console.log(layer.feature.properties.name)
//         // console.log(layer.feature.properties.startDate)
//       }
//     });
//   });
// };


// function onEachFeature(feature, layer){
//   console.log(feature.properties.id)
// }
//
// function addFiltered(startDate, endDate, groupLayer){
//   L.geoJSON(groupLayer, {
//     onEachFeature: onEachFeature
//   })
// }

// function filtergeojson(startDate, endDate) {
//   actLayerGroup.eachLayer(function(groupLayer) {
//     actLayerGroup.removeLayer(groupLayer);
//     actLayerGroup.addLayer(addFiltered(startDate, endDate, groupLayer));
//   });
// };

// function onEachFeature(feature, layer) {
//   console.log("Inside oneachfeature function")
//   console.log(feature)
//   console.log(feature.properties.startDate)
// }

// function filtergeojson(startDate, endDate) {
//   actLayerGroup.eachLayer(function(groupLayer) {
//     // console.log("Inside each layer of groupLayer")
//     console.log(groupLayer)
//     // onEachFeature: onEachFeature
//     filter
//   });
// };


// https://stackoverflow.com/questions/49925646/issue-with-nested-functions-eachlayer-and-oneach-feature-of-leaflet-with-geoson
// https://stackoverflow.com/questions/50354728/leaflet-eachlayer-function-does-not-iterate-through-all-layers
// https://stackoverflow.com/questions/43125924/loop-through-leaflet-featuregroup
// function filtergeojson(startDate, endDate) {
//   actLayerGroup.eachLayer(function(groupLayer) {
//     console.log(groupLayer._layers)
//     console.log(groupLayer._layers.properties.startDate)
//   })
// };

// function filtergeojson(startDate, endDate) {
//   actLayerGroup.eachLayer(function(layer){
//     filter: function(feature, layer){
//       feature.properties.startDate
//     }
//   });
// });

// function filtergeojson(startDate, endDate) {
//   actLayerGroup.eachLayer(function(groupLayer){
//     onEachFeature(feature, layer) {
//       console.log(feature.properties.startDate);
//     }
//   });
// };

// function filtergeojson(startDate, endDate) {
//   actLayerGroup.eachLayer(function(groupLayer) {
//     // console.log("Inside each layer of groupLayer")
//     // console.log(groupLayer)
//     onEachFeature: onEachFeature(feature, layer) {
//       console.log("Inside oneachfeature function")
//       console.log(feature)
//       console.log(feature.properties.startDate)
//     }
//   })
// };


// function filtergeojson(startDate, endDate) {
//   actLayerGroup.eachLayer(function(groupLayer){
//     console.log(groupLayer);
//   });
// };
