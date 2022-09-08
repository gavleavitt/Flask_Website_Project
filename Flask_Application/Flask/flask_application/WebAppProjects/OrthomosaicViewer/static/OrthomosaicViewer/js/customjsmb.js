L.mapbox.accessToken = 'pk.eyJ1IjoiZ2F2bGVhd2ViIiwiYSI6ImNrcnNodWNkZzBodWIydW13dHZveWZrencifQ.Cj0Qfq4uAXPu8ets-9lObQ';
var map = L.mapbox.map('viewDiv')
    .setView([34.437206, -119.919715], 15)
    .addLayer(L.mapbox.styleLayer('mapbox://styles/mapbox/streets-v11'));
// -119.919715, 34.437206
