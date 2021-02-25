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
