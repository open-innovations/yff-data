import { LeafletMap, SVGMap, HexMap } from '/src/_lib/oi/map.js';
import { loadDataFile } from '/src/_lib/oi/util.js'


export const css = `
.map { background: #e2e2e2; position: relative; }
.map .leaflet { width: 100%; aspect-ratio: 16 / 9; background: #e2e2e2; position: relative; }
.map .leaflet a { background-image: none!important; color: inherit!important; }
.map .legend { text-align: left; line-height: 18px; color: #555; background: rgba(255,255,255,0.8); padding: 1em; }
.map .legend i { width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 1; }
.map .leaflet-popup-content-wrapper { border-radius: 0; }
.map .leaflet-popup-content { margin: 1em; }
.map .leaflet-container, .map .leaflet-popup-content-wrapper, .map .leaflet-popup-content { font-size: 1em; font-family: "CenturyGothicStd", "Century Gothic", Helvetica, sans-serif; line-height: inherit; }
.map .leaflet-popup-content-wrapper, .map .leaflet-popup-tip { box-shadow: none; }
.map .leaflet-popup { filter: drop-shadow(0 1px 1px rgba(0,0,0,0.7)); }
.map .leaflet-popup > * { filter: none; }
.map .leaflet-container a.leaflet-popup-close-button { color: inherit; }
.map .leaflet-control { z-index: 400; }
.map .leaflet-top, .leaflet-bottom { position: absolute; z-index: 400; pointer-events: none; }
.leaflet-top { top: 0; }
.leaflet-right { right: 0; }
.leaflet-bottom { bottom: 0; }
.leaflet-left { left: 0; }
`;

function clone(a){ return JSON.parse(JSON.stringify(a)); }

export default function ({ config, sources }) {

	// Load the data from the sources
	const csv = loadDataFile(config, sources);

	// Set the output to "?" as a default
	let html = "?";

	if(csv){
		
		var map;

		// Make a clone of the original config to avoid updating the contents elsewhere
		const configcopy = clone(config);

		if(configcopy.geojson){
			var files = {
				'NUTS1':'/data/maps/NUTS_Level_1_(January_2018)_Boundaries.geojson',
				'NUTS2':'/data/maps/NUTS_Level_2_(January_2018)_Boundaries.geojson',
				'NUTS3':'/data/maps/NUTS_Level_3_(January_2018)_Boundaries.geojson',
				'ITL1':'/data/maps/International_Territorial_Level_1_(January_2021)_UK_BUC.geojson',
				'ITL2':'/data/maps/International_Territorial_Level_2_(January_2021)_UK_BUC_V2.geojson',
				'ITL3':'/data/maps/International_Territorial_Level_3_(January_2021)_UK_BUC_V3.geojson',
				'LAD21':'/data/maps/Local_Authority_Districts_(December_2021)_GB_BUC.geojson',
				'PCON21':'/data/maps/Westminster_Parliamentary_Constituencies_(December_2021)_UK_BUC.geojson'
			}
			// If no explicit GeoJSON file provided, check if a "layout" key has been set instead
			if(!configcopy.geojson.file){
				if(configcopy.geojson.layout && files[configcopy.geojson.layout]) configcopy.geojson.file = files[configcopy.geojson.layout];
				else configcopy.geojson.file = files['NUTS3'];
			}
		}
		if(configcopy.hexjson){
			var files = {
				'NUTS1':'/data/maps/uk-nuts1.hexjson',
				'NUTS2':'/data/maps/uk-nuts2.hexjson',
				'NUTS3':'/data/maps/uk-nuts3.hexjson'
			}
			// If no explicit HexJSON file provided, check if a "layout" key has been set instead
			if(!configcopy.hexjson.file){
				if(configcopy.hexjson.layout && files[configcopy.hexjson.layout]) configcopy.hexjson.file = files[configcopy.hexjson.layout];
				else configcopy.hexjson.file = files['NUTS3'];
			}
		}

		if(configcopy.type=="leaflet-map"){

			// Create a new Leaflet map
			map = new LeafletMap(configcopy,csv);

		}else if(configcopy.type=="svg-map"){

			// Create a new simple SVG map
			map = new SVGMap(configcopy,csv,sources);

		}else if(configcopy.type=="hex-map"){
			
			map = new HexMap(configcopy,csv,sources);

		}

		// Get the output
		if(map) html = map.getHTML();

	}else{

		console.warn('WARNING: No CSV contents at '+config.file);

	}

	return html;
}