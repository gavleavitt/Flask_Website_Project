
// zoom is slow, look into https://github.com/chartjs/chartjs-plugin-zoom/issues/356
// zoomPlugin = {
//   zoom: {
// 							pan: {
// 								enabled: true,
// 								mode: 'y'
// 							},
// 							zoom: {
// 								enabled: true,
// 								mode: 'y'
// 							}
// 						}
// }

// function getDistanceAlongLine(portionAlong){
//   // Get active geometry from Leaflet
//   // variable holding active data
//   console.log(portionAlong);
//   // filteredGroup.eachLayer(function(layer){
//   //   console.log(layer)
//   // })
// };


// Creates single activity chart in initial state with placeholder data, this allows for a better initial transition from the multi-activity bar plot
function createStreamLineChart(){
  // See: https://stackoverflow.com/a/45172506
  // Method taken from: https://stackoverflow.com/a/45800841
  // Adds vertical bar based on cursor location
  Chart.plugins.register({
     afterDatasetsDraw: function(chart) {
        if (chart.tooltip._active && chart.tooltip._active.length) {
           var activePoint = chart.tooltip._active[0],
              ctx = chart.ctx,
              y_axis = chart.scales['y-axis-0'],
              x = activePoint.tooltipPosition().x,
              topY = y_axis.top,
              bottomY = y_axis.bottom;
           // draw line
           ctx.save();
           ctx.beginPath();
           ctx.moveTo(x, topY);
           ctx.lineTo(x, bottomY);
           ctx.lineWidth = 2;
           ctx.strokeStyle = '#0f0f0f';
           ctx.stroke();
           ctx.restore();
        }
     }
  });
  // Consider using down-sample plugin to reduce data size: https://github.com/AlbinoDrought/chartjs-plugin-downsample
  var streamChart = document.getElementById('chart-line').getContext('2d');
  actStreamLineChart = new Chart(streamChart, {
    type: 'line',
    data:{
      labels: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
      datasets:[{
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data:[30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30],
        pointHitRadius: 0,
        pointHoverRadius: 0,
      },{
        backgroundColor: 'rgb(0, 0, 0, 0)',
        borderColor: 'rgb(82, 82, 82, 0.8)',
        fill: false,
        borderWidth: 3,
        data:[30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30],
        pointHitRadius: 0,
        pointHoverRadius: 0,
      }]
    },
    options:{
      hover: {
         // mode: 'nearest',
         // intersect: true,
         mode: 'index',
         intersect: false,
         // see https://stackoverflow.com/a/58529907
         // place onHover in here with hover options so I can extend the functionality
         onHover: function(event, activeElements) {
           if (activeElements.length > 0){
             // Get index location of on hover event
             var index = activeElements[0]._index;
             // Get latlngs at cursor location
             var latlng = csvDatObject[index]['latlng'].split(",");
             //Clear any existing markers
             markerGroup.clearLayers();
             // close any open popups
             map.closePopup();
             // Add new marker to marker group
             L.marker([latlng[0],latlng[1]]).addTo(markerGroup);
           }
         }
      },
      tooltips: {
        mode: 'index',
        caretPadding: 50,
        // xAlign: "left",
        // custom alighment: https://stackoverflow.com/a/54988724
        position: 'cursor',
        intersect: false,
        // Filter out average bar tooltip information
        filter: function (tooltipItem) {
          // Get dataset index value
          var dSet = tooltipItem.datasetIndex;
          // Average dataset will always be dataset index 1
          if (dSet == 1) {  // <-- dataset index
              return false;
          } else {
              return true;
          }
        },
        // Populate ancillary data in tooltip
        callbacks: {
           afterBody: function(t, d) {
              // Get hover location index
              index = t[0].index
              return populateAncillaryData(index)
           }
        }
      },
      elements:{
        point:{
          radius:0,
          pointRadius: 0
        },
        line:{
          borderWidth: 1
        }
      },
      scales:{
        xAxes:[{
          // Added, testing if zoom plugin works better with large data if x is set to time
          // type: "time",
          // time: {
          //   format: 'HH:mm',
          //    unit: 'minute',
          //    // unit: 'hour',
          //    displayFormats: {
          //      minute: 'HH:mm'
          //      // hour: 'HH:mm'
          //    }
          //  },
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
      },
      // plugins: zoomPlugin
    }
  })
  // see https://stackoverflow.com/questions/38072572/position-tooltip-based-on-mouse-position
  // Tooltip draws at mouse cursor position, instead of at intersection point with dataset
  Chart.Tooltip.positioners.cursor = function(chartElements, coordinates) {
    return coordinates;
   };
}

function getS3StreamURL(actID){
  csvAPIURL = '/api/v0.1/getstravastreamurl'
  return $.ajax({
      url:csvAPIURL,
      //https://stackoverflow.com/questions/47523265/jquery-ajax-no-access-control-allow-origin-header-is-present-on-the-requested
      data: {actID:actID},
      type: 'GET',
      dataType: 'text'
  });
}

function getS3CSVData(presignedURL){
  return $.ajax({
    url:presignedURL,
    //https://stackoverflow.com/questions/47523265/jquery-ajax-no-access-control-allow-origin-header-is-present-on-the-requested
    headers: {  'Access-Control-Allow-Origin': 'https://trimmedstreamdata.s3-us-west-1.amazonaws.com' },
    crossOrigin: true,
    // data: {csvName:'4413728207.csv'},
    type: 'GET',
    dataType: 'text'
  });
}


function handleStreamChartUpdate(streamType, filteredGroup){
  filteredGroup.eachLayer(function(layer){
    layer.eachLayer(function(feature){
      // Get activity type:
      var actType = feature.feature.properties.type_extended
      if (feature.feature.properties.actID == actID){
        // This CSV has already been loaded, update existing table
        actID = feature.feature.properties.actID
        streamdata = populateStreamChartUpdateData(streamType);
        updateStreamChart(streamdata, actType);
      } else {
        // This CSV has not been loaded, load it
        actID = feature.feature.properties.actID
        getS3StreamURL(actID).then(function(presignedURL){
          return getS3CSVData(presignedURL)
        }).then(function(csvData){
          csvDatObject = $.csv.toObjects(csvData);
          streamdata = populateStreamChartUpdateData(streamType);
          // updateStreamChart(streamdata["dataX"],streamdata["dataY"], actType, streamdata["dataYAvg"], streamdata["yLabel"], streamdata["xLabel"])
          updateStreamChart(streamdata, actType);
        })
      }
    })
  })
}

// see https://stackoverflow.com/questions/30024948/flask-download-a-csv-file-on-clicking-a-button
// Callback function approach
//https://stackoverflow.com/a/14220323
//https://stackify.com/return-ajax-response-asynchronous-javascript-call/
function updateStreamChart(streamdata, actType){
  // Update x, time, data
  actStreamLineChart.data.labels = streamdata["dataX"]
  // Update main, displayed, data
  actStreamLineChart.data.datasets[0].data = streamdata["dataY"]
  // Update Y-data label, used on mouseover tooltip
  actStreamLineChart.data.datasets[0].label = streamdata["yLabel"]
  // Turn off legend, not needed
  actStreamLineChart.options.legend.display = false
  actStreamLineChart.options.scales.yAxes[0].scaleLabel.labelString = streamdata["yLabel"]
  // Color based on activity type, backgroundColor is the fill under the data and borderColor is the line color
  if (actType=="Mountain Bike") {
    actStreamLineChart.data.datasets[0].backgroundColor = 'rgba(228, 26, 28, 0.4)'
    actStreamLineChart.data.datasets[0].borderColor = 'rgba(228, 26, 28)'
  } else if (actType == "Road Cycling") {
    actStreamLineChart.data.datasets[0].backgroundColor =  'rgba(55, 126, 184, 0.4)'
    actStreamLineChart.data.datasets[0].borderColor = 'rgba(55, 126, 184)'
  } else if (actType =="Run") {
    actStreamLineChart.data.datasets[0].backgroundColor =  'rgba(166, 86, 40, 0.4)'
    actStreamLineChart.data.datasets[0].borderColor = 'rgba(166, 86, 40)'
  } else if (actType == "Walk") {
    actStreamLineChart.data.datasets[0].backgroundColor =  'rgba(152, 78, 163, 0.4)'
    actStreamLineChart.data.datasets[0].borderColor = 'rgba(152, 78, 163)'
  }

  // Add average data
  actStreamLineChart.data.datasets[1].data = streamdata["dataYAvg"];
  actStreamLineChart.data.datasets[1].label = "";
  // Tooltip info for average bar, disabled for now
  // actStreamLineChart.data.datasets[1].label = "Average " + streamdata["yLabel"]

  // actStreamLineChart.data.datasets[1].backgroundColor = 'rgba(3, 140, 5, 0.4)'
  // actStreamLineChart.data.datasets[1].borderColor = 'rgba(3, 140, 5)'

  // Issue data update
  actStreamLineChart.update();
}

// Formats ancillary data displayed in the single activity chart tooltip
function populateAncillaryData(index){
  // Get active button
  var active = document.getElementsByClassName('singleAct chart-active')[0].id
  // Get object details at index location
  var ancilObj = csvDatObject[index];
  // Return formatted text for tooltip depending on which stream dataset is active
  if (active == "elevation-stream-btn"){
    return checkAncillaryData("distance", ancilObj["distance"]) + "Elevation(Feet):" + ancilObj["altitude"] + "\n" + "Speed(mph):" + ancilObj["velocity_smooth"] + "\n" + "Grade(%):" + ancilObj["grade_smooth"] + "\n" + checkAncillaryData("cadence", ancilObj["cadence"]) + checkAncillaryData("heartrate",ancilObj["heartrate"])
  } else if (active == "speed-stream-btn"){
    return checkAncillaryData("distance", ancilObj["distance"]) + "Elevation(Feet):" + ancilObj["altitude"] + "\n" + "Grade(%):" + ancilObj["grade_smooth"] + "\n" + checkAncillaryData("cadence", ancilObj["cadence"]) + checkAncillaryData("heartrate",ancilObj["heartrate"])
  } else if (active == "grade-stream-btn"){
    return checkAncillaryData("distance", ancilObj["distance"]) + "Elevation(Feet):" + ancilObj["altitude"] + "\n" +  "Speed(mph):" + ancilObj["velocity_smooth"] + "\n" + checkAncillaryData("cadence", ancilObj["cadence"]) + checkAncillaryData("heartrate",ancilObj["heartrate"])
  } else if (active == "cadence-stream-btn"){
    return checkAncillaryData("distance", ancilObj["distance"]) + "Elevation(Feet):" + ancilObj["altitude"] + "\n" +  "Speed(mph):" + ancilObj["velocity_smooth"] + "\n" + "Grade(%):" + ancilObj["grade_smooth"] + "\n" + checkAncillaryData("heartrate",ancilObj["heartrate"])
  } else if (active == "heartrate-stream-btn"){
    return checkAncillaryData("distance", ancilObj["distance"]) + "Elevation(Feet):" + ancilObj["altitude"] + "\n" + "Speed(mph):" + ancilObj["velocity_smooth"] + "\n" + "Grade(%):" + ancilObj["grade_smooth"]  + "\n" + checkAncillaryData("cadence", ancilObj["cadence"])
  } else if (active == "temperature-stream-btn"){
    // Do nothing for now
  }
}


// Check if Wahoo and other sensor data is available, if so set text, if not return empty text
function checkAncillaryData(datType, sensorData){
  if (typeof sensorData !== "undefined"){
    if (datType == "cadence"){
      return "Cadence(rpm):" + sensorData + "\n"
    } else if (datType == "heartrate"){
      return "Heart Rate(bpm):" + sensorData
    } else if (datType == "distance"){
        return "Distance(Miles):" + (sensorData*0.000189394).toFixed(1) + "\n"
    }
  } else {
    return ""
  }
}

function populateStreamChartUpdateData(streamType){
  var dataY = []
  var dataX = []
  var dataYAvg = []
  for (i of Object.keys(csvDatObject)){
    if (streamType == "elevation-stream-btn" || streamType === null){
      dataY.push(Math.round(parseFloat(csvDatObject[i].altitude)*3.28))
      var yLabel = "Elevation(Feet)"
    } else if (streamType == "speed-stream-btn"){
      dataY.push((parseFloat(csvDatObject[i].velocity_smooth)*2.23694).toFixed(1))
      var yLabel = "Speed(mph)"
    } else if (streamType == "grade-stream-btn") {
      dataY.push(parseFloat(csvDatObject[i].grade_smooth).toFixed(1))
      var yLabel = "Grade(%)"
    } else if (streamType == "cadence-stream-btn") {
      dataY.push(parseFloat(csvDatObject[i].cadence).toFixed(1))
      var yLabel = "Cadence(rpm)"
    } else if (streamType == "heartrate-stream-btn") {
      dataY.push(parseFloat(csvDatObject[i].heartrate).toFixed(1))
      var yLabel = "Heart Rate(bpm)"
    } else if (streamType == "temperature-stream-btn") {
      dataY.push((parseFloat(csvDatObject[i].temp)*1.8+32).toFixed(1))
      var yLabel = "Temperature(F)"
    }
    var xLabel = "Time"
    // Populate x-axis (time data)
    dataX.push(new Date(parseInt(csvDatObject[i].time)*1000).toISOString().substr(11,5));
    // Momemt approach
    // see https://stackoverflow.com/a/43787158
    // dataX.push(moment.utc(csvDatObject[i].time*1000).format('HH:mm'));
  }
  // console.log(dataY)
  // Get total value
  var totalValue = 0
  for (i = 0; i < dataY.length; i++) {
    totalValue += parseFloat(dataY[i])
  }
  // Calculate average
  var averageDat = totalValue/dataY.length
  // build average array
  for (i = 0; i < dataY.length; i++) {
    dataYAvg.push(averageDat.toFixed(1))
  }
  return {"dataX":dataX, "xLabel":xLabel, "dataY":dataY, "yLabel":yLabel, "dataYAvg":dataYAvg}
}
