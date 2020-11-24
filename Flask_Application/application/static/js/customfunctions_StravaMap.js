function binActData(filteredGroup){
  // console.log(filteredGroup)
  geoJSONDat = filteredGroup.toGeoJSON()
  actDataDict = {}
  dateDataList = []
  yearList = []
  for (i of geoJSONDat.features) {
    // Extract just year from datetime information
    featYear = i.properties.startDate.substr(0,4)
    actType = i.properties.type_extended
    distance = i.properties.distance * 0.000621371
    // console.log("Working on year and act type:")
    // console.log(featYear)
    // console.log(actType)
    // Add activity to object if not yet added
    if (Object.keys(actDataDict).indexOf(actType) == -1) {
      actDataDict[actType] = [];
    };
    if (actDataDict[actType].length == 0) {
      // console.log("Act type is empty, adding first entry!")
      actDataDict[actType].push({"x":featYear,"y":distance});
    } else {
      // Loop over all object entries checking if date matches, if so add this distance to it
      inDict = false
      for (a of actDataDict[actType]){
        if (a["x"] == featYear){
          // console.log("Adding distance to year!")
          a["y"] += distance;
          a["y"] = Math.round(a["y"])
          inDict = true
          break;
        }
      }
      // Add date and distance to activity type object
      if (inDict == false){
        actDataDict[actType].push({"x":featYear,"y":distance});
      }
    }
  }
  // Reverse order of years in inside objects
  for (m of Object.keys(actDataDict)){
    actDataDict[m].reverse()
  };
  // console.log(actDataDict)
  console.log(actDataDict)
  return actDataDict
};

// Generate x-axis labels using nested dates
function createXaxisLabels(chartData){
  labelList = []
  // console.log(chartData)
  // console.log(chartData)
  for (i of Object.keys(chartData)){
    // console.log(i)
    for (a of Object.keys(chartData[i])) {
      // console.log(a)
      // console.log(chartData[i][a]["x"])
      if (!labelList.includes(chartData[i][a]["x"])) {
        labelList.push(chartData[i][a]["x"])
      };
    }
  };
  labelList.sort()
  // console.log(labelList);
  return labelList;
};

function generateDatasetOptions(chartData) {
  var datasetOptions = []
  for (i of Object.keys(chartData)){
    options = {label:i,data:chartData[i],borderWidth: 1}
    if (i=="Mountain Bike") {
      options['label'] = "MTB"
      options['backgroundColor'] = 'rgba(228, 26, 28, 0.8)'
      options['borderColor'] = 'rgba(228, 26, 28)'
    } else if (i == "Road Cycling") {
      options['label'] = "Road Rides"
      options['backgroundColor'] = 'rgba(55, 126, 184, 0.8)'
      options['borderColor'] = 'rgba(55, 126, 184)'
    } else if (i =="Run") {
      options['backgroundColor'] = 'rgba(166, 86, 40, 0.8)'
      options['borderColor'] = 'rgba(166, 86, 40)'
    } else if (i == "Walk") {
      options['backgroundColor'] = 'rgba(152, 78, 163, 0.8)'
      options['borderColor'] = 'rgba(152, 78, 163)'
    }
    datasetOptions.push(options);
  }
  return datasetOptions;
};


function createActivityChart(chartData) {
  var ctx = document.getElementById('chart').getContext('2d');
  actChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: createXaxisLabels(chartData),
          datasets:  generateDatasetOptions(chartData)
          // datasets: [{
          //     label: 'MTB',
          //     data: chartData["Mountain Bike"],
          //     backgroundColor:'rgba(228, 26, 28, 0.8)',
          //     borderColor:'rgba(228, 26, 28)',
          //     borderWidth: 1
          // },
          // {
          //     label: 'Road Ride',
          //     data: chartData['Road Cycling'],
          //     backgroundColor: 'rgba(55, 126, 184, 0.8)',
          //     borderColor: 'rgba(55, 126, 184)',
          //     borderWidth: 1
          // },
          // {
          //     label: 'Run',
          //     data: chartData['Run'],
          //     backgroundColor:'rgba(166, 86, 40, 0.8)',
          //     borderColor:'rgba(166, 86, 40)',
          //     borderWidth: 1
          // },
          // {
          //     label: 'Walk',
          //     data: chartData['Walk'],
          //     backgroundColor:'rgba(152, 78, 163, 0.8)',
          //     borderColor:'rgba(152, 78, 163)',
          //     borderWidth: 1
          // }]
      },
      options: {
        legend: {
          labels:{
            fontSize: 16,
            fontStyle: "bold",
            fontColor: "black"
          }
        },
        scales: {
          xAxes:[{
            // type: 'time',
            // stacked:true
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: "Total Distance(Miles)",
              fontSize: 16,
              fontColor: "black",
              fontStyle: "bold"
            },
            // stacked:true,
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
  });
};

// Update chart labels and datasets based on user button selections
function updateChart(filteredGroup){
  // Create formatted dataset
  chartData = binActData(filteredGroup);
  // Calculate date labels (x-axis)
  actChart.data.labels = createXaxisLabels(chartData);
  // Use formatted data to generate legend labels and colors based on activity type
  actChart.data.datasets = generateDatasetOptions(chartData);
  //
  actChart.update();
}

// Used to display singular activites only on map and in dashboard panels, such as when searched or selected
function filterSingleActDisplay(actID) {
  // Filter geoJSON to display only the searched feature
  searchedActivityOnly = actFilter(null, null, null, actID);
  // Open popup for activity, for some reason I can't open the popup through just .openPopup here, so this method is used instead
  filteredGroup.eachLayer(function(layer) {
    // Get the id of the layer within the layer group, this number is dynamically generated by Leaflet so has to be called using .keys() and extracted from the first index location, there will only ever be one layer within this feature group
    id = Object.keys(layer._layers)[0]
    // Bind the popup using the previously bond popup content
    layer.bindPopup(layer._layers[id]._popup._content);
    // Open the popup
    layer.openPopup();
  });
  // Update dashbaord panels
  updateDataPanels(filteredGroup,actDataDict, "True");
  // Get a list of all active buttons
  active = document.querySelectorAll('.filterbtn');
  // iterate over active buttons, turning them to inactive
  for (var h = 0; h < active.length; h++) {
    active[h].className = active[h].className.replace(" active-btn", "");
  };
  // Set All button text to "Add Layers" to reflect its behavior
  document.getElementById("All").innerHTML = "&nbsp;&nbsp;&nbsp;Add&nbsp;&nbsp;&nbsp;&nbsp;<br>Layers";
};

// Create Leafet search option using activity name
// This only searches active geoJSON data, without needing to be re-initialized, I am not sure why but it must automatically update when the layergroup its pointing to updates
function createSearchControl(layerGroup) {
  var searchControl = new L.Control.Search({
    layer:layerGroup,
    propertyName: 'name',
    zoom:15,
    marker:false,
    autoCollapse:true,
    initial:false,
    // set move to location to capture the full extend of the activity
    moveToLocation: function(latlng, OBJECTID, map) {
      map.fitBounds(latlng.layer.getBounds());
    }
  });
  // Add search control to map
  map.addControl(searchControl);
  // When a search location is selected filter to show that activity only
  searchControl.on('search:locationfound', function(e) {
    filterSingleActDisplay(e.layer.feature.properties.actID)
  });
  // Search option activated
  searchControl.on('search:expanded', function(e) {
    map.closePopup()
    // Clear and add all layers to display and search options
    filteredGroup.clearLayers()
    actFilter("All")
  });
}

// Renderer with extra clicking tolerance, not supported in IE I think
var myRenderer = L.canvas({ tolerance:10 });
actWeight = 2
actOpacity = 0.7
// Set linestyles for each activity type, these match button colors
var mtb_lineStyle =  {"weight":actWeight,"opacity":actOpacity,"renderer":myRenderer,"color":"#e41a1c"}
var walk_lineStyle = {"weight":actWeight,"opacity":actOpacity,"renderer":myRenderer,"color":"#984ea3"}
var road_lineStyle = {"weight":actWeight,"opacity":actOpacity,"renderer":myRenderer,"color":"#377eb8"}
var run_lineStyle =  {"weight":actWeight,"opacity":actOpacity,"renderer":myRenderer,"color":"#a65628"}


// Style linestyles according to their properties, uses type_extended for rides since they are not differentiated in type property.
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
// Add onclick action to filter display when user clicks a activity
function popupAction(layerGroup) {
  layerGroup.eachLayer(function(layer) {
    layer.on('click', function(e) {
      filterSingleActDisplay(e.layer.feature.properties.actID)
    });
  });
};

// Populate popups using property information, distances come from server in meters and are converted to feet/miles, link to public activites on Strava.
function onEachFeatureAct(feature,layer) {
  layer.bindPopup(
    "<div class='spanbotbord'><b>" + feature.properties.name + "</b></div>" +
      "<div><b>Type: " + feature.properties.type + "</b></div>" +
    "<div><b>Date (PST): " + feature.properties.startDate + "</b></div>" +
    "<div><b>Moving Time: " + convertDuration(feature.properties.moving_time) + "</b></div>" +
    "<div><b>Total Activity Time: " + convertDuration(feature.properties.elapsed_time) + "</b></div>" +
    "<div><b>Distance (Miles): " + (feature.properties.distance * 0.000621371).toFixed(1) + "</b></div>" +
    "<div><b>Elevation gain (Feet): " + (feature.properties.total_elevation_gain * 3.28084).toFixed(1) + "</b></div>" +
    "<div><b>Calories burned: " + feature.properties.calories + "</b></div>" +
    "<div><b>Average speed (mph): " + (feature.properties.average_speed * 2.23694).toFixed(1) + "</b></div>" + "<div><b>Max speed (mph): " + (feature.properties.max_speed * 2.23694).toFixed(1) + "</b></div>" + wattText(feature.properties.type, feature.properties.average_watts) +
    "<div><b>Activity ID: " + feature.properties.actID + "</b></div>" +
    privatecheck(feature.properties.private, feature.properties.actID)
  )
};

function wattText (type, avgWatts){
  if (type == "Ride"){
    return "<div><b>Average Watts: " + avgWatts + "</b></div>";
  } else {
    return "<span></span>";
  }
};

// Check if activity is flagged as private, if so say as such, otherwise create link to activity page on Strava
function privatecheck(privacy, actID) {
  if (privacy == "true"){
    res = "<div><b>Private Activity</b></div>"
  } else {
    res = "<div><b><a href=https://www.strava.com/activities/" + actID + ">Strava Activity Page</a></b></div>"
  }
  return res
};

// Duration is provided as seconds, convert to HH-MM-SS format
// I believe this effectively creates a datetime that's duration seconds since epoch, then extracts only HH-MM-SS seconds from that datetime
function convertDuration(seconds){
  // Create null date
  var date = new Date(null);
  // set date doing duration seconds
  date.setSeconds(seconds);
  // Extract HH-MMM-SS information
  var result = date.toISOString().substr(11, 8);
  return result
};

// If gearname is not null then the activity was a ride, return name of bike formatted with HTML
function geartext(gearname) {
  if (gearname){
    res = "<div><b>Bike: " + gearname + "</b></div>"
    return res
  }
};


// Un-used function to reset daterange picker to all activities (all-time)
function resetAll() {
  // $('#reportrange').data('daterangepicker').setStartDate(start);
  // $('#reportrange').data('daterangepicker').setEndDate(end);
  console.log("clicked reset button!")
  $('#reportrange').data('daterangepicker').setStartDate(start);
  $('#reportrange').data('daterangepicker').setEndDate(end);
  // $('#reportrange').updateView();
  console.log($('#reportrange').data('daterangepicker'))
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
        updateDataPanels(filteredGroup, actDataDict, "True")
        document.getElementById("All").innerHTML = "Remove<br>Layers";
        // set "All" button to active
        this.className += " active-btn";
        // change text of "All" to tell user that clicking it will remove all activity layers
        document.getElementById("All").innerHTML = "Remove<br>Layers";
      // Check if user click target is a button flagged as active
      } else if (obj.target.className.includes("active-btn")) {
        console.log("case B")
        // Remove active class from button, reverting it to the disabled opacity
        this.className = this.className.replace(" active-btn","");
        // If the target was the All button, clear all layers from display
        if (obj.target.id == "All"){
          // change text of "All" to tell user that clicking it will add all activity layers
          document.getElementById("All").innerHTML = "&nbsp;&nbsp;&nbsp;Add&nbsp;&nbsp;&nbsp;&nbsp;<br>Layers";
          filteredGroup.clearLayers();
          updateDataPanels(filteredGroup, actDataDict, "True")
        // if user clicks an active button that is not All, remove just that layer from display
        // A dictionary is used for lookup to select the correct layer using the target button's ID value
        } else {
          filteredGroup.clearLayers();
          // Add geojson data for all active buttons
          addActiveLayers();
          updateDataPanels(filteredGroup, actDataDict, "True")
          // document.getElementById("All").innerHTML = "Remove<br>Layers";
          // filteredGroup.removeLayer(layerGroupDict[obj.target.id]);
        }
      // Check if user click target is NOT the "All" button, but the "All" button is flagged as active
      // Used to determine if a user is selecting activity button when the "All" button is active
      } else if ((!(obj.target.id.includes("All"))) && (document.getElementById("All").className.includes("active-btn"))) {
          console.log("case C")
          // Remove the active flag from the "All" button, reverting to disabled opacity
          document.getElementById("All").className = document.getElementById("All").className.replace(" active-btn", "");
          // change text of "All" to tell user that clicking it will add all activity layers
          document.getElementById("All").innerHTML = "&nbsp;&nbsp;&nbsp;Add&nbsp;&nbsp;&nbsp;&nbsp;<br>Layers";
          // Set the target button to active
          this.className += " active-btn";
          // Remove all activity layers
          filteredGroup.clearLayers();
          // Add the activity layer associated with the button clicker by the user
          actFilter(obj.target.id);
          updateDataPanels(filteredGroup, actDataDict, "True")
      // User selected "All" button when no activity buttons are active
      } else if ((obj.target.id == "All") && (active.length == 0)) {
        console.log("case D")
        document.getElementById("All").innerHTML = "&nbsp;&nbsp;&nbsp;Add&nbsp;&nbsp;&nbsp;&nbsp;<br>Layers";
        this.className += " active-btn";
        actFilter(obj.target.id);
        updateDataPanels(filteredGroup, actDataDict, "True")
      // Last chase, user is multi-selecting activities, i.e. "All" is disabled and at least one other activity
      // is flagged as active
      } else if (active.length == 0) {
        console.log("Case E")
        filteredGroup.clearLayers();
        this.className += " active-btn";
        actFilter(obj.target.id);
        updateDataPanels(filteredGroup, actDataDict, "True")
      } else {
        console.log("case F")
        // Set this activity to active, in addition to other active buttons
        this.className += " active-btn";
        // Add the layer associated with the button clicker by the user.
        // This is added in addition to other active layers
        actFilter(obj.target.id);
        updateDataPanels(filteredGroup, actDataDict, "True")
      }
      updateChart(filteredGroup);
    });
  }
};

// Selects active buttons, excluding the "All" button, and interates over them rebuilding the associated geojson layers using the user selected dates.
// Start and end dates are set to null for initialization of the dataset.
// This function is called as a callback whenever the user changes the daterange selection or selects a activity filter button, maintaining previous date selections.
function addActiveLayers(userStartDate = null, userEndDate = null, actType = null) {
  // If the "All" button is active, select all other activity buttons and set filters on all activities.
  if (document.getElementById('All').className.includes("active") == true) {
    active = document.querySelectorAll('.filterbtn:not(#All)');
    for (var h = 0; h < active.length; h++) {
      actFilter(active[h].id, userStartDate, userEndDate)
    }
  // "All" button is inactive, select all active buttons and filter their associated activity layers using user selected dates.
  } else if (actType !== null) {
    actFilter(actType, userStartDate, userEndDate);
  } else {
    active = document.querySelectorAll('.active-btn:not(#All)');
    for (var h = 0; h < active.length; h++) {
      actFilter(active[h].id, userStartDate, userEndDate)
    };
  };
};

// Applies filters to displayed geoJSON based on activity button and/or daterange selections.
// Leaflet only applies filters when a geoJSON layer is initialized, these settings cannot be changed after a geoJSON layer is created.
// In order to apply filters on the fly, new geoJSON layers need to be re-initialized using the original un-aletered data (rawGeoJSON) with new filters in place.
function actFilter(actType = null, userStartDate = null, userEndDate = null, actID = null) {
  if ((userStartDate == null) && (userEndDate == null)) {
    // This function wasn't called by a change in the daterange selection. Use the default (includes all activities) or previously set daterange by selecting the displayed date range
    // and setting that as the filter range
    displayDate = document.getElementById("display-date").textContent.split(" - ");
    userStartDate = moment(new Date(displayDate[0])).format().slice(0,10)
    userEndDate = moment(new Date(displayDate[1])).format().slice(0,10)
  }
  // User selected an activity type or changed the daterange selection, create new geoJSON layer(s) with new filters in place that are based on on activity type and start and end dates
  filteredAct = L.geoJson(rawGeoJSON, {
      style: actStyle,
      onEachFeature: onEachFeatureAct,
			filter: function(feature, layer) {
        if (actType == "Walk"||actType == "Hike") {
            if ((feature.properties.type == "Walk"||feature.properties.type == "Hike") && (feature.properties.startDate.slice(0,10) >= userStartDate.slice(0,10)) && (feature.properties.startDate.slice(0,10) <= userEndDate.slice(0,10))) {
              return true
            }
        } else if (actType == "Run") {
            if ((feature.properties.type == "Run") && (feature.properties.startDate.slice(0,10) >= userStartDate.slice(0,10)) && (feature.properties.startDate.slice(0,10) <= userEndDate.slice(0,10))) {
              return true
            }
        } else if (actType == "MTB") {
            if ((feature.properties.type_extended == "Mountain Bike") && (feature.properties.startDate.slice(0,10) >= userStartDate.slice(0,10)) && (feature.properties.startDate.slice(0,10) <= userEndDate.slice(0,10))) {
              return true
            }
        } else if (actType == "Road") {
            if ((feature.properties.type_extended == "Road Cycling") && (feature.properties.startDate.slice(0,10) >= userStartDate.slice(0,10)) && (feature.properties.startDate.slice(0,10) <= userEndDate.slice(0,10))) {
              return true
            }
        } else if (actType == "All") {
            // Clear layers from group before re-adding
            filteredGroup.clearLayers();
            if (feature.properties.startDate.slice(0,10) >= userStartDate.slice(0,10) && (feature.properties.startDate.slice(0,10) <= userEndDate.slice(0,10))) {
              return true
            }
        } else if (actID !== null){
          // User has searched for an activity by name, show only that activity
          filteredGroup.clearLayers();
          if (feature.properties.actID == actID) {
            return true
          }
        }
			}
  });
  // Add new layer to existing filtered group, which may be empty or contain additional geoJSON layers depending on user selections
  filteredGroup.addLayer(filteredAct);
  //
  popupAction(filteredGroup);
};

// Updates data summary panels
function updateDataPanels(groupLayer, actDataDict, clear){
  // Clear existing dictionary of values
  if (clear == "True"){
    var actDataDict = {"count":0, "dist":0, "elev":0, "calories":0, "totalTime":0, "speed":0, "moveTime":0, "maxSpeed":0}
  }
  // Iterate over each layer in layer group
  filteredGroup.eachLayer(function(layer){
    // Get keys for layer (activity) objects
    layerKeys = Object.keys(layer._layers)
    	for (i of layerKeys) {
        // Get property data
        propertyData = layer._layers[i].feature.properties;
        // Add property data to dictionary, converting metric to U.S. customary units
        actDataDict["count"] += 1;
        actDataDict["dist"] += Math.round(propertyData.distance*0.000621371);
        actDataDict["elev"] += Math.round(propertyData.total_elevation_gain*3.28084);
        actDataDict["calories"] += propertyData.calories;
        actDataDict["totalTime"] += propertyData.elapsed_time;
        actDataDict["moveTime"] += propertyData.moving_time;
        actDataDict["speed"] += (propertyData.average_speed*2.23694);
        // if ((propertyData.max_speed*2.23694) > actDataDict["maxSpeed"]) {
        //   console.log("Assigning new max speed!")
        //   actDataDict["maxSpeed"] = (propertyData.max_speed*2.23694).toFixed(1);
        // };
      };
  });
  // If count is 0, set avg speed to 0, otherwise calculate, avoids NaN error
  if (actDataDict["count"] == 0) {
    avgSpeed = 0
  } else {
    avgSpeed = (actDataDict["speed"]/actDataDict["count"]).toFixed(1)
  }
  // Get activity total duration as hours
  totalHours = moment.duration(actDataDict["totalTime"], 'seconds').asHours()
  // Get movement duration as hours
  movementHours = moment.duration(actDataDict["moveTime"], 'seconds').asHours()
  // Update panel information
  document.getElementById('actCount').innerHTML = actDataDict["count"];
  document.getElementById('totalDist').innerHTML = actDataDict["dist"] + " miles";
  document.getElementById('totalElev').innerHTML = actDataDict["elev"] + " feet";
  document.getElementById('totalCalories').innerHTML = actDataDict["calories"];
  // Total time
  // document.getElementById('totalTime').innerHTML = Math.trunc(totalHours) + "H" + ":" + (((totalHours-Math.floor(totalHours))*60).toFixed(0) + "M");
  // moving time
  document.getElementById('movingTime').innerHTML = Math.trunc(movementHours) + "H" + ":" + (((movementHours-Math.floor(movementHours))*60).toFixed(0) + "M");
  document.getElementById('avgSpeed').innerHTML = avgSpeed + " mph";
  // document.getElementById('maxSpeed').innerHTML = actDataDict["maxSpeed"]+ " mph";
};
