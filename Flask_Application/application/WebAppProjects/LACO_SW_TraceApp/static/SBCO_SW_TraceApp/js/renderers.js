const pointResultRenderer = {
  type: "unique-value",
  legendOptions: {
    title: "Structures"
  },
  field: "factype",
  uniqueValueInfos: [{
    value: "S",
    label: "State highway",
    symbol: {
      type: "simple-line",
      color: "#e6d800",
      width: "6px",
      style: "solid"
    }
  }, {
    value: "I",
    label: "Interstate",
    symbol: {
      type: "simple-line",
      color: "#e60049",
      width: "6px",
      style: "solid"
    }
  }, {
    value: "U",
    label: "US Highway",
    symbol: {
      type: "simple-line",
      color: "#9b19f5",
      width: "6px",
      style: "solid"
    }
  }]
};
