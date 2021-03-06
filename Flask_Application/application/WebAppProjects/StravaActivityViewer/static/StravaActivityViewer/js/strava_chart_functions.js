// Groups, zero-fills, and sorts activities by activity type and date to provide data that are formatted for use in Chart.JS. Format is: {ActivityType1:[{"x":x-value(dateValue),"y":y-value(distance, elevation, etc),"z":date-sorting value},...], ...}
function binActData(filteredGroup, btnSelection){
  //TODO
  // if (clear == "Yes"){
  //   geoJSONDat = null
  // }
  // Convert data in filtered group into GeoJSON format so its easier to process and extract details from
  geoJSONDat = filteredGroup.toGeoJSON()
  // console.log("raw geojson is:")
  // console.log(JSON.parse(JSON.stringify(geoJSONDat)))
  binnedActDataDict = {}
  // This logs the state upon creation, normal console.log() returns as it is when viewing, doesn't reflect state at the time of processing
  // I think this creates a clone of the data as a string at this point in time instead of referring to the object itself
  // console.log is async and objects are logged when expanded, not when calculated. see:
  // https://stackoverflow.com/questions/11214430/wrong-value-in-console-log
  // console.log(JSON.parse(JSON.stringify(binnedActDataDict)))
  var dateDataList = []
  var yearList = []
  // Set dateType based on current user daterange selection
  var dateType = checkDateRange();
  // console.log("datatype is:")
  // console.log(dateType)
  var sortVal = null
  var featDate = null
  var count = 0
  // Iterate over features in the raw geojson dataset and get the x and z values for the binned chart data based on the selected date type
  for (i of geoJSONDat.features) {
    var actType = i.properties.type_extended
    if (dateType == "default/year") {
      featDate = i.properties.startDate.substr(0,4);
      sortVal =  parseInt(i.properties.startDate.substr(0,4))
    } else if (dateType == "month") {
      featDate = sortLookUp(parseInt(i.properties.startDate.substr(5,2)), "month")['label'];
      sortVal = sortLookUp(parseInt(i.properties.startDate.substr(5,2)), "month")['sort'];
    } else if (dateType == "week") {
      featDate = sortLookUp(parseInt(i.properties.startDate.substr(8,2)), "week")['label'];
      sortVal = sortLookUp(parseInt(i.properties.startDate.substr(8,2)), "week")['sort'];
    } else if (dateType == "day") {
      // console.log("Datetype is day, setting featdate and sortVal!")
      featDate = i.properties.startDate.substr(5,5)
      sortVal =  parseInt(i.properties.startDate.substr(8,2))
    }
    //
    // console.log("Tab datatype is:")
    // console.log(tabDataType)
    // Get the binned chart data y-value based on user selected button
    if (btnSelection == "count-btn"){
      var yValue = 1
    } else if (btnSelection == "distance-btn") {
      var yValue = i.properties.distance * 0.000621371;
    } else if (btnSelection == "elevation-btn") {
      var yValue = i.properties.total_elevation_gain * 3.28084;
    } else if (btnSelection == "time-btn") {
      var yValue = i.properties.moving_time;
    } else if (btnSelection == "Avg Speed") {
      var yValue = i.properties.average_speed;
      count = 1;
    } else if (btnSelection == "avgwatt-btn"){
      var yValue = i.properties.average_watts;
      count = 1
    }
    // Add activity to binnedActDataDict object if not yet added, use index location to determine existence in object
    // Each activity is added seperately to the object, if the activity has already been added then add to existing, if not add it to the object
    if (Object.keys(binnedActDataDict).indexOf(actType) == -1) {
      binnedActDataDict[actType] = [{"x":featDate,"y":yValue, "z":sortVal, "count":count}];
    } else {
      // activity is already part of the binnedActDataDict object, loop over all object entries checking if date matches, if so add feature's distance to it
      // Use inDict to track if dateValue is already inside activity object
      var inDict = false
      for (a of binnedActDataDict[actType]){
        if (a["x"] == featDate){
          a["y"] += yValue;
          a["count"] += count
          // Set inDict date flag to true and break, no need to keep looping over stored dates
          inDict = true
          break;
        }
      }
      // If inDict is false then this date has not yet been added to the acttype object, add date and distance to activity type object
      if (inDict == false){
        binnedActDataDict[actType].push({"x":featDate,"y":yValue, "z":sortVal, "count":count});
      }
    }
  }
  // console.log(JSON.parse(JSON.stringify(binnedActDataDict)))
  // Average values if tabDataType is an average and set the y value
  if (btnSelection == "avgwatt-btn"){
    for (a of Object.keys(binnedActDataDict)) {
      for (i of Object.keys(binnedActDataDict[a])) {
        binnedActDataDict[a][i]["y"] = (binnedActDataDict[a][i]["y"]/binnedActDataDict[a][i]["count"])
      }
    };
  }
  // Convert seconds to hours:minutes and set the y value
  if (btnSelection == "time-btn"){
    for (a of Object.keys(binnedActDataDict)) {
      for (i of Object.keys(binnedActDataDict[a])) {
        // binnedActDataDict[a][i]["y"] = moment.duration(binnedActDataDict[a][i]["y"], 'seconds').asHours()
        binnedActDataDict[a][i]["y"] = (moment.duration(binnedActDataDict[a][i]["y"], 'seconds').hours() + "." + moment.duration(binnedActDataDict[a][i]["y"], 'seconds').minutes())
      }
    };
  }

  // Round y values
  if (btnSelection != "time-btn"){
    for (a of Object.keys(binnedActDataDict)) {
      for (i of Object.keys(binnedActDataDict[a])) {
        binnedActDataDict[a][i]["y"] = (binnedActDataDict[a][i]["y"]).toFixed(0)
      }
    };
  }
  // Get single array of all unique dateValues(x-axis groupings/labels) in activity object, including all activity types
  // Add dateValues and zero-filled y-values to any activity type missing a unique dateValue
  // This ensures that all datasets are of the same length, even if some activity types don't have activities in that time period.
  // This ensures that mouse-over data values show the correct information. I think these mouse-over values use a index based on all dateValues in the table, any empty values break the index and may result in incorrect values
  uniqueLabels = getUniqueDateValues(binnedActDataDict);
  for (label of uniqueLabels){
    for (actType of Object.keys(binnedActDataDict)) {
      actLabelList = []
      for (dateEntry of Object.keys(binnedActDataDict[actType])) {
        actLabelList.push(binnedActDataDict[actType][dateEntry]["x"]);
      }
      if (!actLabelList.includes(label)){
        binnedActDataDict[actType].push({"x":label,"y":0,"z":sortLookUp(label,dateType)["sort"]});
      }
    }
  }
  // Sort dates from low to high based on the z sort value
  // see https://stackoverflow.com/a/979289
  // I have no idea how this works
  for (actType of Object.keys(binnedActDataDict)) {
    binnedActDataDict[actType].sort((a, b) => parseFloat(a.z) - parseFloat(b.z));
  }
  // console.log(JSON.parse(JSON.stringify(binnedActDataDict)))
  // Patch fix, for some reason a null entry is coming through, may be stored as null in database
  delete binnedActDataDict.null
  return binnedActDataDict
};




// Generates label and color options for each activity type within a single array. Array is formatted to be a Chart.JS setting
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

function setDisplaysize(){
  dimen = {'width': window.innerWidth,'height':window.innerHeight};
}

function getChartTextSizes(){
  // var dimen = getDisplaysize();
  if (dimen.width <= 1300) {
    return 12;
  } else {
    return 16;
  }
}

function setChartTextSizes(){
  // dimen = getDisplaysize();;
  if (dimen.width <= 1300 && dimen.width > 800){
    size = 12;
  } else if (dimen.width <= 800) {
    size = 12
  } else {
    size = 16;
  }
  actChart.options.title.fontSize = size;
  actChart.options.legend.labels.fontSize = size;
  // Issue data update
  actChart.update();
}

function getYLabelText(tabDataType){
  if (tabDataType == "count-btn"){
    return "Count"
  } else if (tabDataType == "distance-btn"){
    return "Miles"
  } else if (tabDataType== "elevation-btn"){
    return "Feet"
  } else if (tabDataType== "Average Speed"){
      return "Speed (mph)"
  } else if (tabDataType == "time-btn"){
    return "Hours"
  } else if (tabDataType == "avgwatt-btn") {
    return "Avg Watts"
  }
}

// Create initial Chart.JS barplot using initial load state of dashboard. Chart is updated with javascript events as selections are made
// To add events and grab details see:
// https://stackoverflow.com/a/58222435
// https://stackoverflow.com/a/41870115
// https://stackoverflow.com/a/44160605
function createActivityChart(chartData) {
  var ctx = document.getElementById('chart').getContext('2d');
  actChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: getUniqueDateValues(chartData),
          datasets: generateDatasetOptions(chartData)
      },
      options: {
        // Trying to set point radius, doesnt appear to work
        elements:{
          point:{
            radius: 0,
            pointRadius: 0
          }
        },
        onClick:function(click,item) {
          // console.log("Clicked!")
          // console.log(click)
          // console.log(item)
          // dat = i[0];
          // var x_value = this.data.labels[dat._index];
          // var y_value = this.data.datasets[0].data[dat._index];
          // console.log(x_value);
          // console.log(y_value);
        },
        responsive: true,
        maintainAspectRatio: false,
        title:{
          display: true,
          // text: tabDataType,
          fontSize: getChartTextSizes(),
          fontColor: "black",
          padding: 5
        },
        legend: {
          labels:{
            fontSize: getChartTextSizes(),
            fontStyle: "bold",
            fontColor: "black",
            padding: 5
          }
        },
        // https://stackoverflow.com/questions/55428160/wrong-label-value-is-displayed-on-point-hover-chart-js
        scales: {
          xAxes:[{
            // type: 'time',
            // stacked:true
          }],
          yAxes: [{
            afterFit: function(scale) {
              // scale.width = 56  //<-- set value as you wish
            },
            scaleLabel: {
              display: true,
              labelString: getYLabelText("count-btn"),
              fontSize: getChartTextSizes(),
              fontStyle: "bold",
              fontColor: "black",
              padding: 5
              // fontStyle: "bold"
            },
            // stacked:true,
            ticks: {
              beginAtZero: true,
              maxTicksLimit: 8
            }
          }]
        }
      }
  });
};


// Update chart labels and datasets based on user button selections
function updateChart(filteredGroup,tabDataType){
  // console.log(document.querySelector('.show-data').querySelectorAll(".chart-active"))
  // // Create formatted dataset
  // chartData = binActData(filteredGroup, tabDataType);
  var actCount = parseInt(document.getElementById("actCount").innerText)
  // see https://stackoverflow.com/a/55972382 for div update method
  if (actCount == 0){
    // TODO:
    // chartData = binActData(filteredGroup, btnSelection);
    // clear out binned actdata
    // actDataDict = {"count":null, "dist":null, "elev":null, "calories":null, "totalTime":null, "speed":null, "moveTime":null}
    geoJSONDat = null
    document.getElementById("chart-cont").classList.remove("show-data");
    document.getElementById("chart-cont").classList.add("no-data");
    document.getElementById("chart-line-cont").classList.remove("show-data");
    document.getElementById("chart-line-cont").classList.add("no-data");
  	document.getElementById("no-data-text").classList.add("show-data");
    document.getElementById("no-data-text").classList.remove("no-data");
  } else if (actCount == 1) {
    // Create formatted dataset
    btnSelection = document.querySelectorAll('.singleAct.chart-active')[0].id
    // chartData = binActData(filteredGroup, btnSelection);
    // setCSVStreamData(btnSelection,filteredGroup);
    handleStreamChartUpdate(btnSelection, filteredGroup);
    // Export filtered group data to GeoJSON, this is a patch fix since this is needed for single activity processing.
    // This step is normally called when actCount > 1, consider having this step occur before the actCount logic
    // getCSVData(btnSelection, filteredGroup)
    // https://stackoverflow.com/a/43909756
    document.getElementById("chart-cont").classList.remove("show-data");
    document.getElementById("chart-cont").classList.add("no-data");
    document.getElementById("no-data-text").classList.remove("show-data");
    document.getElementById("no-data-text").classList.add("no-data");
    document.getElementById("chart-line-cont").classList.add("show-data");
    document.getElementById("chart-line-cont").classList.remove("no-data");
    // $("chart-line-cont").fadeIn();
  } else {
    btnSelection = document.querySelectorAll('.multiAct.chart-active')[0].id
    // Create formatted dataset
    chartData = binActData(filteredGroup, btnSelection);
    // console.log("btnsel is:")
    // console.log(btnSelection)
    document.getElementById("no-data-text").classList.remove("show-data");
    document.getElementById("no-data-text").classList.add("no-data");
    document.getElementById("chart-line-cont").classList.remove("show-data");
    document.getElementById("chart-line-cont").classList.add("no-data");
    document.getElementById("chart-cont").classList.add("show-data");
    document.getElementById("chart-cont").classList.remove("no-data");

    // Calculate date labels (x-axis)
    actChart.data.labels = getUniqueDateValues(chartData);
    // Use formatted data to generate legend labels and colors based on activity type
    actChart.data.datasets = generateDatasetOptions(chartData);
    actChart.options.scales.yAxes[0].scaleLabel.labelString = getYLabelText(btnSelection);
    // actChart.options.title.text = tabDataType
    // Issue data update
    actChart.update();
  }
}

function checkDateRange(){
  if ((typeof userStart !== 'undefined') && (typeof userEnd !== 'undefined')) {
    //Get activity count:
    var actCount = parseInt(document.getElementById('actCount').innerHTML)
    if (actCount <= 10 || (userStart.substr(2,2) == userEnd.substr(2,2))) {
      return "day"
    } else if (userStart.substr(0,4) !== userEnd.substr(0,4)){
      return "default/year"
    } else {
      return "month"
    }
  } else {
    return "default/year";
  }
}

// Create a single array of unique dateValue/label values that includes all activity types, used to generate x-axis labels to and determine if any dateValues need 0 values added
function getUniqueDateValues(chartData){
  labelList = []
  for (i of Object.keys(chartData)){
    for (a of Object.keys(chartData[i])) {
      if (!labelList.includes(chartData[i][a]["x"])) {
        labelList.push(chartData[i][a]["x"])
      };
    }
  };
  return labelList;
};

// Sort and Label value lookups for all dateValue and dateType entries. Used to allow sorting on non-date formatted dateValue aggregations. DateValue strings and integers are handled.
function sortLookUp(dateValue, dateType=null) {
  if ((dateType == "month") && ((dateValue == 1) || (dateValue == 2))){
    return {"label":"Jan-Feb", "sort":1};
  } else if ((dateType == "month") && ((dateValue == 3) || (dateValue == 4))){
    return {"label":"Mar-Apr", "sort":2};
  } else if ((dateType == "month") && ((dateValue == 5) || (dateValue == 6))){
    return {"label":"May-Jun", "sort":3};
  } else if ((dateType == "month") && ((dateValue == 7) || (dateValue == 8))){
    return {"label":"Jul-Aug", "sort":4};
  } else if ((dateType == "month") && ((dateValue == 9) || (dateValue == 10))){
    return {"label":"Sep-Oct", "sort":5};
  } else if ((dateType == "month") && ((dateValue== 11) || (dateValue == 12))){
    return {"label":"Nov-Dec", "sort":6};
  } else if ((dateType == "week") && (dateValue >= 1 && dateValue <= 7)){
    return {"label":"Week 1", "sort":1};
  } else if ((dateType == "week") && (dateValue >= 8 && dateValue <= 15)){
    return {"label":"Week 2", "sort":2};
  } else if ((dateType == "week") && (dateValue >= 16 && dateValue <= 23)){
    return  {"label":"Week 3", "sort":3};
  } else if ((dateType == "week") && (dateValue >= 24 && dateValue <= 31)){
    return  {"label":"Week 4", "sort":4};
  } else if (dateValue == "Jan-Feb"){
    return {"sort":1}
  } else if (dateValue == "Mar-Apr"){
    return {"sort":2}
  } else if (dateValue == "May-Jun"){
    return {"sort":3}
  } else if (dateValue == "Jul-Aug"){
    return {"sort":4}
  } else if (dateValue == "Sep-Oct"){
    return {"sort":5}
  } else if (dateValue == "Nov-Dec"){
    return {"sort":6}
  } else if (dateType == "default/year"){
    return {"sort":parseInt(dateValue)};
  }  else if (dateType == "week" && dateValue == "Week 1"){
    return {"sort":1}
  } else if (dateType == "week" && dateValue == "Week 2"){
    return {"sort":2}
  } else if (dateType == "week" && dateValue == "Week 3"){
    return {"sort":3}
  } else if (dateType == "week" && dateValue == "Week 4"){
    return {"sort":4}
  } else if (dateType == "day") {
    return {"sort":parseInt(dateValue.substr(3,2))}
  }
}

function updateChartBtn(btnID,actDataSource){
  // console.log(document.querySelectorAll('.chart-active')[0].classList)
  if (actDataSource == "topoJSON"){
    for (i of document.querySelectorAll('.multiAct.chart-active')){
      i.classList.remove("chart-active")
    }
    // document.querySelectorAll('.multiAct, .chart-active')[0].classList.remove("chart-active")
  } else {
    for (i of document.querySelectorAll('.singleAct.chart-active')){
      i.classList.remove("chart-active")
    }
    // console.log(document.querySelectorAll('.singleAct, .chart-active')[0].classList)
    // document.querySelectorAll('.singleAct, .chart-active')[0].classList.remove("chart-active")
  }
  document.getElementById(btnID).classList.add("chart-active")
}

//// TODO:
// Get point at distance along line
// see http://turfjs.org/docs/#along
function getDistanceAlongLine(portionAlong){

}
