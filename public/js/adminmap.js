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
	

	// create the tile layer with correct attribution
	var osmUrl='http://otile1.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png';

	//var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Data, imagery and map information provided by MapQuest, OpenStreetMap <http://www.openstreetmap.org/copyright> and contributors, ODbL <http://wiki.openstreetmap.org/wiki/Legal_FAQ#I_would_like_to_use_OpenStreetMap_maps._How_should_I_credit_you.#> .'
		
	//osm layer using mapquest	
	var osm = new L.TileLayer(osmUrl, {minZoom: 12, maxZoom: 18, attribution: osmAttrib});	
	

	var neuPlaces = L.geoJson(neuPlacesList, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: neuIcon});
		},

		onEachFeature: onEachFeature
	});
	
	// set up the map
	map = new L.Map('map', {
		center: [51.335, 12.37],
	    	zoom: 13,
		layers: [osm, 
			neuPlaces]	
	});

	var overlays = {
		    "Neue Orte": neuPlaces
	};
	
	L.control.layers(null, overlays).addTo(map);	

}

var neuIcon = L.icon({
    iconUrl: 'images/neu.png',
    shadowUrl: 'images/new_shadow.png',

    iconSize:     [54, 80], // size of the icon
    shadowSize:   [54, 20], // size of the shadow
    iconAnchor:   [27, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [27, 10],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

function initApp()	{
	var geojsonfile = "/admin/geojson?" + window.location.search.substring(1);
	$.getJSON( geojsonfile, function( data ) {
		neuPlacesList = data;
		initMap();
		})
}

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}
