function format_time(jsontime){
   datetime = new Date(jsontime);
   datetime = datetime.toLocaleString()
   return datetime;
}


function timedif(jsontime){
  /*see https://stackoverflow.com/questions/1322732/convert-seconds-to-hh-mm-ss-with-javascript */
  currenttime = new Date();
  datetime = new Date(jsontime);
  msdif = (currenttime - datetime);
  seconds = msdif/1000;
  hours = seconds/3600;
  if (hours > 24){
    return "Over a day old!"
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
  } else if(seconds < 60){
    return "Less than a minute ago!";
    //dif = new Date(msdif).toISOString().substr(17, 2)
    //form_dif = dif + " Seconds ago"
  }else{
    return "Time difference error!";
  }
}
