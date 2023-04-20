import { colours, scales } from '/src/_data/colours.js';
import { Colour, ColourScale } from 'local/oi/colours.js';
import { loadDataFile } from '/src/_lib/oi/util.js';

export const css = `
  .table-holder { display: block; overflow-x: auto; }
  table { border-collapse: collapse; width: 100%; }
  th { border: 0; font-weight: bold; }
  td { border: 1px solid black; }
  td:first-child { border-left: 0; }
  td:last-child { border-right: 0; }
  td, th { padding: 0.25em; }
`;

export default (context) => {
  const { config } = context;
  // Get loaded data from sources object
  // Data structure will include the following:
  //   headers = 2d array of headers
  //   names = column names (rows concatenated)
  //   data = 2d array of data
  //   rows = array of objects with data referenced by name
  //   columns = object with column data as array
  let table = loadDataFile(config, context);

  // Create array to store html text
  const html = [];
  // Start table
  html.push('<div class="table-holder"><table>');

  // Build header cells
  html.push('<thead>');

	var r,c,c1,m,label,cspan,rspan,r2,c2,n;

	// Create 2D array of cells mimicing header/body cells
	// Each array element stores if we've processed this cell
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

		// For each of the columns in the config
		for(c = 0; c < config.columns.length; c++){

			// Get the column number of this column in the data table
			c1 = table.colnum[config.columns[c].name];

			// The number of cells to merge horizontally
			m = 1;

			// Get the label for the header cell
			label = table.header[r][c1]||"";

			// If the column hasn't been processed we see how many of the subsequent columns need merging
			if(!done.head[r][c]){

				// Set it to processed
				done.head[r][c] = true;

				// The column/row spanning
				cspan = 1;
				rspan = 1;

				// If we are renaming the column we don't want to process any of the other header rows in this column.
				if(config.columns[c].rename){

					// The label is set to the rename value
					label = config.columns[c].rename;

					// Set the rest of rows in this column to done
					for(r2 = r+1; r2 < table.header.length; r2++){
						done.head[r2][c] = true;
						rspan++;	// Increment the row span value
					}

					// Loop over subsequent columns
					for(n = c+1; n < config.columns.length; n++){

						// Find the column number of the next named column
						c2 = table.colnum[config.columns[n].name];

						// If the value in the first column equals this next one we mark this as done and increase the col span value
						if(table.names[c1]==table.names[c2]){
							done.head[r][n] = true;
							cspan++;
						}else{
							break;
						}
					}
					
				}else{
				
					if(typeof c1==="number"){

						// Loop over subsequent columns
						for(n = c+1; n < config.columns.length; n++){

							// Find the column number of the next named column
							c2 = table.colnum[config.columns[n].name];

							// If the value in the first column equals this next one we mark this as done and increase the col span value
							if(table.header[r][c1]==table.header[r][c2]){
								done.head[r][n] = true;
								cspan++;
							}else{
								break;
							}
						}
					}
				}
				// Return the column header cell <th>
				html.push('<th'+(cspan > 1 ? ' colspan="'+cspan+'"':'')+(rspan > 1 ? ' rowspan="'+rspan+'"':'')+(config.columns[c].width ? ' width="'+config.columns[c].width+'"':'')+'>'+label.replace(/\n/g,"<br />")+'</th>');
			}
		}
		html.push('</tr>');
	}

  html.push('</thead>');

  // Build data part
  html.push('<tbody>');

	// Find the min/max values of a column (as a fallback if none provided)
	var min,max,bg,col,sty,txt,scale;

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

	// Loop over each row
	for(r = 0; r < table.data.length; r++){

		html.push('<tr>');

		// Loop over the columns
		for(c = 0; c < config.columns.length; c++){

			// Get index of column in the data structure
			c2 = table.colnum[config.columns[c].name];

			// The number of cells to merge
			m = 1;

			// If this is a merging column we work out how many rows to merge
			if(config.columns[c].mergerows){

				// Loop over subsequent rows checking if the value matches the current one
				for(r2 = r+1; r2 < table.data.length; r2++){
					if(table.data[r][c2]==table.data[r2][c2]){
						done.data[r2][c2] = true;
						m++;
					}else{
						// Break out of the loop
						r2 = table.data.length;
					}
				}
			}

			// If this cell isn't classed as done
			if(!done.data[r][c2]){

				html.push('<td'+(m > 1 ? ' rowspan="'+m+'"':'')+' style="');
				sty = '';
				sty += (config.columns[c].align ? 'text-align:'+config.columns[c].align+';':'');
				var v = table.data[r][c2];
				// If this column has heatmap=true and the value for this cell is a number we will work out the foreground/background colours
				if(config.columns[c].heatmap && typeof v=="number"){
					if(!isNaN(v)){

						// Get the ColourScale from either:
						// string - a key referencing a scale
						// object:
						//     function: 'round'
						//     stops:
						//         - { value: 0, colour: name1 }
						//         - { value: 50, colour: name2 }
						//         - { value: 100, colour: name3 }
						scale = (typeof config.columns[c].scale==="string") ? scales[(scales[config.columns[c].scale] ? config.columns[c].scale : 'Viridis')] : ColourScale(config.columns[c].scale);

						// Find the background colour
						bg = scale(table.data[r][c2],config.columns[c].min,config.columns[c].max);

						// If it is a named colour we'll use that
						if(colours && colours[bg]) bg = colours[bg];

						sty += 'background:'+bg+';';
						sty += 'color:'+ Colour(bg).contrast+';';
					}else{
						v = "";
					}
				}
				html.push(sty+'">'+(typeof v=="undefined" ? "" : v)+'</td>');

			}
		}

		html.push('</tr>');

	}

	html.push('</tbody>')
	html.push('</table></div>')

	// Join the array
	return html.join('\n');
}
