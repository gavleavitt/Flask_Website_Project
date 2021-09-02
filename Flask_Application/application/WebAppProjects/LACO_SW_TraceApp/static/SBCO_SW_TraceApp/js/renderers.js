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
      size: 8,
      style: "square",
      // color: "#0007cf"
      color: [0, 7, 209, 0.60]
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
      size: 10,
      color:  [235, 227, 0, 0.60],
      outline: {  // autocasts as new SimpleLineSymbol()
        width: 4,
        color: "black"
      }
    }
    // fix link to make work:
    // symbol:{
    //   type: 'picture-marker',
    //   url: "/static/icons_images/manhole_yellow.svg",
    //   width: '20px',
    //   height: '20px'
    // }
  }, {
    value: "Outlets",
    label: "Outlet",
    symbol: {
      type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
      size: 14,
      color: "red",
      outline: {  // autocasts as new SimpleLineSymbol()
        width: 4,
        color: "black"
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
      // color: "#1bcc4a",
      color: [0, 207, 65, 0.50],
      width: "10px",
      style: "solid",
      opacity: "0.75"
    }
  }, {
    value: "Gravity Mains",
    label: "Gravity Mains",
    symbol: {
      type: "simple-line",
      join: "miter",
      // color: "209, 6, 20",
      color: [209, 6, 20, 0.50],
      width: "10px",
      style: "solid"
    }
  },{
    value: "Force Mains",
    label: "Force Mains",
    symbol: {
      type: "simple-line",
      color: "#d40f0f",
      width: "6px",
      style: "solid",
      opacity: "0.5"
    }
  }]
};

let startrenderer = {
  type: "simple",  // autocasts as new SimpleRenderer()
  symbol: {
    type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
    size: 20,
    style: "x",
    color: "red",
    outline: {  // autocasts as new SimpleLineSymbol()
      width: 10,
      color: "red"
    }
  }
};
