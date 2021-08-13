const pointResultRenderer = {
  type: "unique-value",
  legendOptions: {
    title: "Structures"
  },
  field: "factype",
  defaultSymbol: { type: "simple-marker" },
  uniqueValueInfos: [{
    value: "Inlet",
    label: "Inlet",
    symbol: {
      type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
      size: 4,
      style: "square",
      color: "blue"
      // outline: {  // autocasts as new SimpleLineSymbol()
      //   width: 1,
      //   color: "white"
      // }
    }
  }, {
    value: "Maintenance Holes",
    label: "Maintenance Holes",
    symbol: {
      type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
      size: 4,
      color: "red",
      outline: {  // autocasts as new SimpleLineSymbol()
        width: 1,
        color: "white"
      }
    }
    // symbol: getUniqueValueSymbol("/static/icons_images/manhole_yellow.svg")
  }, {
    value: "Outlets",
    label: "Outlet",
    symbol: {
      type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
      size: 4,
      color: "red",
      outline: {  // autocasts as new SimpleLineSymbol()
        width: 1,
        color: "white"
      }
    }
  }]
};

const lineResultRenderer = {
  type: "unique-value",
  legendOptions: {
    title: "Drainage"
  },
  field: "factype",
  uniqueValueInfos: [{
    value: "Laterals",
    label: "Laterals",
    symbol: {
      type: "simple-line",
      color: "#1bcc4a",
      width: "6px",
      style: "solid"
    }
  }, {
    value: "Gravity Mains",
    label: "Gravity Mains",
    symbol: {
      type: "simple-line",
      color: "#0f1cd4",
      width: "6px",
      style: "solid"
    }
  },{
    value: "Force Mains",
    label: "Force Mains",
    symbol: {
      type: "simple-line",
      color: "#d40f0f",
      width: "6px",
      style: "solid"
    }
  }]
};
