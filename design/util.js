/**
 * CSVToArray parses any String of Data including '\r' '\n' characters,
 * and returns an array with the rows of data.
 * @param {String} CSV_string - the CSV string you need to parse
 * @param {String} delimiter - the delimeter used to separate fields of data
 * @returns {Array} rows - rows of CSV where first row are column headers
 */
function CSVToArray (CSV_string, delimiter) {
	delimiter = (delimiter || ","); // user-supplied delimeter or default comma

	var pattern = new RegExp( // regular expression to parse the CSV values.
		( // Delimiters:
			"(\\" + delimiter + "|\\r?\\n|\\r|^)" +
			// Quoted fields.
			"(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +
			// Standard fields.
			"([^\"\\" + delimiter + "\\r\\n]*))"
		), "gi"
	);

	var rows = [[]];  // array to hold our data. First row is column headers.
	// array to hold our individual pattern matching groups:
	var matches = false; // false if we don't find any matches
	// Loop until we no longer find a regular expression match
	while (matches = pattern.exec( CSV_string )) {
		var matched_delimiter = matches[1]; // Get the matched delimiter
		// Check if the delimiter has a length (and is not the start of string)
		// and if it matches field delimiter. If not, it is a row delimiter.
		if (matched_delimiter.length && matched_delimiter !== delimiter) {
			// Since this is a new row of data, add an empty row to the array.
			rows.push( [] );
		}
		var matched_value;
		// Once we have eliminated the delimiter, check to see
		// what kind of value was captured (quoted or unquoted):
		if (matches[2]) { // found quoted value. unescape any double quotes.
			matched_value = matches[2].replace(
				new RegExp( "\"\"", "g" ), "\""
			);
		} else { // found a non-quoted value
			matched_value = matches[3];
		}
		// Now that we have our value string, let's add
		// it to the data array.
		rows[rows.length - 1].push(matched_value);
	}
	return rows; // Return the parsed data Array
}

// Function to parse a CSV file and return a JSON structure
// Guesses the format of each column based on the data in it.
function CSV2JSON(data,start,end){
	// Version 1.1

	// If we haven't sent a start row value we assume there is a header row
	if(typeof start!=="number") start = 1;
	// Split by the end of line characters
	if(typeof data==="string") data = CSVToArray(data);
	// The last row to parse
	if(typeof end!=="number") end = data.length;
	for(var i = start; i < data.length; i++){
		if(data[i][0]=="---"){
			start = i;
			// Remove header spacer row
			data.splice(i,1);
			continue;
		}
	}

	if(end > data.length){
		// Cut down to the maximum length
		end = data.length;
	}

	var line,datum,header,types;
	var newdata = [];
	var rowdata = [];
	var coldata = {};
	var headers = [];
	var formats = [];
	var req = [];
	
	var j,i,k,rows;

	// Build the header names by concatenating header rows with a "."
	for(i = 0, rows = 0 ; i < start; i++) headers[i] = clone(data[i]);
	names = new Array(headers[0].length);
	for(j = 0; j < names.length; j++){
		names[j] = "";
		for(i = 0; i < headers.length; i++) names[j] += (names[j] && headers[i][j] ? '.':'')+headers[i][j];
		coldata[names[j]] = new Array(end-start);
	}

	for(i = start, rows = 0 ; i < end; i++, rows++){

		// If there is no content on this line we skip it
		if(data[i] == "") continue;

		line = data[i];

		dat = {};
		datum = new Array(line.length);
		types = new Array(line.length);
		
		rowdata[rows] = {};

		// Loop over each column in the line
		for(j=0; j < line.length; j++){

			// Replace undefined values with empty strings
			if(typeof line[j]==="undefined") line[j] = "";

			// Remove any quotes around the column value
			datum[j] = (line[j][0]=='"' && line[j][line[j].length-1]=='"') ? line[j].substring(1,line[j].length-1) : line[j];

			// If the value parses as a float
			if(typeof parseFloat(datum[j])==="number" && parseFloat(datum[j]) == datum[j]){
				types[j] = "float";
				// Check if it is actually an integer
				if(typeof parseInt(datum[j])==="number" && parseInt(datum[j])+"" == datum[j]){
					types[j] = "integer";
					// If it is an integer and in the range 1700-2100 we'll guess it is a year
					if(datum[j] >= 1700 && datum[j] < 2100) types[j] = "year";
				}
				datum[j] = parseFloat(datum[j]);
			}else if(datum[j].search(/^(true|false)$/i) >= 0){
				// The format is boolean
				types[j] = "boolean";
			}else if(datum[j].search(/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)/) >= 0){
				// The value looks like a URL
				types[j] = "URL";
			}else if(!isNaN(Date.parse(datum[j]))){
				// The value parses as a date
				types[j] = "datetime";
			}else{
				// Default to a string
				types[j] = "string";
				// If the string value looks like a time we set it as that
				if(datum[j].search(/^[0-2]?[0-9]\:[0-5][0-9]$/) >= 0) types[j] = "time";
			}
			if(names[j]){
				rowdata[rows][names[j]] = datum[j];
				coldata[names[j]][rows] = datum[j];
			}
		}
		newdata[rows] = datum;
		formats[rows] = types;
	}

	// Now, for each column, we sum the different formats we've found
	var format = new Array(names.length);
	for(j = 0; j < names.length; j++){
		var count = {};
		var empty = 0;
		for(i = 0; i < newdata.length; i++){
			if(!newdata[i][j]) empty++;
		}
		for(i = 0 ; i < formats.length; i++){
			if(!count[formats[i][j]]) count[formats[i][j]] = 0;
			count[formats[i][j]]++;
		}
		var mx = 0;
		var best = "";
		for(k in count){
			if(count[k] > mx){
				mx = count[k];
				best = k;
			}
		}
		// Default
		format[j] = "string";

		// If more than 80% (arbitrary) of the values are a specific format we assume that
		if(mx > 0.8*newdata.length) format[j] = best;

		// If we have a few floats in with our integers, we change the format to float
		if(format[j] == "integer" && count.float > 0.1*newdata.length) format[j] = "float";

		req.push(names[j] ? true : false);
	}

	// Data structure will include the following:
	//   headers = 2d array of headers
	//   names = column names (rows concatenated)
	//   data = 2d array of data
	//   rows = array of objects with data referenced by name
	//   columns = object with column data as array
	return { 'names': names, 'format': format, 'data': newdata, 'headers':headers, 'rows':rowdata,'columns':coldata };
}
// Function to clone a hash otherwise we end up using the same one
function clone(hash) {
	var json = JSON.stringify(hash);
	var object = JSON.parse(json);
	return object;
}
function buildTable(txt,config){
	var r,r2,c,c2,i,j,html,csv,done = {'data':[],'head':[]},align = {},columns = [];

	csv = CSV2JSON(txt);

	if(!config.columns) config.columns = [];
	for(c = 0; c < csv.names.length; c++){
		j = -1;
		for(i = 0; i < config.columns.length; i++){
			if(csv.names[c]==config.columns[i].name) j = i;
		}
		columns[c] = (j >= 0) ? config.columns[j] : {};
	}
	html = '<table>';

	// Create 2D array of cells
	for(r = 0; r < csv.data.length; r++){
		done.data[r] = [];
		for(c = 0; c < csv.data[r].length; c++) done.data[r][c] = false;
	}
	for(r = 0; r < csv.headers.length; r++){
		done.head[r] = [];
		for(c = 0; c < csv.headers[r].length; c++) done.head[r][c] = false;
	}

	// Build header cells
	for(r = 0; r < csv.headers.length; r++){
		html += '<tr>';
		for(c = 0; c < csv.headers[r].length; c++){
			// Work out how many columns to merge
			m = 1;
			for(c2 = c+1; c2 < csv.headers[r].length; c2++){
				if(csv.headers[r][c]!=csv.headers[r][c2]) break;
				done.head[r][c2] = true;
				m++;
			}
			if(!done.head[r][c]) html += '<th'+(m > 1 ? ' colspan="'+m+'"':'')+'>'+csv.headers[r][c]+'</th>';
		}
		html += '</tr>';
	}
	var min,max;
	for(c = 0; c < columns.length; c++){
		if(csv.format[c]==="integer" || csv.format[c]==="float"){
			min = 1e100;
			max = -1e100;
			for(r = 0; r < csv.data.length; r++){
				if(typeof csv.data[r][c]==="number"){
					min = Math.min(min,csv.data[r][c]);
					max = Math.max(max,csv.data[r][c]);
				}
			}
			if(typeof columns[c].min!=="number") columns[c].min = min;
			if(typeof columns[c].max!=="number") columns[c].max = max;
		}
	}
	// Loop over rows
	for(r = 0; r < csv.data.length; r++){
		html += '<tr>';
		for(c = 0; c < columns.length; c++){
			m = 0;
			// If this is a merging column we work out how many rows to merge
			if(columns[c].mergerows){
				m = 1;
				for(r2 = r+1; r2 < csv.data.length; r2++){
					if(csv.data[r][c]!=csv.data[r2][c]) break;
					done.data[r2][c] = true;
					m++;
				}
			}
			if(!done.data[r][c]){
				html += '<td'+(m > 1 ? ' rowspan="'+m+'"':'')+' style="';
				html += (columns[c].align ? 'text-align:'+columns[c].align+';':'');
				if(columns[c].heatmap && typeof csv.data[r][c]==="number"){
					bg = colours.getColourFromScale(columns[c].scale||'Viridis',csv.data[r][c],columns[c].min,columns[c].max);
					html += 'background:'+bg+';';
					col = new Colour(bg);
					html += 'color:'+col.text+';';
				}
				html += '">'+csv.data[r][c]+'</td>';
			}
		}
		html += '</tr>';
	}
	html += '</table>';
	return html;

}
