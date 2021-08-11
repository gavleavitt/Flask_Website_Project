const pointResultRenderer = {
  type: "unique-value",
  legendOptions: {
    title: "Structures"
  },
  field: "factype",
  defaultSymbol: { type: "simple-marker" },
  uniqueValueInfos: [{
    value: "inlet",
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
    value: "manhole",
    label: "Maintenance Hole",
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
    value: "outlet",
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
    title: "Structures"
  },
  field: "factype",
  uniqueValueInfos: [{
    value: "inlet",
    label: "Inlet",
    symbol: {
      type: "simple-line",
      color: "#e6d800",
      width: "6px",
      style: "solid"
    }
  }, {
    value: "manhole",
    label: "Maintenance Hole",
    symbol: {
      type: "simple-line",
      color: "#e60049",
      width: "6px",
      style: "solid"
    }
  }, {
    value: "outlet",
    label: "Outlet",
    symbol: {
      type: "simple-line",
      color: "#9b19f5",
      width: "6px",
      style: "solid"
    }
  }]
};
