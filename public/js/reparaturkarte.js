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
	
	//Holz-Werkstätten	
	var holzPlaces = L.geoJson(holzPlacesList, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: holzIcon});
		},

		onEachFeature: onEachFeature
	});
	
	//Fahrrad-Werkstätten	
	var fahrradPlaces = L.geoJson(fahrradPlacesList, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: fahrradIcon});
		},

		onEachFeature: onEachFeature
	});
	
	//Textil-Werkstätten	
	var textilPlaces = L.geoJson(textilPlacesList, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: textilIcon});
		},

		onEachFeature: onEachFeature
	});
	
	//Technik-Werkstätten	
	var technikPlaces = L.geoJson(technikPlacesList, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: technikIcon});
		},

		onEachFeature: onEachFeature
	});
	
	//Sonstiges-Werkstätten	
	var sonstigesPlaces = L.geoJson(sonstigesPlacesList, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: sonstigesIcon});
		},

		onEachFeature: onEachFeature
	});

	//Auto-Werkstätten	
	var autoPlaces = L.geoJson(autoPlacesList, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: autoIcon});
		},

		onEachFeature: onEachFeature
	});

	//Schuhe-Werkstätten	
	var schuhePlaces = L.geoJson(schuhePlacesList, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: schuheIcon});
		},

		onEachFeature: onEachFeature
	});

	// set up the map
	map = new L.Map('map', {
		center: [51.335, 12.37],
	    	zoom: 13,
		layers: [osm, 
			holzPlaces,
			sonstigesPlaces,
			autoPlaces,
			schuhePlaces,
			textilPlaces,
			technikPlaces,
			fahrradPlaces]	
	});

	var overlays = {
		    "Technik": technikPlaces,
		    "Fahrrad": fahrradPlaces,
		    "Holz": holzPlaces,
		    "Textil": textilPlaces,
		    "Sonstiges": sonstigesPlaces,
		    "Auto": autoPlaces,
		    "Schuhe": schuhePlaces
	};
	
	L.control.layers(null, overlays).addTo(map);	

}

var technikIcon = L.icon({
    iconUrl: 'images/technik.png',
    shadowUrl: 'images/new_shadow.png',

    iconSize:     [54, 80], // size of the icon
    shadowSize:   [54, 20], // size of the shadow
    iconAnchor:   [27, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [27, 10],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

var fahrradIcon = L.icon({
    iconUrl: 'images/fahrrad.png',
    shadowUrl: 'images/new_shadow.png',

    iconSize:     [54, 80], // size of the icon
    shadowSize:   [54, 20], // size of the shadow
    iconAnchor:   [27, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [27, 10],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

var holzIcon = L.icon({
    iconUrl: 'images/holz.png',
    shadowUrl: 'images/new_shadow.png',

    iconSize:     [54, 80], // size of the icon
    shadowSize:   [54, 20], // size of the shadow
    iconAnchor:   [27, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [27, 10],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

var textilIcon = L.icon({
    iconUrl: 'images/textil.png',
    shadowUrl: 'images/new_shadow.png',

    iconSize:     [54, 80], // size of the icon
    shadowSize:   [54, 20], // size of the shadow
    iconAnchor:   [27, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [27, 10],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

var sonstigesIcon = L.icon({
    iconUrl: 'images/sonstiges.png',
    shadowUrl: 'images/new_shadow.png',

    iconSize:     [54, 80], // size of the icon
    shadowSize:   [54, 20], // size of the shadow
    iconAnchor:   [27, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [27, 10],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

var autoIcon = L.icon({
    iconUrl: 'images/auto.png',
    shadowUrl: 'images/new_shadow.png',

    iconSize:     [54, 80], // size of the icon
    shadowSize:   [54, 20], // size of the shadow
    iconAnchor:   [27, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [27, 10],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

var schuheIcon = L.icon({
    iconUrl: 'images/schuhe.png',
    shadowUrl: 'images/new_shadow.png',

    iconSize:     [54, 80], // size of the icon
    shadowSize:   [54, 20], // size of the shadow
    iconAnchor:   [27, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [27, 10],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

function initApp()	{

$.getJSON( "Technik_places.json", function( data ) {
	technikPlacesList = data;
	$.getJSON( "Holz_places.json", function( data ) {
		holzPlacesList = data;
		$.getJSON( "Fahrrad_places.json", function( data ) {
			fahrradPlacesList = data;
			$.getJSON( "Textil_places.json", function( data ) {
				textilPlacesList = data;
				$.getJSON( "Sonstiges_places.json", function( data ) {
					sonstigesPlacesList = data;
					$.getJSON( "Auto_places.json", function( data ) {
						autoPlacesList = data;
						$.getJSON( "Schuhe_places.json", function( data ) {
							schuhePlacesList = data;
							initMap();
						})
					})
				})
			})
		})
	})
})


}

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}
