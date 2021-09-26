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
      color: [0, 207, 65, 0.75],
      width: "12px",
      style: "solid"
      // opacity: "0.85"
    }
  }, {
    value: "Gravity Mains",
    label: "Gravity Mains",
    symbol: {
      type: "simple-line",
      join: "miter",
      // color: "209, 6, 20",
      color: [209, 6, 20, 0.75],
      width: "12px",
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
      opacity: "0.85"
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

const resultsrenderer = {
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
      color: [0, 207, 65, 0.45],
      width: "12px",
      style: "solid"
      // opacity: "0.85"
    }
  }, {
    value: "Gravity Mains",
    label: "Gravity Mains",
    symbol: {
      type: "simple-line",
      join: "miter",
      // color: "209, 6, 20",
      color: [209, 6, 20, 0.45],
      width: "12px",
      style: "solid"
    }
  }, {
    value: "Force Mains",
    label: "Force Mains",
    symbol: {
      type: "simple-line",
      color: "#d40f0f",
      width: "6px",
      style: "solid",
      opacity: "0.85"
    }
  }, {
    value: "Inlets",
    label: "Inlets",
    symbol: {
      type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
      size: 12,
      style: "square",
      // color: "#0007cf"
      color: [0, 7, 209, 0.45],
      outline: {  // autocasts as new SimpleLineSymbol()
        width: 4,
        color: "black"
      }
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
    label: "Outlets",
    symbol: {
      type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
      size: 14,
      color: "red",
      outline: {  // autocasts as new SimpleLineSymbol()
        width: 4,
        color: "black"
      }
    }
  }, {
    value: "startpoint",
    label: "Start Point",
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
  }
]
};
