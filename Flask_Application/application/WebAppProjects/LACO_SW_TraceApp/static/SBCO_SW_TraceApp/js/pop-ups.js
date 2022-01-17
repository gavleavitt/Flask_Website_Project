// // pop-ups
function populatepopupResults(title){
  const popupResults = {
    title: `<b>Trace Result - ${title}: {facid}</b>`,
    content: [
      {
        type: "fields",
        fieldInfos: [
          {
            fieldName: "facid",
            label: "Facility ID"
          },
          {
            fieldName: "dwgno",
            label: "DWG Number"
          },
          {
            fieldName: "uuid",
            label: "UUID"
          }
        ]
      }
    ]
  }
  if (title.includes("Laterals") || title.includes("Gravity Mains")){
    insert = [
        {
          fieldName: "size_in",
          label: "Pipe Diameter (in)"
        },
        {
          fieldName: "material",
          label: "Material"
        },{
        fieldName: "pipelength_ft",
        label: "Pipe Length (ft)",
        format: {
          digitSeparator: true,
          places: 1
        }
      }
    ]
  } else {
      insert = [
        {
          fieldName: "facsubtype",
          label: "Facility Type"
        }
      ]
  }
  popupResults.content[0].fieldInfos.splice(1, 0, ...insert)
  return popupResults
}


const popupGM = {
  "title": "<b>Gravity Main: {name}</b>",
  "content": [{
    "type":"fields",
    "fieldInfos": [
                {
                    "fieldName": "FID",
                    "label": "FID",
                    "isEditable": false,
                    "tooltip": "",
                    "visible": false
                },
                {
                    "fieldName": "name",
                    "label": "name",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": true
                },
                {
                    "fieldName": "expression/expr0",
                    "visible": true
                },
                {
                    "fieldName": "expression/expr2",
                    "visible": true,
                    "format": {
                        "places": 0,
                        "digitSeparator": false
                    }
                },
                {
                    "fieldName": "expression/expr1",
                    "visible": true
                },
                {
                    "fieldName": "slope",
                    "label": "slope",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 2,
                        "digitSeparator": true
                    }
                },
                {
                    "fieldName": "plan_no",
                    "label": "plan_no",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false
                },
                {
                    "fieldName": "owner",
                    "label": "owner",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 0,
                        "digitSeparator": true
                    }
                },
                {
                    "fieldName": "t_station",
                    "label": "t_station",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 0,
                        "digitSeparator": true
                    }
                },
                {
                    "fieldName": "cross_sect",
                    "label": "cross_sect",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 0,
                        "digitSeparator": true
                    }
                },
                {
                    "fieldName": "material",
                    "label": "material",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 2,
                        "digitSeparator": true
                    }
                },
                {
                    "fieldName": "q_design",
                    "label": "q_design",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 0,
                        "digitSeparator": true
                    }
                },
                {
                    "fieldName": "dn_elev",
                    "label": "dn_elev",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 0,
                        "digitSeparator": false
                    }
                },
                {
                    "fieldName": "subtype",
                    "label": "subtype",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 0,
                        "digitSeparator": true
                    }
                },
                {
                    "fieldName": "maintained",
                    "label": "maintained",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false
                },
                {
                    "fieldName": "diameter_h",
                    "label": "diameter_h",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 2,
                        "digitSeparator": true
                    }
                },
                {
                    "fieldName": "jhsrc",
                    "label": "jhsrc",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": true
                },
                {
                    "fieldName": "dwgno",
                    "label": "dwgno",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": true
                },
                {
                    "fieldName": "sheet_no",
                    "label": "sheet_no",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": true,
                    "format": {
                        "places": 0,
                        "digitSeparator": false
                    }
                },
                {
                    "fieldName": "eqnum",
                    "label": "eqnum",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": true
                },
                {
                    "fieldName": "pmnum",
                    "label": "pmnum",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": true
                },
                {
                    "fieldName": "remarks",
                    "label": "remarks",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false
                },
                {
                    "fieldName": "width",
                    "label": "width",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 0,
                        "digitSeparator": true
                    }
                },
                {
                    "fieldName": "permit_no",
                    "label": "permit_no",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false
                },
                {
                    "fieldName": "alias",
                    "label": "alias",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false
                },
                {
                    "fieldName": "barcode",
                    "label": "barcode",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false
                },
                {
                    "fieldName": "uuid",
                    "label": "uuid",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": true
                },
                {
                    "fieldName": "edge_fk",
                    "label": "edge_fk",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 2,
                        "digitSeparator": true
                    }
                },
                {
                    "fieldName": "factype",
                    "label": "factype",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false
                },
                {
                    "fieldName": "facid",
                    "label": "facid",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false
                },
                {
                    "fieldName": "Shape__Length",
                    "label": "Shape__Length",
                    "isEditable": false,
                    "tooltip": "",
                    "visible": false,
                    "format": {
                        "places": 2,
                        "digitSeparator": true
                    }
                },
                {
                    "fieldName": "link",
                    "label": "link",
                    "isEditable": true,
                    "visible": false
                },
                {
                    "fieldName": "abandoned",
                    "label": "abandoned",
                    "isEditable": true,
                    "visible": false
                },
                {
                    "fieldName": "us_water",
                    "label": "us_water",
                    "isEditable": true,
                    "visible": false
                }
            ]
  }],
  "expressionInfos": [
                {
                    "name": "expr0",
                    "title": "Material",
                    "expression": "// Write a script to return a value to show in the pop-up.\n// For example, get the average of 4 fields:\n// Average($feature.SalesQ1, $feature.SalesQ2, $feature.SalesQ3, $feature.SalesQ4)\n\nvar matcode = $feature.material;\nvar mat = Decode(matcode, 1, 'Reinforced Concrete Pipe (RCP)', 2, 'Plastic Pipe', 3, 'Reinforced Concrete Box (RCB)', 4, 'Corrugated Metal Pipe (CMP)', 5, 'Reinforced Concrete Arch (RCA)', 6, 'Cast/Ductile Iron Pipe (CIP)',8,'Corrugated Steel Pipe (CSP)',11,'Polyvinyl Chloride (PVC)', 22,'High Density Polyethylene Pipe (HDPE)', 'Other');\nreturn mat",
                    "returnType": "string"
                },
                {
                    "name": "expr1",
                    "title": "Owner",
                    "expression": "// Write a script to return a value to show in the pop-up.\n// For example, get the average of 4 fields:\n// Average($feature.SalesQ1, $feature.SalesQ2, $feature.SalesQ3, $feature.SalesQ4)\n\nreturn Decode($feature.owner, 1,'City of Los Angeles', 3,'State of California', 4,'Private', 5,'US Army Corps of Engineers', 6,'The Port of Los Angeles', 99,'Other', 0,'Not Coded', -9,'Error?', 7,'Agoura Hills', 8,'Alhambra', 9,'Arcadia', 10,'Artesia', 2,'LACFCD', 11,'Avalon', 12,'Azusa', 13,'Baldwin Park', 14,'Bell', 15,'Bell Gardens', 16,'Bellflower', 17,'Beverly Hills', 18,'Bradbury', 19,'Burbank', 20,'Calabasas', 21,'Carson', 22,'Cerritos', 23,'Claremont', 24,'Commerce', 25,'Compton', 26,'Covina', 27,'Cudahy', 28,'Culver City', 29,'Diamond Bar', 30,'Downey', 31,'Duarte', 32,'El Monte', 33,'El Segundo', 34,'Gardena', 35,'Glendale', 36,'Glendora', 38,'Hawthorne', 39,'Hermosa Beach', 40,'Hidden Hills', 41,'Huntington Park', 42,'Industry', 43,'Inglewood', 44,'Irwindale', 45,'La Canada Flintridge', 46,'La Habra Heights', 47,'La Mirada', 48,'La Puente', 49,'La Verne', 50,'Lakewood', 51,'Lancaster', 52,'Lawndale', 53,'Lomita', 54,'Long Beach', 55,'Lynwood', 56,'Malibu', 57,'Manhattan Beach', 59,'Monrovia', 60,'Montebello', 61,'Monterey Park', 62,'Norwalk', 63,'Palmdale', 64,'Palos Verdes Estates', 65,'Paramount', 66,'Pasadena', 67,'Pico Rivera', 68,'Pomona', 69,'Rancho Palos Verdes', 70,'Redondo Beach', 71,'Rolling Hills', 72,'Rolling Hills Estates', 73,'Rosemead', 74,'San Dimas', 75,'San Fernando', 76,'San Gabriel', 77,'San Marino', 78,'Santa Clarita', 79,'Santa Fe Springs', 80,'Santa Monica', 81,'Sierra Madre', 82,'Signal Hill', 83,'South El Monte', 84,'South Gate', 85,'South Pasadena', 86,'Temple City', 87,'Torrance', 88,'Vernon', 89,'Walnut', 90,'West Covina', 91,'West Hollywood', 92,'Westlake Village', 93,'Whittier', 58,'Maywood', 94,'Road Maintenance Division', 37,'Hawaiian Gardens', 95,'Unincorporated','Other')\n",
                    "returnType": "string"
                },
                {
                    "name": "expr2",
                    "title": "Diameter",
                    "expression": "// Write a script to return a value to show in the pop-up.\n// For example, get the average of 4 fields:\n// Average($feature.SalesQ1, $feature.SalesQ2, $feature.SalesQ3, $feature.SalesQ4)\n\nCeil($feature.diameter_h,0)",
                    "returnType": "number"
                }
            ]
}

const popupLat = {
  "title": "<b>Lateral: {name}</b>",
  "content": [{
    "type":"fields",
    "fieldInfos": [
                    {
                        "fieldName": "expression/expr0",
                        "visible": true
                    },
                    {
                        "fieldName": "jhsrc",
                        "label": "jhsrc",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "fid",
                        "label": "fid",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "id",
                        "label": "id",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "owner",
                        "label": "owner",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "t_station",
                        "label": "t_station",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "cross_section_shape",
                        "label": "cross_section_shape",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "material",
                        "label": "material",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "slope",
                        "label": "slope",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "q_design",
                        "label": "q_design",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "asbdate",
                        "label": "asbdate",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "name",
                        "label": "name",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "dn_elev",
                        "label": "dn_elev",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "subtype",
                        "label": "subtype",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "maintained_by",
                        "label": "maintained_by",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "diameter_height",
                        "label": "diameter_height",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": false
                        }
                    },
                    {
                        "fieldName": "dwgno",
                        "label": "dwgno",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "link",
                        "label": "link",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "eqnum",
                        "label": "eqnum",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "width",
                        "label": "width",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "abandoned",
                        "label": "abandoned",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "permit_no",
                        "label": "permit_no",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "remarks",
                        "label": "remarks",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "layer",
                        "label": "layer",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "path",
                        "label": "path",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "factype",
                        "label": "factype",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "uuid",
                        "label": "uuid",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "edge_fk",
                        "label": "edge_fk",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "ObjectId",
                        "label": "ObjectId",
                        "isEditable": false,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "Shape__Length",
                        "label": "Shape__Length",
                        "isEditable": false,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 2,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "sheet_no",
                        "label": "sheet_no",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "plan_no",
                        "label": "plan_no",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    }
                ]
  }],
  "expressionInfos": [
    {
        "name": "expr0",
        "title": "Material",
        "expression": "// Write a script to return a value to show in the pop-up.\n// For example, get the average of 4 fields:\n// Average($feature.SalesQ1, $feature.SalesQ2, $feature.SalesQ3, $feature.SalesQ4)\n\nvar matcode = $feature.material;\nvar mat = Decode(matcode, 1, 'Reinforced Concrete Pipe (RCP)', 2, 'Plastic Pipe', 3, 'Reinforced Concrete Box (RCB)', 4, 'Corrugated Metal Pipe (CMP)', 5, 'Reinforced Concrete Arch (RCA)', 6, 'Cast/Ductile Iron Pipe (CIP)',8,'Corrugated Steel Pipe (CSP)',11,'Polyvinyl Chloride (PVC)', 22,'High Density Polyethylene Pipe (HDPE)', 'Other');\nreturn mat",
        "returnType": "string"
    }
  ]
}

const popupMH = {
  "title": "<b>Maintenance hole: {jhsrc}</b>",
  "content": [{
    "type":"fields",
    "fieldInfos": [
                    {
                        "fieldName": "FID",
                        "label": "FID",
                        "isEditable": false,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "expression/expr0",
                        "visible": true
                    },
                    {
                        "fieldName": "plan_no",
                        "label": "plan_no",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "sheet_no",
                        "label": "sheet_no",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "owner",
                        "label": "owner",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "stnd_plan",
                        "label": "stnd_plan",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "material",
                        "label": "material",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "subtype",
                        "label": "subtype",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "maintained",
                        "label": "maintained",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "dwgno",
                        "label": "dwgno",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "jhsrc",
                        "label": "jhsrc",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "station",
                        "label": "station",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 2,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "eqnum",
                        "label": "eqnum",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "name",
                        "label": "name",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "abandoned",
                        "label": "abandoned",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "permit_no",
                        "label": "permit_no",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "remarks",
                        "label": "remarks",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "layer",
                        "label": "layer",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "uuid",
                        "label": "uuid",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "node_fk",
                        "label": "node_fk",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 2,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "factype",
                        "label": "factype",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    }
                ]
  }],
  "expressionInfos": [
                    {
                        "name": "expr0",
                        "title": "Description",
                        "expression": "return Decode($feature[\"stnd_plan\"], 'B-1700','B-1700', 'not-std','Not Standard', 'Other','Junction Chamber', 'S-300-1','Junction Structure A', 'S-301-1','Junction Structure D', 'S-302-1','Junction Structure B', 'S-320-0','Sidewalk Outlet Structure', 'S-322-2','Sidewalk Culvert with Steel Plate', 'S-323-1','Low Flow Inlet and Outlet Structure', 'S-331-1','Monolithic Connection', 'S-330-0','Concrete Collar for Storm Drain Pipe', 'S-345-2','Catch Basin Rectangular MH Frame & Cover', 'S-346-2','Catch Basin MH Frame & Cover 22 in Diameter', 'S-351-1','Side Opening Catch Basin', 'S-354-0','Curbside Grate Basin', 'S-355-0','Alley Grating Basin', 'S-361-0','Catch Basin #61', 'S-362-0','Catch Basin #62', 'S-372-1','Transition Structure C', 'S-381-0','MH EZ', 'S-383-0','MH BX (Box)', 'S-384-0','MH JM (Junction)', 'S-387-1','MH Shaft', 'S-303-0','Junction Structure C', '1','300-2, CURB OPENING CATCH BASIN', '2','301-2, CURB OPENING CATCH BASIN W/ GRATING(S) & DEBRIS SKIMMER', '3','302-2, CURB OPENING CATCH BASIN W/ GRATING(S)', '4','303-2, CURBSIDE GRATING CATCH BASIN', '5','304-2, GRATING CATCH BASIN-ALLEY (LONGITUDINAL)', '6','305-2, GRATING CATCH BASIN-ALLEY (TRANSVERSE)', '7','306-2, CURB OPENING CATCH BASIN AT DRIVEWAY', '8','307-2, CURB OPENING CATCH BASIN W/ MANHOLE IN STREET', '9','320-1, MANHOLE PIPE TO PIPE MAIN LINE ID=900MM (36 in) OR LARGER', '10','321-1, MANHOLE PIPE TO PIPE (ONE OR BOTH MAIN LINE ID ftS 825MM (33 in) OR SMALLER)', '11','322-1, MANHOLE PIPE TO PIPE (LARGE SIDE INLET)', '12','323-1, MANHOLE-CONCRETE BOX STORM DRAIN', '13','331-2, JUNCTION STRUCTURE-PIPE TO PIPE INLET ID>= 600MM (24 in) OR OD > 1/2 MAIN LINE ID', '14','332-1, JUNCTION STRUCTURE-PIPE TO PIPE [ID <=600MM (24 in)]', '15','333-1, JUNCTION STRUCTURE-PIPE TO RCB', '16','334-1, JUNCTION STRUCTURE-PIPE TO RVC INLET IN <= 750MM (30 in)', '17','335-1, PIPE CONNECTIONS TO EXISTING STORM DRAINS', '18','340-1, TRANSITION STRUCTURE PIPE TO PIPE', '19','341-1, TRANSITION STRUCTURE SINGLE RCB TO SINGLE RCB', '20','342-1, TRANSITION STRUCTURE RCB TO PIPE', '21','343-1, TRANSITION STRUCTURE SINGLE RCB TO DOUBLE RCB', '22','344-1, TRANSITION STRUCTURE DOUBLE RCB TO DOUBLE RCB', '23','345-1, TRANSITION STRUCTURE DOUBLE RCB TO TRIPLE RCB', '24','346-1, TRANSITION STRUCTURE TRIPLE RCB TO TRIPLE RCB', '25','351-1, CSP FLARED INLET', '26','361-0, TRASH RACK (INCLINED)', '27','380-3, CONCRETE COLLAR FOR RCP 300MM (12 in) THROUGH 1800MM (72 in)', '28','3061-2, AUTOMATIC FLAP GATE INLET (2000 EDITION)', '29','3087-2, SUB DRAINAGE SYSTEM FOR R.C. RECTANGULAR OPEN CHANNEL (2000 EDITION)', '33','C.B. No.39', '34','60-12, BOX CULVERT NO. 12', '31','64-12,C.B. No.12 PER L.A.C.R.D Std Plan.', '32','64-16,C.B. No.16 PER L.A.C.R.D Std Plan.', '35','C.B 10', '36','C.B 11', '37','64-14, C.B. No.14 PER  LAC RD. STD PLAN', '30','308-1, MONOLITHIC CATCH BASIN CONNECTION', '38','DB 2424 2X2 GRATE DRAIN', '39','324-1, MANHOLE SHAFT- WITH ECCENTRIC REDUCER', '40','326-1, MANHOLE SHAFT- 900mm(36 in)WITHOUT REDUCER', '41','327-4, MANHOLE FOR EXISTING RCB', '42','328-1, PRESSURE MANHOLE SHAFT-WITH ECCENTRIC REDUCER', '43','329-1, PRESSURE MANHOLE SHAFT AND PRESSURE PLATE WITHOUT REDUCER', '44','335-1, PIPE CONNECTIONS TO EXISTING STORM DRAINS', '45','72-06, MANHOLE NO 6', '46','3015-0, RURAL CATCH BASIN','Other')\n",
                        "returnType": "string"
                    }
                ]
}

const popupIN = {
  "title": "<b>Inlet: {eqnum}</b>",
  "content": [{
    "type":"fields",
    "fieldInfos": [
                    {
                        "fieldName": "FID",
                        "label": "FID",
                        "isEditable": false,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "expression/expr1",
                        "visible": true
                    },
                    {
                        "fieldName": "expression/expr2",
                        "visible": true
                    },
                    {
                        "fieldName": "plan_no",
                        "label": "plan_no",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "owner",
                        "label": "owner",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "stnd_plan",
                        "label": "stnd_plan",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "no_grates",
                        "label": "no_grates",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "vdepth",
                        "label": "vdepth",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 2,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "vdepth2",
                        "label": "vdepth2",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 2,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "width",
                        "label": "width",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 2,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "subtype",
                        "label": "subtype",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 0,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "maintained",
                        "label": "maintained",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "dwgno",
                        "label": "dwgno",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "bmp",
                        "label": "bmp",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "eqnum",
                        "label": "eqnum",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "name",
                        "label": "name",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "outlet_dia",
                        "label": "outlet_dia",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 2,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "sump",
                        "label": "sump",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "permit_no",
                        "label": "permit_no",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "ownership",
                        "label": "ownership",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "node_fk",
                        "label": "node_fk",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox",
                        "format": {
                            "places": 2,
                            "digitSeparator": true
                        }
                    },
                    {
                        "fieldName": "factype",
                        "label": "factype",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": false,
                        "stringFieldOption": "textbox"
                    },
                    {
                        "fieldName": "uuid",
                        "label": "uuid",
                        "isEditable": true,
                        "tooltip": "",
                        "visible": true,
                        "stringFieldOption": "textbox"
                    }
                ]
  }],
  "expressionInfos": [
                    {
                        "name": "expr1",
                        "title": "Inlet Type",
                        "expression": "// Write a script to return a value to show in the pop-up.\n// For example, get the average of 4 fields:\n// Average($feature.SalesQ1, $feature.SalesQ2, $feature.SalesQ3, $feature.SalesQ4)\n\nreturn Decode($feature.stnd_plan, 'B-1700','B-1700', 'not-std','Not Standard', 'Other','Junction Chamber', 'S-300-1','Junction Structure A', 'S-301-1','Junction Structure D', 'S-302-1','Junction Structure B', 'S-320-0','Sidewalk Outlet Structure', 'S-322-2','Sidewalk Culvert with Steel Plate', 'S-323-1','Low Flow Inlet and Outlet Structure', 'S-331-1','Monolithic Connection', 'S-330-0','Concrete Collar for Storm Drain Pipe', 'S-345-2','Catch Basin Rectangular MH Frame & Cover', 'S-346-2','Catch Basin MH Frame & Cover 22 in Diameter', 'S-351-1','Side Opening Catch Basin', 'S-354-0','Curbside Grate Basin', 'S-355-0','Alley Grating Basin', 'S-361-0','Catch Basin #61', 'S-362-0','Catch Basin #62', 'S-372-1','Transition Structure C', 'S-381-0','MH EZ', 'S-383-0','MH BX (Box)', 'S-384-0','MH JM (Junction)', 'S-387-1','MH Shaft', 'S-303-0','Junction Structure C', '1','300-2, CURB OPENING CATCH BASIN', '2','301-2, CURB OPENING CATCH BASIN W/ GRATING(S) & DEBRIS SKIMMER', '3','302-2, CURB OPENING CATCH BASIN W/ GRATING(S)', '4','303-2, CURBSIDE GRATING CATCH BASIN', '5','304-2, GRATING CATCH BASIN-ALLEY (LONGITUDINAL)', '6','305-2, GRATING CATCH BASIN-ALLEY (TRANSVERSE)', '7','306-2, CURB OPENING CATCH BASIN AT DRIVEWAY', '8','307-2, CURB OPENING CATCH BASIN W/ MANHOLE IN STREET', '9','320-1, MANHOLE PIPE TO PIPE MAIN LINE ID=900MM (36 in) OR LARGER', '10','321-1, MANHOLE PIPE TO PIPE (ONE OR BOTH MAIN LINE ID ftS 825MM (33 in) OR SMALLER)', '11','322-1, MANHOLE PIPE TO PIPE (LARGE SIDE INLET)', '12','323-1, MANHOLE-CONCRETE BOX STORM DRAIN', '13','331-2, JUNCTION STRUCTURE-PIPE TO PIPE INLET ID>= 600MM (24 in) OR OD > 1/2 MAIN LINE ID', '14','332-1, JUNCTION STRUCTURE-PIPE TO PIPE [ID <=600MM (24 in)]', '15','333-1, JUNCTION STRUCTURE-PIPE TO RCB', '16','334-1, JUNCTION STRUCTURE-PIPE TO RVC INLET IN <= 750MM (30 in)', '17','335-1, PIPE CONNECTIONS TO EXISTING STORM DRAINS', '18','340-1, TRANSITION STRUCTURE PIPE TO PIPE', '19','341-1, TRANSITION STRUCTURE SINGLE RCB TO SINGLE RCB', '20','342-1, TRANSITION STRUCTURE RCB TO PIPE', '21','343-1, TRANSITION STRUCTURE SINGLE RCB TO DOUBLE RCB', '22','344-1, TRANSITION STRUCTURE DOUBLE RCB TO DOUBLE RCB', '23','345-1, TRANSITION STRUCTURE DOUBLE RCB TO TRIPLE RCB', '24','346-1, TRANSITION STRUCTURE TRIPLE RCB TO TRIPLE RCB', '25','351-1, CSP FLARED INLET', '26','361-0, TRASH RACK (INCLINED)', '27','380-3, CONCRETE COLLAR FOR RCP 300MM (12 in) THROUGH 1800MM (72 in)', '28','3061-2, AUTOMATIC FLAP GATE INLET (2000 EDITION)', '29','3087-2, SUB DRAINAGE SYSTEM FOR R.C. RECTANGULAR OPEN CHANNEL (2000 EDITION)', '33','C.B. No.39', '34','60-12, BOX CULVERT NO. 12', '31','64-12,C.B. No.12 PER L.A.C.R.D Std Plan.', '32','64-16,C.B. No.16 PER L.A.C.R.D Std Plan.', '35','C.B 10', '36','C.B 11', '37','64-14, C.B. No.14 PER  LAC RD. STD PLAN', '30','308-1, MONOLITHIC CATCH BASIN CONNECTION', '38','DB 2424 2X2 GRATE DRAIN', '39','324-1, MANHOLE SHAFT- WITH ECCENTRIC REDUCER', '40','326-1, MANHOLE SHAFT- 900mm(36 in)WITHOUT REDUCER', '41','327-4, MANHOLE FOR EXISTING RCB', '42','328-1, PRESSURE MANHOLE SHAFT-WITH ECCENTRIC REDUCER', '43','329-1, PRESSURE MANHOLE SHAFT AND PRESSURE PLATE WITHOUT REDUCER', '44','335-1, PIPE CONNECTIONS TO EXISTING STORM DRAINS', '45','72-06, MANHOLE NO 6', '46','3015-0, RURAL CATCH BASIN','Other')\n",
                        "returnType": "string"
                    },
                    {
                        "name": "expr2",
                        "title": "Owner",
                        "expression": "// Write a script to return a value to show in the pop-up.\n// For example, get the average of 4 fields:\n// Average($feature.SalesQ1, $feature.SalesQ2, $feature.SalesQ3, $feature.SalesQ4)\n\nreturn Decode($feature.owner, 1,'City of Los Angeles', 3,'State of California', 4,'Private', 5,'US Army Corps of Engineers', 6,'The Port of Los Angeles', 99,'Other', 0,'Not Coded', -9,'Error?', 7,'Agoura Hills', 8,'Alhambra', 9,'Arcadia', 10,'Artesia', 2,'LACFCD', 11,'Avalon', 12,'Azusa', 13,'Baldwin Park', 14,'Bell', 15,'Bell Gardens', 16,'Bellflower', 17,'Beverly Hills', 18,'Bradbury', 19,'Burbank', 20,'Calabasas', 21,'Carson', 22,'Cerritos', 23,'Claremont', 24,'Commerce', 25,'Compton', 26,'Covina', 27,'Cudahy', 28,'Culver City', 29,'Diamond Bar', 30,'Downey', 31,'Duarte', 32,'El Monte', 33,'El Segundo', 34,'Gardena', 35,'Glendale', 36,'Glendora', 38,'Hawthorne', 39,'Hermosa Beach', 40,'Hidden Hills', 41,'Huntington Park', 42,'Industry', 43,'Inglewood', 44,'Irwindale', 45,'La Canada Flintridge', 46,'La Habra Heights', 47,'La Mirada', 48,'La Puente', 49,'La Verne', 50,'Lakewood', 51,'Lancaster', 52,'Lawndale', 53,'Lomita', 54,'Long Beach', 55,'Lynwood', 56,'Malibu', 57,'Manhattan Beach', 59,'Monrovia', 60,'Montebello', 61,'Monterey Park', 62,'Norwalk', 63,'Palmdale', 64,'Palos Verdes Estates', 65,'Paramount', 66,'Pasadena', 67,'Pico Rivera', 68,'Pomona', 69,'Rancho Palos Verdes', 70,'Redondo Beach', 71,'Rolling Hills', 72,'Rolling Hills Estates', 73,'Rosemead', 74,'San Dimas', 75,'San Fernando', 76,'San Gabriel', 77,'San Marino', 78,'Santa Clarita', 79,'Santa Fe Springs', 80,'Santa Monica', 81,'Sierra Madre', 82,'Signal Hill', 83,'South El Monte', 84,'South Gate', 85,'South Pasadena', 86,'Temple City', 87,'Torrance', 88,'Vernon', 89,'Walnut', 90,'West Covina', 91,'West Hollywood', 92,'Westlake Village', 93,'Whittier', 58,'Maywood', 94,'Road Maintenance Division', 37,'Hawaiian Gardens', 95,'Unincorporated','Other')\n",
                        "returnType": "string"
                    }
                ]
}

// const popupOL = {
//   "title": "<b>Maintenance hole: {jhsrc}</b>"
//   "content": [{
//     "type":"fields",
//     "fieldInfos": [
//                     {
//                         "fieldName": "FID",
//                         "label": "FID",
//                         "isEditable": false,
//                         "tooltip": "",
//                         "visible": false,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "expression/expr0",
//                         "visible": true
//                     },
//                     {
//                         "fieldName": "plan_no",
//                         "label": "plan_no",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "sheet_no",
//                         "label": "sheet_no",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox",
//                         "format": {
//                             "places": 0,
//                             "digitSeparator": true
//                         }
//                     },
//                     {
//                         "fieldName": "owner",
//                         "label": "owner",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": false,
//                         "stringFieldOption": "textbox",
//                         "format": {
//                             "places": 0,
//                             "digitSeparator": true
//                         }
//                     },
//                     {
//                         "fieldName": "stnd_plan",
//                         "label": "stnd_plan",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "material",
//                         "label": "material",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox",
//                         "format": {
//                             "places": 0,
//                             "digitSeparator": true
//                         }
//                     },
//                     {
//                         "fieldName": "subtype",
//                         "label": "subtype",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox",
//                         "format": {
//                             "places": 0,
//                             "digitSeparator": true
//                         }
//                     },
//                     {
//                         "fieldName": "maintained",
//                         "label": "maintained",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "dwgno",
//                         "label": "dwgno",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "jhsrc",
//                         "label": "jhsrc",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "station",
//                         "label": "station",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox",
//                         "format": {
//                             "places": 2,
//                             "digitSeparator": true
//                         }
//                     },
//                     {
//                         "fieldName": "eqnum",
//                         "label": "eqnum",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "name",
//                         "label": "name",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "abandoned",
//                         "label": "abandoned",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "permit_no",
//                         "label": "permit_no",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "remarks",
//                         "label": "remarks",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "layer",
//                         "label": "layer",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": false,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "uuid",
//                         "label": "uuid",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": true,
//                         "stringFieldOption": "textbox"
//                     },
//                     {
//                         "fieldName": "node_fk",
//                         "label": "node_fk",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": false,
//                         "stringFieldOption": "textbox",
//                         "format": {
//                             "places": 2,
//                             "digitSeparator": true
//                         }
//                     },
//                     {
//                         "fieldName": "factype",
//                         "label": "factype",
//                         "isEditable": true,
//                         "tooltip": "",
//                         "visible": false,
//                         "stringFieldOption": "textbox"
//                     }
//                 ]
//   }],
//   "expressionInfos": [
//                     {
//                         "name": "expr0",
//                         "title": "Description",
//                         "expression": "return Decode($feature[\"stnd_plan\"], 'B-1700','B-1700', 'not-std','Not Standard', 'Other','Junction Chamber', 'S-300-1','Junction Structure A', 'S-301-1','Junction Structure D', 'S-302-1','Junction Structure B', 'S-320-0','Sidewalk Outlet Structure', 'S-322-2','Sidewalk Culvert with Steel Plate', 'S-323-1','Low Flow Inlet and Outlet Structure', 'S-331-1','Monolithic Connection', 'S-330-0','Concrete Collar for Storm Drain Pipe', 'S-345-2','Catch Basin Rectangular MH Frame & Cover', 'S-346-2','Catch Basin MH Frame & Cover 22 in Diameter', 'S-351-1','Side Opening Catch Basin', 'S-354-0','Curbside Grate Basin', 'S-355-0','Alley Grating Basin', 'S-361-0','Catch Basin #61', 'S-362-0','Catch Basin #62', 'S-372-1','Transition Structure C', 'S-381-0','MH EZ', 'S-383-0','MH BX (Box)', 'S-384-0','MH JM (Junction)', 'S-387-1','MH Shaft', 'S-303-0','Junction Structure C', '1','300-2, CURB OPENING CATCH BASIN', '2','301-2, CURB OPENING CATCH BASIN W/ GRATING(S) & DEBRIS SKIMMER', '3','302-2, CURB OPENING CATCH BASIN W/ GRATING(S)', '4','303-2, CURBSIDE GRATING CATCH BASIN', '5','304-2, GRATING CATCH BASIN-ALLEY (LONGITUDINAL)', '6','305-2, GRATING CATCH BASIN-ALLEY (TRANSVERSE)', '7','306-2, CURB OPENING CATCH BASIN AT DRIVEWAY', '8','307-2, CURB OPENING CATCH BASIN W/ MANHOLE IN STREET', '9','320-1, MANHOLE PIPE TO PIPE MAIN LINE ID=900MM (36 in) OR LARGER', '10','321-1, MANHOLE PIPE TO PIPE (ONE OR BOTH MAIN LINE ID ftS 825MM (33 in) OR SMALLER)', '11','322-1, MANHOLE PIPE TO PIPE (LARGE SIDE INLET)', '12','323-1, MANHOLE-CONCRETE BOX STORM DRAIN', '13','331-2, JUNCTION STRUCTURE-PIPE TO PIPE INLET ID>= 600MM (24 in) OR OD > 1/2 MAIN LINE ID', '14','332-1, JUNCTION STRUCTURE-PIPE TO PIPE [ID <=600MM (24 in)]', '15','333-1, JUNCTION STRUCTURE-PIPE TO RCB', '16','334-1, JUNCTION STRUCTURE-PIPE TO RVC INLET IN <= 750MM (30 in)', '17','335-1, PIPE CONNECTIONS TO EXISTING STORM DRAINS', '18','340-1, TRANSITION STRUCTURE PIPE TO PIPE', '19','341-1, TRANSITION STRUCTURE SINGLE RCB TO SINGLE RCB', '20','342-1, TRANSITION STRUCTURE RCB TO PIPE', '21','343-1, TRANSITION STRUCTURE SINGLE RCB TO DOUBLE RCB', '22','344-1, TRANSITION STRUCTURE DOUBLE RCB TO DOUBLE RCB', '23','345-1, TRANSITION STRUCTURE DOUBLE RCB TO TRIPLE RCB', '24','346-1, TRANSITION STRUCTURE TRIPLE RCB TO TRIPLE RCB', '25','351-1, CSP FLARED INLET', '26','361-0, TRASH RACK (INCLINED)', '27','380-3, CONCRETE COLLAR FOR RCP 300MM (12 in) THROUGH 1800MM (72 in)', '28','3061-2, AUTOMATIC FLAP GATE INLET (2000 EDITION)', '29','3087-2, SUB DRAINAGE SYSTEM FOR R.C. RECTANGULAR OPEN CHANNEL (2000 EDITION)', '33','C.B. No.39', '34','60-12, BOX CULVERT NO. 12', '31','64-12,C.B. No.12 PER L.A.C.R.D Std Plan.', '32','64-16,C.B. No.16 PER L.A.C.R.D Std Plan.', '35','C.B 10', '36','C.B 11', '37','64-14, C.B. No.14 PER  LAC RD. STD PLAN', '30','308-1, MONOLITHIC CATCH BASIN CONNECTION', '38','DB 2424 2X2 GRATE DRAIN', '39','324-1, MANHOLE SHAFT- WITH ECCENTRIC REDUCER', '40','326-1, MANHOLE SHAFT- 900mm(36 in)WITHOUT REDUCER', '41','327-4, MANHOLE FOR EXISTING RCB', '42','328-1, PRESSURE MANHOLE SHAFT-WITH ECCENTRIC REDUCER', '43','329-1, PRESSURE MANHOLE SHAFT AND PRESSURE PLATE WITHOUT REDUCER', '44','335-1, PIPE CONNECTIONS TO EXISTING STORM DRAINS', '45','72-06, MANHOLE NO 6', '46','3015-0, RURAL CATCH BASIN','Other')\n",
//                         "returnType": "string"
//                     }
//                 ]
// }

const popupfilteredparcels = {
  "title": "<b>APN: {APN}</b>",
  "content": "<b>Situs Address: {SitusFullAddress}<br>Land Use code: {UseCode}<b><br>Use type: {UseType}<br>Use Description: {UseDescription}</b>"
}
