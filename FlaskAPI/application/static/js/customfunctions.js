
function gpsmarker(feature, latlng){
  /**
  Returns marker for gps point.
  */
  return L.circleMarker(latlng,livemarkersettings);
};

function format_time(jsontime){
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
  console.log(hours)
  if (hours > 24){
    res = "Over a day old!"
    return res;
  } else if (hours < 24.0 && hours > 1.0){
    //Hours, minutes
    dif = new Date(msdif).toISOString().substr(11, 5);
    form_dif = dif.substr(0,2) + " Hours " + dif.substr(3,2) + " Minutes ago";
    return form_dif;
  } else if ( hours < 1 && seconds > 60) {
    //Minutes, seconds
    dif = new Date(msdif).toISOString().substr(14, 5);
    form_dif = dif.substr(0,2) + " Minutes " + dif.substr(3,2) + " Seconds ago";
    return form_dif;
  } else if (seconds < 60){
    return "Less than a minute ago!";
  } else {
    return "Time difference error!";
  }
};

function locationtext(poi,city,county,trail,disttrail){
  /**
  Formats location responses
  */
 if (["Home","Work"].includes(poi)){
   display_text = "<span class='poi-text'>" + poi + "</span>" + "" + region(city,county);
 } else if (poi !== null){
   trail_text = trailinfo(poi,trail,disttrail);
   region_text = region(city,county);
   display_text = "<br>" + poi + "" + trail_text + region_text;
 } else {
   display_text = region(city,county);
 };
return display_text
};

function nearestroad(road,distroad){
  /**
  Formats nearest road information.
  */
  road_text = road + " (" +
    distroad.toString().split(".")[0] + " feet away)"
  return road_text
};

function region(city,county){
  /**
  Formats region information.
  */
  if (city !== null){
    cityloc = "<br><div class='detail-context'>City:</div>" + city;
  } else {
    cityloc = "<br>City:<br>Not in a CA city";
  }
  if (county !== null){
    countyloc = "<br><span class='detail-context'>County:</span>" + county ;
  } else {
    countyloc = "<br>County:Not in California!";
  }
  res = cityloc + countyloc;
  return res;
};

function trailinfo(poi,trail,disttrail,speed){
  /**
  Formats trail information.
  */
  res = "<br>Nearest trail is:<br>" + trail + "<br>(" + disttrail.toString().split(".")[0] + " feet away";
  if (speed == 0){
    res += "<br>Not moving!";
  } else {
    res += "<br>Speed: " + "" + (speed*2.24).toString().split(".")[0] + "mph"
  }
  return res;
};

function batteryinfo(battery){
  /**
  Formats battery display.
  Add logic and calls to static files to display a battery icon.
  */
  return battery;
}

function batteryicon(battery){
/**
*/
if (battery >= 70){
  return "{{ url_for('static', filename='images/batterygreen.') }}";
} else if (battery >= 45){
  return "{{ url_for('static', filename='images/batteryyellow.') }}";
} else if (battery >= 10){
  return "{{ url_for('static', filename='images/batterydead.') }}";
} else {
  return "{{ url_for('static', filename='images/batteryerror.') }}";
};

function coors(lat,lon,provider){
  /**
  Formats location information.
  */
  lat = lat.toString().split(".")[0] + "." + lat.toString().split(".")[1].substr(0,4);
  lon = lon.toString().split(".")[0] + "." + lon.toString().split(".")[1].substr(0,4);
  if (provider == "network"){
    accur_stat = "(Low accuracy GPS!)";
  } else {
    accur_stat = "(High accuarcy GPS!)";
  }
  res = "Lat: " + lat + ", " + "Lon: " + lon + "<br>" + accur_stat + "";
  return res
};
