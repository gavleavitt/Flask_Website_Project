function setCSVStreamData(streamType){
  var csvURL = '/static/documents/4413728207.csv'
  // Issue jquery ajax request:
  $.ajax({
    url:csvURL,
    dataType: 'text'
  }).done(function(data){
    var csvDatObject = $.csv.toObjects(data);
    dataY = []
    dataX = []
    // var count = null
    // var max = null
    for (i of Object.keys(csvDatObject)){
      if (streamType == "elevation-stream-btn" || streamType === null){
        dataY.push(Math.round(parseFloat(csvDatObject[i].altitude)*3.28))
        yLabel = "Feet"
      } else if (streamType == "speed-stream-btn"){
        dataY.push((parseFloat(csvDatObject[i].velocity_smooth)*2.23694).toFixed(1))
        yLabel = "Speed(mph)"
      } else if (streamType == "grade-stream-btn") {
        dataY.push(parseFloat(csvDatObject[i].grade_smooth).toFixed(1))
        yLabel = "Grade(%)"
      }
      // dataX.push(parseInt(csvDatObject[i].time))
      dataX.push(new Date(parseInt(csvDatObject[i].time)*1000).toISOString().substr(11,5));
      // count += 1
      // if (parseInt(csvDatObject[i].time) > max){
      //   max = parseInt(csvDatObject[i].time)
      // }
    }
    // console.log("key count is:")
    // console.log(count)
    // console.log("max value is:")
    // console.log(max)
    // maxTime = (Object.keys(csvDatObject).length - 1)
    // data = {"x":xVal,"y":yVal};
    // console.log(data["y"])
    // console.log("Y data are:")
    // console.log(dataY)
    // console.log("X data are:")
    // console.log(dataX)
    // Process X-data, get the max time, not max length, convert to hours/minutes (string) then divide by 8 to get intervals. Create new X-dataset which is empty arrays, '', for the length of the original x/y dataset. Find the index locations within the original dataset that match with the new intervals then insert these at the index locations within the new x-dataset

    // see https://stackoverflow.com/questions/22064577/limit-labels-number-on-chart-js-line-chart
    // actChart.data.labels = ""
    // Use formatted data to generate legend labels and colors based on activity type
    // actStreamLineChart.data.datasets.data = dataY;
    actStreamLineChart.data.labels = dataX
    actStreamLineChart.data.datasets[0].data = dataY;
    actStreamLineChart.data.datasets[0].label = yLabel
    // actStreamLineChart.data.datasets.label = "test!"
    actStreamLineChart.options.legend.display = false
    actStreamLineChart.options.scales.yAxes[0].scaleLabel.labelString = yLabel
    // actStreamLineChart.data.datasets.label = "test2";
    // actChart.options.scales.yAxes[0].scaleLabel.labelString = getYLabelText();
    // actChart.options.title.text = tabDataType
    // Issue data update
    actStreamLineChart.update();
    // console.log(actStreamLineChart.data.datasets)
    // console.log(actStreamLineChart.data.labels)
    // console.log(actStreamLineChart)
  })
}


// Groups, zero-fills, and sorts activities by activity type and date to provide data that are formatted for use in Chart.JS. Format is: {ActivityType1:[{"x":x-value(dateValue),"y":y-value(distance, elevation, etc),"z":date-sorting value},...], ...}
function binActData(filteredGroup, btnSelection){
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
    // Add activity to object if not yet added, use index location to determine existence
    if (Object.keys(binnedActDataDict).indexOf(actType) == -1) {
      binnedActDataDict[actType] = [{"x":featDate,"y":yValue, "z":sortVal, "count":count}];
    } else {
      // Loop over all object entries checking if date matches, if so add feature's distance to it
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
      // If inDict is false then this date has not yet been added to the acttpye object, add date and distance to activity type object
      if (inDict == false){
        binnedActDataDict[actType].push({"x":featDate,"y":yValue, "z":sortVal, "count":count});
      }
    }
  }
  // console.log(JSON.parse(JSON.stringify(binnedActDataDict)))
  // Average values if tabDataType is an average
  if (tabDataType == "Avg Watts"){
    for (a of Object.keys(binnedActDataDict)) {
      for (i of Object.keys(binnedActDataDict[a])) {
        binnedActDataDict[a][i]["y"] = (binnedActDataDict[a][i]["y"]/binnedActDataDict[a][i]["count"])
      }
    };
  }

  // Convert seconds to hours
  if (tabDataType == "Time"){
    for (a of Object.keys(binnedActDataDict)) {
      for (i of Object.keys(binnedActDataDict[a])) {
        binnedActDataDict[a][i]["y"] = moment.duration(binnedActDataDict[a][i]["y"], 'seconds').asHours()
      }
    };
  }

  // Round y values
  for (a of Object.keys(binnedActDataDict)) {
    for (i of Object.keys(binnedActDataDict[a])) {
      binnedActDataDict[a][i]["y"] = Math.round(binnedActDataDict[a][i]["y"])
    }
  };
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
  return binnedActDataDict
};

// Generates label and color options for each activity type within a single array. Array is formatted to be accepted a Chart.JS setting
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

function createStreamLineChart(){
  var streamChart = document.getElementById('chart-line').getContext('2d');
  actStreamLineChart = new Chart(streamChart, {
    type: 'line',
    data:{
      // labels: [2,540,700],
      datasets:[{
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)'
        // data: [{"x":5,"y":65},{"x":600,"y":800}]
      }]
    },
    options:{
      scales:{
        xAxes:[{
          scaleLabel:{
            display: true,
            labelString: "Time(HH:MM)",
            fontSize: getChartTextSizes(),
            fontStyle: "bold",
            fontColor: "black",
          },
          ticks:{
            maxTicksLimit: 2,
            minRotation: 0,
            maxRotation: 0
          }
        }],
        yAxes:[{
          scaleLabel:{
            display: true,
            fontSize: getChartTextSizes(),
            fontStyle: "bold",
            fontColor: "black",
          },
          ticks:{
            beginAtZero: true
          }
        }]
      }
    }
  })
}

// Create initial Chart.JS barplot using initial load state of dashboard. Chart is updated with javascript events as selections are made
function createActivityChart(chartData) {
  var ctx = document.getElementById('chart').getContext('2d');
  actChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: getUniqueDateValues(chartData),
          datasets: generateDatasetOptions(chartData)
      },
      options: {
        responsive: true,
        // maintainAspectRatio: false,
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

// function activateChartButton(){
//   // When user picks a new date range or activity type, active the correct active chart type button
//   console.log("Activating button for:")
//   console.log(document.querySelector('.show-data').querySelectorAll(".chart-active")[0])
//   document.querySelector('.show-data').querySelectorAll(".chart-active")[0].click()
// }

// Update chart labels and datasets based on user button selections
// function updateChart(filteredGroup,tabDataType){
function updateChart(filteredGroup,tabDataType){
  // console.log(document.querySelector('.show-data').querySelectorAll(".chart-active"))
  // // Create formatted dataset
  // chartData = binActData(filteredGroup, tabDataType);
  var actCount = parseInt(document.getElementById("actCount").innerText)
  // see https://stackoverflow.com/a/55972382 for div update method
  if (actCount == 0){
    document.getElementById("chart-cont").classList.remove("show-data");
    document.getElementById("chart-line-cont").classList.remove("show-data");
  	document.getElementById("no-data-text").classList.add("show-data");
  } else if (actCount == 1) {
    // Create formatted dataset
    btnSelection = document.querySelectorAll('.singleAct.chart-active')[0].id
    // chartData = binActData(filteredGroup, btnSelection);
    setCSVStreamData(btnSelection);
    document.getElementById("chart-cont").classList.remove("show-data")
    document.getElementById("no-data-text").classList.remove("show-data");
    document.getElementById("chart-line-cont").classList.add("show-data");
  } else {
    // Create formatted dataset
    btnSelection = document.querySelectorAll('.multiAct.chart-active')[0].id
    chartData = binActData(filteredGroup, btnSelection);
    // console.log("btnsel is:")
    // console.log(btnSelection)
    document.getElementById("no-data-text").classList.remove("show-data");
    document.getElementById("chart-line-cont").classList.remove("show-data");
    document.getElementById("chart-cont").classList.add("show-data");
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
    if (actCount <= 10 || (userStart.substr(5,2) == userEnd.substr(5,2))) {
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
