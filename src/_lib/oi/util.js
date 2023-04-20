import { colours } from '/src/_data/colours.js';
import { Colour, ColourScale } from 'local/oi/colours.js';

export function transpose(matrix) {
  return matrix[0].map((_, colIndex) => matrix.map(row => row[colIndex]));
}

export function range(array) {
  return {
    min: Math.min(...array.filter(x => x)),
    max: Math.max(...array.filter(x => x)),
  };
}

/**
 * unction to resolve data from a given context
 *
 * @param ref dot-separated reference to the dataset
 * @param context the context in which to search for the data
 * @returns
 */
export function resolveData(
  ref,
  context,
) {
  // Initialise the result to be the whole context.
  // If we provide no key, we should return the whole thing!
  let result = context;
  // Split the ref by the '.' character and iterate over the resulting array
  for (const key of ref.split('.')) {
    result = result[key];
  }
  return result;
}

export function mapPotentiallyFakePath(path) {
  if (path.match('/')) { // Assume that this is a fake path
    // So map to the sources data element
    return path.replace(/\//g, '.').replace(/^.*?data/, 'sources').replace(/\.[^\.]*$/, '');
  }
  return path;
}

export function loadDataFile(path, context) {
  let config;

	if(typeof path==="object"){
		config = path;
		path = path.file;
	}
  const name = mapPotentiallyFakePath(path);
	let data = structuredClone(resolveData(name, context));
	
	if(typeof config==="object"){
		data = augmentTable(config,data);
	}
	
	return data;
}

// Add some extra filters for templates:
//   toFixed(n)
//   multiply(n)
//   toLocaleString()
//   colourScale(scale,min,max) - this let's us get a colour to, for example, use as a background style
//   contrastColour - find the most contrasting colour so that, for example, we can contrast the text colour
export function applyReplacementFilters(value,options) {

	var c,r,v,col,nc,h,bits,p1,rtn,b,scale,min,max,colour;

	// For each {{ value }} we will parse it to see if we recognise it
	value = value.replace(/\{\{ *([^\}]+) *\}\}/g,function(m,p1){

		// Remove a trailing space
		p1 = p1.replace(/ $/g,"");

		// Split by pipes
		bits = p1.split(/ \| /);

		// The value is the first part
		p1 = bits[0];

		if(options.table){
			// Log a warning if the column doesn't exist
			if(!options.table.columns[p1] && options.r==0) console.warn('No column '+p1+' appears to exist in the table '+config.file);

			// Get the value from the table if one exists
			p1 = (options.table.columns[p1] ? options.table.columns[p1][options.r] : "");
		}

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

			// colourScale(scale,min,max)
			rtn = bits[b].match(/colourScale\([\"\']([^\"]+)[\"\']([^\)]*)\)/);
			if(p1 && rtn){
				min = 0;
				max = 0;
				scale = rtn[1]||"Viridis";
				if(rtn[2]){
					rtn = rtn[2].match(/^\,([0-9\.\-\+]*) ?\,([0-9\.\-\+]*)/);
					if(rtn.length > 1){
						min = parseFloat(rtn[1]);
						max = parseFloat(rtn[2]);
					}
				}
				// Get the ColourScale from either:
				// string - a key referencing a scale
				// object:
				//     function: 'round'
				//     stops:
				//         - { value: 0, colour: name1 }
				//         - { value: 50, colour: name2 }
				//         - { value: 100, colour: name3 }
				var scaleObj = scales[(scales[scale] ? config.columns[c].scale : 'Viridis')];

				// Find the background colour
				p1 = scaleObj(parseFloat(p1),min,max);

			}

			// colour()
			rtn = bits[b].match(/colour\(\)/);
			if(p1 && rtn) p1 = (colours[p1]||p1);

			// colour(name)
			rtn = bits[b].match(/colour\([\"\']([^\"]+)[\"\']\)/);
			if(p1 && rtn){
				colour = rtn[1]||"";
				p1 = (colours[colour]||"#000000");
			}

			// contrastColour()
			rtn = bits[b].match(/contrastColour\(\)/);
			if(p1 && rtn) p1 = Colour(colours[p1]||p1).contrast;

			// contrastColour(name)
			rtn = bits[b].match(/contrastColour\([\"\']([^\"]+)[\"\']\)/);
			if(p1 && rtn){
				p1 = Colour(colours[p1]||p1).contrast;
			}
			
		}

		return p1;
	});

	return value;
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

					v = applyReplacementFilters(config.columns[c].template,{'table':table,'r':r});

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

/**
 * This is not a pure function
 * 
 * @param obj1 
 * @param obj2 
 * @returns 
 */
export function mergeDeep( obj1, obj2) {
  for (const p in obj2) {
    try {
      if (obj2[p].constructor == Object) obj1[p] = mergeDeep(obj1[p], obj2[p]);
      else obj1[p] = obj2[p];
    } catch (e) {
      obj1[p] = obj2[p];
    }
  }
  return obj1;
}
