# yff-data

> Source of the Youth Futures Foundation data portal

## Data

Data to drive visualisations is managed in the `_data/sources` directory.
This allows it to be loaded as [Lume shared data](https://lume.land/docs/creating-pages/shared-data/).
During the build process, this directory is first copied to the `src/data` directory, and from there
to the `/data` path in the built site. This provides the exact data used as a static asset.

In visualisations, the path to data files is provided in the format `/data/path/to/data.csv`.
This is converted to the loaded data path (e.g. `sources.path.to.data`) by the visualisation components.
Please note, that the extension is ignored. Note that data files with the same name but a different
extension will be merged at the object level. Any keys will be taken from the last loaded value, which is 
potentially indeterminate! The safest thing is to ensure no potential clashes.

### Importing external data

Remote data is imported using the `dvc import-url` command.

```sh
dvc import-url <remote_url> <local_filename>
```

This creates a `<local_filename>.dvc` which tracks the remote file. It can be refreshed using the command `dvc update <local_filename>.dvc`.

## Pre-requisites

You will need to have [`deno` installed](https://deno.land/#installation) and in your path.

## Building / Serving

The `deno.json` file includes useful tasks:

`deno task serve` - serves the site at https://localhost:3000/.

`deno task build` - builds the site into `_site`

## Versioned content

Navigation order and inclusion is set on a per-page basis by including the nav_order data in the front-matter for a page. It takes the following format:

```
nav_order:
  <version_tag>: <ordering>
```

in `_config.ts`, the `version` global data is set. By convention this is set to `v1`, `v2`, etc - but could be anything.

The `nav` component interprets this and selects the pages to include based on the presence of the relevant key.

Similarly, the homepage versions (`/home/v1.njk`, `/home/v2.njk`) are set to be the site homepage by comparison between their slug (`v1`, `v2`) and the global data version. If the slug matches the version, the url for the page is set to `/`, otherwise it defaults to `/home/v<x>/`. This is done in the `/home/_data.ts` file.

## License

The code to build this portal is [licensed under the terms of an MIT License](./LICENSE) by [Open Innovations](https://open-innovations.org).
