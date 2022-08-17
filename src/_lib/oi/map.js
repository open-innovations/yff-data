import { document } from '/src/_lib/oi/document.ts';
import { colourScales, Colour } from '/src/_lib/oi/colour.js';

// This component uses "/assets/js/dashboard.js" to make things interactive in the browser.
// It will only get included in pages that need it by using the "data-dependencies" attribute.

const ns = 'http://www.w3.org/2000/svg';

function clone(a){ return JSON.parse(JSON.stringify(a)); }

export function LeafletMap(config,csv){

	this.getHTML = function(){
		var html,i,panel,r,cls,p,idx;
		
		html = ['<div class="map" data-dependencies="/assets/leaflet/leaflet.js,/assets/leaflet/leaflet.css">'];
		
		html.push('<script>');
		html.push('var p = document.currentScript.parentNode;');
		html.push('var el = document.createElement("div");');
		html.push('el.classList.add("leaflet");');
		html.push('p.appendChild(el);');
		html.push('var map = L.map(el);');
		if(config.bounds) html.push('map.fitBounds([['+config.bounds[0]+'],['+config.bounds[1]+']]);');
		html.push('L.tileLayer("https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png", { maxZoom: 19, attribution: "Tiles: &copy; OpenStreetMap/CartoDB", subdomains: "abcd" }).addTo(map);');
		html.push('map.attributionControl.setPrefix("Youth Futures Foundation");\n');
		
		html.push('// Create a map label pane so labels can sit above polygons\n');
		html.push('map.createPane("labels");\n');
		html.push('map.getPane("labels").style.zIndex = 650;\n');
		html.push('map.getPane("labels").style.pointerEvents = "none";\n');
		html.push('	L.tileLayer("https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png", {\n');
		html.push('		attribution: "",\n');
		html.push('		pane: "labels"\n');
		html.push('	}).addTo(map);\n');
		
		html.push('fetch("'+config.geojson.file+'").then(response => {');
		html.push('		if(!response.ok) throw new Error("Network response was not OK");');
		html.push('		return response.json();');
		html.push('}).then(json => {');
		
		var rows = clone(csv.rows);
		for(var r = 0; r < rows.length; r++){
			rows[r].colour = colourScales.getColourFromScale(config.scale||'Viridis',rows[r][config.value],config.min,config.max);
		}
		var legend = '';
		for(var i in config.legend){
			legend += '<i style=\\"background:'+colourScales.getColourFromScale(config.scale||'Viridis',config.legend[i].value,config.min,config.max)+'\\"></i> ' + config.legend[i].label + '<br />';
		}

		html.push('		var csv = '+JSON.stringify(rows)+';');
		html.push('		var geokey = "'+config.geojson.key+'";');
		html.push('		var key = "'+config.key+'";');

		html.push('		function getData(k){\n');
		html.push('			for(var i = 0; i < csv.length; i++){\n');
		html.push('				if(csv[i][key] == k) return csv[i];\n');
		html.push('			}\n');
		html.push('			return {};\n');
		html.push('		}\n');
		html.push('		function style(feature) {');
		html.push('			var d = getData(feature.properties[geokey]);');
		html.push('			return {');
		html.push('				weight: 0.5,');
		html.push('				opacity: 1,');
		html.push('				color: "#B2B2B2",');
		html.push('				fillOpacity: 0.8,');
		html.push('				fillColor: d.colour||"transparent"');
		html.push('			};');
		html.push('		}');

		html.push('		var geoattrs = { "style": style };\n');
		html.push('		var geo = L.geoJSON(json,geoattrs);\n');
		html.push('		geo.addTo(map);\n');
		if(!config.bounds) html.push('		map.fitBounds(geo.getBounds());\n');

		// Create the legend
		html.push('		var legend = L.control({position: "bottomright"});\n');
		html.push('		legend.onAdd = function (map){\n');
		html.push('			var div = L.DomUtil.create("div", "info legend");\n');
		html.push('			div.innerHTML = "'+legend+'";\n');
		html.push('			return div;\n');
		html.push('		}\n');
		html.push('		legend.addTo(map);');



		html.push('}).catch(error => {\n');
		html.push('		console.error("Unable to load the data",error);\n');
		html.push('});\n');
		html.push('</script>\n');

		html.push('</div>');

		return html.join('');
	};
	return this;
}