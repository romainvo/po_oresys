
var map = new mapboxgl.Map({
    container: 'map',
    style: 'https://openmaptiles.geo.data.gouv.fr/styles/osm-bright/style.json', 
    center: [2.349014, 48.85500],
    zoom: 11.5,
    minZoom: 1,
    maxZoom: 19
    });
 
map.addControl(new mapboxgl.NavigationControl());

var hoveredStateId =  null;

map.on('load', function () {
    map.addSource('arrondissements', {
        'type': 'geojson',
        'generateId' : true,
        'data': '/donneesgeos/arrondissements_municipaux-20180711.json'
    });

    map.addLayer({
        "id": "arrondissements-contour",
        "type": "line",
        "source": "arrondissements",
        "layout": {},
        "paint": {
            "line-color": "#000000",
            "line-width": 1
        },
        "filter": ["==", "$type", "Polygon"]
    });
         
    map.addLayer({
        "id": "arrondissements-fill",
        "type": "fill",
        "source": "arrondissements",
        "layout": {},
        "paint": {
            "fill-color": "#627BC1",
            "fill-opacity": ["case",
                ["boolean", ["feature-state", "hover"], false],
                0.5,
                0
            ]
        },
        "filter": ["==", "$type", "Polygon"]
    });

    // When the user moves their mouse over the arrondissements-fill layer, 
    // we'll update the feature state for the feature under the mouse.
    map.on("mousemove", "arrondissements-fill", function(e) {
        var canvas = map.getCanvas();
        canvas.style.cursor = 'pointer';

        if (e.features.length > 0) {
            if (hoveredStateId) {
            map.setFeatureState({source: 'arrondissements', id: hoveredStateId}, { hover: false});
            }
            hoveredStateId = e.features[0].id;
            map.setFeatureState({source: 'arrondissements', id: hoveredStateId}, { hover: true});
        }
    });
        
    // When the mouse leaves the state-fill layer, update the feature state of the
    // previously hovered feature.
    map.on("mouseleave", "arrondissements-fill", function() {
        var canvas = map.getCanvas();
        canvas.style.cursor = '';

        if (hoveredStateId) {
            map.setFeatureState({source: 'arrondissements', id: hoveredStateId}, { hover: false});
        }
        hoveredStateId =  null;
    });

});