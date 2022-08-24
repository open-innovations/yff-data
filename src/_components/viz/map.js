import { LeafletMap, SVGMap } from '/src/_lib/oi/map.js';
import { loadDataFile } from '/src/_lib/oi/util.js'


export const css = `
.map { background: #e2e2e2; }
.map .leaflet { width: 100%; aspect-ratio: 16 / 9; background: #e2e2e2; position: relative; }
.map .leaflet a { background-image: none!important; color: inherit!important; }
.map .leaflet .legend { text-align: left; line-height: 18px; color: #555; }
.map .leaflet .legend i { width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 1; }
.map .leaflet .legend { background: rgba(255,255,255,0.8); padding: 1em; }
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

		if(configcopy.type=="leaflet-map"){

			// Create a new Leaflet map
			map = new LeafletMap(configcopy,csv);

		}else if(configcopy.type=="svg-map"){

			// Create a new simple SVG map
			map = new SVGMap(configcopy,csv,sources);

		}

		// Get the output
		if(map) html = map.getHTML();

	}else{

		console.warn('WARNING: No CSV contents at '+config.file);

	}

	return html;
}