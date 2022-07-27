# yff-wireframe

> Experimentation in YFF dashboards

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

## Pre-requisites

You will need to have [`deno` installed](https://deno.land/#installation) and in your path.

## Building / Serving

The `deno.json` file includes useful tasks:

`deno task serve` - serves the site at https://localhost:3000/.

`deno task build` - builds the site into `_site`