import { dirname, fromFileUrl } from "https://deno.land/std@0.188.0/path/mod.ts";
import { patchVisualisation } from "../../../../../lib/visualisation-minimiser.ts";

const makeMapper = (title: string, id: string) => (theViz) => {
  theViz.title = title;
  theViz.config.id = id;
  theViz.config.axis.x.title = undefined;
  theViz.config.axis.y.title = undefined;
  theViz.config.axis.y.ticks = 'unlabelled';
  theViz.config.legend.show = false;
  theViz.config.columns = [
    { name: 'x_tick_labels', template: '' }
  ];
  return theViz;
}

export const estimatedVacancies = await patchVisualisation(
  `${dirname(fromFileUrl(import.meta.url))}/estimated_vacancies.yml`,
  makeMapper(
    "Estimated vacancies trend since 2001",
    "estimated-vacancies",
  )
);
