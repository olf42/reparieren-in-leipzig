var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];
var places;

window.onDomReady = initReady;
window.onDomReady(initApp);

function initReady(fn)	{
	if(document.addEventListener) {
		document.addEventListener("DOMContentLoaded", fn, false);
	}
}

function initMap() {
	// set up the map
	map = new L.Map('map');

	// create the tile layer with correct attribution
	//var osmUrl='http://{s}.tile.cloudmade.com/API-key/997/256/{z}/{x}/{y}.png';
	var osmUrl='http://otile1.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png';
	//var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Data, imagery and map information provided by MapQuest, OpenStreetMap <http://www.openstreetmap.org/copyright> and contributors, ODbL <http://wiki.openstreetmap.org/wiki/Legal_FAQ#I_would_like_to_use_OpenStreetMap_maps._How_should_I_credit_you.#> .'
	var osm = new L.TileLayer(osmUrl, {minZoom: 12, maxZoom: 18, attribution: osmAttrib});		

	map.setView(new L.LatLng(51.335, 12.37),14);
	map.addLayer(osm);
	
	L.geoJson(places, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: rkIcon2});
		},

		onEachFeature: onEachFeature
	}).addTo(map);

}

var rkIcon2 = L.icon({
    iconUrl: 'images/technik.png',
    shadowUrl: 'images/new_shadow.png',

    iconSize:     [54, 80], // size of the icon
    shadowSize:   [54, 20], // size of the shadow
    iconAnchor:   [27, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [27, 10],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

var rkIcon = L.icon({
    iconUrl: 'images/marker.png',
    shadowUrl: 'images/shadow.png',

    iconSize:     [50, 80], // size of the icon
    shadowSize:   [50, 74], // size of the shadow
    iconAnchor:   [25, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [25, 60],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

function initApp()	{

$.getJSON( "places.json", function( data ) {
	places = data;
	initMap();
	console.log( "success" );
})


}

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}
