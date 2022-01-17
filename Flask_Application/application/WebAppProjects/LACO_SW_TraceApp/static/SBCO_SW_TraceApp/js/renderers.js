
const selectionMarkerSymbol = {
   type: "simple-marker",
   style: "x",
   color: "blue",
   size:"15px",
   angle: 45,
   outline: {
       color: "blue", // White
       width: "5px"
   }
};

const blockingMarkerSymbol = {
   type: "simple-marker",
   style: "triangle",
   color: "orange",
   size:"24px",
   outline: {
       color: "red", // White
       width: "1px"
   }
};

let countyBorder = {
  type: "simple",  // autocasts as new SimpleRenderer()
  symbol: {
    type: "simple-fill",  // autocasts as new SimpleMarkerSymbol()
    color: [0, 0, 0, 0],
    // size: 6,
    // color: "black",
    outline: {  // autocasts as new SimpleLineSymbol()
      width: 3,
      style: "dash",
      color: "green"
    }
  }
};

let cityBorder = {
  type: "simple",  // autocasts as new SimpleRenderer()
  symbol: {
    type: "simple-fill",  // autocasts as new SimpleMarkerSymbol()
    color: [0, 0, 0, 0],
    // size: 6,
    // color: "black",
    outline: {  // autocasts as new SimpleLineSymbol()
      width: 2,
      style: "dash",
      color: [148, 9, 150]
    }
  }
};

let parcelFilterBorder = {
  type: "simple",  // autocasts as new SimpleRenderer()
  symbol: {
    type: "simple-fill",  // autocasts as new SimpleMarkerSymbol()
    color: [0, 0, 0, 0],
    // size: 6,
    // color: "black",
    outline: {  // autocasts as new SimpleLineSymbol()
      width: 2,
      // style: "dash",
      color: "#51ff00"
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
      color: [0, 207, 65, 0.30],
      width: "16px",
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
      color: [209, 6, 20, 0.30],
      width: "16px",
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
      color: [0, 7, 209, 0.20],
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
      color:  [235, 227, 0, 0.20],
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
      size: 16,
      color: "red",
      style: "diamond",
      outline: {  // autocasts as new SimpleLineSymbol()
        width: 4,
        color: "black"
      }
    }
  },
  {
   value: "subwatersheds",
   label: "Subwatersheds",
   symbol: {
     type: "simple",  // autocasts as new SimpleRenderer()
     type: "simple-fill",  // autocasts as new SimpleMarkerSymbol()
     color: [0, 0, 0, 0],
     // size: 6,
     // color: "black",
     outline: {  // autocasts as new SimpleLineSymbol()
       width: 3,
       style: "solid",
       color: "blue"
     }
   }
 },
  {
    value: "startpoint",
    label: "Start Point",
    symbol: {
      type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
      size: 15,
      angle: 45,
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
const gravityMainsCIM = {
          type: "unique-value", // autocasts as UniqueValueRenderer
          field: "material",
          defaultSymbol: {
            type: "cim", // autocasts as CIMSymbol
            data: {
              type: "CIMSymbolReference",
              symbol: {
                type: "CIMLineSymbol",
                symbolLayers: [{
                    // black 1px line symbol
                    type: "CIMSolidStroke",
                    enable: true,
                    width: 3,
                    color: [
                      175,
                      175,
                      175,
                      255
                    ]
                  },
                  {
                    // arrow symbol
                    type: "CIMVectorMarker",
                    enable: true,
                    size: 14,
                    markerPlacement: {
                      // see https://github.com/Esri/cim-spec/blob/master/docs/v2/CIMSymbols.md#enumeration-placementendings
                      // see https://github.com/Esri/cim-spec/blob/master/docs/v2/CIMSymbols.md#cimmarkerplacementatratiopositions
                      type: "CIMMarkerPlacementAtRatioPositions",
                      beginPosition: 1,
                      endPosition: 1,
                      positionArray: [0.5],
                      angleToLine: true, // symbol will maintain its angle to the line when map is rotated
                      // type: "CIMMarkerPlacementAlongLineSameSize", // places same size markers along the line
                      // endings: "WithMarkers",
                      // placementTemplate: [60], // determines space between each arrow
                      // angleToLine: true // symbol will maintain its angle to the line when map is rotated
                    },
                    frame: {
                      xmin: -5,
                      ymin: -5,
                      xmax: 5,
                      ymax: 5
                    },
                    markerGraphics: [{
                      type: "CIMMarkerGraphic",
                      geometry: {
                        rings: [
                          [
                            [
                              8,
                              5.47
                            ],
                            [
                              8,
                            -  5.6
                            ],
                            [
                              -1.96,
                              0.03
                            ],
                            [
                              8,
                              5.47
                            ]
                          ]
                        ]
                      },
                      symbol: {
                        // black fill for the arrow symbol
                        type: "CIMPolygonSymbol",
                        symbolLayers: [{
                          type: "CIMSolidFill",
                          enable: true,
                          color: [
                            0,
                            0,
                            0,
                            255
                          ]
                        }]
                      }
                    }]
                  }
                ]
              }
            }
          },
          // defaultSymbol: {
          //   type: "simple-line" // default SimpleLineSymbol
          // },
          uniqueValueInfos: [{
            value: "1", // when one-way='yes', create CIMSymbol line with arrows
            symbol: {
              type: "cim", // autocasts as CIMSymbol
              data: {
                type: "CIMSymbolReference",
                symbol: {
                  type: "CIMLineSymbol",
                  symbolLayers: [{
                      // black 1px line symbol
                      type: "CIMSolidStroke",
                      enable: true,
                      width: 3,
                      color: [
                        237,
                        81,
                        81,
                        255
                      ]
                    },
                    {
                      // arrow symbol
                      type: "CIMVectorMarker",
                      enable: true,
                      size: 14,
                      markerPlacement: {
                        type: "CIMMarkerPlacementAtRatioPositions",
                        // rotation: 180,
                        positionArray: [-0.5],
                        angleToLine: true // symbol will maintain its angle to the line when map is rotated
                      },
                      frame: {
                        xmin: -5,
                        ymin: -5,
                        xmax: 5,
                        ymax: 5
                      },
                      markerGraphics: [{
                        type: "CIMMarkerGraphic",
                        geometry: {
                          rings: [
                            [
                              [
                                8,
                                5.47
                              ],
                              [
                                8,
                              -  5.6
                              ],
                              [
                                -1.96,
                                0.03
                              ],
                              [
                                8,
                                5.47
                              ]
                            ]
                          ]
                        },
                        symbol: {
                          // black fill for the arrow symbol
                          type: "CIMPolygonSymbol",
                          symbolLayers: [{
                            type: "CIMSolidFill",
                            enable: true,
                            color: [
                              0,
                              0,
                              0,
                              255
                            ]
                          }]
                        }
                      }]
                    }
                  ]
                }
              }
            }
          }, {
            value: "3",
            symbol: {
              type: "cim", // autocasts as CIMSymbol
              data: {
                type: "CIMSymbolReference",
                symbol: {
                  type: "CIMLineSymbol",
                  symbolLayers: [{
                      // black 1px line symbol
                      type: "CIMSolidStroke",
                      enable: true,
                      width: 3,
                      color: [
                        255,
                        170,
                        0,
                        255
                      ]
                    },
                    {
                      // arrow symbol
                      type: "CIMVectorMarker",
                      enable: true,
                      size: 14,
                      markerPlacement: {
                        type: "CIMMarkerPlacementAtRatioPositions",
                        positionArray: [0.5],
                        angleToLine: true // symbol will maintain its angle to the line when map is rotated
                      },
                      frame: {
                        xmin: -5,
                        ymin: -5,
                        xmax: 5,
                        ymax: 5
                      },
                      markerGraphics: [{
                        type: "CIMMarkerGraphic",
                        geometry: {
                          rings: [
                            [
                              [
                                8,
                                5.47
                              ],
                              [
                                8,
                              -  5.6
                              ],
                              [
                                -1.96,
                                0.03
                              ],
                              [
                                8,
                                5.47
                              ]
                            ]
                          ]
                        },
                        symbol: {
                          // black fill for the arrow symbol
                          type: "CIMPolygonSymbol",
                          symbolLayers: [{
                            type: "CIMSolidFill",
                            enable: true,
                            color: [
                              0,
                              0,
                              0,
                              255
                            ]
                          }]
                        }
                      }]
                    }
                  ]
                }
              }
            }
          }
        ]
};


// countyCIM = {
//   data:{
//     "type": "CIMPolygonSymbol",
//     "symbolLayers": [
//       {
//         "type": "CIMSolidStroke",
//         "effects": [
//           {
//             "type": "CIMGeometricEffectDashes",
//             "dashTemplate": [
//               20,
//               10,
//               20,
//               10
//             ],
//             "lineDashEnding": "HalfPattern",
//             "controlPointEnding": "NoConstraint"
//           },
//           {
//             "type": "CIMGeometricEffectOffset",
//             "method": "Bevelled",
//             "offset": 0,
//             "option": "Fast"
//           }
//         ],
//         "enable": true,
//         "colorLocked": true,
//         "capStyle": "Round",
//         "joinStyle": "Round",
//         "lineStyle3D": "Strip",
//         "miterLimit": 10,
//         "width": 8,
//         "color": [
//           0,
//           0,
//           0,
//           255
//         ]
//       }
//     ]
//   }
// };

// const pointResultRenderer = {
//   type: "unique-value",
//   legendOptions: {
//     title: "Structures"
//   },
//   field: "factype",
//   defaultSymbol: { type: "simple-marker" },
//   uniqueValueInfos: [{
//     value: "Inlet",
//     label: "Inlet",
//     symbol: {
//       type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
//       size: 6,
//       style: "square",
//       // color: "#0007cf"
//       color: [0, 7, 209, 0.60]
//       // outline: {  // autocasts as new SimpleLineSymbol()
//       //   width: 1,
//       //   color: "white"
//       // }
//     }
//   }, {
//     value: "Maintenance Holes",
//     label: "Maintenance Holes",
//     symbol: {
//       type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
//       size: 10,
//       color:  [235, 227, 0, 0.60],
//       outline: {  // autocasts as new SimpleLineSymbol()
//         width: 4,
//         color: "black"
//       }
//     }
//     // fix link to make work:
//     // symbol:{
//     //   type: 'picture-marker',
//     //   url: "/static/icons_images/manhole_yellow.svg",
//     //   width: '20px',
//     //   height: '20px'
//     // }
//   }, {
//     value: "Outlets",
//     label: "Outlet",
//     symbol: {
//       type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
//       size: 16,
//       color: "red",
//       style: "diamond",
//       outline: {  // autocasts as new SimpleLineSymbol()
//         width: 4,
//         color: "black"
//       }
//     }
//   }]
// };

// const lineResultRenderer = {
//   type: "unique-value",
//   legendOptions: {
//     title: "Drainage"
//   },
//   field: "factype",
//   uniqueValueInfos: [{
//     value: "Laterals",
//     label: "Laterals",
//     symbol: {
//       type: "simple-line",
//       // color: "#1bcc4a",
//       color: [0, 207, 65, 0.75],
//       width: "12px",
//       style: "solid"
//       // opacity: "0.85"
//     }
//   }, {
//     value: "Gravity Mains",
//     label: "Gravity Mains",
//     symbol: {
//       type: "simple-line",
//       join: "miter",
//       // color: "209, 6, 20",
//       color: [229, 185, 0, 0.85],
//       width: "12px",
//       style: "solid"
//     }
//   },{
//     value: "Force Mains",
//     label: "Force Mains",
//     symbol: {
//       type: "simple-line",
//       color: "#d40f0f",
//       width: "6px",
//       style: "solid",
//       opacity: "0.85"
//     }
//   }]
// };

// let startrenderer = {
//   type: "simple",  // autocasts as new SimpleRenderer()
//   symbol: {
//     type: "simple-marker",  // autocasts as new SimpleMarkerSymbol()
//     size: 10,
//     style: "x",
//     angle: 45,
//     color: "red",
//     // outline: {  // autocasts as new SimpleLineSymbol()
//     //   width: 10,
//     //   color: "red"
//     // }
//   }
// };
