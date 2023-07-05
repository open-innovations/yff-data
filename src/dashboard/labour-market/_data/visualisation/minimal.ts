import { dirname, fromFileUrl } from "https://deno.land/std@0.188.0/path/mod.ts";
import { patchVisualisation } from "../../../../../lib/visualisation-minimiser.ts";

const makeMapper = (title: string, id: string) => (theViz) => {
  theViz.title = title;
  theViz.config.id = id;
  theViz.config.axis.x.title = undefined;
  theViz.config.axis.y.title = undefined;
  theViz.config.axis.y.ticks = 'unlabelled';
  theViz.config.legend.show = true;
  theViz.config.columns = [
    { name: 'x_tick_labels', template: '' }
  ];
  return theViz;
}

export const educationStatus = await patchVisualisation(
  `${dirname(fromFileUrl(import.meta.url))}/economic_activity_not_in_full_time_education_3_years.yml`,
  makeMapper(
    "NFTE employment status trends last three years",
    "education-status",
  )
);

export const longTermUnemployment = await patchVisualisation(
  `${dirname(fromFileUrl(import.meta.url))}/long_term_unemployment_3_years.yml`,
  makeMapper(
    "Long-term unemployment trends last three years",
    "long-term-unemployment",
  )
);
