import { colourScales, Colour } from '/oi/colour.js';
import { loadDataFile } from '/oi/util.js';

export const css = `
  table { border-collapse: collapse; width: 100%; overflow-x: scroll; display: block; }
  th { border: 0; font-weight: bold; }
  td { border: 1px solid black; }
  td:first-child { border-left: 0; }
  td:last-child { border-right: 0; }
  td, th { padding: 1rem; }
`;

export default ({ config, sources }) => {
  // Get loaded data from sources object
  // Data structure will include the following:
  //   headers = 2d array of headers
  //   names = column names (rows concatenated)
  //   data = 2d array of data
  //   rows = array of objects with data referenced by name
  //   columns = object with column data as array
  const table = loadDataFile(config.file, sources);

  // Create array to store html text
  const html = [];
  // Start table
  html.push('<table>');

  // Build header cells
  html.push('<thead>');
  for (const row of table.header) {
    html.push('<tr>');
    const spans = row.reduce((acc, curr) => {
      if (acc.prev != curr) acc.header.push({ name: curr, count: 0 })
      acc.header[acc.header.length - 1].count++;
      acc.prev = curr;
      return acc;
    }, { header: [] });
    for (const cell of spans.header) {
      const { name, count } = cell;
      html.push(`<th${(count > 1) ? ' colspan=' + count : ''}>${name}</th>`)
    }
    html.push('</tr>');
  }
  html.push('</thead>');

  const mergeRows = table.names.reduce((acc, key) => ({ ...acc, [key]: config.columns?.find(x => x.name === key)?.mergeRows || false }), {});

  // Build data part
  html.push('<tbody>')
  for (const [rowNumber, row] of table.data.entries()) {
    html.push('<tr>');
    for (const [colNumber, cell] of row.entries()) {
      const colName = table.names[colNumber];
      let count = undefined;
      let output = true;
      if (mergeRows[colName]) {
        if (rowNumber === 0 || table.columns[colName][rowNumber - 1] !== cell) {
          count = 0;
          const restOfCol = table.columns[colName].slice(rowNumber);
          for (const [i, v] of restOfCol.entries()) {
            if (v !== cell) break;
            count++;
          }
        } else {
          output = false;
        }
      };
      const rowSpan = count ? 'rowspan=' + count : '';
      const cellText = (isNaN(cell) && ['float'].includes(table.types[colNumber])) ? '' : cell;
      const { align, heatmap, scale = 'Viridis', min, max } = config.columns?.find(x => x.name === colName) || {};
      let heatMapStyle = '';
      if (heatmap && !isNaN(cell)) {
        const background = colourScales.getColourFromScale(scale, cell, min, max);
        const textCol = (new Colour(background)).text;
        heatMapStyle = `background: ${background}; color: ${textCol};`;
      }
      const style = `style="
      ${ align ? 'text-align: ' + align + ';' : ''}
      ${ heatMapStyle }
      "`;
      if (output) html.push(`<td ${rowSpan} ${style}>${cellText}</td>`)
    }
    html.push('</tr>');
  }
  html.push('</tbody>')
  html.push('</table>')

  // Join the array
  return html.join('\n');
}
