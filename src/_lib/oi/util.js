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

	var c,r,v,col,nc,h;
	// We want to build any custom columns here
	nc = table.names.length;
	if(config.columns){
		for(c = 0; c < config.columns.length; c++){
			if(config.columns[c].template){
				col = config.columns[c];
				table.names.push(col.name);
				table.colnum[col.name] = nc;
				table.columns[col.name] = [];
				table.range[col.name] = undefined;
				for(r = 0; r < table.data.length; r++){
					v = config.columns[c].template.replace(/\{\{ *([^\}]+) *\}\}/g,function(m,p1){
						p1 = p1.replace(/ $/g,"");
						return table.columns[p1][r] || "";
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