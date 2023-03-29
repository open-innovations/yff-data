import { document } from '/src/_lib/oi/document.ts';
import { loadDataFile } from '/src/_lib/oi/util.js';
import { colourScales, Colour } from '/src/_lib/oi/colour.js';


function clone(a){ return JSON.parse(JSON.stringify(a)); }


// This component uses "/assets/leaflet/leaflet.js" and "/assets/leaflet/leaflet.css" to make things interactive in the browser.
// It will only get included in pages that need it by using the "data-dependencies" attribute.
export function LeafletMap(config,csv){

	this.getHTML = function(){
		var html,i,r,file;

		if(config.geojson.file) file = config.geojson.file;
		else console.error('No GeoJSON file given');

		// Add a colour-scale colour to each row based on the "value" column
		var rows = clone(csv.rows);
		for(r = 0; r < rows.length; r++){
			rows[r].colour = colourScales.getColourFromScale(config.scale||'Viridis',rows[r][config.value],config.min,config.max);
		}

		// Build a legend
		var legend = getLegend(config).replace(/\"/g,'\\"');

		html = ['<div class="map" data-dependencies="/assets/leaflet/leaflet.js,/assets/leaflet/leaflet.css">'];
		
		html.push('<script>');
		html.push('(function(root){');
		html.push('	var p = document.currentScript.parentNode;');
		html.push('	var el = document.createElement("div");');
		html.push('	el.classList.add("leaflet");');
		html.push('	p.appendChild(el);');
		html.push('	var map = L.map(el);');

		// Store the map in an array for the page
		html.push('	if(!root.OI) root.OI = {};\n');
		html.push('	if(!root.OI.maps) root.OI.maps = [];\n');
		
		html.push('	var id = root.OI.maps.length;\n');
		html.push('	root.OI.maps.push({"map":map,"bounds":null});\n');

		if(config.bounds){
			html.push(' OI.maps[id].bounds = [['+config.bounds[0]+'],['+config.bounds[1]+']];');
			html.push('	map.fitBounds([['+config.bounds[0]+'],['+config.bounds[1]+']]);');
		}
		html.push('	L.tileLayer("https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png", { maxZoom: 19, attribution: "Tiles: &copy; OpenStreetMap/CartoDB", subdomains: "abcd" }).addTo(map);');
		html.push('	map.attributionControl.setPrefix("Youth Futures Foundation");\n');
		
		// Create a map label pane so labels can sit above polygons
		html.push('	map.createPane("labels");\n');
		html.push('	map.getPane("labels").style.zIndex = 650;\n');
		html.push('	map.getPane("labels").style.pointerEvents = "none";\n');
		html.push('	L.tileLayer("https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png", {\n');
		html.push('		attribution: "",\n');
		html.push('		pane: "labels"\n');
		html.push('	}).addTo(map);\n');

		// Fetch the GeoJSON file
		// Alternatively we could have loaded it and inserted it here in the page directly
		html.push('	fetch("'+file+'").then(response => {\n');
		html.push('		if(!response.ok) throw new Error("Network response was not OK");\n');
		html.push('		return response.json();\n');
		html.push('	}).then(json => {\n');
		html.push('		var csv = '+JSON.stringify(rows)+';\n');
		html.push('		var geokey = "'+config.geojson.key+'";\n');
		html.push('		var key = "'+config.key+'";\n');

		// A function to return the row for a given key
		html.push('		function getData(k){\n');
		html.push('			for(var i = 0; i < csv.length; i++){\n');
		html.push('				if(csv[i][key] == k) return csv[i];\n');
		html.push('			}\n');
		html.push('			return {};\n');
		html.push('		}\n');

		// A function to style each GeoJSON feature
		html.push('		function style(feature){\n');
		html.push('			var d = getData(feature.properties[geokey]);\n');
		html.push('			return {\n');
		html.push('				weight: 0.5,\n');
		html.push('				opacity: 0.5,\n');
		html.push('				color: "#ffffff",\n');
		html.push('				fillOpacity: 1,\n');
		html.push('				fillColor: d.colour||"transparent"\n');
		html.push('			};\n');
		html.push('		}\n');

		// Add the GeoJSON to the map
		html.push('		var geoattrs = { "style": style };\n');
		html.push('		geoattrs.onEachFeature = function(feature, layer){\n');
		html.push('			var d = getData(feature.properties[geokey]);\n');
		html.push('			layer.bindPopup(d["Label"]||feature.properties[geokey]).on("popupopen",function(ev){\n');
		html.push('				var ps = ev.popup._container;\n');
		// Set the background colour of the popup
		html.push('				ps.querySelector(".leaflet-popup-content-wrapper").style["background-color"] = d.colour;\n');
		html.push('				ps.querySelector(".leaflet-popup-tip").style["background-color"] = d.colour;\n');
		// Set the text colour of the popup
		html.push('				ps.querySelector(".leaflet-popup-content-wrapper").style["color"] = OI.contrastColour(d.colour);\n');
		html.push('				ps.style["color"] = OI.contrastColour(d.colour);\n');
		html.push('			});\n');
		html.push('		};\n');
					
		html.push('		var geo = L.geoJSON(json,geoattrs);\n');
		html.push('		geo.addTo(map);\n');
		html.push('		OI.maps[id].bounds = geo.getBounds();\n');
		if(!config.bounds) html.push('		map.fitBounds(geo.getBounds());\n');

		if(config.legend){
			// Create the legend and add it to the map
			html.push('		var legend = L.control({position: "'+((config.legend.position||"bottom right").replace(/ /g,""))+'"});\n');
			html.push('		legend.onAdd = function (map){\n');
			html.push('			var div = L.DomUtil.create("div", "info legend");\n');
			html.push('			div.innerHTML = "'+legend+'";\n');
			html.push('			return div;\n');
			html.push('		}\n');
			html.push('		legend.addTo(map);\n');
		}

		html.push('	}).catch(error => {\n');
		html.push('		console.error("Unable to load the data",error);\n');
		html.push('	});\n');


		html.push('})(window || this);\n');
		html.push('</script>\n');

		html.push('</div>\n');

		return html.join('');
	};
	return this;
}

// This component creates a hex map layout
export function HexMap(config,csv,sources){

	var el = document.createElement('div');
	this.container = el;
	el.innerHTML = "";
	setAttr(this.container,{'style':'overflow:hidden'});

	let range = {};
	this.w = (config.width || 1200);
	this.h = (config.height || 675);
	this.attr = config;
	const fs = config['font-size'] || 17;

	this.style = {
		'default': { 'fill': '#cccccc', 'fill-opacity': 1, 'font-size': fs, 'stroke-width': 1.5, 'stroke-opacity': 1, 'stroke': '#ffffff' },
		'highlight': { 'fill': '#1DD3A7' },
		'grid': { 'fill': '#aaa', 'fill-opacity': 0.1 }
	};

	if(!config.hexjson.file){
		console.error('No HexJSON file given');
		return this;
	}

	// Create the SVG element
	let svg = svgEl('svg');
	setAttr(svg,{'xmlns':'http://www.w3.org/2000/svg','version':'1.1','viewBox':'0 0 '+this.w+' '+this.h,'overflow':'visible','style':'max-width:100%;max-height:100%;background:'+(config.background||"transparent"),'preserveAspectRatio':'xMidYMid meet'});
	svg.innerHTML = "";
	svg.setAttribute('data-type','hex-map');

	// Create a group which has a class list data-layer so that the interactive JS can find it
	let group = svgEl('g');
	group.classList.add('data-layer');
	add(group,svg);

	this.areas = {};

	let min = 0;
	let max = 1;
	// Set min/max to the range for the value column
	if(config.value && csv.range[config.value]) min = csv.range[config.value].min;
	if(config.value && csv.range[config.value]) max = csv.range[config.value].max;
	// Override min/max if provided in config
	if(typeof config.min==="number") min = config.min;
	if(typeof config.max==="number") max = config.max;


	this.getHTML = function(){

		var html = ['<div class="map hex-map" data-dependencies="/assets/js/svg-map.js">'];

		html.push(svg.outerHTML);

		// Create the legend
		var legend = buildLegend(config);
		html.push(legend.outerHTML);

		html.push('</div>\n');

		return html.join('');
	};
	this.init = function(){
		// Get the contents of the HexJSON file
		var hexjson = loadFromSources(config.hexjson.file,sources);
		
		// Process the HexJSON
		this.setMapping(hexjson);
		return this;
	};
	this.setMapping = function (mapping){
		let region, p, s;
		this.mapping = mapping;

		if(!this.properties) this.properties = { "x": 100, "y": 100 };
		p = mapping.layout.split("-");
		this.properties.shift = p[0];
		this.properties.orientation = p[1];

		range = { 'r': { 'min': Infinity, 'max': -Infinity }, 'q': { 'min': Infinity, 'max': -Infinity } };
		for(region in this.mapping.hexes){
			if(this.mapping.hexes[region]){
				p = updatePos(this.mapping.hexes[region].q, this.mapping.hexes[region].r, this.mapping.layout);
				if (p.q > range.q.max) range.q.max = p.q;
				if (p.q < range.q.min) range.q.min = p.q;
				if (p.r > range.r.max) range.r.max = p.r;
				if (p.r < range.r.min) range.r.min = p.r;
			}
		}
		// Find range and mid points
		range.q.d = range.q.max - range.q.min;
		range.r.d = range.r.max - range.r.min;
		range.q.mid = range.q.min + range.q.d / 2;
		range.r.mid = range.r.min + range.r.d / 2;
		this.range = clone(range);
		
		if(this.properties.orientation == "r") s = Math.min(0.5 * this.h / (range.r.d * 0.75 + 1), (1 / Math.sqrt(3)) * this.w / (range.q.d + 1));	// Pointy-topped
		else s = Math.min((1 / Math.sqrt(3)) * this.h / (range.r.d + 1), 0.5 * this.w / (range.q.d * 0.75 + 1));	// Flat-topped

		if(typeof config.size !== "number"){
			if (typeof s !== "number") s = 10;
			s = Math.round(100 * s) / 100;
			config.size = s;
			this.properties.size = s;	
		}
		this.properties.s = { 'cos': Math.round(10 * this.properties.size * Math.sqrt(3) / 2) / 10, 'sin': this.properties.size * 0.5 };
		this.properties.s.c = this.properties.s.cos.toFixed(2);
		this.properties.s.s = this.properties.s.sin.toFixed(2);

		return this.draw();
	};

	// Create an object for the q,r coordinates that contains:
	// array: <array> - the path for the hexagon as an array
	// path: <string> - the path for the hexagon as a string
	// x: <number> - the x position of the hexagon
	// y: <number> - the y position of the hexagon
	this.drawHex = function (q, r) {
		if(this.properties){
			let x, y;
			const cs = this.properties.s.cos;
			const ss = this.properties.s.sin;

			const p = updatePos(q, r, this.mapping.layout);

			if(this.properties.orientation == "r"){
				// Pointy topped
				x = (this.w / 2) + ((p.q - this.range.q.mid) * cs * 2);
				y = (this.h / 2) - ((p.r - this.range.r.mid) * ss * 3);
			}else{
				// Flat topped
				x = (this.w / 2) + ((p.q - this.range.q.mid) * ss * 3);
				y = (this.h / 2) - ((p.r - this.range.r.mid) * cs * 2);
			}
			x = parseFloat(x.toFixed(1));
			const path = [['M', [x, y]]];
			if(this.properties.orientation == "r"){
				// Pointy topped
				path.push(['m', [cs, -ss]]);
				path.push(['l', [0, 2 * ss, -cs, ss, -cs, -ss, 0, -2 * ss, cs, -ss, cs, ss]]);
				path.push(['z', []]);
			}else{
				// Flat topped
				path.push(['m', [-ss, cs]]);
				path.push(['l', [2 * ss, 0, ss, -cs, -ss, -cs, -2 * ss, 0, -ss, cs]]);
				path.push(['z', []]);
			}
			return { 'array': path, 'path': toPath(path), 'x': x, 'y': y };
		}
		return this;
	};

	this.draw = function () {
		let r, q, h, region;

		const range = this.range;
		for (region in this.mapping.hexes) {
			if (this.mapping.hexes[region]) {
				q = this.mapping.hexes[region].q;
				r = this.mapping.hexes[region].r;
				if (q > range.q.max) range.q.max = q;
				if (q < range.q.min) range.q.min = q;
				if (r > range.r.max) range.r.max = r;
				if (r < range.r.min) range.r.min = r;
			}
		}

		// Add padding to range
		range.q.min -= this.padding;
		range.q.max += this.padding;
		range.r.min -= this.padding;
		range.r.max += this.padding;

		// q,r coordinate of the centre of the range
		const qp = (range.q.max + range.q.min) / 2;
		const rp = (range.r.max + range.r.min) / 2;

		this.properties.x = (this.w / 2) - (this.properties.s.cos * 2 * qp);
		this.properties.y = (this.h / 2) + (this.properties.s.sin * 3 * rp);

		// Store this for use elsewhere
		this.range = clone(range);

		let path, colour, title, hexid;

		let style = clone(this.style['default']);
		style['class'] = 'hex-cell';

		for(r in this.mapping.hexes){
			if(this.mapping.hexes[r]){

				h = this.drawHex(this.mapping.hexes[r].q, this.mapping.hexes[r].r);

				// Create a <path> for the hexagon outline
				path = svgEl('path');

				// Create a <title> to go inside the path - gives us tooltips by default
				title = svgEl('title');

				// Set the default for the title to the name in the HexJSON or the ID of the hex
				title.innerHTML = (this.mapping.hexes[r].n || r);

				// Add the <title> to the <path>
				add(title,path);

				// Define the path and some properties
				setAttr(path, { 'd': h.path, 'class': 'hex-cell', 'transform-origin': h.x + 'px ' + h.y + 'px', 'data-q': this.mapping.hexes[r].q, 'data-r': this.mapping.hexes[r].r });

				// Apply more styles to the path
				setAttr(path, style);

				// Add the path to the data-layer group
				group.appendChild(path);

				// Keep the DOM elements for this hex to use later
				this.areas[r] = { 'hex': path, 'data': this.mapping.hexes[r], 'orig': h, 'title': title };

				// We need to update the hex's colour and title.
				// First check if we have key/value columns.
				if(config.key && csv.columns[config.key] && config.value && csv.columns[config.value]){

					// Loop over the rows in the CSV to check each one
					for(var i = 0; i < csv.rows.length; i++){

						hexid = r;
						if(config.hexjson.key && this.mapping.hexes[r][config.hexjson.key]) hexid = this.mapping.hexes[r][config.hexjson.key];

						// If the CSV row matches the hexagon key
						if(csv.rows[i][config.key]==hexid){

							// Update the colour of the hexagon
							colour = colourScales.getColourFromScale(config.scale||'Viridis',csv.rows[i][config.value],min,max);
							setAttr(this.areas[r].hex,{'fill':colour,'data-value':csv.rows[i][config.value]});

							// Update the title for the hexagon
							if(config.label && csv.columns[config.label]) title.innerHTML = csv.rows[i][config.label];
						}

					}
				}

				// Apply some styles/colours to the hexagon
				setAttr(this.areas[r].hex, { 'stroke': this.style['default'].stroke, 'stroke-opacity': this.style['default']['stroke-opacity'], 'stroke-width': this.style['default']['stroke-width'], 'title': this.mapping.hexes[r].n, 'data-regions': r, 'style': 'cursor: pointer;' });
			}
		}

		return this;
	};
	function updatePos(q, r, layout) {
		if (layout == "odd-r" && (r % 2) != 0) q += 0.5;	// "odd-r" horizontal layout shoves odd rows right
		if (layout == "even-r" && (r % 2) == 0) q += 0.5; // "even-r" horizontal layout shoves even rows right
		if (layout == "odd-q" && (q % 2) != 0) r += 0.5;	// "odd-q" vertical layout shoves odd columns down
		if (layout == "even-q" && (q % 2) == 0) r += 0.5; // "even-q" vertical layout shoves even columns down
		return { 'q': q, 'r': r };
	}
	function toPath(p) {
		let str = '';
		for (let i = 0; i < p.length; i++) str += ((p[i][0]) ? p[i][0] : ' ') + (p[i][1].length > 0 ? p[i][1].join(',') : ' ');
		return str;
	}

	return this.init();
}

// This component uses "/assets/js/svg-map.js" to make things interactive in the browser.
// It will only get included in pages that need it by using the "data-dependencies" attribute.
export function SVGMap(config,csv,sources){

	let geo = loadFromSources(config.geojson.file,sources);
	let bg = loadFromSources((config.background ? config.background.file : "")||"data/maps/simple-UK.geojson",sources);
	//let motorways = loadFromSources("data/maps/simple-motorways.geojson",sources);
	let places = loadFromSources("data/maps/simple-places.csv", sources);

	console.log('TYPE: SVG-MAP',config.geojson.file);

	// IF the GeoJSON object doesn't contain a type: FeatureCollection we stop
	if(!geo.type || !geo.type == "FeatureCollection"){
		throw new Error("No FeatureCollection in the GeoJSON: "+config.geojson.file);
	}

	// Add a colour-scale colour to each row based on the "value" column
	var rows = clone(csv.rows);
	for(var r = 0; r < rows.length; r++){
		rows[r].colour = colourScales.getColourFromScale(config.scale||'Viridis',rows[r][config.value],config.min,config.max);
	}

	// Work out default max/min from data
	var min = 1e100;
	var max = -1e100;
	if(csv.columns[config.value]){
		for(var i = 0; i < csv.columns[config.value].length; i++){
			if(typeof csv.columns[config.value][i]==="number"){
				min = Math.min(min,csv.columns[config.value][i]);
				max = Math.max(max,csv.columns[config.value][i]);
			}
		}
	}
	// Override defaults if set
	if(typeof config.min=="number") min = config.min;
	if(typeof config.max=="number") max = config.max;

	function getData(csv,key,k){
		for(var i = 0; i < csv.length; i++){
			if(csv[i][key] == k) return csv[i];
		}
		return false;
	}

	var map = new BasicMap(config,{
		'background': 'transparent',
		'layers': [{
			'id': 'background',
			'data': bg,
			'options': { 'color': '#fafaf8' }
		},/*{
			'id': 'motorways',
			'data': motorways,
			'options': { 'color': '#e8e8e7', 'stroke-width': 1.2 }
		},*/{
			'id': 'data-layer',
			'data': geo,
			'options': { 'color': '#b2b2b2' },
			'values': { 'column': config.key, 'geokey': config.geojson.key, 'min':min, 'max': max, 'rows': rows, 'colour': 'red' },
			'style': function(feature,el){
				var v,code,r,i,title;
				v = this.attr.values;
				code = feature.properties[v.geokey];
				var row = getData(this.attr.values.rows,this.attr.values.column,code);
				if(row){
					if(row.Label){
						// Add a text label 
						title = document.createElement('title');
						title.innerHTML = row.Label;
						el.appendChild(title);
					}
					el.setAttribute('fill-opacity',1);
					el.setAttribute('fill',row.colour);
					el.setAttribute('stroke','white');
					el.setAttribute('stroke-width',2);
					el.setAttribute('stroke-opacity',0.1);
				}else{
					el.setAttribute('style','display:none');
				}
			}
		},{
			'id': 'labels',
			'data': places,
			'options': { 'fill': '#4c5862', 'stroke': 'white', 'stroke-width': '0.7%', 'stroke-linejoin': 'round'	},
			'type': 'text',
			'values': {'places':config.places||[]},
			'process': function(d,map){
				var i,c,locations,fs,f,loc,threshold,place,p;

				locations = [];
				fs = 1;
				threshold = 100000;

				for(i = 0; i < d.rows.length; i++){

					place = -1;
					for(p = 0; p < this.attr.values.places.length; p++){
						if(this.attr.values.places[p].name==d.rows[i].Name) place = p;
					}
					if(place >= 0){
						loc = {'type':'Feature','properties':{},'style':{},'geometry':{'type':'Point','coordinates':[]}};

						for(c in d.rows[i]) loc.properties[c] = d.rows[i][c];
						for(c in this.attr.values.places[place]) loc.style[c] = this.attr.values.places[place][c];
						loc.name = loc.properties.Name;

						f = fs*0.75;
						if(loc.properties.Population){
							if(loc.properties.Population > 100000) f += fs*0.125;
							if(loc.properties.Population > 250000) f += fs*0.125;
							if(loc.properties.Population > 750000) loc.name = loc.name.toUpperCase();
						}
						loc.properties.fontsize = 12*f;
						loc.geometry.coordinates = [loc.properties.Longitude,loc.properties.Latitude];
						if(typeof this.attr.values.places[place].longitude==="number") loc.geometry.coordinates[0] = this.attr.values.places[place].longitude;
						if(typeof this.attr.values.places[place].latitude==="number") loc.geometry.coordinates[1] = this.attr.values.places[place].latitude;
						if(loc.properties.Population >= threshold) locations.push(loc);
					}
				}
				this.data = {'features':locations};
			}
		}],
		'complete': function(){
			if(config.bounds){
				if(typeof config.bounds==="string") return this.zoomToData(config.bounds);
				else if(config.bounds.lat && config.bounds.lon) return this.setBounds(new BBox(config.bounds.lat,config.bounds.lon));
			}
			if(this.getLayerPos('data-layer') >= 0) this.zoomToData('data-layer');
			else this.zoomToData('background');
		}
	});

	return map;

}

function getLegend(config){
	
	// Build a legend
	var legend = '';
	if(config.legend && config.legend.items){
		for(var i = 0; i < config.legend.items.length; i++){
			legend += '<i style="background:'+colourScales.getColourFromScale(config.scale||'Viridis',config.legend.items[i].value,config.min,config.max)+'"></i> ' + config.legend.items[i].label + '<br />';
		}
	}
	return legend;
}

// Build a legend in SVG
function buildLegend(config){

	var container = document.createElement('div');
	if(config.legend){
		if(!config.legend.position) config.legend.position = "bottom right";
		config.legend.position = config.legend.position.replace(/(^| )/g,function(m,p1){ return p1+'leaflet-'; });
		setAttr(container,{'class':config.legend.position});
	}
	
	if(config.legend && config.legend.items){
		var legend = document.createElement('div');
		setAttr(legend,{'class':'legend leaflet-control'});
		legend.innerHTML = getLegend(config);
		add(legend,container);
	}
	return container;
}

function loadFromSources(path,sources){

	var name,bits,data;
	name = path.replace(/\//g, '.').replace(/^.*data/, 'sources').replace(/\.[^\.]*$/, '');
	bits = name.split(".");
	data = {};
	if(bits[0]=="sources"){
		data = clone(sources);
		for(var b = 1; b < bits.length; b++){
			if(data[bits[b]]) data = data[bits[b]];
			else return {};
		}
	}
	return data;
}



function BasicMap(config,attr){
	if(!attr) attr = {};
	var el = document.createElement('div');
	this.container = el;
	el.innerHTML = "";
	setAttr(this.container,{'style':'overflow:hidden'});

	var o = {'width':1200,'height':675};
	this.w = (attr.w || o.width);
	this.h = (attr.h || o.height);
	this.attr = attr;

	// Add the SVG
	this.svg = svgEl('svg');
	setAttr(this.svg,{'class':'map-inner','xmlns':'http://www.w3.org/2000/svg','version':'1.1','width':this.w,'height':this.h,'viewBox':'-180 0 360 180','overflow':'visible','style':'max-width:100%;max-height:100%;background:'+(attr.background||"white"),'preserveAspectRatio':'xMidYMid meet'});
	el.appendChild(this.svg);

	this.layers = [];
	this.zoom = 12;
	this.bounds = new BBox();
	this.places = (attr.places||[]);
	this.place = (attr.place||"");

	this.getHTML = function(){

		var html = ['<div class="map svg-map" data-dependencies="/assets/js/svg-map.js">'];

		html.push(this.svg.outerHTML);

		// Create the legend
		var legend = buildLegend(config);
		html.push(legend.outerHTML);

		html.push('</div>\n');

		return html.join('');
	};
	
	this.insertLayer = function(l,i){
		if(typeof l!=="object" || typeof l.id!=="string"){
			console.warn('Layer does not appear to contain a key',l);
			return {};
		}
		l = new Layer(l,this,i);
		if(l.id){
			if(typeof i==="number") this.layers.splice(Math.max(i,0),0,l);
			else this.layers.push(l);
			l.load();
		}
		return l;	
	};
	
	this.addLayers = function(ls,cb,i){
		if(typeof ls.length!=="number") ls = [ls];
		
		function isFinished(){
			if(typeof cb==="function") cb.call(this);
		}
		for(var l = 0; l < ls.length; l++){
			ls[l].callback = isFinished;
			this.insertLayer(ls[l],i);
		}
		return this;
	};

	this.addLayersAfter = function(name,ls){
		var i = this.getLayerPos(name)+1;
		return this.addLayers(ls,this.attr.complete,i);
	};

	this.addLayersBefore = function(name,ls){
		var i = this.getLayerPos(name)||0;
		return this.addLayers(ls,this.attr.complete,i);
	};

	this.getLayerPos = function(l){
		if(typeof l==="string"){
			for(var i = 0; i < this.layers.length; i++){
				if(this.layers[i].id==l) return i;
			}
			return -1;	// No matches
		}
		return l;
	};

	this.removeLayer = function(l){
		// Get the index of the layer
		var i = this.getLayerPos(l);
		if(i >= 0 && i < this.layers.length){
			// Remove SVG content for this layer
			this.layers[i].clear();
			// Remove layer from array
			return this.layers.splice(i,1)[0];
		}else{
			return false;
		}
	};

	// Set the bounds of the map
	this.setBounds = function(bbox){

		this.bounds = bbox;
		var tileBox = bbox.asTile(this.zoom);

		// Set the view box
		setAttr(this.svg,{'viewBox': (tileBox.x.min)+' '+(tileBox.y.max)+' '+(tileBox.x.range)+' '+(tileBox.y.range)});

		// Scale text labels
		var tspans = this.svg.querySelectorAll('tspan');
		var svgLabels = this.svg.querySelectorAll('text');
		if(svgLabels.length > 0){
			var pc = 100;
			pc = 100*(tileBox.x.range > tileBox.y.range ? tileBox.x.range/this.w : tileBox.y.range/this.h);
			var i;
			for(i = 0; i < tspans.length; i++){
				tspans[i].setAttribute('style','font-size:'+pc.toFixed(3)+'%;');
			}
		}

		return this;
	};

	this.getBounds = function(){ return this.bounds; };

	this.clear = function(){
		// TODO: clear SVG
		this.layers = [];
		return this;
	};

	this.zoomToData = function(id){

		// Get bounding box range from all layers
		var bbox = new BBox();
		for(var l = 0; l < this.layers.length; l++){
			if(this.layers[l].bbox){
				if(!id || id == this.layers[l].id){
					bbox.expand(this.layers[l].bbox);
				}
			}
		}
		return this.setBounds(bbox);
	};

	if(attr.layers) this.addLayers(attr.layers,attr.complete);

	return this;

}

function Layer(attr,map,i){
	if(!attr.id){
		console.error('Layer does not have an ID set');
		return {};
	}
	this.id = attr.id;

	if(typeof attr.data==="string"){
		this._url = attr.data;
		this.data = null;
	}else{
		this.data = attr.data;
	}
	this.attr = (attr || {});
	this.options = (this.attr.options || {});
	if(!this.options.fillOpacity) this.options.fillOpacity = 1;
	if(!this.options.opacity) this.options.opacity = 1;
	if(!this.options.color) this.options.color = '#000000';
	if(typeof this.options.useforboundscalc==="undefined") this.options.useforboundscalc = true;

	var g = svgEl('g');
	var gs;
	setAttr(g,{'class':this.class||this.id});

	if(map && map.svg){
		if(typeof i==="number"){
			gs = map.svg.querySelectorAll('g');
			gs[i].insertAdjacentElement('beforebegin', g);
		}else{
			map.svg.appendChild(g);
		}
	}

	this.clear = function(){ g.innerHTML = ''; return this; };

	function addToPath(path,xy){
		xy = {'x':xy.x.toFixed(2),'y':xy.y.toFixed(2),'t':xy.t};
		if(path.length == 0) path.push(xy);
		else{
			if(path[path.length-1].x!=xy.x || path[path.length-1].y!=xy.y || path[path.length-1].t!=xy.t) path.push(xy); 
		}
		return path;
	}
	function formatPath(path){
		var p = "";
		var t = "";
		for(var i = 0; i < path.length; i++){
			if(path[i].t!=t) p += path[i].t;
			else p += ', ';
			p += path[i].x+' '+path[i].y;
		}
		return p+'Z';
	}

	// Function to draw it on the map
	this.update = function(){
		// Clear existing layer
		this.clear();
		// Find the map bounds and work out the scale
		var f,i,j,k,dlat,dlon,feature,w,h,b,p,c,d,xy,tspan,path;
		w = map.w;
		h = map.h;
		b = map.getBounds();
		dlat = (b.lat.max - b.lat.min);
		dlon = (b.lon.max - b.lon.min);
		this.bbox = new BBox();
		
		if(this.data && this.data.features){

			for(f = 0; f < this.data.features.length; f++){
				if(this.data.features[f]){
					feature = this.data.features[f];
					c = feature.geometry.coordinates;
					if(feature.geometry.type == "MultiPolygon"){
						p = svgEl('path');
						setAttr(p,{
							'stroke': this.options.color||this.options.stroke,
							'stroke-opacity':this.options.opacity,
							'stroke-width': this.options['stroke-width']
						});
						path = [];
						for(i = 0; i < c.length; i++){
							for(j = 0; j < c[i].length; j++){
								for(k = 0; k < c[i][j].length; k++){
									this.bbox.expand(c[i][j][k]);
									xy = latlon2xy(c[i][j][k][1],c[i][j][k][0],map.zoom);
									xy.t = (k==0 ? 'M':'L');
									addToPath(path,xy);
								}
							}
						}
						d = formatPath(path);
						setAttr(p,{
							'd':d,
							'fill': this.options.color||this.options.fill,
							'fill-opacity': this.options.fillOpacity,
							'vector-effect':'non-scaling-stroke',
							'stroke': this.options.stroke||this.options.color,
							'stroke-width': this.options['stroke-width']||'0.4%',
							'stroke-opacity': this.options['stroke-opacity']||1
						});
						if(typeof attr.style==="function") attr.style.call(this,feature,p);
					}else if(feature.geometry.type == "Polygon"){
						p = svgEl('path');
						setAttr(p,{
							'stroke': this.options.color||this.options.stroke,
							'stroke-opacity':this.options.opacity,
							'stroke-width': this.options['stroke-width']
						});
						path = [];
						for(i = 0; i < c.length; i++){
							for(j = 0; j < c[i].length; j++){
								this.bbox.expand(c[i][j]);
								xy = latlon2xy(c[i][j][1],c[i][j][0],map.zoom);
								xy.t = (j==0 ? 'M':'L');
								addToPath(path,xy);
							}
						}
						d = formatPath(path);
						setAttr(p,{
							'd':d,
							'fill': this.options.color||this.options.fill,
							'fill-opacity': this.options.fillOpacity,
							'vector-effect':'non-scaling-stroke',
							'stroke': this.options.stroke||this.options.color,
							'stroke-width': this.options['stroke-width']||'0.4%',
							'stroke-opacity': this.options['stroke-opacity']||1
						});
						if(typeof attr.style==="function") attr.style.call(this,feature,p);
					}else if(feature.geometry.type == "MultiLineString"){
						p = svgEl('path');
						setAttr(p,{
							'stroke': this.options.color||this.options.stroke,
							'stroke-opacity':this.options.opacity,
							'stroke-width': this.options['stroke-width']
						});
						path = [];
						for(i = 0; i < c.length; i++){
							for(j = 0; j < c[i].length; j++){
								this.bbox.expand(c[i][j]);
								xy = latlon2xy(c[i][j][1],c[i][j][0],map.zoom);
								xy.t = (j==0 ? 'M':'L');
								addToPath(path,xy);
								//lat = (90 - c[i][j][1]).toFixed(5);
								//lon = (c[i][j][0]).toFixed(5);
								//if(j==0) d += 'M'+xy.x.toFixed(2)+' '+xy.y.toFixed(2);
								//else d += (j==1 ? 'L':', ')+xy.x.toFixed(2)+' '+xy.y.toFixed(2);
							}
						}
						d = formatPath(path);
						setAttr(p,{
							'd':d,
							'fill':'transparent',
							'vector-effect':'non-scaling-stroke'
						});
						if(typeof attr.style==="function") attr.style.call(this,feature,p);
					}else if(feature.geometry.type == "Point"){
						this.bbox.expand(c);
						xy = latlon2xy(c[1],c[0],map.zoom);

						p = svgEl('text');
						tspan = svgEl('tspan');
						tspan.innerHTML = feature.name;
						p.appendChild(tspan);
						setAttr(p,{
							'fill': this.options.fill||this.options.color,
							'fill-opacity': this.options.fillOpacity,
							'font-weight': this.options['font-weight']||'',
							'stroke': this.options.stroke||this.options.color,
							'stroke-width': this.options['stroke-width']||'0.4%',
							'stroke-linejoin': this.options['stroke-linejoin'],
							'text-anchor': this.options.textAnchor||feature.style['text-anchor']||'middle',
							'font-family': feature.style['font-family']||'Century Gothic',
							'font-size': (feature.properties.fontsize ? feature.properties.fontsize : 1),
							'paint-order': 'stroke',
							'x': xy.x.toFixed(2),
							'y': xy.y.toFixed(2)
						});
						if(typeof attr.style==="function") attr.style.call(this,feature,p);
					}
					g.appendChild(p);
				}
			}
		}else{
			console.warn('No data features',this.data);
		}
		return this;
	};
	
	this.load = function(){
		if(!this.data){
			console.error('No data structure given',this);
		}else{
			if(typeof attr.process==="function") attr.process.call(this,this.data,map);
			this.update();
			// Final callback
			if(typeof attr.callback==="function") attr.callback.call(map);
		}
	};

	return this;
}

function BBox(lat,lon){
	this.lat = lat||{'min':90,'max':-90};
	this.lon = lon||{'max':-180,'min':180};
	this.expand = function(c){
		if(c.length == 2){
			this.lat.max = Math.max(this.lat.max,c[1]);
			this.lat.min = Math.min(this.lat.min,c[1]);
			this.lon.max = Math.max(this.lon.max,c[0]);
			this.lon.min = Math.min(this.lon.min,c[0]);
		}else if(c.lat && c.lon){
			this.lat.max = Math.max(this.lat.max,c.lat.max);
			this.lat.min = Math.min(this.lat.min,c.lat.min);
			this.lon.max = Math.max(this.lon.max,c.lon.max);
			this.lon.min = Math.min(this.lon.min,c.lon.min);
		}else{
			console.warn('updateBBox wrong shape',c);
		}
		return this;
	};
	this.asTile = function(zoom){
		var x = {'min':lon2tile(this.lon.min,zoom),'max':lon2tile(this.lon.max,zoom)};
		var y = {'min':lat2tile(this.lat.min,zoom),'max':lat2tile(this.lat.max,zoom)};
		x.range = Math.abs(x.max-x.min);
		y.range = Math.abs(y.max-y.min);
		return {'x':x,'y':y };
	};
	return this;
}

function add(el,to){ return to.appendChild(el); }
function setAttr(el,prop){
	for(var p in prop){
		if(prop[p]) el.setAttribute(p,prop[p]);
	}
	return el;
}
function svgEl(t){ return document.createElement(t);/*return document.createElementNS(ns,t);*/ }

// Map maths for the Web Mercator projection (like Open Street Map) e.g. https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
var d2r = Math.PI/180;
function lon2tile(lon,zoom){ return ((lon+180)/360)*Math.pow(2,zoom); }
function lat2tile(lat,zoom){ return ((1-Math.log(Math.tan(lat*d2r) + 1/Math.cos(lat*d2r))/Math.PI)/2)*Math.pow(2,zoom); }
function latlon2xy(lat,lon,zoom){ return {'x':lon2tile(lon,zoom),'y':lat2tile(lat,zoom)}; }

