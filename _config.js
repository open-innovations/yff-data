import lume from 'lume/mod.ts';

import jsonLoader from 'lume/core/loaders/json.ts';
import basePath from 'lume/plugins/base_path.ts';
import esbuild from 'lume/plugins/esbuild.ts';
import inline from "lume/plugins/inline.ts";
import netlifyCMS from 'lume/plugins/netlify_cms.ts';
import postcss from "lume/plugins/postcss.ts";
import date from "lume/plugins/date.ts"; // To format dates see: https://lume.land/plugins/date/ and https://date-fns.org/v2.22.0/docs/format
import enGB from "npm:date-fns/locale/en-GB/index.js";
import resolveUrls from 'lume/plugins/resolve_urls.ts';
import slugifyUrls from 'lume/plugins/slugify_urls.ts';
import { stringify as yamlStringify } from 'std/encoding/yaml.ts';
import { walkSync } from 'std/fs/mod.ts';
import csvLoader from 'oi-lume-utils/loaders/csv-loader.ts';
import autoDependency from 'oi-lume-utils/processors/auto-dependency.ts';
import { applyReplacementFilters } from '/src/_lib/oi/util.js';
import injector from '/src/_lib/oi/processor/injector.js';
import pagefind from "lume/plugins/pagefind.ts";

import { generateTickArray } from './src/_lib/chart-filters.ts';

import oiLumeViz from "https://deno.land/x/oi_lume_viz@v0.13.2/mod.ts";

const site = lume({
  src: './src',
  location: new URL('https://yff-wireframe.open-innovations.org/'),
});

// Change this to update the version of the site that is built. This mainly affects navigation.
site.data('version', Deno.env.get('VERSION') || 'v2');

// To set the DEBUG global data, start the process with DEBUG=true in the environment
if (Deno.env.get('DEBUG') !== undefined) site.data('DEBUG', true);

// Set up search engine
site.use(pagefind());

// Process all css files
site.use(postcss());
site.use(inline());

// Also process .html files
site.loadPages(['.html']);

// Setup admin
site.use(netlifyCMS({
  previewStyle: '/assets/style/yff.css',
  extraHTML: `<script src='/admin/netlify-extras.js'></script>`,
}));

site.use(oiLumeViz({
	'assetPath': '/assets/oi',
  'font': {
    family: 'CenturyGothicStd,"Century Gothic",sans-serif'
  },
	'colour': {
		'scales': {
			'YFF': '#000000 0%, #7D2248 33%, #e55912 62%, #f7ab3d 84%, #fcddb1 100%',
		},
    names: {
      "Gold": "#F7AB3D","Gold-1": "#f9bc64","Gold-2": "#facd8b","Gold-3": "#fcddb1","Gold-4": "#fdeed8",
      "Orange": "#E55912","Orange-1": "#eb7a41","Orange-2": "#f09c71","Orange-3": "#f5bda0","Orange-4": "#faded0",
      "Turquoise": "#69C2C9","Turquoise-1": "#87ced4","Turquoise-2": "#a5dadf","Turquoise-3": "#c3e7ea","Turquoise-4": "#e1f3f4",
      "Cherry": "#E52E36","Cherry-1": "#eb585e","Cherry-2": "#f08286","Cherry-3": "#f5abae","Cherry-4": "#fad5d7",
      "Chartreuse": "#C7B200","Chartreuse-1": "#d2c233","Chartreuse-2": "#ddd166","Chartreuse-3": "#e9e099","Chartreuse-4": "#f4f0cc",
      "Plum": "#7D2248","Plum-1": "#974e6d","Plum-2": "#b17a91","Plum-3": "#cba7b6","Plum-4": "#e5d3da",
      "Grey": "#B2B2B2","Grey-1": "#c1c1c1","Grey-2": "#d1d1d1","Grey-3": "#e0e0e0","Grey-4": "#f0f0f0",
      "Blue": "#005776","Blue-1": "#337991","Blue-2": "#669aad","Blue-3": "#99bcc8","Blue-4": "#ccdde4",
      "Raisin": "#874245","Raisin-1": "#9f686a","Raisin-2": "#b78e8f","Raisin-3": "#cfb4b5","Raisin-4": "#e7d9da",
      "Rose": "#FF808B","Rose-1": "#ff9aa2","Rose-2": "#ffb3b9","Rose-3": "#ffccd1","Rose-4": "#ffe6e8",
      "Forest": "#4A783C","Forest-1": "#6e9363","Forest-2": "#92ae8a","Forest-3": "#b7c9b1","Forest-4": "#dbe4d8",
      "Black": "#000000","Black-1": "#595b61","Black-2": "#85878b","Black-3": "#b0b1b3","Black-4": "#d8d9da",
      // Genders
      "Female":"#ee7e3b",
      "Male":"#264c59",
      // Ethnicities
      "Bangladeshi":"#7D2248","Black/African/Caribbean/Black British":"#75b8d3","Chinese":"#fe9400", "Indian":"#274b57","Mixed/Multiple":"#E55912","Other":"#0685cc","Pakistani":"#874245","Other Asian":"#39c2b0","White":"#fdc358", "Total":"#ee7e3b", "White (exclu. Irish)":"#39c2b0","Asian/Asian British":"#7D2248", "Middle Eastern":"#274b57",
      // Religions
      "Any other religion":"#69C2C9","Buddhist":"#C7B200","Christian":"#E55912","Hindu":"#874245","Jewish":"#7D2248","Muslim":"#005776","None":"#fdc358","Sikh":"#69C2C9",
      // Age groups
      "16-17":"#E52E36","18-24":"#F7AB3D","25-49":"#C7B200","50-64":"#005776"
    },
    series:["#E55912", "#005776", "#F7AB3D", "#4A783C" ],
	}
}));

site.copy(['.min.js']);
// site.copy(['.css']);
site.copy(['.svg']);
site.copy(['.png']);

// Process Javascript files
site.use(
  esbuild({
    options: {
      bundle: true,
      format: 'iife',
      minify: true,
      keepNames: true,
      platform: 'browser',
      target: 'es6',
      treeShaking: true,
    },
  })
);
  
// Format dates
site.use(date({
  locales: { enGB },
  formats: {
    "YFF": "MMMM yyyy",
  }
}));

// Add csv loader
site.loadData(['.csv'], csvLoader);
site.loadData(['.geojson', '.hexjson'], jsonLoader);
site.loadData(['.md']);

/**
 * Descend into a folder tree and remotely map each file to the Lume build
 * 
 * @param {string} source Source directory, relative to this file
 * @param {string} target Location in the lume build virtual file system
 */
function remoteTree(source, target) {
  const files = Array.from(walkSync(source, {
    includeDirs: false,
  })).map(({ path }) => path);

  files.forEach(remote => {
    const local = remote.replace(source, target);
    site.remoteFile(local, './' + remote);
  });
}

site.remoteFile("/assets/images/open-innovations-logo.svg", "https://open-innovations.org/resources/images/logos/oi-square-black.svg")

const dataPath = '/data';
// Mirror source data files to live site
remoteTree('src/_data/sources', dataPath);
// Mirror raw data tiles to live site
remoteTree('data', dataPath + '/raw');

// Copy /data to live site
site.copy(dataPath);

site.preprocess([".html"], (page) => {
  page.data.srcPath = 'src' + page.src.path + page.src.ext;
});

// Processor to extract content from a page and insert it into the body of another page
site.process(['.html'], injector);
// Processor which adds dependencies into the page head
site.process(['.html'], autoDependency);

// Add filters
site.filter('yaml', (value, options = {}) => yamlStringify(value, options));
site.filter('striplinks', (value) => value.replace(/<a\b[^>]*>([^\<]*)<\/a>/gi, function (m, p1) { return p1; }));
site.filter('applyReplacementFilters', (value, options = { 'filter': true }) => applyReplacementFilters(value, options));

site.filter('pick', (list, ...keys) => keys.map(i => list[i] || null));
site.filter('isArray', (item) => Array.isArray(item));
site.filter('getAttr', (object, attr) => object.map(x => x[attr]));

site.filter('max', (list) => Math.max(...list));

site.filter('autoLegend', (config, labelFormatter=(x) => `${x}%`) => {
  const values = config.data.map(x => x[config.value]);
  // Max rounded to nearest 5
  const max = Math.ceil(Math.max(...values)/5)*5;
  const steps = 5;
  const legendValues = Array.from(Array(steps).keys()).map(x => x * max / (steps-1)).reverse();
  const legend = {
    position: 'top right',
    items: legendValues.map(x => ({ value: x, label: labelFormatter(x) }))
  }
  // Construct config
  return {
    min: 0,
    max: max,
    ...config,
    legend: {
      ...legend,
      ...config.legend,
    },
  }
})

site.filter('findByAttribute', (list, key, value) => list.filter(x => x[key] === value))

// TODO fix this function!
// Timezone awareness is an issue
function dateBetween(start, end) {
  const now = Date.now();
  const latest = new Date(end);
  latest.setUTCDate(latest.getUTCDate() + 1);
  if (now < start.getTime()) return false;
  if (latest.getTime() < now) return false;
  return true;
}

site.filter('get_annotations', (object, path) => Object
  .values(object)
  .filter(a => a.relates_to === path)
  .filter(a => dateBetween(a.start_date, a.end_date))
  .sort((a, b) => new Date(a.start_date) - new Date(b.start_date))
);

site.filter('autoTicks', generateTickArray)

// URL re-writing plugins. These have to be last to enable any urls installed by the
// processors to be re-written
site.use(basePath());
site.use(resolveUrls());
site.use(slugifyUrls());

// Define remote access to the font files
[
  'CenturyGothicStd.woff2',
  'CenturyGothicStd.woff',
  'CenturyGothicStdBold.woff2',
  'CenturyGothicStdBold.woff',
].forEach(font => {
  site.remoteFile(`/assets/fonts/${font}`, `https://youthfuturesfoundation.org/wp-content/themes/youthfutures/assets/fonts/${font}`);
})
// Force provisioning of font files
site.copy('/assets/fonts');

// Define remote image assets from wordpress theme
[
  'Orange_arrow_right-01.svg',
  'Grey_arrow_right-01.svg',
].forEach(image => {
  site.remoteFile(`/assets/images/yff/${image}`, `https://youthfuturesfoundation.org/wp-content/themes/youthfutures/assets/img/${image}`);
});
site.copy('/assets/images/yff');

// Prevent jekyll building
site.copy('.nojekyll');

// Add CNAME file
site.copy('CNAME');

export default site;
