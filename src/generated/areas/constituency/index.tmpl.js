export const layout = 'layouts/areas/pcon.njk';

export const tags = ['constituency'];

export default function*({ areas, page }) {
  // Iterate over all the areas
  for (const area of areas.reference.pcon) {
    // Read the keys out of the area and map to more friendly names
    const { PCON22NM: name, PCON22CD: code } = area;
	
	// Yield the data which creates the page
    yield {
      title: name,
      url: `/areas/constituency/${ code }/`,
      area: {
        code: code,
        type: 'PCON22',
		summary: page.data[code].summary||{},
		map: page.data[code].map||{}
      }
    }
  }

}