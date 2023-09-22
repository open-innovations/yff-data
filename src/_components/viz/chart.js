import { CategoryChart, LineChart, BarChart, StackedBarChart } from '/src/_lib/oi/charts.js';
import { loadDataFile } from '/src/_lib/oi/util.js'

const divisor = function* () {
  let range = 0;
  while(true) {
    for (const base of [1, 2, 5]) yield base * 10**range;
    range++;
  }
};

function calculateStep(range) {
  const g = divisor();
  let step = g.next().value;
  while ((range / step) >= 10) {
    step = g.next().value;
  }
  return step;
}

function generateTickValues(max, min=0) {
  const range = max - min;
  const step = calculateStep(range);
  const numTicks = Math.floor(range / step) + 1;

  return Array.from(new Array(numTicks))
    .map((_, i) => i * step + min);
}

// This component uses "/assets/js/chart.js" to make things interactive in the browser.
// It will only get included in pages that need it by using the "data-dependencies" attribute.

export const css = `
.chart .series path.line { stroke-width: 4px; }
.chart .legend span { font-family: CenturyGothicStd, 'Century Gothic', sans-serif; font-weight: bold; }
.chart .legend { display: inline-block; text-align: center; padding: 0.5em; margin-bottom: 1em; max-width: calc(100% - 3em); }
.chart .legend-item { margin-left: 4px; display: inline-block; padding-right: 0.5em; font-family: CenturyGothicStd, 'Century Gothic', sans-serif; font-weight: bold; cursor: pointer; line-height: 1.5em; }
.chart .legend-item svg { margin: 0.25em 0.25em 0.25em 0.5em; float: left; }
.chart .legend-item:hover:not(.series-lock), .chart .legend-item:focus:not(.series-lock) { background: rgba(255,255,255,0.5); outline: 1px dotted #7b2347; }
.chart .legend-item.series-lock { background: white; outline: 1px solid #7b2347;  }
.tooltip { color: black; margin-top: -0.75em; transition: left 0.03s linear, top 0.03s linear; font-family: CenturyGothicStd, 'Century Gothic', sans-serif; filter: drop-shadow(0px 1px 1px rgba(0,0,0,0.7)); }
.tooltip .inner { padding: 1em; width: 100%; }
circle.selected { r: 5px; }
.chart rect { transition: 0.1s ease-in x; }
`;

function clone(a){ return JSON.parse(JSON.stringify(a)); }

export default function (context) {
  const { config } = context; 

	// Load the data from the sources
	const csv = loadDataFile(config, context);

	var chart,html;

	// Set the output to "?" as a default
	html = "?";

	// Make a clone of the original config to avoid updating the contents elsewhere
	const configcopy = clone(config);

  if (configcopy.type == "line-chart") {
    // Patch the config
    if (configcopy.axis.x.min === undefined) configcopy.axis.x.min = 0;
    if (configcopy.axis.x.max === undefined) configcopy.axis.x.max = csv.rows.length - 1;
    if (configcopy.axis.y.min === undefined) configcopy.axis.y.min = 0;
    if (configcopy.axis.y.max === undefined) {
      const max = Math.max(...configcopy.series.map(s => s.y).map(s => csv.columns[s]).flat())
      const d = 10 ** (Math.round(max).toString().length - 2);
      const roundedMax = Math.ceil(max / d) * d;
      configcopy.axis.y.max = roundedMax;
    }

    if (configcopy.axis.x.ticks === undefined) {
      const tickValues = generateTickValues(
        configcopy.axis.x.max,
        configcopy.axis.x.min
      );
      const ticks = tickValues.map(v => {
        const index = csv.rows.length - 1 - v;
        return {
          value: index,
          label: (typeof csv.columns.x_tick_labels==="object" ? csv.columns.x_tick_labels[index] : "")
        }
      });
      configcopy.axis.x.ticks = ticks;
    }

    if (configcopy.axis.y.ticks === undefined || configcopy.axis.y.ticks === 'unlabelled') {
      const tickValues = generateTickValues(
        configcopy.axis.y.max,
        configcopy.axis.y.min
      );
      const ticks = tickValues.map(v => ({
        value: v,
        label: configcopy.axis.y.ticks === 'unlabelled' ? '' : v.toString(),
        grid: true,
      }));
      configcopy.axis.y.ticks = ticks;
    }

    // Create a new Line Chart
    chart = new LineChart(configcopy, csv);

  } else if (configcopy.type == "category-chart") {

    // Create a new Category Chart
    chart = new CategoryChart(configcopy, csv);

  } else if (configcopy.type == "bar-chart") {

    // Create a new Category Chart
    chart = new BarChart(configcopy, csv);

  } else if (configcopy.type == "stacked-bar-chart") {

    // Create a new Category Chart
    chart = new StackedBarChart(configcopy, csv);

  }

  // Get the output
  if (chart) html = chart.getSVG();

	return ['<div class="chart" data-dependencies="/assets/js/chart.js">',
		html,
		'</div>'
	].join('');
}