import lume from 'lume/mod.ts';

import jsonLoader from 'lume/core/loaders/json.ts';
import basePath from 'lume/plugins/base_path.ts';
import esbuild from 'lume/plugins/esbuild.ts';
import inline from "lume/plugins/inline.ts";
import netlifyCMS from 'lume/plugins/netlify_cms.ts';
// import postcss from "lume/plugins/postcss.ts";
import resolveUrls from 'lume/plugins/resolve_urls.ts';
import slugifyUrls from 'lume/plugins/slugify_urls.ts';
import { stringify as yamlStringify } from 'std/encoding/yaml.ts';
import { copy } from 'std/fs/copy.ts';
import autoDependency from '/src/_lib/oi/auto-dependency.ts';
import csvLoader from '/src/_lib/oi/csv-loader.ts';

const site = lume({
  src: './src',
  location: new URL('https://yff-wireframe.open-innovations.org/'),
});

// To set the DEBUG global data, start the process with DEBUG=true in the environment
if (Deno.env.get('DEBUG') !== undefined) site.data('DEBUG', true);

// Also process .html files
site.loadPages(['.html']);

site.use(inline());

// Setup admin
site.use(
  netlifyCMS({
    previewStyle: '/style/wireframe.css',
    extraHTML: `<script src='/admin/netlify-extras.js'></script>`,
  })
);

// Process all css files
// site.use(postcss({ sourceMap: true }));
site.copy(['.js']);
site.copy(['.css']);
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

// Add csv loader
site.loadData(['.csv'], csvLoader);
site.loadData(['.geojson', '.hexjson'], jsonLoader);

// Copy source data files to live site
const interimDataDir = 'generated-data-directory';
site.script('copy-data-files', async () => {
  await copy('src/_data/sources', `src/${interimDataDir}/`, {
    overwrite: true,
  });
});

// Execute it before the site is built
site.addEventListener('beforeBuild', 'copy-data-files');

site.copy(interimDataDir, 'data');

site.process(['.html'], autoDependency);

// Add filters
site.filter('yaml', (value, options = {}) => yamlStringify(value, options));
site.filter('striplinks', (value) => value.replace(/<a\b[^>]*>/gi).replace(/<\/a>/gi) );

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

// Prevent jekyll building
site.copy('.nojekyll');

// Add CNAME file
site.copy('CNAME');

export default site;
