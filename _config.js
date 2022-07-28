import lume from "lume/mod.ts";

import jsonLoader from "lume/core/loaders/json.ts";
import basePath from "lume/plugins/base_path.ts";
import netlifyCMS from "lume/plugins/netlify_cms.ts";
// import postcss from "lume/plugins/postcss.ts";
import resolveUrls from "lume/plugins/resolve_urls.ts";
import slugifyUrls from "lume/plugins/slugify_urls.ts";
import { stringify as yamlStringify } from "std/encoding/yaml.ts";
import { copy } from "std/fs/copy.ts";
import csvLoader from '/oi/csv-loader.ts';

const site = lume({
  src: './src',
  location: new URL("https://open-innovations.github.io/yff-wireframe/"),
});

// Also process .html files
site.loadPages(['.html'])

site.use(basePath());
site.use(resolveUrls());
site.use(slugifyUrls());

// Setup admin
site.use(netlifyCMS());

// Process all css files
// site.use(postcss({
//   sourceMap: true,
//   plugins: [
//     postcssNesting(),
//     autoprefixer(),
//   ],
// }));
site.copy(['.css']);

// Add csv loader
site.loadData([".csv"], csvLoader);
site.loadData([".geojson", ".hexjson"], jsonLoader);

// Copy source data files to live site
site.script("copy-data-files", async () => {
  await copy("src/_data/sources", "src/data/", {
    overwrite: true,
  });
});

// Execute it before the site is built
site.addEventListener("beforeBuild", "copy-data-files");

site.copy('data', 'data');

// Add filters
site.filter("yaml", (value, options = {}) => yamlStringify(value, options));

export default site;
