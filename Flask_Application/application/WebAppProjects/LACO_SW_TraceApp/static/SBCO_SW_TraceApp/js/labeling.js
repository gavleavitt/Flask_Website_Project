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

const gravityMainsLabels = {
  // autocasts as new LabelClass()
  symbol: {
    type: "text",  // autocasts as new TextSymbol()
    color: "black",
    haloColor: "white",
    haloSize: "1px",
    yoffset: "30px",
    xoffset: "30px",
    font: {  // autocast as new Font()
      // family: "Playfair Display",
      size: 12,
      weight: "bold"
    }
  },
  labelPlacement: "above-center",
  // labelPlacement: "center-along",
  labelExpressionInfo: {
    expression: "Ceil($feature.diameter_h,0) + '\" ' + Decode($feature.material, 1,'Reinforced Concrete Pipe (RCP)', 2,'Plastic Pipe', 3,'Reinforced Concrete Box (RCB)', 4,'Corrugated Metal Pipe (CMP)', 5,'Reinforced Concrete Arch (RCA)', 6,'Cast/Ductile Iron Pipe (CIP)', 7,'Improved Channel', 8,'Corrugated Steel Pipe (CSP)', 9,'Concrete Pipe', 10,'Acrylonitrile-Butadiene-Styrene (ABS)', 11,'Polyvinyl Chloride (PVC)', 12,'Steel Pipe', 13,'Vitrified Clay Pipe (VCP)', 14,'Unreinforced Concrete Pipe', 15,'Asbestos Cement Pipe', 16,'Polyethylene Liner', 17,'Techite', 18,'Dirt Channel', 19,'Dirt Swale', 20,'Brick', 21,'Cured-In-Place Pipe Liner (CIPP)', 22,'High Density Polyethylene Pipe (HDPE)', 98,'?', 99,'Other', 0,'Not Coded', -9,'Error?', 23,'Reinforced Cement Concrete(RCC)', 24,'TRUSS PIPE','Other')"
  }
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
