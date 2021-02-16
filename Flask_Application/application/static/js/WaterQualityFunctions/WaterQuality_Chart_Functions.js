function createChart(beachName){
  console.log("Clicked history button!")
  // Query API for records
  getBeachHistory(beachName).then(function(beachHistory){
    // console.log("Creating beach history chart")

    // Set chart display div to display block
    var historyChartContent = document.getElementById('hist-Tab');
    historyChartContent.style.display = "block";
    var historyChartDiv = document.getElementById('history-chart').getContext('2d');
    // Destroy chart if already existing
    if(window.historyChart instanceof Chart)
      {
        // console.log("Destroying exsiting chart!")
        window.historyChart.destroy();
      }
    resizePopupforChart()
    var parsedData = parseBeachData(beachHistory);
    // https://stackoverflow.com/questions/43090102/chartjs-mapping-non-numeric-y-and-x
    // console.log("Creating new chart!")
    historyChart = new Chart(historyChartDiv, {
      type: 'line',
      data:{
        yLabels: ["Open","Warning","Closed"],
        xLabels: parsedData["dataX"],
        datasets:[{
          data:parsedData["dataY"],
          showLine: false,
          label: "Status"
        }]
      },
      options: {
        layout:{
          padding:{
            right: 15
          }
        },
        title: {
          display: true,
          text: beachName,
          padding: 15,
          fontSize: 15
        },
        legend: {
          display: false
        },
        responsive: true,
        scales: {
          xAxes: [{
            ticks:{
              fontStyle: 'bold',
              padding: 10
            }
          }],
          yAxes:[{
            type:'category',
            position: "left",
            ticks:{
              labels: ["Open","Warning", "Closed"],
              padding: 10,
              fontStyle: 'bold'
            }
          }]
        },
        elements:{
          point:{
            radius: 10,
            hoverRadius: 15,
            pointStyle: function(context){
              var index = context.dataIndex;
              var value = context.dataset.data[index];
              if (value == "Open"){
                return 'circle'
              }
              else if (value == 'Warning'){
                return "triangle"
              } else if (value == 'Closed'){
                return 'cross'
              }
            },
            backgroundColor: function(context){
              var index = context.dataIndex;
              var value = context.dataset.data[index];
              if (value == "Open"){
                return 'rgba(81, 75, 191)'
              }
              else if (value == 'Warning'){
                return 'rgba(255, 215, 100)'
              } else if (value == 'Closed'){
                return 'rgba(244, 67, 54)'
              }
            }
          }
        }
      },
    })
  })
};

function getBeachHistory(beachName){
  beachHistoryURL = '/api/v0.1/getbeachhistory'
  return $.ajax({
      url:beachHistoryURL,
      //https://stackoverflow.com/questions/47523265/jquery-ajax-no-access-control-allow-origin-header-is-present-on-the-requested
      data: {beachName:beachName},
      type: 'GET',
      dataType: 'json'
  });
};

function parseBeachData(beachHistory){
  dataY = []
  dataX = []
  // console.log(beachHistory)
  for (i of Object.keys(beachHistory)){
    // console.log(beachHistory[i])
    // dataY.push(moment(beachHistory[i].date, 'DD-MM-YY').toDate());
    dataX.push(moment(beachHistory[i].date, 'YYYY-MM-DD').format("MMM-DD-YY"));
    dataY.push(beachHistory[i].status)
  }
  // console.log("Data X:")
  // console.log(dataX)
  // console.log("Data Y:")
  // console.log(dataY)
  return {"dataX":dataX, "dataY":dataY}
};

function resizePopupforChart(){
  var popupContent = document.getElementsByClassName('leaflet-popup-content-wrapper')
  var historyContent = document.getElementById('hist-content')
  popupContent[0].style.width = "500px";
  historyContent.style.width = "400px";
  popupContent[0].style.height = "300px";
  historyContent.style.height = "200px";
  var textContent = document.getElementById('text-content');
  textContent.style.display = "none";
}
