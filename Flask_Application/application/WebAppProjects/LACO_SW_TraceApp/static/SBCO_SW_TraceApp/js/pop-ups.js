// pop-ups
const popupInlet = {
  "title": "<b>Inlet: {facid}</b>",
  "content": "<b>Type:</b> {facsubtype}"
}

const popupOutlet = {
  "title": "<b>Outlet: {facid}</b>",
  "content": "<b>Type:</b> {facsubtype}"
}

const popupMH = {
  "title": "<b>Maintenance Hole: {facid}</b>",
  "content": "<b>Type:</b> {facsubtype}"
}

// const popupGM = {
//   "title": "<b>Gravity Main: {facid}</b>",
//   "content": "<b>Material:</b> {material}<br><b>Size:</b> {size}\""
// }

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
                    "stringFieldOption": "textbox",
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
                    "fieldName": "t_station",
                    "label": "t_station",
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
                    "fieldName": "cross_sect",
                    "label": "cross_sect",
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
                    "stringFieldOption": "textbox",
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
                    "stringFieldOption": "textbox",
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
                    "visible": false,
                    "stringFieldOption": "textbox"
                },
                {
                    "fieldName": "diameter_h",
                    "label": "diameter_h",
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
                    "fieldName": "jhsrc",
                    "label": "jhsrc",
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
                    "fieldName": "sheet_no",
                    "label": "sheet_no",
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
                    "fieldName": "eqnum",
                    "label": "eqnum",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": true,
                    "stringFieldOption": "textbox"
                },
                {
                    "fieldName": "pmnum",
                    "label": "pmnum",
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
                    "visible": false,
                    "stringFieldOption": "textbox"
                },
                {
                    "fieldName": "width",
                    "label": "width",
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
                    "fieldName": "permit_no",
                    "label": "permit_no",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "stringFieldOption": "textbox"
                },
                {
                    "fieldName": "alias",
                    "label": "alias",
                    "isEditable": true,
                    "tooltip": "",
                    "visible": false,
                    "stringFieldOption": "textbox"
                },
                {
                    "fieldName": "barcode",
                    "label": "barcode",
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
                    "fieldName": "facid",
                    "label": "facid",
                    "isEditable": true,
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
                    "fieldName": "link",
                    "label": "link",
                    "isEditable": true,
                    "visible": false,
                    "stringFieldOption": "textbox"
                },
                {
                    "fieldName": "abandoned",
                    "label": "abandoned",
                    "isEditable": true,
                    "visible": false,
                    "stringFieldOption": "textbox"
                },
                {
                    "fieldName": "us_water",
                    "label": "us_water",
                    "isEditable": true,
                    "visible": false,
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
  "title": "<b>Lateral: {facid}</b>",
  "content": "<b>Material:</b> {material}<br><b>Size:</b> {size}\""
}

const popupfilteredparcels = {
  "title": "<b>APN: {APN}</b>",
  "content": "<b>Situs Address: {SitusFullAddress}<br>Land Use code: {UseCode}<b><br>Use type: {UseType}<br>Use Description: {UseDescription}</b>"
}
