import { CategoryChart, LineChart } from '/oi/charts.js';
import { colourScales, Colour } from '/oi/colour.js';
import { loadDataFile } from '/oi/util.js'

export const css = `
.chart .line { stroke-width: 4px; }
.key:before { content: "Key: "; font-family: 'Century Gothic', sans-serif; font-weight: bold; }
.key { display: inline-block; text-align: center; background: #efefef; padding: 0.5em; margin-bottom: 1em; }
.keyitem { display: inline-block; padding-right: 0.5em; font-family: 'Century Gothic', sans-serif; font-weight: bold; cursor: pointer; }
.keyitem:hover { background: white; }

.tooltip { color: black; margin-top: -0.75em; transition: left 0.03s linear, top 0.03s linear; white-space: nowrap; font-family: 'Century Gothic', sans-serif; }
.tooltip .inner { padding: 1em; }
circle.selected { r: 5px; }
`;

export default function ({ config, sources }) {
  const csv = loadDataFile(config.file, sources);

console.log(config.type)
  var chart,html;
  html = "?";
  if(config.type=="line-chart"){
    chart = new LineChart(config,csv);
	html = chart.getSVG();
  }else if(config.type=="category-chart"){
    chart = new CategoryChart(config,csv);
	html = chart.getSVG();
  }
  return ['<div class="chart">',
    html,
    '</div>'
  ].join('');
}