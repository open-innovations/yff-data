import { Colours, Colour } from '/oi/colour.js';

export const css = `
  table { border-collapse: collapse; width: 100%; overflow-x: scroll; display: block; }
  th { border: 0; font-weight: bold; }
  td { border: 1px solid black; }
  td:first-child { border-left: 0; }
  td:last-child { border-right: 0; }
  td, th { padding: 1rem; }
`;

const colourScales = new Colours({
  'Viridis': 'rgb(122,76,139) 0%, rgb(124,109,168) 12.5%, rgb(115,138,177) 25%, rgb(107,164,178) 37.5%, rgb(104,188,170) 50%, rgb(133,211,146) 62.5%, rgb(189,229,97) 75%, rgb(254,240,65) 87.5%, rgb(254,240,65) 100%',
  'Heat': 'rgb(0,0,0) 0%, rgb(128,0,0) 25%, rgb(255,128,0) 50%, rgb(255,255,128) 75%, rgb(255,255,255) 100%',
  'Planck': 'rgb(0,0,255) 0%, rgb(0,112,255) 16.666%, rgb(0,221,255) 33.3333%, rgb(255,237,217) 50%, rgb(255,180,0) 66.666%, rgb(255,75,0) 100%',
  'Plasma': 'rgb(12,7,134) 0%, rgb(82,1,163) 12.5%, rgb(137,8,165) 25%, rgb(184,50,137) 37.5%, rgb(218,90,104) 50%, rgb(243,135,72) 62.5%, rgb(253,187,43) 75%, rgb(239,248,33) 87.5%',
  'YFF': 'rgb(99,190,123) 0%, rgb(250,233,131) 50%, rgb(248,105,107) 100%'
});

function loadDataFile(path, sources) {
  const name = path.replace(/\//g, '.').replace(/^.*data/, 'sources').replace(/\.[^\.]*$/, '');
  return eval(name);
}

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
