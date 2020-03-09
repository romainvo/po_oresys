var bounds_paris = new mapboxgl.LngLatBounds(
    new mapboxgl.LngLat(2.1565006829, 48.80361985565),
    new mapboxgl.LngLat(2.5291462587, 48.91621970507)
  );

var map = new mapboxgl.Map({
    container: 'map',
    style: 'https://openmaptiles.geo.data.gouv.fr/styles/osm-bright/style.json', 
    center: [2.349014, 48.85500],
    zoom: 11.5,
    minZoom: 1,
    maxZoom: 19,
    maxBounds: bounds_paris
    });
 
map.addControl(new mapboxgl.NavigationControl());

var hoveredStateId =  null;

var coordinates = document.getElementById('coordinates');

map.on('load', function () {
    /*
    map.addSource('arrondissements', {
        'type': 'geojson',
        'generateId' : true,
        'data': '/donneesgeos/arrondissements_municipaux-20180711.json'
    });*/

    map.addSource('rpls', {
        type: 'geojson',
        generateId: true,
        data: '/donneesgeos/rpls.geojson',
        cluster: true,
        clusterMaxZoom: 12, // Max zoom to cluster points on
        clusterRadius: 70 // Radius of each cluster when clustering points (defaults to 50)    
    });

    map.addSource('airbnb', {
        type: 'geojson',
        generateId: true,
        data: '/donneesgeos/airbnb.geojson',
        cluster: true,
        clusterMaxZoom: 14, // Max zoom to cluster points on
        clusterRadius: 70 // Radius of each cluster when clustering points (defaults to 50)    
    });

    map.addSource('croisements', {
        type: 'geojson',
        generateId: true,
        data: '/donneesgeos/croisementBis.geojson',  
    });

    map.addLayer({
        id: "rpls-cluster",
        type: "circle",
        source: "rpls",
        layout: {
            visibility: "visible"
        },
        filter: ["has", "point_count"],
        paint: {
            "circle-color": [
                "step",
                ["get", "point_count"],
                "#0000AA", //"#51bbd6",
                100,
                "#0000AA", //"#f1f075",
                750,
                "#0000AA", //"#f28cb1"
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
        id: "rpls-cluster-count",
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
        id: "rpls-unclustered-points",
        type: "circle",
        source: "rpls",
        layout: {
            visibility: "visible"
        },
        filter: ["!", ["has", "point_count"]],
        paint: {
            "circle-color": "#0000AA",//"#11b4da",
            "circle-radius": 4,
            "circle-stroke-width": 1,
            "circle-stroke-color": "#FFFFFF"
        }
    });

    map.addLayer({
        id: "airbnb-cluster",
        type: "circle",
        source: "airbnb",
        layout: {
            visibility: "visible"
        },
        filter: ["has", "point_count"],
        paint: {
            "circle-color": [
                "step",
                ["get", "point_count"],
                "#FF0000", //"#51bbd6",
                100,
                "#FF0000", //"#f1f075",
                750,
                "#FF0000", //"#f28cb1"
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
        id: "airbnb-cluster-count",
        type: "symbol",
        source: "airbnb",
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
        id: "airbnb-unclustered-points",
        type: "circle",
        source: "airbnb",
        layout: {
            visibility: "visible"
        },        
        "filter": ["!", ["has", "point_count"]],
        paint: {
            "circle-radius": 4,
            "circle-color": "#FF0000",
            "circle-stroke-width": 1,
            "circle-stroke-color": "#FFFFFF"
        },
    });
    /*
    map.addLayer({
        id: "arrondissements-contour",
        type: "line",
        source: "arrondissements",
        layout: {},
        paint: {
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
    });*/

    map.addLayer({
        id: "croisements-points",
        type: "circle",
        source: "croisements",
        layout: {
            visibility: "visible"
        },   
        paint: {
            "circle-color": "rgba(0,255,0,0.5)",//"#11b4da",
            "circle-radius": 5,
            "circle-stroke-width": 1,
            "circle-stroke-color": "#FFFFFF"
        }
    });

    // When the user moves their mouse over the arrondissements-fill layer, 
    // we'll update the feature state for the feature under the mouse.
    /*map.on("mousemove", "arrondissements-fill", function(e) {
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
    });*/

    map.on('mousemove', function (e) {
        document.getElementById('coordinates').innerHTML =
        // e.point is the x, y coordinates of the mousemove event relative
        // to the top-left corner of the map
        JSON.stringify(e.point) + '<br />' +
        // e.lngLat is the longitude, latitude geographical position of the event
        JSON.stringify(e.lngLat.wrap());
    });

    map.on('click',function(e){
        // On récupère les infos (les id_rpls correspondants) du point du layer croisement sur lequel on clique
        var features = map.queryRenderedFeatures(e.point, { layers: ['croisements-points'] });
        if(features.length>0){

            var listIdRpls = [];
            for(name in features[0].properties) { 
                console.log(features[0].properties[name])
                listIdRpls.push(features[0].properties[name])
            }  

            // On cherche les coordonnées des id_rpls trouvés
            var requestURL = '/donneesgeos/coord_rpls.json';
            var request = new XMLHttpRequest();
            request.open('GET', requestURL);
            request.responseType = 'json';
            request.send();
            request.onload = function() {
                var dataRpls = request.response;

                newDataRpls = {'type':'FeatureCollection',
                'features':[{}]
                }
                
                // On met à jour les data des sources avec les coordonnées des points qu'on veut afficher
                listIdRpls.forEach(function(idRpls){
                    newDataRpls.features.push({'type':'Feature',
                    'geometry':  {
                        'type':'Point',
                        'coordinates':[dataRpls.longitude[idRpls], dataRpls.latitude[idRpls]]
                    }})
                    console.log(idRpls)
                ;})
                newDataCroisement = {'type':'FeatureCollection',
                    'features':[{
                        'type':'Feature',
                        'geometry':  {
                            'type':'Point',
                            'coordinates':[features[0].geometry.coordinates[0],features[0].geometry.coordinates[1]]
                      }
                    }]
                };
                map.getSource('rpls').setData(newDataRpls)
                map.getSource('croisements').setData(newDataCroisement)
     
                map.setPaintProperty('rpls-unclustered-points', 'circle-radius', 6);
            }

        }
    });
    
    map.on('click',function(e){

        // On remet à jour les data des sources pour afficher à nouveau tous les points
        map.getSource('rpls').setData('/donneesgeos/rpls.geojson');
        map.getSource('croisements').setData('/donneesgeos/croisementBis.geojson')
        map.setPaintProperty('rpls-unclustered-points', 'circle-radius', 4);

    });

});

var toggleableLayerIds = ['RPLS', 'AirBnB', 'Croisements'];
var link1 = document.createElement('a');
var link2 = document.createElement('a');
var link3 = document.createElement('a');

clickedLayers = [['rpls-cluster','rpls-unclustered-points'], 
['airbnb-cluster','airbnb-unclustered-points'],
['croisements-points']];

var links = [link1, link2, link3];

var layers = document.getElementById('hide_layers');

for (var i = 0; i < 3; i++) {
    var id = toggleableLayerIds[i];

    links[i].href = '#';
    links[i].className = 'active';
    links[i].textContent = id;

    if (i == 0) {
        links[i].onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
    
            console.log(clickedLayers);
            console.log(i);
            var visibility = map.getLayoutProperty(clickedLayers[0][0], 'visibility');
    
            if (visibility === 'visible') {
                for (var j=0; j<clickedLayers[0].length; j++) {
                    map.setLayoutProperty(clickedLayers[0][j], 'visibility', 'none');
                }
                this.className = '';
            } else {
                this.className = 'active';
                for (var j=0; j<clickedLayers[0].length; j++) {
                    map.setLayoutProperty(clickedLayers[0][j], 'visibility', 'visible');
                }
            }
        };
        layers.appendChild(links[i]);

    } else if (i == 1) {
        links[i].onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
    
            console.log(clickedLayers);
            console.log(i);
            var visibility = map.getLayoutProperty(clickedLayers[1][0], 'visibility');
    
            if (visibility === 'visible') {
                for (var j=0; j<clickedLayers[1].length; j++) {
                    map.setLayoutProperty(clickedLayers[1][j], 'visibility', 'none');
                }
                this.className = '';
            } else {
                this.className = 'active';
                for (var j=0; j<clickedLayers[1].length; j++) {
                    map.setLayoutProperty(clickedLayers[1][j], 'visibility', 'visible');
                }
            }
        };
        layers.appendChild(links[i]);

    } else if (i == 2) {

        links[i].onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();

            console.log(clickedLayers);
            console.log(i);
            var visibility = map.getLayoutProperty(clickedLayers[2][0], 'visibility');

            if (visibility === 'visible') {
                for (var j=0; j<clickedLayers[2].length; j++) {
                    map.setLayoutProperty(clickedLayers[2][j], 'visibility', 'none');
                }
                this.className = '';
            } else {
                this.className = 'active';
                for (var j=0; j<clickedLayers[2].length; j++) {
                    map.setLayoutProperty(clickedLayers[2][j], 'visibility', 'visible');
                }
            }
        };
        layers.appendChild(links[i]);
    }
}