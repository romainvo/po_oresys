
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

var coordinates = document.getElementById('coordinates');

map.on('load', function () {
    map.addSource('arrondissements', {
        'type': 'geojson',
        'generateId' : true,
        'data': '/donneesgeos/arrondissements_municipaux-20180711.json'
    });

    map.addSource('rpls', {
        type: 'geojson',
        generateId: true,
        data: '/donneesgeos/rpls.geojson',
        cluster: true,
        clusterMaxZoom: 12, // Max zoom to cluster points on
        clusterRadius: 70 // Radius of each cluster when clustering points (defaults to 50)    
    });

    map.addLayer({
        id: "clusters",
        type: "circle",
        source: "rpls",
        filter: ["has", "point_count"],
        paint: {
            "circle-color": [
                "step",
                ["get", "point_count"],
                "#000000", //"#51bbd6",
                100,
                "#000000", //"#f1f075",
                750,
                "#000000", //"#f28cb1"
            ],
            "circle-radius": [
                "step",
                ["get", "point_count"],
                20,
                100,
                30,
                750,
                40
            ],
            "circle-stroke-width": 1,
            "circle-stroke-color": "#FFFFFF"
        }
    }); 
    
    map.addLayer({
        id: "cluster-count",
        type: "symbol",
        source: "rpls",
        filter: ["has", "point_count"],
        layout: {
            "text-field": "{point_count_abbreviated}",
            "text-font": ["DIN Offc Pro Medium", "Arial Unicode MS Bold"],
            "text-size": 12
        },
        paint: {
            "text-color": "#FFFFFF"
        }
    });
         
    map.addLayer({
        id: "unclustered-point",
        type: "circle",
        source: "rpls",
        filter: ["!", ["has", "point_count"]],
        paint: {
            "circle-color": "#000000",//"#11b4da",
            "circle-radius": 4,
            "circle-stroke-width": 1,
            "circle-stroke-color": "#fff"
        }
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
        //"filter": ["==", "$type", "Polygon"]
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
        //"filter": ["==", "$type", "Polygon"]
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

    /*map.addLayer({
        "id": "rpls-points",
        "type": "circle",
        "source": "rpls",
        "layout": {},
        "paint": {
            "circle-radius": 2,
            "circle-color": "#000000"
        },
    });*/

    map.on('mousemove', function (e) {
        document.getElementById('coordinates').innerHTML =
        // e.point is the x, y coordinates of the mousemove event relative
        // to the top-left corner of the map
        JSON.stringify(e.point) + '<br />' +
        // e.lngLat is the longitude, latitude geographical position of the event
        JSON.stringify(e.lngLat.wrap());
        });

});