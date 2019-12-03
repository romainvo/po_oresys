var map = new mapboxgl.Map({
    container: 'map',
    style: 'https://openmaptiles.geo.data.gouv.fr/styles/osm-bright/style.json', 
    //'https://openmaptiles.github.io/klokantech-basic-gl-style/style-cdn.json',
    //'https://openmaptiles.github.io/osm-bright-gl-style/style-cdn.json',
    center: [3, 47],
    zoom: 5,
    minZoom: 1,
    maxZoom: 19
    });