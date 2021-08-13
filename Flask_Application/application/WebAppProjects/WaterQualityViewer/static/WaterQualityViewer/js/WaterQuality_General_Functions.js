// Modal from https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_modal
// Get the modal
var modal = document.getElementById("myModal");

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
// Open modal when window loads
window.onload = function(){
  modal.style.display = "block";
}

// see https://github.com/Leaflet/Leaflet/issues/4811
// calculatues window size, used for determining if the user's screen is small
const windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
const windowHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
const windowArea = windowWidth * windowHeight;

//Set email address using Javascript, harder for crawlers to grab
var email = "gav" + "lea" + "web" + "@g" + "mail" + ".com";
document.getElementById("emailaddr").innerHTML = "<a href='mailto:" + email + "'>" + email + "</a>"
// Make basemaps
// var streetsnight = L.esri.Vector.basemap('StreetsNight');
var imageryesri = L.esri.basemapLayer('Imagery');

var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
// var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'})

var pointstyle = {
  radius: 8,
  fillColor:"#aba9db",
  color: "#000",
  weight: 1,
  fillOpacity: 0.7
};

// intilize map with basemap:
var map = L.map('map',
  {layers: [osm]}).setView([34.7,-119.86],10);
// Add flaticon attribution
if (window.innerWidth > 500){
  map.attributionControl.addAttribution("Icons made by <a href='https://www.flaticon.com/authors/freepik' title='Freepik'>Freepik</a> taken from <a href='https://www.flaticon.com/' title='Flaticon'> www.flaticon.com</a> and edited by Gavin Leavitt")
}
// map.attributionControl.addAttribution("Icons made by <a href='https://www.flaticon.com/authors/freepik' title='Freepik'>Freepik</a> taken from <a href='https://www.flaticon.com/' title='Flaticon'> www.flaticon.com</a> and edited by Gavin Leavitt")
// Add beach report records as geoJSON to map
beachreports = L.geoJSON(waterquality_geojson, {
// Create custom icons for each point, depending on its open status
  pointToLayer: function(feature, latlng){
    if (feature.properties.BeachStatus == "Open"){
      var beach_icon = L.icon({
        iconUrl: beachOpenIconUrl,
        iconSize: [50, 50]
      });
    }else if (feature.properties.BeachStatus == "Warning"){
      var beach_icon = L.icon({
        iconUrl: beachWarningIconUrl,
        iconSize: [50, 50]
      });
    }else if (feature.properties.BeachStatus == "Closed"){
      var beach_icon = L.icon({
        iconUrl: beachClosedIconUrl,
        iconSize: [50, 50]
      });
    }
    // Add marker for each beach
    return L.marker(latlng,{icon: beach_icon});
  },
  // Populate popup window text for each feature
  onEachFeature: function(feature,layer){
    // layer.bindTooltip(feature.properties.Name, {
    // 	permanent: true,
    // 	// offset: [0, -30],
    // 	'className': 'beachLabel'
    // })
    // Init chart when user clicks a beach
    // layer.on('click', function(e){
    // 	createChart(feature.properties.Name);
    // })

    // Set beach name variable when user clicks on a beach
    layer.on('click', function(e){
      clickedBeach = feature.properties.Name;
    })


    // Bind popup contents
    layer.bindPopup(
        '<div class="tabs">' +  '<div class="tab" id="tab-1">' +
        '<div id="text-content" class="content">' +
        '<div class="spanbotbord"><b>' + feature.properties.Name + '</b></div>' +
        '<span>PDF Report (Release) Date: <b>' + feature.properties.insDate + '</b></span>' +
        '<br><span>Beach status: <b>' + colortext(feature.properties.BeachStatus) + '</b></span>' +
        '<br><span>Fecal Coliform Count: <b>' + subTenOrExceeds(feature.properties.FecColi,standards["Fecal Coliform State Health Standard"]) + '</b> (' + standards["Fecal Coliform State Health Standard"].toLocaleString() + ')</span>' +
        '<br><span>Total Coliform Count: <b>' + subTenOrExceeds(feature.properties.TotColi,standards["Total Coliform State Health Standard"]) + '</b> (' + standards["Total Coliform State Health Standard"].toLocaleString() + ')</span>' +
        '<br><span>Enterococcus Count: <b>' + subTenOrExceeds(feature.properties.Entero,standards["Enterococcus State Health Standard"]) + '</b> (' + standards["Enterococcus State Health Standard"].toLocaleString() + ')</span>' +
        '<br><span>Exceeds Coliform Ratio: <b>' + subTenOrExceeds(feature.properties.ExceedsRatio) + '</b></span>' +
        '<br><span>Reporting week: <b>' + feature.properties.pdfDate + '</b></span>' +
        '<br><span>Report Link: <b><a href=' + feature.properties.s3PDFURL + '>Download PDF</a></b></span>' +
        '<br><span><b>*</b>Results are given as MPN (most probable number), an approximation of bacteria per 100 ml of water.<span>' +
        '<br><span><b>**</b>State Health Standards are enclosed with parentheses, (), as MPN.</span>' +
        '</div>' +
        '</div>' +
        '<div class="tab" id="hist-Tab">' +
        '<div id="hist-content" class="content">' +
        '<canvas id=history-chart></canvas>' +
        '</div>' +
        '</div>' +
        '<ul id="tabs-link" class="tabs-link">' +
        '<li id="current" class="tab-link active-link"><span>Current</span></li>' +
        '<button id="history-button" class="tab-link" onclick="createChart(clickedBeach)"><li id="History"><span>History</span></li></button>' +
        '</ul>' +
        '</div>'
    )
    // see https://github.com/Leaflet/Leaflet/issues/4811
    // Query Leaflet control/UI elements
    // leaflet-top elements
    const leafletTopElements = document.querySelectorAll('div.leaflet-top');
    // leaflet-bottom elements
    const leafletBottomElements = document.querySelectorAll('div.leaflet-bottom');
    // Pop-up control for small screen sizes
    if (windowArea < 315000 ) {
        // Hide leaflet controls when pop-up opens
        layer.on('popupopen', function() {
            leafletTopElements.forEach(function(element) {
                element.style.opacity = 0;
            });

            leafletBottomElements.forEach(function(element) {
                element.style.opacity = 0;
            });
        });
        // Display Leaflet controls when pop-up closes
        layer.on('popupclose', function() {
            leafletTopElements.forEach(function(element) {
                element.style.opacity = 1;
            });

            leafletBottomElements.forEach(function(element) {
                element.style.opacity = 1;
            });
        });
    }
  }
}).addTo(map);


beachreports.on('click', function(event){
  // Reset size of popup
  var popupContent = document.getElementsByClassName('leaflet-popup-content-wrapper')
  popupContent[0].style.width = "auto";
  popupContent[0].style.height = "auto";
  // Reset active-link status
  var current = document.getElementById("current");
  current.classList.add("active-link");

  // popupContent[0].style.height = "300px";
  // Add active class to the current button (highlight it)
  // var header = document.getElementById("tabs-link");
  var btns = document.getElementsByClassName("tab-link");
  // console.log(btns)
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
      // console.log("Adding event listeners!")
      var currentActive = document.getElementsByClassName("active-link");
      currentActive[0].className = currentActive[0].className.replace(" active-link", "");
      this.className += " active-link";
      if (currentActive[0].id == "current"){
        // console.log("Clicked current tab")

        // Reset context arrow location
        var contextArrow = document.getElementsByClassName('leaflet-popup-tip-container')[0]
        contextArrow.style.marginLeft = "-20px";

        // Hide chart div
        var historyChartContent = document.getElementById('hist-Tab');
        historyChartContent.style.display = "none";
        // Reset size of popup
        var popupContent = document.getElementsByClassName('leaflet-popup-content-wrapper')
        popupContent[0].style.width = "auto";
        popupContent[0].style.height = "auto";
        var textContent = document.getElementById('text-content');
        textContent.style.display = "block";
        // popupContent[0].style.height = "300px";
      } else if (currentActive[0].id == "history-button") {
        // var popupContent = document.getElementsByClassName('leaflet-popup-content-wrapper')
        // popupContent[0].style.height = "320px";
        // var histContent = document.getElementById('hist-content');
        // histContent.style.height = "200px";
        // var textContent = document.getElementById('text-content');
        // textContent.style.display = "none";
      }
    });
  }
});


// Basemaps dictionary used for layer control
var basemaps = {
  "<span>Imagery (Raster)</span>": imageryesri,
  "<span>OSM (Vector)</span>": osm
};
// Styling for text of layers
var layers = {
  "<span><b>Beaches</b></span>":beachreports
}
//Add control menu for basemaps
L.control.layers(basemaps,layers).addTo(map);

//This requires HTTPS to work!
//L.control.locate({drawCircle: false, showCompass: false}).addTo(map);

//Leaflet search, see https://github.com/stefanocudini/leaflet-search
// Build search control object, set to search beach name
var searchControl = new L.Control.Search({
  layer: beachreports,
  propertyName: 'Name',
  zoom:15,
  marker:false,
  autoCollapse:true
});

//Adds a .on listener to pan to selected location and open a popup
//See example: https://github.com/stefanocudini/leaflet-search/blob/master/examples/geojson-layer.html
searchControl.on('search:locationfound', function(e) {
  //e.layer.setStyle({fillColor: '#3f0', color: '#0f0'});
  //Not sure how this works, opens popup
  if(e.layer._popup)
    e.layer.openPopup();
});

searchControl.on('search:expanded', function(e) {
  map.closePopup()
});

map.addControl(searchControl); // Add control to map

//Add a legend using native Leaflet customfunctions
var legend = L.control({position: 'bottomright'});
//Populate legend by creating a div inside Leaflet to hold divs, images, and text
//These will be added to the legend object using .onAdd when the container is added to the DOM
legend.onAdd = function (map) {
  var div = L.DomUtil.create('div', 'infolegend');
  div.innerHTML =  "<div class='legendheader spanbotbord'><b>Beach Status</b><span>"
  div.innerHTML += "<div><img src='" + beachOpenIconUrl + "' class='legendicon'><span class='legendtext'>Open</span></div>";
  div.innerHTML += "<div><img src='" + beachWarningIconUrl + "'class='legendicon'><span class='legendtext'>Warning</span></div>";
  div.innerHTML += "<div><img src='" + beachClosedIconUrl + "'class='legendicon'><span class='legendtext'>Closed</span></div>";
  return div;
};
// Add legend to map
legend.addTo(map);

// Set last updated text using the most recent record date
document.getElementById("Title").innerHTML += "<div id='last-updated'>(Last updated " + recentrecord + ")</div>"

// Change "0" to ""<10" and null results to "Results Pending"
function subTenOrExceeds(number, standard){
  if (number == 0){
    return "<10"
  } else if (number == null) {
    return "Results Pending"
  } else if (number > standard) {
    return "<span style='color:#ff8400'>" + number.toLocaleString() + "</span>"
  } else if (number == "Yes") {
    return "<span style='color:#ff8400'>" + number + "</span>"
  } else {
    return number.toLocaleString()
  }
};

// Color open status text depending on status
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
