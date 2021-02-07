function initTable(groupedData){
  //  see example: http://tabulator.info/docs/4.9/quickstart
  // Generate and format geosjson data into format:
  var dataTab = generateTableFormatedData(groupedData);
  var table = new Tabulator("#datatable", {
    height:200,
    data:dataTab,
    cellHozAlign:"center",
    headerHozAlign:"center",
    layout:"fitColumns",
    // maxHeight:"100%",
    columns:[
      {title:"Name", field:"name"},
      {title:"Date", field:"date", sorter:"date", hozAlign:"center"},
      {title:"Activity Type", field:"typeExtended"},
      {title:"Distance", field:"distance", hozAlign:"left"},
      {title:"Elevation Gain", field:"elevationGain", hozAlign:"left"},
      {title:"Duration", field:"movingTime", hozAlign:"left"},
    ],
    rowClick:function(e, row){ //trigger an alert message when the row is clicked
      alert("Row " + row.getData().id + " Clicked!!!!");
    },
  });
};


function generateTableFormatedData(groupedData){
  console.log("inside function!")
  // console.log(geoJSONDat);
  var tabData = []
  id = 0
  for (i of geoJSONDat.features) {
    id ++
    var name = i.properties.name
    var date = i.properties.startDate
    var type = i.properties.type
    var typeExtended = i.properties.type_extended
    var movingTime = convertDuration(i.properties.moving_time)
    var distance = i.properties.distance
    var elevationGain = i.properties.total_elevation_gain

    tabData.push({id:id,name:name,date:date,type:type,typeExtended:typeExtended,
      movingTime:movingTime,distance:distance,elevationGain:elevationGain})
  }
  return tabData
  // groupedData.eachLayer(function(layer){
  //   console.log(layer.feature.properties.actID)
  // })
};
