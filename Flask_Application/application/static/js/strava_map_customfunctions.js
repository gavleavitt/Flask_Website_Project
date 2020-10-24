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
  actLayerGroup.addLayer(addLayer);
};

// Helper functions called when user clicks a button, button IDs match the strings
// used in the equality statements
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
function loadActivityListener() {
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
        // change text of "All" to tell user that clicking it will remove all activity layers
        document.getElementById("All").innerHTML = "Clear all";
      // Check if user click target is a button flagged as active
      } else if (obj.target.className.includes("active")) {
        // Remove active class from button, reverting it to the disabled opacity
        this.className = this.className.replace(" active","");
        // If the target was the All button, clear all layers from display
        if (obj.target.id == "All"){
          // change text of "All" to tell user that clicking it will add all activity layers
          document.getElementById("All").innerHTML = "Add all";
          actLayerGroup.clearLayers()
        // if user clicks an active button that is not All, remove just that layer from display
        // A dictionary is used for lookup to select the correct layer using the target button's ID value
        } else {
          actLayerGroup.removeLayer(layerGroupDict[obj.target.id]);
        }
      // Check if user click target is NOT the "All" button, but the "All" button is flagged as active
      // Used to determine if a user is selecting activity button when the "All" button is active
      } else if ((!(obj.target.id.includes("All"))) && (document.getElementById("All").className.includes("active"))) {
          // Remove the active flag from the "All" button, reverting to disabled opacity
          document.getElementById("All").className = document.getElementById("All").className.replace(" active", "");
          // change text of "All" to tell user that clicking it will add all activity layers
          document.getElementById("All").innerHTML = "Add all";
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


function loadtimefilterlistener(){
  map.eachLayer(function(layer) {

  })
}
