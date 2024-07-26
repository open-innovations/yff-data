export const layout = 'layouts/areas/pcon.vto';

export const tags = ['area', 'constituency'];

const makeUrl = (key) => `/areas/constituency/${key}/`;

export default function*({ areas, build, map, summary: allSummary }) {

  let areasToBuild = areas.reference.pcon;

  if (build.small_site) {
    areasToBuild = areas.reference.pcon.slice(0, 10);
  }

  // Iterate over all the areas
  for (const area of areasToBuild) {
    // Read the keys out of the area and map to more friendly names
    const {
      PCON24NM: name,
      PCON24CD: code,
      PCON21CD: old_code,
    } = area;

    const summary = allSummary[code];
    if (!summary) {
      console.error(`No summary data for ${name} (${code})...`);
      dataSource=undefined;
    }

  	// Yield the data which creates the page
    yield {
      title: `Constituency: ${ name }`,
      url: makeUrl(code),
      oldUrl: [
        old_code
      ].filter(x => x).map(makeUrl),
      topics: ['Constituency'],
      area: {
        name: name,
        code: code,
        type: 'PCON24',
        pcon21cd: old_code,
      },

      // Overriding map and summary
      map: map[code],
      summary: summary,

      // masking large datasets at top-level
      areas: 'MASKED AT THIS LEVEL',
      sources: 'MASKED AT THIS LEVEL',
    }
  }

}