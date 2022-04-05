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


// COG source:
const source = new ol.source.GeoTIFF({
  sources: [
    {
      url: "https://xyztiles.s3.us-west-1.amazonaws.com/odm_orthophoto_OL_Example2.tif",
      // bands: [1],

      // url: "https://xyztiles.s3.us-west-1.amazonaws.com/odm_orthophoto_masked_OL/Band_1.tif",
      // nodata: 135,
    },
  ],
  convertToRGB: true,
  // wrapX: true,
});

// see: https://github.com/openlayers/openlayers/issues/13122#issuecomment-995959507
// api doc: https://openlayers.org/en/latest/apidoc/module-ol_style_expressions.html#~ExpressionValue
var glTile = new ol.layer.WebGLTile({
  source: source,
  crossOrigin: 'anonymous',
//   style: {
//   color: [
//     'case',
//     ['==', ['band', 2], 135],
//     [0, 0, 0, 0],
//     [
//       'interpolate',
//       ['linear'],
//       ['band', 2],
//       0,
//       [0, 60, 136, 1],
//       30,
//       [250, 150, 50, 1],
//     ],
//   ],
// },
})

var map = new ol.Map({
  target: 'viewDiv',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    }),
    glTile,
  ],
  view: new ol.View({
    projection: projection,
    center: ol.proj.fromLonLat([-119.919715, 34.437206]),
    // center: [34.437206, -119.919715],
    zoom: 17
  })
  // view: source.getView()
});

// taken from: https://codesandbox.io/s/cog-forked-dqreb?file=/main.js:1418-1704
map.on("singleclick", (evt) => {
  const pixel = map.getEventPixel(evt.originalEvent);
  const gl = glTile.getRenderer().helper.getGL();
  const pixelData = new Uint8Array(4);
  gl.readPixels(pixel[0], pixel[1], 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, pixelData);
  console.log(pixelData);
});


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
