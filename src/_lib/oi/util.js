export function transpose(matrix) {
  return matrix[0].map((_, colIndex) => matrix.map(row => row[colIndex]));
}

export function range(array) {
  return {
    min: Math.min(...array.filter(x => x)),
    max: Math.max(...array.filter(x => x)),
  };
}

export function loadDataFile(path, sources) {
	let config,data;

	if(typeof path==="object"){
		config = path;
		path = path.file;
	}
	const name = path.replace(/\//g, '.').replace(/^.*data/, 'sources').replace(/\.[^\.]*$/, '');
	data = eval(name);
	
	if(typeof config==="object"){
		data = augmentTable(config,data);
	}
	
	return data;
}

function augmentTable(config, table){

	var c,r,v,col,nc,h,bits,p1,rtn,b;
	
	// We want to build any custom columns here
	if(config.columns && table.names){
		nc = table.names.length;
		for(c = 0; c < config.columns.length; c++){
			if(config.columns[c].template){
				col = config.columns[c];
				table.names.push(col.name);
				table.colnum[col.name] = nc;
				table.columns[col.name] = [];
				table.range[col.name] = undefined;
				for(r = 0; r < table.data.length; r++){
					v = config.columns[c].template.replace(/\{\{ *([^\}]+) *\}\}/g,function(m,p1){

						// Remove a trailing space
						p1 = p1.replace(/ $/g,"");

						// Split by pipes
						bits = p1.split(/ \| /);

						// The value is the first part
						p1 = bits[0];

						// Log a warning if the column doesn't exist
						if(!table.columns[p1] && r==0) console.warn('No column '+p1+' appears to exist in the table '+config.file);

						// Get the value from the table if one exists
						p1 = (table.columns[p1] ? table.columns[p1][r] : "");

						// Process each filter in turn
						for(b = 1; b < bits.length; b++){

							// toFixed(n)
							rtn = bits[b].match(/toFixed\(([0-9]+)\)/);
							if(p1 && rtn && rtn.length == 2){
								if(typeof p1==="string") p1 = parseFloat(p1);
								p1 = p1.toFixed(rtn[1]);
							}

							// multiply(n)
							rtn = bits[b].match(/multiply\(([0-9\.\-\+]+)\)/);
							if(p1 && rtn && rtn.length == 2){
								if(typeof p1==="string") p1 = parseFloat(p1);
								p1 = p1 * parseFloat(rtn[1]);
							}

							// toLocaleString()
							rtn = bits[b].match(/toLocaleString\(\)/);
							if(p1 && rtn){
								if(typeof p1==="string") p1 = parseFloat(p1);
								p1 = p1.toLocaleString();
							}
						}

						return p1;
					});
					table.columns[col.name].push(v);
					table.data[r].push(v);
					//table.raw[r].push(v);
					table.rows[r][col.name] = v;
				}
				for(h = 0; h < table.header.length; h++) table.header[h].push(h==0 ? col.name : "");
				nc++;
			}
		}
	}
  
	return table;
}