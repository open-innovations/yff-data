import { Dashboard } from '/src/_lib/oi/dashboard.js';
import { loadDataFile } from '/src/_lib/oi/util.js'

export const js = `
if(!ready){
	function ready(fn){
		// Version 1.1
		if(document.readyState != 'loading') fn();
		else document.addEventListener('DOMContentLoaded', fn);
	}
}
if(!window.requestAnimFrame){
	// shim layer with setTimeout fallback
	window.requestAnimFrame = (function(){
		return  window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || function( callback ){ window.setTimeout(callback, 1000 / 60); };
	})();
}
ready(function(){
	var dashboards = document.querySelectorAll(".dashboard");
	function animateNumber(el,val,duration){
		if(typeof val!=="number"){
			val = el.getAttribute('data')||el.innerHTML;
			if(val) val = parseFloat(val);
			el.innerHTML = '';
		}
		var start = new Date();
		var pre = el.getAttribute('data-prefix')||'';
		var post = el.getAttribute('data-postfix')||'';
		var v;
		if(typeof duration!=="number") duration = 300;

		function frame(){
			var now = new Date();
			// Set the current time in milliseconds
			var f = (now - start)/duration;
			if(f < 1){
				v = formatNumber(Math.round(val*f));
				el.innerHTML = pre+v+post;
				window.requestAnimFrame(frame);
			}else{
				el.innerHTML = (pre||"")+formatNumber(val)+(post||"");
			}
		}

		if(typeof val==="number") frame();
		return;			
	}
	function formatNumber(v){
		if(typeof v !== "number") return v;
		if(v > 1e7) return Math.round(v/1e6)+"M";
		if(v > 1e6) return (v/1e6).toFixed(1)+"M";
		if(v > 1e5) return Math.round(v/1e3)+"k";
		if(v > 1e4) return Math.round(v/1e3)+"k";
		return v;
	}
	function inViewport(el) {
		var bounding = el.getBoundingClientRect();
		var h = el.offsetHeight;
		var w = el.offsetWidth;

		if(bounding.top >= -h 
			&& bounding.left >= -w
			&& bounding.right <= (window.innerWidth || document.documentElement.clientWidth) + w
			&& bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) + h){
			return true;
		}else{
			return false;
		}
		return false;
	}

	function activateDashboards(){
		for(var d = 0; d < dashboards.length; d++){
			if(!dashboards[d].getAttribute('activated') && inViewport(dashboards[d])){
				dashboards[d].setAttribute('activated',true);
				// Now trigger the number animations
				panels = dashboards[d].querySelectorAll('.bignum');
				for(var p = 0; p < panels.length; p++) animateNumber(panels[p]);
			}
		}
	}
	document.addEventListener('scroll', activateDashboards);
	activateDashboards();
});

`

export const css = `
.dashboard {
	width: 100%;
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	grid-gap: 1em;
}
.dashboard h3 { color: inherit!important; }
.panel { background: #efefef; padding: 1em; }
.dashboard .bignum { font-size: 4em; line-height: 1.25em; font-weight: bold; text-align: center; display: block; margin-top: 0; }
.dashboard .note { font-size: 0.7em; text-align: center; display: block; }
`;

function clone(a){ return JSON.parse(JSON.stringify(a)); }

export default function ({ config, sources }) {

	// Load the data from the sources
	const csv = loadDataFile(config, sources);

	// Set the output to "?" as a default
	let html = "?";

	if(csv){

		// Make a clone of the original config to avoid updating the contents elsewhere
		const configcopy = clone(config);

		// Create a new Line Chart
		let dashboard = new Dashboard(configcopy,csv);

		// Get the output
		if(dashboard) html = dashboard.getHTML();

	}else{

		console.warn('WARNING: No CSV contents at '+config.file);

	}

	return html;
}