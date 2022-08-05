import { CategoryChart, LineChart } from '/oi/charts.js';
import { colourScales, Colour } from '/oi/colour.js';
import { loadDataFile } from '/oi/util.js'

export const js = `
(function(root){
	var ns = 'http://www.w3.org/2000/svg';
	function svgEl(t){ return document.createElementNS(ns,t); }
	function add(el,to){ return to.appendChild(el); }
	function setAttr(el,prop){
		for(var p in prop) el.setAttribute(p,prop[p]);
		return el;
	}
	function addEv(ev,el,data,fn){
		el.addEventListener(ev,function(e){
			e.data = data;
			fn.call(data.this||this,e);
		});
	}
	function addClasses(el,cl){
		for(var i = 0; i < cl.length; i++) el.classList.add(cl[i]);
		return el;
	}
	function InteractiveChart(el){
		var svg = el.querySelector('svg');
		var key = el.querySelector('.key');
		var serieskey = el.querySelectorAll('.series');
		var s,d,i,p;
		var pt = el.querySelectorAll('.series circle');
		var pts = [];
		var series = [];
		for(p = 0; p < pt.length; p++){
			s = parseInt(pt[p].getAttribute('data-series'));
			i = parseInt(pt[p].getAttribute('data-i'))
			pts[p] = {'el':pt[p],'series':s,'i':i,'tooltip':pt[p].querySelector('title').innerHTML};
			if(!series[s]) series[s] = [];
			if(!series[s][i]) series[s][i] = pts[p];
		}
		this.enabled = true;
		this.selected = null;
		
		this.reset = function(e){
			return this.clearSeries(e).clearTooltip(e);
		};
		this.setSeries = function(e){
			this.enabled = !this.enabled;
			if(this.enabled) e.data.s = null;
			this.highlightSeries(e);
			return this;
		};
		this.clearSeries = function(e){
			if(this.enabled){
				e.data.s = null;
				this.enabled = true;
				this.highlightSeries(e);
			}
			return this;
		};
		this.highlightSeries = function(e){
			if(this.enabled){
				var d = e.data.s;
				this.selected = d;
				var selected = el.querySelector('.series-'+d);
				for(var s = 0; s < serieskey.length; s++){
					if(d){
						if(serieskey[s]==selected){
							serieskey[s].style.opacity = 1;
							// Simulate z-index by moving to the end
							serieskey[s].parentNode.appendChild(serieskey[s]);
						}else{
							serieskey[s].style.opacity = 0.1;
						}
					}else{
						serieskey[s].style.opacity = 1;
					}
				}
			}
			return this;
		};
		this.triggerTooltip = function(e){
			for(var i = 0; i < pts.length; i++){
				if(pts[i].el==e.target) return this.showTooltip(pts[i].series,pts[i].i);
			}
			return this;
		};
		this.clearTooltip = function(e){
			if(this.tip && this.tip.parentNode) this.tip.parentNode.removeChild(this.tip);
			return this;
		};
		function hsv_to_hsl(h, s, v) {
			// both hsv and hsl values are in [0, 1]
			var l = (2 - s) * v / 2;
			if (l != 0) {
				if (l == 1) {
					s = 0
				} else if (l < 0.5) {
					s = s * v / (l * 2)
				} else {
					s = s * v / (2 - l * 2)
				}
			}
			return {'h':h,'s':s,'l':l};
		}
		this.showTooltip = function(s,i){
			el.style.position = 'relative';

			var txt,bb,bbo;
			this.tip = el.querySelector('.tooltip');
			if(!this.tip){
				this.tip = document.createElement('div');
				this.tip.innerHTML = '<div class="inner" style="background: #b2b2b2;position:relative;"></div><div class="arrow" style="position: absolute; bottom: auto; width: 0; height: 0; border: 0.5em solid transparent; border-bottom: 0; left: 50%; top: 100%; transform: translate3d(-50%,0,0); border-color: transparent; border-top-color: green;"></div>';
				addClasses(this.tip,['tooltip']);
				add(this.tip,el);
			}

			// Set the contents
			txt = series[s][i].tooltip.replace(/\\n/g,'<br />');

			fill = new Colour(series[s][i].el.getAttribute('fill'));
			hsv = fill.hsv;
			hsl = hsv_to_hsl(hsv[0]*360,hsv[1],hsv[2]);
			//hsl.l += 0.25;


			// Remove current selections
			selected = el.querySelectorAll('circle.selected');
			for(var j = 0; j < selected.length; j++) selected[j].classList.remove('selected');
			
			// Select this point
			series[s][i].el.classList.add('selected');

			this.tip.querySelector('.inner').innerHTML = (txt);

			// Position the tooltip
			bb = series[s][i].el.getBoundingClientRect();	// Bounding box of the element
			bbo = el.getBoundingClientRect(); // Bounding box of SVG holder

			this.tip.setAttribute('style','position:absolute;left:'+(bb.left + bb.width/2 - bbo.left).toFixed(2)+'px;top:'+(bb.top + bb.height/2 - bbo.top).toFixed(2)+'px;transform:translate3d(-50%,calc(-100% - 4px),0);display:'+(txt ? 'block':'none')+';');
			this.tip.querySelector('.inner').style.background = 'hsl('+hsl.h+','+(hsl.s*100)+'%,'+(hsl.l*100)+'%)';
			this.tip.querySelector('.arrow').style['border-top-color'] = 'hsl('+hsl.h+','+(hsl.s*100)+'%,'+(hsl.l*100)+'%)';
			this.tip.style.color = fill.text;

			return this;
		}
		// Find the nearest point
		this.findPoint = function(e){
			var i,d,dx,dy,p,idx,min,dist;
			min = 20;
			dist = 1e100;
			var snap_to_x = true;
			var matches = [];
			var typ = svg.getAttribute('data-type');
			

			for(s = 0; s < series.length; s++){
				if(series[s]){
					ok = true;
					if(this.selected != null && s!=this.selected) ok = false;
					if(ok){
						dist = 1e100;
						d = -1;
						idx = -1;
						for(i = 0; i < series[s].length; i++){
							p = series[s][i].el.getBoundingClientRect();
							if(typ=="category-chart"){
								dx = Math.abs((p.x+p.width/2)-e.clientX);	// Find distance from circle centre to cursor
								dy = Math.abs((p.y+p.width/2)-e.clientY);
								if(dy < min && dy < dist){
									idx = i;
									dist = dy;
									d = Math.sqrt(dx*dx + dy*dy);
								}
							}else{
								dx = Math.abs((p.x+p.width/2)-e.clientX);	// Find distance from circle centre to cursor
								dy = Math.abs((p.y+p.width/2)-e.clientY);
								if(dx < min && dx < dist){
									idx = i;
									dist = dx;
									d = Math.sqrt(dx*dx + dy*dy);
								}
							}
						}
						if(idx >= 0){
							matches.push({'dist':d,'distx':dist,'pt':series[s][idx]});
						}
					}
				}
			}

			dist = 1e100;
			idx = -1;
			for(s = 0; s < matches.length; s++){
				if(matches[s].dist < dist){
					dist = matches[s].dist;
					idx = s;
				}
			}
			if(idx >= 0) this.showTooltip(matches[idx].pt.series,matches[idx].pt.i);
			else this.clearTooltip();
			return this;
		}
		if(key){
			// We build an HTML version of the key
			var newkey = document.createElement('div');
			newkey.classList.add('key');
			el.insertBefore(newkey, el.firstChild);


			var keyseries = key.querySelectorAll('.data-series');
			for(var s = 0; s < keyseries.length; s++){
				// Create a key item <div>
				keyitem = document.createElement('div');
				keyitem.classList.add('keyitem');
				add(keyitem,newkey);

				// Make the new SVG just for the icon
				icon = svgEl('svg');
				add(icon,keyitem);

				// Get the text for the series
				txt = document.createElement('span');
				txt.classList.add('label');
				txt.innerHTML = keyseries[s].querySelector('text tspan').innerHTML;
				add(txt,keyitem);

				// Now remove the text label (we'll recreate it with HTML)
				keyseries[s].querySelector('text').parentNode.removeChild(keyseries[s].querySelector('text'));
				// Get the existing viewBox
				viewBox = svg.getAttribute('viewBox').split(/ /);
				xscale = parseFloat(viewBox[2])/svg.getBoundingClientRect().width;
				yscale = parseFloat(viewBox[3])/svg.getBoundingClientRect().height;
				viewBox[0] = 0;
				viewBox[1] = 0;
				viewBox[2] = parseFloat(viewBox[2])*keyseries[s].getBoundingClientRect().width/svg.getBoundingClientRect().width;
				viewBox[3] = parseFloat(viewBox[3])*keyseries[s].getBoundingClientRect().height/svg.getBoundingClientRect().height;
				// Get the offsets
				dx = (keyseries[s].getBoundingClientRect().x-svg.getBoundingClientRect().x)*xscale;
				dy = (keyseries[s].getBoundingClientRect().y-svg.getBoundingClientRect().y)*yscale;

				setAttr(keyseries[s],{'transform':'translate(-'+dx+' -'+dy+')'});
				add(keyseries[s],icon);
				setAttr(icon,{'width':keyseries[s].getBoundingClientRect().width,'height':keyseries[s].getBoundingClientRect().height,'viewBox':viewBox.join(" ")});
				setAttr(keyitem,{'data-series':keyseries[s].getAttribute('data-series'),'tabindex':0,'title':'Highlight series: '+txt.innerHTML});


				addEv('mouseover',keyitem,{'this':this,'s':keyseries[s].getAttribute('data-series')},this.highlightSeries);
				addEv('focus',keyitem,{'this':this,'s':keyseries[s].getAttribute('data-series')},this.highlightSeries);
				addEv('click',keyitem,{'this':this,'s':keyseries[s].getAttribute('data-series')},this.setSeries);
				addEv('mouseout',keyitem,{'this':this,'s':null},this.highlightSeries);

			}
			// Hide the original key
			key.style.display = 'none';
			addEv('mouseleave',el,{'this':this,'s':''},this.reset);
			addEv('mousemove',svg,{'this':this},this.findPoint);
		}
		if(pts){
			for(var p = 0; p < pts.length; p++){
				addEv('focus',pts[p].el,{'this':this},this.triggerTooltip);
			}
		}
		return this;
	}
	root.InteractiveChart = InteractiveChart;

	var colours = new Colours({
		'Viridis': 'rgb(122,76,139) 0%, rgb(124,109,168) 12.5%, rgb(115,138,177) 25%, rgb(107,164,178) 37.5%, rgb(104,188,170) 50%, rgb(133,211,146) 62.5%, rgb(189,229,97) 75%, rgb(254,240,65) 87.5%, rgb(254,240,65) 100%',
		'Heat': 'rgb(0,0,0) 0%, rgb(128,0,0) 25%, rgb(255,128,0) 50%, rgb(255,255,128) 75%, rgb(255,255,255) 100%',
		'Planck': 'rgb(0,0,255) 0%, rgb(0,112,255) 16.666%, rgb(0,221,255) 33.3333%, rgb(255,237,217) 50%, rgb(255,180,0) 66.666%, rgb(255,75,0) 100%',
		'Plasma': 'rgb(12,7,134) 0%, rgb(82,1,163) 12.5%, rgb(137,8,165) 25%, rgb(184,50,137) 37.5%, rgb(218,90,104) 50%, rgb(243,135,72) 62.5%, rgb(253,187,43) 75%, rgb(239,248,33) 87.5%',
		'YFF': 'rgb(99,190,123) 0%, rgb(250,233,131) 50%, rgb(248,105,107) 100%'
	});

	/* ============== */
	/* Colours v0.3.2 */
	// Define colour routines
	function Colour(c,n){
		if(!c) return {};
		function d2h(d) { return ((d < 16) ? "0" : "")+d.toString(16);}
		function h2d(h) {return parseInt(h,16);}
		/**
		 * Converts an RGB color value to HSV. Conversion formula
		 * adapted from http://en.wikipedia.org/wiki/HSV_color_space.
		 * Assumes r, g, and b are contained in the set [0, 255] and
		 * returns h, s, and v in the set [0, 1].
		 *
		 * @param	Number  r		 The red color value
		 * @param	Number  g		 The green color value
		 * @param	Number  b		 The blue color value
		 * @return  Array			  The HSV representation
		 */
		function rgb2hsv(r, g, b){
			r = r/255;
			g = g/255;
			b = b/255;
			var max = Math.max(r, g, b), min = Math.min(r, g, b);
			var h, s, v = max;
			var d = max - min;
			s = max == 0 ? 0 : d / max;
			if(max == min) h = 0; // achromatic
			else{
				switch(max){
					case r: h = (g - b) / d + (g < b ? 6 : 0); break;
					case g: h = (b - r) / d + 2; break;
					case b: h = (r - g) / d + 4; break;
				}
				h /= 6;
			}
			return [h, s, v];
		}

		this.alpha = 1;

		// Let's deal with a variety of input
		if(c.indexOf('#')==0){
			this.hex = c;
			this.rgb = [h2d(c.substring(1,3)),h2d(c.substring(3,5)),h2d(c.substring(5,7))];
		}else if(c.indexOf('rgb')==0){
			var bits = c.match(/[0-9\.]+/g);
			if(bits.length == 4) this.alpha = parseFloat(bits[3]);
			this.rgb = [parseInt(bits[0]),parseInt(bits[1]),parseInt(bits[2])];
			this.hex = "#"+d2h(this.rgb[0])+d2h(this.rgb[1])+d2h(this.rgb[2]);
		}else return {};
		this.hsv = rgb2hsv(this.rgb[0],this.rgb[1],this.rgb[2]);
		this.name = (n || "Name");
		var r,sat;
		for(r = 0, sat = 0; r < this.rgb.length ; r++){
			if(this.rgb[r] > 200) sat++;
		}
		this.toString = function(){
			return 'rgb'+(this.alpha < 1 ? 'a':'')+'('+this.rgb[0]+','+this.rgb[1]+','+this.rgb[2]+(this.alpha < 1 ? ','+this.alpha:'')+')';
		};
		this.text = (this.rgb[0]*0.299 + this.rgb[1]*0.587 + this.rgb[2]*0.114 > 186 ? "black":"white");
		return this;
	}
	function Colours(scales){
		if(!scales) scales = { 'Viridis': 'rgb(68,1,84) 0%, rgb(72,35,116) 10%, rgb(64,67,135) 20%, rgb(52,94,141) 30%, rgb(41,120,142) 40%, rgb(32,143,140) 50%, rgb(34,167,132) 60%, rgb(66,190,113) 70%, rgb(121,209,81) 80%, rgb(186,222,39) 90%, rgb(253,231,36) 100%'};
		function col(a){
			if(typeof a==="string") return new Colour(a);
			else return a;
		}
		this.getColourPercent = function(pc,a,b,inParts){
			var c;
			pc /= 100;
			a = col(a);
			b = col(b);
			c = {'r':parseInt(a.rgb[0] + (b.rgb[0]-a.rgb[0])*pc),'g':parseInt(a.rgb[1] + (b.rgb[1]-a.rgb[1])*pc),'b':parseInt(a.rgb[2] + (b.rgb[2]-a.rgb[2])*pc),'alpha':1};
			if(a.alpha<1 || b.alpha<1) c.alpha = ((b.alpha-a.alpha)*pc + a.alpha);
			if(inParts) return c;
			else return 'rgb'+(c.alpha && c.alpha<1 ? 'a':'')+'('+c.r+','+c.g+','+c.b+(c.alpha && c.alpha<1 ? ','+c.alpha:'')+')';
		};
		this.makeGradient = function(a,b){
			a = col(a);
			b = col(b);
			var grad = a.toString()+' 0%, '+b.toString()+' 100%';
			if(b) return 'background: '+a.toString()+'; background: -moz-linear-gradient(left, '+grad+');background: -webkit-linear-gradient(left, '+grad+');background: linear-gradient(to right, '+grad+');';
			else return 'background: '+a.toString()+';';
		};
		this.getGradient = function(id){
			return 'background: -moz-linear-gradient(left, '+scales[id].str+');background: -webkit-linear-gradient(left, '+scales[id].str+');background: linear-gradient(to right, '+scales[id].str+');';
		};
		this.addScale = function(id,str){
			scales[id] = str;
			processScale(id,str);
			return this;
		};
		this.quantiseScale = function(id,n,id2){
			var cs,m,pc,step,i;
			cs = [];
			m = n-1;
			pc = 0;
			step = 100/n;
			for(i = 0; i < m; i++){
				cs.push(this.getColourFromScale(id,i,0,m)+' '+(pc)+'%');
				cs.push(this.getColourFromScale(id,i,0,m)+' '+(pc+step)+'%');
				pc += step;
			}
			cs.push(this.getColourFromScale(id,1,0,1)+' '+(pc)+'%');
			cs.push(this.getColourFromScale(id,1,0,1)+' 100%');
			this.addScale(id2,cs.join(", "));
			return this;
		};
		function processScale(id,str){
			if(scales[id] && scales[id].str){
				console.warn('Colour scale '+id+' already exists. Bailing out.');
				return this;
			}
			scales[id] = {'str':str};
			scales[id].stops = extractColours(str);
			return this;
		}
		function extractColours(str){
			var stops,cs,i,c;
			stops = str.replace(/^\s+/g,"").replace(/\s+$/g,"").replace(/\s\s/g," ").split(', ');
			cs = [];
			for(i = 0; i < stops.length; i++){
				var bits = stops[i].split(/ /);
				if(bits.length==2) cs.push({'v':bits[1],'c':new Colour(bits[0])});
				else if(bits.length==1) cs.push({'c':new Colour(bits[0])});
			}
			
			for(c=0; c < cs.length;c++){
				if(cs[c].v){
					// If a colour-stop has a percentage value provided, 
					if(cs[c].v.indexOf('%')>=0) cs[c].aspercent = true;
					cs[c].v = parseFloat(cs[c].v);
				}
			}
			return cs;
		}

		// Process existing scales
		for(var id in scales){
			if(scales[id]) processScale(id,scales[id]);
		}
		
		// Return a Colour object for a string
		this.getColour = function(str){
			return new Colour(str);
		};
		// Return the colour scale string
		this.getColourScale = function(id){
			return scales[id].str;
		};
		// Return the colour string for this scale, value and min/max
		this.getColourFromScale = function(s,v,min,max,inParts){
			var cs,v2,pc,c,cfinal;
			if(typeof inParts!=="boolean") inParts = false;
			if(!scales[s]){
				this.log('WARNING','No colour scale '+s+' exists');
				return '';
			}
			if(typeof v!=="number") v = 0;
			if(typeof min!=="number") min = 0;
			if(typeof max!=="number") max = 1;
			cs = scales[s].stops;
			v2 = 100*(v-min)/(max-min);
			cfinal = {};
			if(v==max){
				cfinal = {'r':cs[cs.length-1].c.rgb[0],'g':cs[cs.length-1].c.rgb[1],'b':cs[cs.length-1].c.rgb[2],'alpha':cs[cs.length-1].c.alpha};
			}else{
				if(cs.length == 1){
					cfinal = {'r':cs[0].c.rgb[0],'g':cs[0].c.rgb[1],'b':cs[0].c.rgb[2],'alpha':(v2/100).toFixed(3)};
				}else{
					for(c = 0; c < cs.length-1; c++){
						if(v2 >= cs[c].v && v2 <= cs[c+1].v){
							// On this colour stop
							pc = 100*(v2 - cs[c].v)/(cs[c+1].v-cs[c].v);
							if(pc > 100) pc = 100;	// Don't go above colour range
							cfinal = this.getColourPercent(pc,cs[c].c,cs[c+1].c,true);
							continue;
						}
					}
				}
			}
			if(inParts) return cfinal;
			else return 'rgba(' + cfinal.r + ',' + cfinal.g + ',' + cfinal.b + ',' + cfinal.alpha + ")";
		};
		
		return this;
	}
	root.Colours = Colours;
	root.Colour = Colour;

	var OI = {};
	OI.ready = function(fn){
		// Version 1.1
		if(document.readyState != 'loading') fn();
		else document.addEventListener('DOMContentLoaded', fn);
	};
	if(!root.OI) root.OI = OI;
})(window || this);
OI.ready(function(){
	var charts = document.querySelectorAll('.chart');
	for(var i = 0; i < charts.length; i++){
		new InteractiveChart(charts[i])
	}
});
`
export const css = `
.chart .line { stroke-width: 4px; }
.key:before { content: "Key: "; font-family: 'Century Gothic', sans-serif; font-weight: bold; }
.key { display: inline-block; text-align: center; background: #efefef; padding: 0.5em; margin-bottom: 1em; }
.keyitem { display: inline-block; padding-right: 0.5em; font-family: 'Century Gothic', sans-serif; font-weight: bold; cursor: pointer; }
.keyitem:hover { background: white; }

.tooltip { color: black; margin-top: -0.75em; transition: left 0.03s linear, top 0.03s linear; white-space: nowrap; font-family: 'Century Gothic', sans-serif; }
.tooltip .inner { padding: 1em; }
circle.selected { r: 5px; }
`;

function clone(a){ return JSON.parse(JSON.stringify(a)); }

export default function ({ config, sources }) {
  const csv = loadDataFile(config.file, sources);

  var chart,html;
  html = "?";

  const configcopy = clone(config);
  configcopy.colours = {
    "Female":"#ee7e3b","Male":"#264c59",
    "Bangladeshi":"#7D2248","Black/African/Caribbean/Black British":"#75b8d3","Chinese":"#fe9400", "Indian":"#274b57","Mixed/Multiple":"#E55912","Other":"#0685cc","Pakistani":"#874245","Other Asian":"#39c2b0","White":"#fdc358",
    "Any other religion":"#69C2C9","Buddhist":"#C7B200","Christian":"#E55912","Hindu":"#874245","Jewish":"#7D2248","Muslim":"#005776","None":"#fdc358","Sikh":"#69C2C9",
    "16-17":"#E52E36","18-24":"#F7AB3D","25-49":"#C7B200","50-64":"#005776"
  };
  if(configcopy.type=="line-chart"){
    chart = new LineChart(configcopy,csv);
	html = chart.getSVG();
  }else if(configcopy.type=="category-chart"){
    chart = new CategoryChart(configcopy,csv);
	html = chart.getSVG();
  }
  return ['<div class="chart">',
    html,
    '</div>'
  ].join('');
}