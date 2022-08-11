import { Dashboard } from '/src/_lib/oi/dashboard.js';
import { loadDataFile } from '/src/_lib/oi/util.js'


export const css = `
.dashboard {
	width: 100%;
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	grid-gap: 1em;
}
.dashboard h3 { color: inherit!important; }
.panel { background: #efefef; padding: 1em; }
.dashboard .bignum { font-size: 4em; line-height: 1.25em; font-weight: bold; text-align: center; display: block; margin-top: 0; }
.dashboard .note { font-size: 0.7em; text-align: center; display: block; }
`;

function clone(a){ return JSON.parse(JSON.stringify(a)); }

export default function ({ config, sources }) {

	// Load the data from the sources
	const csv = loadDataFile(config, sources);

	// Set the output to "?" as a default
	let html = "?";

	if(csv){

		// Make a clone of the original config to avoid updating the contents elsewhere
		const configcopy = clone(config);

		// Create a new Line Chart
		let dashboard = new Dashboard(configcopy,csv);

		// Get the output
		if(dashboard) html = dashboard.getHTML();

	}else{

		console.warn('WARNING: No CSV contents at '+config.file);

	}

	return html;
}