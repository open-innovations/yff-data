import { colourScales, Colour } from '/oi/colour.js';
import { loadDataFile } from '/oi/util.js';

export const css = `
  .table-holder { display: block; overflow-x: auto; }
  table { border-collapse: collapse; width: 100%; }
  th { border: 0; font-weight: bold; }
  td { border: 1px solid black; }
  td:first-child { border-left: 0; }
  td:last-child { border-right: 0; }
  td, th { padding: 0.25em; }
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
  html.push('<div class="table-holder"><table>');

  // Build header cells
  html.push('<thead>');
/* Giles' code
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
  const mergeRows = table.names.reduce((acc, key) => ({ ...acc, [key]: config.columns?.find(x => x.name === key)?.mergeRows || false }), {});
  */

	var r,c,c1,m,label,cspan,rspan,r2,c2,n;

	// Create 2D array of cells to mimic header/body cells
	var done = {'data':[],'head':[]};
	for(r = 0; r < table.header.length; r++){
		done.head[r] = [];
		for(c = 0; c < config.columns.length; c++) done.head[r][c] = false;
	}
	for(r = 0; r < table.data.length; r++){
		done.data[r] = [];
		for(c = 0; c < config.columns.length; c++) done.data[r][c] = false;
	}

	// Build header cells
	// For each row of the headers we will work out if we need to merge
	for(r = 0; r < table.header.length; r++){
		html.push('<tr>');
		for(c = 0; c < config.columns.length; c++){
			c1 = table.colnum[config.columns[c].name];
			m = 1;
			// Get the label for the header cell
			label = table.header[r][c1]||"";
			// If the column hasn't been processed we see how many of the subsequent columns need merging
			if(!done.head[r][c]){
				done.head[r][c] = true;
				cspan = 1;
				rspan = 1;
				if(config.columns[c].rename){
					// If we are renaming the column we don't want to process any of the other header rows in this column.
					label = config.columns[c].rename;
					// Set the rest of rows in this column to done
					for(r2 = r+1; r2 < table.header.length; r2++){
						done.head[r2][c] = true;
						rspan++;
					}
					for(n = c+1; n < config.columns.length; n++){
						c2 = table.colnum[config.columns[n].name];
						if(table.names[c1]==table.names[c2]){
							done.head[r][n] = true;
							cspan++;
						}else{
							break;
						}
					}
					
				}else{
				
					if(typeof c1==="number"){
						for(n = c+1; n < config.columns.length; n++){
							c2 = table.colnum[config.columns[n].name];
							if(table.header[r][c1]==table.header[r][c2]){
								done.head[r][n] = true;
								cspan++;
							}else{
								break;
							}
						}
					}
				}
				html.push('<th'+(cspan > 1 ? ' colspan="'+cspan+'"':'')+(rspan > 1 ? ' rowspan="'+rspan+'"':'')+(config.columns[c].width ? ' width="'+config.columns[c].width+'"':'')+'>'+label.replace(/\n/g,"<br />")+'</th>');
			}
		}
		html.push('</tr>');
	}

  html.push('</thead>');

  // Giles' code: const mergeRows = table.names.reduce((acc, key) => ({ ...acc, [key]: config.columns?.find(x => x.name === key)?.mergeRows || false }), {});
  // Build data part
  html.push('<tbody>');
/* Giles' code
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
*/
	// Find the min/max values of a column (as a fallback if none provided)
	var min,max,bg,col;

	for(c = 0; c < config.columns.length; c++){
		c2 = table.colnum[config.columns[c].name];
		if(table.types[c2]=="integer" || table.types[c2]=="float"){
			min = 1e100;
			max = -1e100;
			for(r = 0; r < table.data.length; r++){
				if(typeof table.data[r][c2]==="number"){
					min = Math.min(min,table.data[r][c2]);
					max = Math.max(max,table.data[r][c2]);
				}
			}
			if(typeof config.columns[c].min!="number") config.columns[c].min = min;
			if(typeof config.columns[c].max!="number") config.columns[c].max = max;
		}
	}

	// Loop over rows
	for(r = 0; r < table.data.length; r++){
		html.push('<tr>');
		for(c = 0; c < config.columns.length; c++){
			// Get index of column in the data structure
			c2 = table.colnum[config.columns[c].name];
			m = 0;
			// If this is a merging column we work out how many rows to merge
			if(config.columns[c].mergerows){
				m = 1;
				for(r2 = r+1; r2 < table.data.length; r2++){
					if(table.data[r][c2]==table.data[r2][c2]){
						done.data[r2][c2] = true;
						m++;
					}else{
						r2 = table.data.length;
					}
				}
			}

			if(!done.data[r][c2]){
				html.push('<td'+(m > 1 ? ' rowspan="'+m+'"':'')+' style="');
				html.push(config.columns[c].align ? 'text-align:'+config.columns[c].align+';':'');
				var v = table.data[r][c2];
				if(config.columns[c].heatmap && typeof v=="number"){
					if(!isNaN(v)){
						bg = colourScales.getColourFromScale(config.columns[c].scale||'Viridis',table.data[r][c2],config.columns[c].min,config.columns[c].max);
						html.push('background:'+bg+';');
						col = new Colour(bg);
						html.push('color:'+col.text+';');
					}else{
						v = "";
					}
				}
				html.push('">'+(typeof v=="undefined" ? "" : v)+'</td>');
			}
		}
		html.push('</tr>');
	}
  html.push('</tbody>')
  html.push('</table></div>')

  // Join the array
  return html.join('\n');
}
