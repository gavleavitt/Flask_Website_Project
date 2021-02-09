function initTable(groupedData){
  //  see example: http://tabulator.info/docs/4.9/quickstart
  // Generate and format geosjson data into format:
  var dataTab = generateTableFormatedData(groupedData);
  table = new Tabulator("#datatable", {
    height:"100%",
    width:"100%",
    data:dataTab,
    cellHozAlign:"center",
    headerHozAlign:"center",
    selectable:1,
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
      // clear existing layers
      filteredGroup.clearLayers();
      // Update map layer
      addActiveLayers(userStartDate = null, userEndDate = null, actType = selectedID)
      // Update Panels
      updateDataPanels(filteredGroup,actDataDict, clear="True");
      // Update chart
      filterSingleActDisplay(selectedID)
      // Update data table
    },
  });
};


function generateTableFormatedData(groupedData, update){
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
  if (update == "Update"){
    // Clear existing data
    table.clearData();
    // Add newly updated data to table
    table.addData(tabData)
    // Re-set sorter, needed to ensure that sorting occurs correctly when multi-selecting or else first activity type added is always first but still sorted
    table.setSort("date","desc")
  }
  else{
    return tabData
  }
  // groupedData.eachLayer(function(layer){
  //   console.log(layer.feature.properties.actID)
  // })
};

// Trigger to highlight row in table when a user selects a activity on the map or searches for an activity
function highlightRow(activityID){

}
