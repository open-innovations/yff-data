import { RankingChart } from '/src/_lib/oi/ranking.js';
import { loadDataFile } from '/src/_lib/oi/util.js';

export const css = `
.ranking svg g:focus { outline: none; }
`;

export default (context) => {
  const { config } = context;

	// Get loaded data from sources object
	// Data structure will include the following:
	//   headers = 2d array of headers
	//   names = column names (rows concatenated)
	//   data = 2d array of data
	//   rows = array of objects with data referenced by name
	//   columns = object with column data as array
	const csv = loadDataFile(config, context);

	var chart,html;

	// Set the output to "?" as a default
	html = "?";

	// Make a clone of the original config to avoid updating the contents elsewhere
	const configcopy = clone(config);

	// Create a new Line Chart
	chart = new RankingChart(configcopy,csv);

	// Get the output
	if(chart) html = chart.getSVG();

	return ['<div class="ranking" data-dependencies="/assets/js/ranking.js">',
		html,
		'</div>'
	].join('');

}

function clone(a){ return JSON.parse(JSON.stringify(a)); }