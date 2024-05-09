export const layout = 'layouts/areas/pcon.njk';

export const tags = ['area', 'constituency'];

export default function*({ areas, build }) {

  let areasToBuild = areas.reference.pcon;

  if (build.small_site) {
    areasToBuild = areas.reference.pcon.slice(0, 10);
  }

  // Iterate over all the areas
  for (const area of areasToBuild) {
    // Read the keys out of the area and map to more friendly names
    const { PCON22NM: name, PCON22CD: code } = area;

	// Yield the data which creates the page
    yield {
      title: `Constituency: ${ name }`,
      url: `/areas/constituency/${ code }/`,
      topics: ['Constituency'],
      area: {
        name: name,
        code: code,
        type: 'PCON22',
        // Removing to save memory in build
        // summary: summary[code]||{},
        // map: map[code] || {}
      }
    }
  }

}