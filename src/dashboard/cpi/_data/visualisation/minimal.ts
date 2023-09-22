import { dirname, fromFileUrl } from "https://deno.land/std@0.188.0/path/mod.ts";
import { patchVisualisation } from "../../../../../lib/visualisation-minimiser.ts";

const makeMapper = (title: string, id: string) => (theViz) => {
  theViz.title = title;
  theViz.config.id = id;
  theViz.config.axis.x.min = -2;
  theViz.config.axis.x.max = 2;
  theViz.config.axis.x.ticks = [];
  // theViz.config.axis.x.title = undefined;
  // theViz.config.axis.y.title = undefined;
  // theViz.config.axis.y.ticks = 'unlabelled';
  theViz.config.legend.show = false;
  // theViz.config.columns = [
  //   { name: 'x_tick_labels', template: '' }
  // ];
  theViz.config.series = theViz.config.series.slice(0,1);

  return theViz;
}

export const cpiYoungPeople = await patchVisualisation(
  `${dirname(fromFileUrl(import.meta.url))}/young_people_barchart.yml`,
  makeMapper(
    "Monthly change in CPI most affecting young people",
    "cpi-young-people",
  )
);
