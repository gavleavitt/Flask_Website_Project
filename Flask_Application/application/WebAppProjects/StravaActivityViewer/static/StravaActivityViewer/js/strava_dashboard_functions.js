// Initializes event listeners
function initializeListeners(){
  // Leaflet fullscreen event listener, if full screen is exited and the device display is less than 600px, close any open popups
  map.on('exitFullscreen', function(){
    // var dimen = getDisplaysize();
    if (dimen.width < 600){
      map.closePopup();
    }
  });
  // After the window has loaded activte the activity filter button event listeners
  window.onload = function(){
    loadActivityBtnListener();
  }
  // Sets text of charts and display depending on page size, not sure why this is set to a resize event, should probably be tied to page dimensions
  window.addEventListener('resize', setChartTextSizes);
  window.addEventListener('resize', setDisplaysize);
  // window.onresize = getChartTextSizes();
}

// Initializes the dashboard display by populating Leafet, ChartJS, Tabulator, Search, popups, and data panels
function initializeDisplay(stravaTopojsonUrl){
  // see http://bl.ocks.org/marcellobenigno/9b09c24850def14250141dfe89f9a296
  // see https://docs.mapbox.com/mapbox.js/example/v1.0.0/omnivore-kml-tooltip/
  // Create a empty geoJSON with style and popup settings.
  orgActivities = L.geoJson(null, {
    style: actStyle,
    onEachFeature: onEachFeatureAct
  });
  createStreamLineChart();
  getActivityTopojsonS3Url(stravaTopojsonUrl).then(function(presignedTopojsonURL){
    // Use Leaflet omnivore to import/process topoJSON data. This function passes the loaded data into a existing empty geoJSON layer.
    // var originalTopoData = omnivore.topojson(jsonDataURL, null, orgActivities)
    omnivore.topojson(presignedTopojsonURL, null, orgActivities).on('ready', function() {
      console.log("topoJSON data has been loaded!")
      // After data have loaded, create a original group layer containing all data, this won't be filtered/changed and is kept to hold original data
      // originalGroup = L.layerGroup([orgActivities]);
      // Create new raw geoJSON dataset using the original, un-aletered, geoJSON layer as dump source.
      // There may be a better method than this, but I believe that L.geoJSON can only take raw geoJSON data, not an existing geoJSON layer.
      // This requires a dump of geoJSON data into a new variable since the raw geoJSON data doesn't get stored automatically, its converted into a geoJSON layer.
      // This may cause performance issues on some browsers/devices since this is effectively storing another copy of the data in addition to what's being displayed
      rawGeoJSON = orgActivities.toGeoJSON()
      // Create a filtered group layer and add to map, this layer group will be changed using filters
      filteredGroup = L.layerGroup([orgActivities]).addTo(map);
      updateDataPanels(filteredGroup, actDataDict, "False")
      // create Leafet search for loaded geoJSON data
      createSearchControl(filteredGroup);
      popupAction(filteredGroup);
      chartActData = binActData(filteredGroup, "count-btn");
      // Remove null entry, not where this is getting populated, this is a patch fix
      delete chartActData.null
      createActivityChart(chartActData, "count-btn");
      initTable(filteredGroup)
      // chartActData = binActData(rawGeoJSON);
      // populateChart(chartActData);
      map.spin(false);
    })
    .on('error', function() {
      alert("Data failed to load, please try again later.")
    })
  })
};

// Queries webserver API for the presigned S3 Bucket URL, grants temporary access
function getActivityTopojsonS3Url(link){
  return $.ajax({
      url:link,
      //https://stackoverflow.com/questions/47523265/jquery-ajax-no-access-control-allow-origin-header-is-present-on-the-requested
      type: 'GET',
      dataType: 'text'
  });
}

// Use the presigned URL to query the full topoJSON file, this is a CORS request
function getActivityTopojsonData(presignedURL){
  console.log("Setting headers!")
  return $.ajax({
    url:presignedURL,
    //https://stackoverflow.com/questions/47523265/jquery-ajax-no-access-control-allow-origin-header-is-present-on-the-requested
    headers: {'Access-Control-Allow-Origin':'https://trimmedstreamdata.s3-us-west-1.amazonaws.com'},
    crossOrigin: true,
    // data: {csvName:'4413728207.csv'},
    type: 'GET',
    dataType: 'jsonp'
  });
}

// Functions to show/hide the modal
function initModal(){
  // Modal from https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_modal
  // Get the modal
  var modal = document.getElementById("myModal");
  // Open modal
  modal.style.display = "block";
  // Get the button that opens the modal
  var btn = document.getElementById("btn");

  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];

  // When the user clicks the button, open the modal
  btn.onclick = function() {
    modal.style.display = "block";
  }

  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
};


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
  // Update chart
  // updateChart(filteredGroup, null, actID);
  updateChart(filteredGroup);
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
    filterSingleActDisplay(e.layer.feature.properties.actID);
    // Select table row
    highlightRow(e.layer.feature.properties.actID)
    toggleFull();
    // Clear any stream highlight markers
    markerGroup.clearLayers();
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

function toggleFull(){
  if ((dimen.width < 600) && fullScreenApi.isFullScreen() === false){
    // map.toggleFullscreen();
    // map.fitBounds(e.latlng);
  }
}


// Add onclick action to filter display when user clicks a activity
function popupAction(layerGroup) {
  layerGroup.eachLayer(function(layer) {
    layer.on('click', function(e) {
      filterSingleActDisplay(e.layer.feature.properties.actID)
      highlightRow(e.layer.feature.properties.actID)
      toggleFull()
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

// Set text for watts
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
function loadActivityBtnListener() {
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
          console.log("Case B not All")
          filteredGroup.clearLayers();
          // console.log(filteredGroup)
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
      // prevMultiActBtn = document.querySelectorAll(".multiAct.chart-active")[0].id
      // updateChart(filteredGroup,prevMultiActBtn);
      updateChart(filteredGroup)
      generateTableFormatedData(filteredGroup, "Update")
      // Clear any stream highlight markers
      markerGroup.clearLayers();
      // activateChartButton();
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
  document.getElementById('totalDist').innerHTML = actDataDict["dist"].toLocaleString() + " miles";
  document.getElementById('totalElev').innerHTML = actDataDict["elev"].toLocaleString() + " feet";
  document.getElementById('totalCalories').innerHTML = actDataDict["calories"].toLocaleString();
  // Total time
  // document.getElementById('totalTime').innerHTML = Math.trunc(totalHours) + "H" + ":" + (((totalHours-Math.floor(totalHours))*60).toFixed(0) + "M");
  // moving time
  document.getElementById('movingTime').innerHTML = Math.trunc(movementHours) + "H" + ":" + (((movementHours-Math.floor(movementHours))*60).toFixed(0) + "M");
  document.getElementById('avgSpeed').innerHTML = avgSpeed + " mph";
  // document.getElementById('maxSpeed').innerHTML = actDataDict["maxSpeed"]+ " mph";
};

// Initializes the datarangepicker functions
function initDateRange(){
  // daterangepicker taken from  https://www.daterangepicker.com/
  // Sets options for daterangepicker
  $(function() {
    // Set format of dates
    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }
    // Apply daterange picker settings
    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        // Show year/month dropdown options when using custom range
        "showDropdowns": true,
        // Minimum date that can be selected, no records before this time
        "minDate":"01/01/2014",
        // Maximum date that can be selected, set to current day
        "maxDate": String(moment().format('MM/DD/YYYY')),
        // "maxYear":"11/18/2020",
        "opens": "center",
        // Stops input from auto updating, no entirely sure what this means but leaving it enabled caused odd/annoying behavior
        // "autoUpdateInput": false,
        "autoUpdateInput": true,
        // Unlink start and end calendars so they don't show the same year/month changed. Leaving it on true creates confusion on whether or not the date was selected properly
        "linkedCalendars": false,
        // Set preset date ranges to select from
        ranges: {
          'All Time (default)': [moment('2014-01-01'), moment().endOf('year')],
          // 'Today': [moment().startOf('day'), moment().endOf('day')],
          'Today': [moment(), moment()],
          'Last 7 Days': [moment().subtract(6, 'days'), moment()],
          'Last 30 Days': [moment().subtract(29, 'days'), moment()],
          'This Month': [moment().startOf('month'), moment().endOf('month')],
          'This Year': [moment().startOf('year'), moment().endOf('year')]
           // 'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);
    // Initializes
    cb(start, end);
  });
  // Callback function that fires when user uses picker, filters activity display
  $("#reportrange").on('apply.daterangepicker', function(ev, picker) {
    // Formats data in a proper date format
    userStart = picker.startDate.format();
    userEnd = picker.endDate.format();
    // console.log(userStart)
    // console.log(userEnd)
    // clear existing layers
    filteredGroup.clearLayers();
    // Re-add active layers with new daterange filter applied
    addActiveLayers(picker.startDate.format(), picker.endDate.format());
    // Update dashboard panels
    updateDataPanels(filteredGroup,actDataDict, "True");
    // Update chart data
    updateChart(filteredGroup);
    // Update data table
    generateTableFormatedData(filteredGroup, "Update")
    // Clear any stream highlight markers
    markerGroup.clearLayers();
    // activateChartButton();
  });
};

function toggleTableOn(){
  // When screen is set to a mobile size, this function toggles the tabulator table on
  // document.getElementById("chart-cont").style.display="none";
  // document.getElementsByClassName("chartPanel")[0].style.display="none";
  // Set charts to no-data class and removes show-data, hiding them
  document.getElementById("chart-cont").classList.add("no-data");
  document.getElementById("chart-cont").classList.remove("show-data");
  document.getElementById("chart-line-cont").classList.add("no-data");
  document.getElementById("chart-line-cont").classList.remove("show-data");
  // Set the tabulator div to display
  document.getElementById("table-container").style.display="block";
  // Regenerate tabulator, this ensures that the data are properly formatted in the window
  initTable(filteredGroup);

}

function toggleGraphOn(){
  // When screen is set to a mobile size, this function toggles the appropriate graph on
  // Get activity count, need to determine which chart to display
  var actCount = parseInt(document.getElementById("actCount").innerText)
  // Hide tabulator table
  document.getElementById("table-container").style.display="none";
  if (actCount == 1){
    document.getElementById("chart-line-cont").classList.add("show-data");
    document.getElementById("chart-line-cont").classList.remove("no-data");
  } else {
    document.getElementById("chart-cont").classList.add("show-data");
    document.getElementById("chart-cont").classList.remove("no-data");
  }
  // document.getElementById("chart-cont").style.display="none";
  // document.getElementsByClassName("chartPanel")[0].style.display="none";
}
