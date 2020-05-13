function format_time(jsontime){
   datetime = new Date(jsontime);
   datetime = datetime.toLocaleString()
   return datetime;
}


function timedif(jsontime){
  /**

  see https://stackoverflow.com/questions/1322732/convert-seconds-to-hh-mm-ss-with-javascript */
  currenttime = new Date();
  datetime = new Date(jsontime);
  msdif = (currenttime - datetime);
  seconds = msdif/1000;
  hours = seconds/3600;
  if (hours > 24){
    res = "Over a day old!"
    return res;
  }else if (24 > hours > 1){
    //Hours, minutes
    dif = new Date(msdif).toISOString().substr(11, 5);
    form_dif = dif.substr(0,2) + " Hours " + dif.substr(3,2) + " Minutes ago";
    return form_dif;
  }else if(hours < 1 && seconds > 60) {
    //Minutes, seconds
    dif = new Date(msdif).toISOString().substr(14, 5);
    form_dif = dif.substr(0,2) + " Minutes " + dif.substr(3,2) + " Seconds ago";
    return form_dif;
  }else if(seconds < 60){
    return "Less than a minute ago!";
  }else{
    return "Time difference error!";
  }
}

function locationtext(poi,city,county,trail,disttrail,road,distroad){
  /**
  Formats location responses
   */
   if (["Home","Work"].includes(poi)){
     location_text =  "Location:<br><b>" + poi + "</b>";
     display_text = region(city,county);
   }else if (poi !== null){
     trail_text = trailinfo(poi,trail,disttrail);
     region_text = region(city,county);
     display_text = "Location:" + "<br><b>" + poi + "</b>" + trail_text + region_text;
   }else{
     display_text = region(city,county);
   }
  road_text = "<br> Nearest road:<br><b>" + road + " (" +
  distroad.toString().split(".")[0] + " feet away)</b>"
  display_text += road_text
  return display_text
  }


function region(city,county){
  /**

  */
  if (city !== null){
    cityloc = "<br>City:<br><b>" + city + "</b>";
  }else{
    cityloc = "<br>City:<br><b>Not in a CA city</b>";
  }
  if (county !== null){
    countyloc = "<br>County:<br><b>" + county + "</b>";
  }else{
    countyloc = "<br>County:<br><b>Not in California!</b>";
  }
  res = cityloc + countyloc;
  return res;
}

function trailinfo(poi,trail,disttrail){
  res = "<br>Nearest trail is:<br><b>" + trail + "<br>(" + disttrail.toString().split(".")[0] + " feet away</b>)";
  return res;
}
