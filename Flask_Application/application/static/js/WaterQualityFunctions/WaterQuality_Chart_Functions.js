function createChart(beachName){
  // Query API for records
  getBeachHistory(beachName).then(function(beachHistory){
    console.log("Creating beach history chart")
    var historyChartDiv = document.getElementById('history-chart').getContext('2d');
    // Destroy chart if already existing
    if(window.historyChart instanceof Chart)
      {
        console.log("Destroying exsiting chart!")
        window.historyChart.destroy();
      }
    var parsedData = parseBeachData(beachHistory);
    // https://stackoverflow.com/questions/43090102/chartjs-mapping-non-numeric-y-and-x
    console.log("Creating new chart!")
    historyChart = new Chart(historyChartDiv, {
      type: 'line',
      options: {
        // responsive: true,
        scales: {
          // xAxes: [{
          //   type: 'time',
          //   time :{
          //     unit: "day"
          //   }
          //   // position: 'left',
          //   // ticks: {
          //   //   labels: ["Open","Warning", "Closed"]
          //   // }
          // }],
          yAxes:[{
            type:'category',
            position: "left"
          }]
          // yAxes:[{
          //   type: 'category',
          //   ticks:{
          //     labels: ["Open","Warning", "Closed"]
          //   }
          // }]
        }
      },
      data:{
        yLabels: ["Open","Warning","Closed"],
        xLabels: parsedData["dataX"],
        datasets:[{
          showLine: false,
          label: "Status",
          // backgroundColor: 'rgb(255, 99, 132)',
          // borderColor: 'rgb(255, 99, 132)',
          data:parsedData["dataY"]
        }]
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
  console.log(beachHistory)
  for (i of Object.keys(beachHistory)){
    // console.log(beachHistory[i])
    // dataY.push(moment(beachHistory[i].date, 'DD-MM-YY').toDate());
    dataX.push(moment(beachHistory[i].date, 'YYYY-MM-DD').format("DD-MM-YY"));
    dataY.push(beachHistory[i].status)
  }
  console.log("Data X:")
  console.log(dataX)
  console.log("Data Y:")
  console.log(dataY)
  return {"dataX":dataX, "dataY":dataY}
};
