var departements = null;
var departementsLayer = {
	id: 'departements-layer',
	source: 'departements',
	type: 'fill',
	paint: fillLayerPaint
}
var departementsContoursLayer = {
	id: 'departements-contours-layer',
	source: 'departements',
	type: 'line',
	paint: contoursPaint
}

var fillColor = '#2a4ba9'
var borderColor = '#627BC1'

var fillLayerPaint = {
	"fill-color": fillColor,
	"fill-outline-color": borderColor,
	"fill-opacity": ["case",
		["boolean", ["feature-state", "hover"], false],
		0.2,
		0
	]
}

var contoursPaint = {
	"line-width": [
		'case',
		["boolean", ["feature-state", "hover"], false],
		3,
		1
	]
}

var map = new mapboxgl.Map({
    container: 'map',
    style: 'https://openmaptiles.geo.data.gouv.fr/styles/osm-bright/style.json', 
    center: [3, 47],
    zoom: 5,
    minZoom: 1,
    maxZoom: 19
    });
 
map.addControl(new mapboxgl.NavigationControl());

map.on('load', function () {
    if (!departements) {
        // Chargement des contours des départements
        $.getJSON("/static/donneesgeo/departements-100m.geojson",
            function (data) {
                departements = data
            }
        ).then(function() {
                map.addSource("departements", {
                    type: 'geojson',
                    generateId: true,
                    data: departements
                })
                map.addLayer(departementsLayer)
                map.addLayer(departementsContoursLayer)
        })
    }
});