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
import autoDependency from '/src/_lib/oi/auto-dependency.ts';
import csvLoader from '/src/_lib/oi/csv-loader.ts';
import { applyReplacementFilters } from '/src/_lib/oi/util.js';

const site = lume({
  src: './src',
  location: new URL('https://yff-wireframe.open-innovations.org/'),
});

// Change this to update the version of the site that is built. This mainly affects navigation.
site.data('version', Deno.env.get('VERSION') || 'v1');

// To set the DEBUG global data, start the process with DEBUG=true in the environment
if (Deno.env.get('DEBUG') !== undefined) site.data('DEBUG', true);

// Process all css files
site.use(postcss());

// Also process .html files
site.loadPages(['.html']);

site.use(inline());

// Setup admin
if (Deno.env.get('EDITOR') !== undefined) site.use(
  netlifyCMS({
    previewStyle: '/style/wireframe.css',
    extraHTML: `<script src='/admin/netlify-extras.js'></script>`,
  })
);

site.copy(['.js']);
// site.copy(['.css']);
site.copy(['.svg']);
site.copy(['.png']);

// Process Javascript files
site.use(
  esbuild({
    extensions: ['.esbuild.js'],
    options: {
      bundle: true,
      format: 'iife',
      minify: true,
      keepNames: true,
      platform: 'browser',
      target: 'es6',
      incremental: true,
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

const dataPath = '/data';
// Mirror source data files to live site
remoteTree('src/_data/sources', dataPath);
// Mirror raw data tiles to live site
remoteTree('data', dataPath + '/raw');

// Copy /data to live site
site.copy(dataPath);

site.process(['.html'], autoDependency);

// Add filters
site.filter('yaml', (value, options = {}) => yamlStringify(value, options));
site.filter('striplinks', (value) => value.replace(/<a\b[^>]*>([^\<]*)<\/a>/gi, function (m, p1) { return p1; }));
site.filter('applyReplacementFilters', (value, options = { 'filter': true }) => applyReplacementFilters(value, options));

site.filter('pick', (list, ...keys) => keys.map(i => list[i] || null));

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
