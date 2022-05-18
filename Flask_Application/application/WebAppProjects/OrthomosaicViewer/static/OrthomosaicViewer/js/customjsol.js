// var tilelayer = new ol.layer.Tile({
//       source: new ol.source.XYZ({
//         url:
//           // 'https://cogorthos.s3.us-west-1.amazonaws.com/Mission_250ft_20220115_Tiles/{z}/{x}/{y}.png'
//           'https://xyztiles.s3.us-west-1.amazonaws.com/Mission_250ft_20220115_Tiles/{z}/{x}/{y}.png',
//         maxZoom: 20
//       }),
//       // maxZoom: 22,
//     })
// var map = new ol.Map({
//   target: 'viewDiv',
//   layers: [
//     new ol.layer.Tile({
//       source: new ol.source.OSM()
//     }),
//     tilelayer
//   ],
//   view: new ol.View({
//     center: ol.proj.fromLonLat([-119.919715, 34.437206]),
//     // center: [34.437206, -119.919715],
//     zoom: 17
//   })
//   // view: source.getView()
// });

const projection = new ol.proj.Projection({
  code: 'EPSG:3857',
  units: 'm',
});

const imageryGroup =  new ol.layer.Group({
      openInLayerSwitcher: true,
      title: "Imagery",
      layers: []
    })
console.log(imageryGroup.getProperties())
var map = new ol.Map({
  target: 'viewDiv',
  // controls: ol.control.defaults().extend([new ol.control.LayerPopup({
  //     collapsed: false,
  //     reordering: true,
  //     extent: true,
  //   }),
  // ]),
  layers: [
    new ol.layer.Tile({
      title: "Open Street Map",
      source: new ol.source.OSM()
    }),
    imageryGroup
  ],
  view: new ol.View({
    projection: projection,
    center: ol.proj.fromLonLat([-119.919715, 34.437206]),
    // center: [34.437206, -119.919715],
    zoom: 17
  })
  // view: source.getView()
});

var srcList = []
// get mission point items
fetch('http://geo.leavitttesting.local:5000/collections/mission_points_extended/items?f=json&lang=en-US&limit=10',
  {
    mode: 'cors',
    headers: {
      'Access-Control-Allow-Origin':'*'
    }
  }
)
  .then(response => response.json())
  .then(data => {
    console.log(data)
    data.features.forEach((item, i) => {
      var cogURL = item.properties.URL
      console.log(item);
      var source = new ol.source.GeoTIFF({
        sources: [
          {
            url: item.properties.URL,
            // Set to value that doesnt exist, this is desirable since setting black, 0, causes large JPG artifacts around the border of the image which have values that not
            // exactly 0,0,0. Setting to 255 instead causes some full white values to dispear instead, creating holes.
            // Setting to 256 effectively turns off nodata
            nodata: 256,
            // bands: [1,2,3],

            // url: "https://xyztiles.s3.us-west-1.amazonaws.com/odm_orthophoto_masked_OL/Band_1.tif",
            // nodata: 135,
          },
        ],
        convertToRGB: true,
        // wrapX: true,
      });
      srcList.push(
        new ol.layer.WebGLTile({
          source: source,
          name: item.properties["Mission Name"],
          title: item.properties["Mission Name"],
          crossOrigin: 'anonymous',
        })
      )
    });
    console.log(srcList)
    imageryGroup.getLayers().extend(srcList)
    // map.getLayers().extend(srcList);
    }
  );


// taken from: https://codesandbox.io/s/cog-forked-dqreb?file=/main.js:1418-1704
map.on("singleclick", (evt) => {
  const pixel = map.getEventPixel(evt.originalEvent);
  const gl = glTile.getRenderer().helper.getGL();
  const pixelData = new Uint8Array(4);
  gl.readPixels(pixel[0], pixel[1], 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, pixelData);
  console.log(pixelData);
});


// Add control inside the map
// var ctrl = new ol.control.LayerSwitcher({
//   // collapsed: false,
//   // mouseover: true
// });
var switcher = new ol.control.LayerSwitcher({
  target:$(".layerSwitcher").get(0),
  // displayInLayerSwitcher: function (l) { return false; },
  show_progress:true,
  collapsed: false,
  extent: true,
  // trash: true,
  // oninfo: function (l) { alert(l.get("title")); }
});
// Add a new button to the list
switcher.on('drawlist', function(e) {
  var layer = e.layer;
  $('<div>').text('?')// addClass('layerInfo')
    .click(function(){
      // Alter to show a popup/window instead of an altert
      alert(layer.get('title'));
    })
    .appendTo($('> .ol-layerswitcher-buttons', e.li));
});
// Add a button to show/hide the layers
// var button = $('<div class="toggleVisibility" title="show/hide">')
//   .text("Show/hide all")
//   .click(function() {
//     var a = map.getLayers().getArray();
//     var b = !a[0].getVisible();
//     if (b) button.removeClass("show");
//     else button.addClass("show");
//     for (var i=0; i<a.length; i++) {
//       a[i].setVisible(b);
//     }
//   });
// switcher.setHeader($('<div>').append(button).get(0))

map.addControl(switcher);
// see: https://viglino.github.io/ol-ext/examples/control/map.switcher.html
// Insert mapbox layer in layer switcher
// function displayInLayerSwitcher(b) {
//   mapbox.set('displayInLayerSwitcher', b);
// }

// Get options values
// if ($("#opb").prop("checked")) $('body').addClass('hideOpacity');
// if ($("#percent").prop("checked")) $('body').addClass('showPercent');
// if ($("#dils").prop("checked")) displayInLayerSwitcher(true);

// open layers code:


  // A group layer for base layers
  // var baseLayers = new ol.layer.Group({
  //   title: 'Base Layers',
  //   openInLayerSwitcher: true,
  //   layers: [
  //     new ol.layer.Tile({
  //       title: "Watercolor",
  //       baseLayer: true,
  //       source: new ol.source.Stamen({ layer: 'watercolor' })
  //     }),
  //     new ol.layer.Tile({
  //       title: "Toner",
  //       baseLayer: true,
  //       visible: false,
  //       source: new ol.source.Stamen({ layer: 'toner' })
  //     }),
  //     new ol.layer.Tile({
  //       title: "OSM",
  //       baseLayer: true,
  //       source: new ol.source.OSM(),
  //       visible: false
  //     })
  //   ]
  // });
  // // A layer with minResolution (hidden on hight zoom level)
  // var mapbox = new ol.layer.Tile({
  //   title: "Pirate Map",
  //   displayInLayerSwitcher: false,
  //   minResolution: 1223,
  //   source: new ol.source.XYZ({
  //     attributions: [
  //       '&copy; <a href="https://www.mapbox.com/map-feedback/">Mapbox</a> ',
  //       ol.source.OSM.ATTRIBUTION
  //     ],
  //     url: 'https://{a-d}.tiles.mapbox.com/v3/aj.Sketchy2/{z}/{x}/{y}.png'
  //   })
  // });
  // // An overlay that stay on top
  // var labels = new ol.layer.Tile({
  //   title: "Labels (on top)",
  //   allwaysOnTop: true,			// Stay on top of layer switcher
  //   noSwitcherDelete: true,		// Prevent deleting from layer switcher
  //   source: new ol.source.Stamen({ layer: 'terrain-labels' })
  // });
  // // WMS with bbox
  // var brgm = new ol.layer.Tile ({
  //   "title": "GEOLOGIE",
  //   "extent": [
  //     -653182.6969582437,
  //     5037463.842847037,
  //     1233297.5065495989,
  //     6646432.677299531
  //   ],
  //   "minResolution": 3.527777777777778,
  //   "maxResolution": 3527.777777777778,
  //   "source": new ol.source.TileWMS({
  //     "url": "https://geoservices.brgm.fr/geologie",
  //     "projection": "EPSG:3857",
  //     "params": {
  //       "LAYERS": "GEOLOGIE",
  //       "FORMAT": "image/png",
  //       "VERSION": "1.3.0"
  //     },
  //     "attributions": [
  //       "<a href='http://www.brgm.fr/'>&copy; Brgm</a>"
  //     ]
  //   })
  // });
  //
  // // The Map
  // var map = new ol.Map({
  //   target: 'map',
  //   view: new ol.View({
  //     zoom: 11,
  //     center: [260497, 6249720]
  //   }),
  //   layers: [ baseLayers, mapbox, brgm, labels ]
  // });
  // // Add control inside the map
  // var ctrl = new ol.control.LayerSwitcher({
  //   // collapsed: false,
  //   // mouseover: true
  // });
  // map.addControl(ctrl);
  // ctrl.on('toggle', function(e) {
  //   console.log('Collapse layerswitcher', e.collapsed);
  // });
  //
  // // Add a layer switcher outside the map
  // var switcher = new ol.control.LayerSwitcher({
  //   target:$(".layerSwitcher").get(0),
  //   // displayInLayerSwitcher: function (l) { return false; },
  //   show_progress:true,
  //   extent: true,
  //   trash: true,
  //   oninfo: function (l) { alert(l.get("title")); }
  // });
  // // Add a new button to the list
  // switcher.on('drawlist', function(e) {
  //   var layer = e.layer;
  //   $('<div>').text('?')// addClass('layerInfo')
  //     .click(function(){
  //       alert(layer.get('title'));
  //     })
  //     .appendTo($('> .ol-layerswitcher-buttons', e.li));
  // });
  // // Add a button to show/hide the layers
  // var button = $('<div class="toggleVisibility" title="show/hide">')
  //   .text("Show/hide all")
  //   .click(function() {
  //     var a = map.getLayers().getArray();
  //     var b = !a[0].getVisible();
  //     if (b) button.removeClass("show");
  //     else button.addClass("show");
  //     for (var i=0; i<a.length; i++) {
  //       a[i].setVisible(b);
  //     }
  //   });
  // switcher.setHeader($('<div>').append(button).get(0))
  //
  // map.addControl(switcher);
  // // Insert mapbox layer in layer switcher
  // function displayInLayerSwitcher(b) {
  //   mapbox.set('displayInLayerSwitcher', b);
  // }
  //
  // // Get options values
  // if ($("#opb").prop("checked")) $('body').addClass('hideOpacity');
  // if ($("#percent").prop("checked")) $('body').addClass('showPercent');
  // if ($("#dils").prop("checked")) displayInLayerSwitcher(true);




//https://openlayers.org/en/latest/examples/interpolation.html
// map.on('singleclick', function(evt) {
//     var xy = evt.pixel;
//     // var canvasContext = $('.ol-unselectable')[0].getContext('2d');
//     // var canvasContext = document.querySelector('.ol-unselectable')[0].getContext('2d');
//     var canvasContext = document.querySelector('.ol-unselectable')
//     console.log(canvasContext)
//     var pixelAtClick = canvasContext.getImageData(xy[0], xy[1], 1, 1).data;
//     var red = pixeAtClick[0]; // green is [1] , blue is [2] , alpha is [4]
//   });








// var map = new ol.Map({
//   target: 'viewDiv',
//   layers: [
//     new ol.layer.Tile({
//       source: new ol.source.OSM()
//     })
//   ],
//   view: new ol.View({
//     center: ol.proj.fromLonLat([37.41, 8.82]),
//     zoom: 4
//   })
// });


//
// // var tilelayer = new ol.layer.Tile({
// //       source: new ol.source.XYZ({
// //         url:
// //           'https://cogorthos.s3.us-west-1.amazonaws.com/Mission_250ft_20220115_Tiles/{z}/{x}/{y}.png'
// //       }),
// //     })
// var map = new ol.Map({
//   target: 'viewDiv',
//   layers: [
//     new ol.layer.Tile({
//       source: new ol.source.OSM()
//     }),
//     new ol.layer.WebGLTile({
//       source: source2
//     }),
//   ],
//   view: new ol.View({
//     center: ol.proj.fromLonLat([-119.919715, 34.437206]),
//     // center: [34.437206, -119.919715],
//     zoom: 17
//   })
//   // view: source.getView()
// });


// var map = new ol.Map({
//   target: 'viewDiv',
//   layers: [
//     new ol.layer.Tile({
//       source: new ol.source.OSM()
//     }),
//     new ol.layer.WebGLTile({
//       source: source2
//     }),
//   ],
//   view: new ol.View({
//     center: ol.proj.fromLonLat([-119.919715, 34.437206]),
//     // center: [34.437206, -119.919715],
//     zoom: 17
//   })
//   // view: source.getView()
// });
