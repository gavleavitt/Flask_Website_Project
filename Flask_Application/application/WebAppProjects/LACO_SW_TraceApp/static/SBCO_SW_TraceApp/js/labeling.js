cityLabel = {  // autocasts as new LabelClass()
  symbol: {
    type: "text",  // autocasts as new TextSymbol()
    // color: "orange",
    color: "#cd7908",
    haloColor: "white",
    haloSize: 1,
    font: {  // autocast as new Font()
       // family: "Ubuntu Mono",
       size: 14,
       weight: "bold"
     }
  },
  labelPlacement: "above-right",
  labelExpression: "[CITY_LABEL]",
  // labelExpressionInfo: {
  //   // expression: "$feature.Team + TextFormatting.NewLine + $feature.Division"
  //   expression: "$CITY_LABEL"
  // },
  // maxScale: 0,
  // minScale: 25000000,
};


parcelFilterLabel = {
  minScale: 20000,
  symbol: {
    type: "text",
    color: "#1c5900",
    haloColor: "white",
    haloSize: 1,
    font: {
       size: 14,
       weight: "bold"
     }
  },
  labelPlacement: "above-right",
  labelExpression: "[APN]",
  minScale: 2000
  // maxScale: 0,
  // minScale: 25000000,
};

// parcelLabeling = {
//   [{
//     labelExpression: "[AIN]",
//     symbol: {
//        type: "text",  // autocasts as new TextSymbol()
//        color: [255, 255, 255, 0.7],
//        haloColor: [0, 0, 0, 0.85],
//        haloSize: 1,
//        font: {
//          size: 11
//        }
//      }
//   }]
// }
