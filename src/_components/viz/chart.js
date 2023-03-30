import { CategoryChart, LineChart, BarChart, StackedBarChart } from '/src/_lib/oi/charts.js';
import { loadDataFile } from '/src/_lib/oi/util.js'

// This component uses "/assets/js/chart.js" to make things interactive in the browser.
// It will only get included in pages that need it by using the "data-dependencies" attribute.

export const css = `
.chart .series path.line { stroke-width: 4px; }
.chart .legend span { font-family: CenturyGothicStd, 'Century Gothic', sans-serif; font-weight: bold; }
.chart .legend { display: inline-block; text-align: center; padding: 0.5em; margin-bottom: 1em; max-width: calc(100% - 3em); }
.chart .legend-item { display: inline-block; padding-right: 0.5em; font-family: CenturyGothicStd, 'Century Gothic', sans-serif; font-weight: bold; cursor: pointer; line-height: 1.5em; }
.chart .legend-item svg { margin: 0.25em 0.25em 0.25em 0.5em; float: left; }
.chart .legend-item:hover { background: white; }

.tooltip { color: black; margin-top: -0.75em; transition: left 0.03s linear, top 0.03s linear; white-space: nowrap; font-family: CenturyGothicStd, 'Century Gothic', sans-serif; }
.tooltip .inner { padding: 1em; }
.tooltip > * { filter: drop-shadow(0px 1px 1px rgba(0,0,0,0.7)); }
circle.selected { r: 5px; }
.chart rect { transition: 0.1s ease-in x; }
`;

function clone(a){ return JSON.parse(JSON.stringify(a)); }

export default function ({ config, sources }) {

	// Load the data from the sources
	const csv = loadDataFile(config, sources);

	var chart,html;

	// Set the output to "?" as a default
	html = "?";

	// Make a clone of the original config to avoid updating the contents elsewhere
	const configcopy = clone(config);

	if(configcopy.type=="line-chart"){

		// Create a new Line Chart
		chart = new LineChart(configcopy,csv);

	}else if(configcopy.type=="category-chart"){

		// Create a new Category Chart
		chart = new CategoryChart(configcopy,csv);

	}else if(configcopy.type=="bar-chart"){

		// Create a new Category Chart
		chart = new BarChart(configcopy,csv);

	}else if(configcopy.type=="stacked-bar-chart"){

		// Create a new Category Chart
		chart = new StackedBarChart(configcopy,csv);

	}

	// Get the output
	if(chart) html = chart.getSVG();

	return ['<div class="chart" data-dependencies="/assets/js/chart.js">',
		html,
		'</div>'
	].join('');
}