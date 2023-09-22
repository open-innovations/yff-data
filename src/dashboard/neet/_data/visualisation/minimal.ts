import { dirname, fromFileUrl } from "https://deno.land/std@0.188.0/path/mod.ts";
import { patchVisualisation } from "../../../../../lib/visualisation-minimiser.ts";

export const allYoungPeople = await patchVisualisation(`${dirname(fromFileUrl(import.meta.url))}/all_young_people.yml`, (theViz) => {
  theViz.title = 'NEET trends since 2001'
  theViz.config.id = "neet-rate-all-time";
  theViz.config.axis.y.title = undefined;
  theViz.config.axis.y.ticks = 'unlabelled';
  theViz.config.legend.show = true;
  theViz.config.columns = [
    { name: 'x_tick_labels', template: '' }
  ];
  return theViz;
});
