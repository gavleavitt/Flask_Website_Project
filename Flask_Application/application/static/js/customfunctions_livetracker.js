function gpsmarker(feature, latlng){
  /**
  Returns marker for gps point. Unused in HTML.
  */
  return L.circleMarker(latlng,livemarkersettings);
};

function formattime(jsontime){
  /**
  Converts JSON gps timestamp from ISO 8601 UTC to local time.
  input:
    jsontime: ISO 8601 timestamp
  returns:
    datetime
  */
   datetime = new Date(jsontime);
   datetime = datetime.toLocaleString()
   return datetime;
};

function timedif(jsontime){
  /**
  Returns formatted local time since last gps log time.
  See https://stackoverflow.com/questions/1322732/convert-seconds-to-hh-mm-ss-with-javascript
  */
  currenttime = new Date();
  datetime = new Date(jsontime);
  msdif = (currenttime - datetime);
  seconds = msdif/1000;
  hours = seconds/3600;
  if (hours > 24){
    res = "Over a day old!"
  } else if (hours < 24.0 && hours > 1.0){
    //Hours, minutes
    dif = new Date(msdif).toISOString().substr(11, 5);
    res = dif.substr(0,2) + " Hours " + dif.substr(3,2) + " Minutes ago";
  } else if ( hours < 1 && seconds > 60) {
    //Minutes, seconds
    dif = new Date(msdif).toISOString().substr(14, 5);
    res = dif.substr(0,2) + " Minutes " + dif.substr(3,2) + " Seconds ago";
  } else if (seconds < 60){
    // console.log(seconds)
    res = "Less than a minute ago!";
  } else {
    res = "Time difference error!";
  }
  return ("<br>("+ res + ")<br>10 Minute Logging Interval")
};

function nearestpathway(road,trail,distroad,disttrail,poi,speed){
  res = ""
  //if ((poi!=["Home","Work","Relative-Home"]) || (poi!=null)){
  if ((!["Home","Work","Relative-Home"].includes(poi)) && (poi != null)){
      if (disttrail < distroad){
        document.getElementById('nearest-road-text').innerHTML = "<div class='detail-context'>Nearest trail/path</div>";
      };
    res += trailinfo(poi,trail,disttrail,speed);
    res += "<div class='detail-context'>Nearest road</div>"
  };
  res += nearestroad(road,distroad);
  return res
};

function activitytext(profile){
  return "<div class='div-span-margin'><span class='teal-text'<br>" + profile + "</div></span>"
};

function locationtext(poi,city,county){
  if (poi !== null){
    display_text = "<div class='div-span-margin'><span class='teal-text'<br>" + poi + "</div></span>" + region(city,county);
  }else{
    display_text = region(city,county);
  };
  return display_text
};

function nearestroad(road,distroad){
  /**
  Formats nearest road information.
  */
  road_text = road + "<br>(" + distroad.toString().split(".")[0] + " feet away)"
  return road_text
};

function region(city,county){
  /**
  Formats region information.
  */
  if (city !== null){
    cityloc = "<div class='detail-context'>City</div>" + city;
  } else {
    cityloc = "<div class='detail-context'>City</div>Not within city-limits";
  };
  if (county == "Out of State!"){
    document.getElementById('nearest-road').innerHTML = "<span class='detail-text-important'>Not near any roads!</span>"
    return "<span class='detail-text-important'>Not in California!</span>";
  }else if (county !== null){
    countyloc = "<br><span class='detail-context'>County</span><br>" + county;
  } else {
    return "<span class='detail-context-important'>Not in California!</span>";
  };
  res = cityloc + countyloc;
  return res;
};

function trailinfo(poi,trail,disttrail,speed){
  /**
  Formats trail information.
  */
  res = "<div class='div-span-nomargin'><span class='teal-text'>" + trail + "</div></span>" + "(" + disttrail.toString().split(".")[0] + " feet away)";
  res += "<div class='detail-context'><br>Speed</div>"
  if (speed == 0){
    res += "Not moving!<br>";
  } else {
    res += (speed*2.24).toString().split(".")[0] + "mph<br>"
  }
  return res;
};

function batteryinfo(battery){
  /**
  Formats battery display.
  Add logic and calls to static files to display a battery icon.
  */
  return (battery + "%");
}

function batteryicon(battery){
/**
*/
if (battery >= 80){
  return '../static/images/battery-green.svg';
} else if (battery >= 60){
  return '../static/images/battery-yellow.svg';
} else if (battery >= 45){
  return '../static/images/battery-orange.svg';
} else if (battery >= 10){
  return '../static/images/battery-red.svg';
} else {
  return '../static/images/battery-red-critical.svg';;
}};

function activityicon(profile){
if (profile == "MTB"){
  document.getElementById('activity-icon').src = '../static/images/Downhill_sketch.svg';
} else if (profile == "Road Biking"){
  document.getElementById('activity-icon').src = '../static/images/roadbike1.svg';
} else if (profile == "Driving"){
  document.getElementById('activity-icon').src = '../static/images/fiesta-white.png';
  document.getElementById("activity-icon").style.width = "9vw";
  document.getElementById("activity-icon").style.height = "4vw";
} else if (profile == "Walking"){
  document.getElementById('activity-icon').src = '../static/images/walk.svg';
} else if (profile == "Running"){
  document.getElementById('activity-icon').src = '../static/images/running-figure.svg';
} else if (profile == "Field Work"){
  document.getElementById('activity-icon').src = '../static/images/Field_Work_Icon.svg';
} else {
  document.getElementById('activity-icon').src = '../static/images/ellipsis.svg';
}
};

function coors(lat,lon,provider){
  /**
  Formats location information.
  */
  lat = lat.toString().split(".")[0] + "." + lat.toString().split(".")[1].substr(0,4);
  lon = lon.toString().split(".")[0] + "." + lon.toString().split(".")[1].substr(0,4);
  if (provider == "network"){
    accur_stat = "(Low accuracy triangulation!)";
  } else {
    accur_stat = "(High accuarcy GPS!)";
  }
  res = "Lat: " + lat + ", " + "Lon: " + lon + "<br>" + accur_stat + "";
  return res
};

function subten(number){
  if (number == 0){
    return "<10"
  } else if (number == null) {
    return "Results Pending"
  } else {
  return number
  }
};

function colortext(status){
  if (status == "Open"){
    res = "<span style='color:#00159e'>" + status + "</span>"
  } else if (status == "Warning"){
    res = "<span style='color:#ff8400'>" + status + "</span>"
  } else if (status == "Closed"){
    res = "<span style='color:#d40808'>" + status + "</span>"
  } else {
    res = "<span>" + status + "</span>"
  }
  return res
};

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

function filterActType(addLayer){
  // actLayerGroup.clearLayers();
  actLayerGroup.addLayer(addLayer);
};


function actFilter(act){
  if(act=="All"){
    actLayerGroup.clearLayers()
    actLayerGroup.addLayer(run_act)
    actLayerGroup.addLayer(walk_act)
    actLayerGroup.addLayer(road_act)
    actLayerGroup.addLayer(mtb_act)
  } else if (act == "MTB") {
    filterActType(mtb_act)
  } else if (act == "Road") {
    filterActType(road_act)
  } else if (act == "Walk") {
    filterActType(walk_act)
  } else if (act == "Run") {
    filterActType(run_act)
  }
};

// Button coloring and filter behavior, allows user to single and multi-select as well add and remove all
// layers with the "All" button.
// This function is loaded asynchronously after the document has loaded in the activity geojson data
function loadActiveListener() {
  // get div that contains the filter buttons
  var group = document.getElementById("act-filter-group");
  // get all buttons within group
  var btns = group.getElementsByClassName("filterbtn");
  // Iterate over buttons in group adding an click event listener to each
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function(obj) {
      //get active buttons, exluding the All button, this is used to determine if multi-selection is occurring
      active = document.querySelectorAll('.active:not(#All)')
      // Check to see if button click target is the "All" button and if any other buttons are also flagged as active,
      // if so remove the active class from these buttons (reverting them to disabled opacity) and set the All button
      // to active and add all activity layers to display
      if ((obj.target.id == "All") && (active.length > 0)) {
        // iterate over buttons flagged as active
        for (var h = 0; h < active.length; h++) {
          // remove active class from buttons, reverting them to disabled opacity
          active[h].className = active[h].className.replace(" active", "");
        }
        // call function to add all activity layers to display
        actFilter("All")
        // set "All" button to active
        this.className += " active";
      // Check if user click target is a button flagged as active
      } else if (obj.target.className.includes("active")) {
        // Remove active class from button, reverting it to the disabled opacity
        this.className = this.className.replace(" active","");
        // If the target was the All button, clear all layers from display
        if (obj.target.id == "All"){
          actLayerGroup.clearLayers()
        // if user clicks an active button that is not All, remove just that layer from display
        } else {
          actLayerGroup.removeLayer(layerGroupDict[obj.target.id]);
        }
      // Check if user click target is NOT the "All" button, but the "All" button is flagged as active
      // Used to determine if a user is selecting activity button when the "All" button is active
      } else if ((!(obj.target.id.includes("All"))) && (document.getElementById("All").className.includes("active"))) {
          // Remove the active flag from the "All" button, reverting to disabled opacity
          document.getElementById("All").className = document.getElementById("All").className.replace(" active", "");
          // Set the target button to active
          this.className += " active";
          // Remove all activity layers
          actLayerGroup.clearLayers();
          // Add the activity layer associated with the button clicker by the user
          actFilter(obj.target.id);
      // Last chase, user is multi-selecting activities, i.e. "All" is disabled and at least one other activity
      // is flagged as active
      } else {
        // Set this activity to active, in addition to other active buttons
        this.className += " active";
        // Add the layer associated with the button clicker by the user.
        // This is added in addition to other active layers
        actFilter(obj.target.id);
      }
    });
  }
}

//
// function loadActiveListener() {
//   var group = document.getElementById("act-filter-group");
//   var btns = group.getElementsByClassName("filterbtn");
//   for (var i = 0; i < btns.length; i++) {
//     btns[i].addEventListener("click", function(obj) {
//       //get active buttons, exluding the All button
//       active = document.querySelectorAll('.active:not(#All)')
//
//       // Check to see if button target is the all button and if any other buttons are active,
//       // if so remove the active class and set the All button to active
//       if ((obj.target.id == "All") && (active.length > 0)) {
//         console.log("Clicked all with other buttons active!")
//         for (var h = 0; h < active.length; h++) {
//           active[h].className = active[h].className.replace("active", "");
//         }
//         actFilter("All")
//       }
//       if (obj.target.className.includes("active")) {
//         this.className = this.className.replace(" active","");
//         if(obj.target.id == "All"){
//           actLayerGroup.clearLayers()
//         } else {
//           actLayerGroup.removeLayer(layerGroupDict[obj.target.id]);
//         }
//       } else {
//         if ((!(obj.target.id.includes("All"))) && (document.getElementById("All").className.includes("active"))) {
//           document.getElementById("All").className = document.getElementById("All").className.replace(" active", "");
//         }
//         this.className += " active";
//         actFilter(obj.target.id);
//       }
//     });
//   }
// }


//Works and allows toggling single layers!
// function loadActiveListener(){
//   var group = document.getElementById("act-filter-group");
//   var btns = group.getElementsByClassName("filterbtn");
//   for (var i = 0; i < btns.length; i++) {
//     btns[i].addEventListener("click", function(obj) {
//       if (obj.target.className.includes("active")){
//         this.className = this.className.replace(" active","");
//         if(obj.target.id == "All"){
//           actLayerGroup.clearLayers()
//         } else {
//           actLayerGroup.removeLayer(layerGroupDict[obj.target.id]);
//         }
//       } else {
//         var current = document.getElementsByClassName("active");
//         if (current.length > 0){
//           current[0].className = current[0].className.replace(" active", "");
//         }
//         this.className += " active";
//     }
//     });
//   }
// }


// Add active class to the current button (highlight it)
// Taken from https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_active_element
//Works!
// function loadActiveListener(){
//   var group = document.getElementById("act-filter-group");
//   var btns = group.getElementsByClassName("filterbtn");
//   for (var i = 0; i < btns.length; i++) {
//     btns[i].addEventListener("click", function() {
// // Current active elements
//       var current = document.getElementsByClassName("active");
// // Set current active to inactive
//       current[0].className = current[0].className.replace(" active", "");
//       this.className += " active";
//     });
//   }
// }
