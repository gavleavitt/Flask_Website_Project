function initTable(groupedData){
  //  see example: http://tabulator.info/docs/4.9/quickstart
  // Generate and format geosjson data into format:
  var dataTab = generateTableFormatedData(groupedData);
  var table = new Tabulator("#datatable", {
    height:"100%",
    width:"100%",
    data:dataTab,
    cellHozAlign:"center",
    headerHozAlign:"center",
    selectable:true,
    rowClick:function(e, row){
      row.deselect(); //toggle row selected state on row click
      console.log(row)
      console.log(e)
    },
    // selectablePersistence:false, // disable rolling selection
    // layout:"fitColumns",
    // layout:"fitData",
    // layout:"fitDataStretch",
    // maxHeight:"100%",
    layout:"fitDataFill",
    columns:[
      {title:"Name", field:"name", hozAlign:"center"},
      {title:"Date(PST)", field:"date", sorter:"date", hozAlign:"center", sorterParams:{format:"YYYY-MM-DD hh:mm A"}},
      {title:"Activity Type", field:"typeExtended", hozAlign:"center"},
      {title:"Distance(Miles)", field:"distance", hozAlign:"center"},
      {title:"Elevation Gain(Feet)", field:"elevationGain", hozAlign:"center"},
      {title:"Duration", field:"movingTime", hozAlign:"center"},
      {title:"Average Watts", field:"avgwatts", hozAlign:"center"},
      {title:"Calories", field:"calories", hozAlign:"center"},
      // {title:"ActID", field:"actID", hozAlign:"center"},
      {title:"ActID", field:"actID", hozAlign:"center", formatter:"link",   formatterParams:{
        labelField:"actID",
        urlPrefix:"https://www.strava.com/activities/",
        target:"_blank",
      }}
    ],
    // Fires when users selects a row in the table, update Leaflet, panels, and chart based on the user's selection
    rowClick:function(e, row){
      selectedID = row.getData().actID
      filteredGroup.clearLayers();
      // Update map layer
      actFilter(actType=null,userStartDate=null,userEndDate=null,actID=selectedID )
      // Update Panels
      updateDataPanels(filteredGroup,actDataDict, clear="True");
      // Update chart
      updateChart(filteredGroup);
      // Update data table
    },
  });
};


function generateTableFormatedData(groupedData){
  // console.log(geoJSONDat);
  var tabData = []
  id = 0
  for (i of geoJSONDat.features) {
    id ++
    var name = i.properties.name
    // Convert datetime format to be easier to read
    var date = moment(i.properties.startDate).format("YYYY-MM-DD hh:mm A")
    var type = i.properties.type
    var typeExtended = i.properties.type_extended
    var movingTime = convertDuration(i.properties.moving_time)
    // Convert meters to miles
    var distance = (i.properties.distance * 0.000621371).toFixed(1)
    // Convert meters to feet
    var elevationGain = i.properties.total_elevation_gain * 3.28084.toFixed()
    var avgwatts = i.properties.average_watts
    var calories = i.properties.calories
    var actID = i.properties.actID
    tabData.push({id:id,name:name,date:date,type:type,typeExtended:typeExtended,
      movingTime:movingTime,distance:distance,elevationGain:elevationGain,avgwatts:avgwatts,calories:calories,actID:actID})
  }
  return tabData
  // groupedData.eachLayer(function(layer){
  //   console.log(layer.feature.properties.actID)
  // })
};
