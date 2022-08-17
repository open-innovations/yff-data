import { LeafletMap } from '/src/_lib/oi/map.js';
import { loadDataFile } from '/src/_lib/oi/util.js'


export const css = `
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

		if(configcopy.type=="leaflet"){

			// Create a new Line Chart
			map = new LeafletMap(configcopy,csv);

		}

		// Get the output
		if(map) html = map.getHTML();

	}else{

		console.warn('WARNING: No CSV contents at '+config.file);

	}

	return html;
}