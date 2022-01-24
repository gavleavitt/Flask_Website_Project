// import 'ol/ol.css';
// import GeoTIFF from 'ol/source/GeoTIFF';
// import Map from 'ol/Map';
// import TileLayer from 'ol/layer/WebGLTile';
var map = new ol.Map({
  target: 'viewDiv',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    })
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([37.41, 8.82]),
    zoom: 4
  })
});

const source = new ol.source.GeoTIFF({
  sources: [
    {
      url: 'https://cogorthos.s3.us-west-1.amazonaws.com/odm_orthophoto.tif',
    },
  ],
  // projection: "EPSG:32611"
});

// var map = new ol.Map({
//   target: 'map',
//   layers: [
//     new ol.layer.Tile({
//       source: new ol.source.OSM()
//     }),
//     new ol.layer.WebGLTile({
//       source: source
//     }),
//   ],
//   // view: new ol.View({
//   //   center: ol.proj.fromLonLat([34.437206, -119.919715]),
//   //   zoom: 4
//   // })
//   view: source.getView()
// });
