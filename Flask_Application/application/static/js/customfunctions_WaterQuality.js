// Change "0" to ""<10" and null results to "Results Pending"
function subten(number){
  if (number == 0){
    return "<10"
  } else if (number == null) {
    return "Results Pending"
  } else {
  return number
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
