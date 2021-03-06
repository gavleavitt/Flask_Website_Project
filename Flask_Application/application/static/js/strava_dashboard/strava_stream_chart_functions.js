zoomPlugin = {
  zoom: {
							pan: {
								enabled: true,
								mode: 'y'
							},
							zoom: {
								enabled: true,
								mode: 'y'
							}
						}
}

// Creates single activity chart in initial state with placeholder data, this allows for a better initial transition from the multi-activity bar plot
function createStreamLineChart(){
  var streamChart = document.getElementById('chart-line').getContext('2d');
  actStreamLineChart = new Chart(streamChart, {
    type: 'line',
    data:{
      labels: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
      datasets:[{
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data:[30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30]
        // pointHitRadius: 50
      },{
        backgroundColor: 'rgb(0, 0, 0, 0)',
        borderColor: 'rgb(3, 140, 5, 0.8)',
        fill: false,
        borderWidth: 3,
        data:[30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30]
      }]
    },
    // Activate label nearest to the pointer
    hover: {
       mode: 'nearest',
       intersect: true,
       // see https://stackoverflow.com/a/58529907
       // place onHover in here with hover options so I can extend the functionality
       onHover: function(event, activeElements) {
         // console.log(e)
         if (activeElements.length > 0){
           var index = activeElements[0]._index
           var totalRecords = actStreamLineChart.data.labels.length
           var portionAlong = (index/totalRecords)
           // Get total length of records
           getDistanceAlongLine(portionAlong);
         }
       }
    },
    options:{
      // onHover: function(event, activeElements) {
      //   // console.log(e)
      //   if (activeElements.length > 0){
      //     var index = activeElements[0]._index
      //     var totalRecords = actStreamLineChart.data.labels.length
      //     var portionAlong = (index/totalRecords)
      //     // Get total length of records
      //     getDistanceAlongLine(portionAlong);
      //   }
      // },
      tooltips: {
        mode: 'index',
        intersect: false,
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
      plugins: zoomPlugin
    }
  })
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
    headers: {  'Access-Control-Allow-Origin': 'https://stravastreamdata.s3-us-west-1.amazonaws.com' },
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
        updateStreamChart(streamdata["dataX"],streamdata["dataY"], actType, streamdata["dataYAvg"], streamdata["yLabel"], streamdata["xLabel"])
      } else {
        // This CSV has not been loaded, load it
        actID = feature.feature.properties.actID
        getS3StreamURL(actID).then(function(presignedURL){
          return getS3CSVData(presignedURL)
        }).then(function(csvData){
          csvDatObject = $.csv.toObjects(csvData);
          streamdata = populateStreamChartUpdateData(streamType);
          updateStreamChart(streamdata["dataX"],streamdata["dataY"], actType, streamdata["dataYAvg"], streamdata["yLabel"], streamdata["xLabel"])
        })
      }
    })
  })
}

// see https://stackoverflow.com/questions/30024948/flask-download-a-csv-file-on-clicking-a-button
// Callback function approach
//https://stackoverflow.com/a/14220323
//https://stackify.com/return-ajax-response-asynchronous-javascript-call/
function updateStreamChart(dataX,dataY, actType, dataYAvg, yLabel, xLabel){
  actStreamLineChart.data.labels = dataX
  actStreamLineChart.data.datasets[0].data = dataY;
  actStreamLineChart.data.datasets[0].label = yLabel
  actStreamLineChart.options.legend.display = false
  actStreamLineChart.options.scales.yAxes[0].scaleLabel.labelString = yLabel
  // Color based on type
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
  actStreamLineChart.data.datasets[1].data = dataYAvg;
  actStreamLineChart.data.datasets[1].label = "Average " + yLabel
  // actStreamLineChart.data.datasets[1].backgroundColor = 'rgba(3, 140, 5, 0.4)'
  // actStreamLineChart.data.datasets[1].borderColor = 'rgba(3, 140, 5)'
  // Issue data update
  actStreamLineChart.update();
}



function populateStreamChartUpdateData(streamType){
  dataY = []
  dataX = []
  dataYAvg = []
  // var count = null
  // var max = null
  for (i of Object.keys(csvDatObject)){
    if (streamType == "elevation-stream-btn" || streamType === null){
      dataY.push(Math.round(parseFloat(csvDatObject[i].altitude)*3.28))
      var yLabel = "Feet"
    } else if (streamType == "speed-stream-btn"){
      dataY.push((parseFloat(csvDatObject[i].velocity_smooth)*2.23694).toFixed(1))
      var yLabel = "Speed(mph)"
    } else if (streamType == "grade-stream-btn") {
      dataY.push(parseFloat(csvDatObject[i].grade_smooth).toFixed(1))
      var yLabel = "Grade(%)"
    } else if (streamType == "cadence-stream-btn") {
      dataY.push(parseFloat(csvDatObject[i].cadence).toFixed(1))
      var yLabel = "Cadence(RPM)"
    } else if (streamType == "heartrate-stream-btn") {
      dataY.push(parseFloat(csvDatObject[i].heartrate).toFixed(1))
      var yLabel = "Heart Rate(BPM)"
    } else if (streamType == "temperature-stream-btn") {
      dataY.push((parseFloat(csvDatObject[i].temp)*1.8+32).toFixed(1))
      var yLabel = "Temperature(F)"
    }
    var xLabel = "Time"
    // dataX.push(parseInt(csvDatObject[i].time))
    dataX.push(new Date(parseInt(csvDatObject[i].time)*1000).toISOString().substr(11,5));
    // count += 1
    // if (parseInt(csvDatObject[i].time) > max){
    //   max = parseInt(csvDatObject[i].time)
    // }
  }
  // console.log(dataY)
  // Get total value
  var totalValue = 0
  for (i = 0; i < dataY.length; i++) {
    totalValue += parseFloat(dataY[i])
  }
  // Calculate average
  var averageDat = totalValue/dataY.length
  console.log(averageDat)
  // build average array
  for (i = 0; i < dataY.length; i++) {
    dataYAvg.push(averageDat.toFixed(1))
  }
  return {"dataX":dataX, "dataY":dataY, "dataYAvg":dataYAvg, "yLabel":yLabel, "xLabel":xLabel}
}
