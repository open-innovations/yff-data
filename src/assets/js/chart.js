/*
	Open Innovations Chart Interactivity v0.2
	Helper function that find ".chart" elements 
	makes a new HTML legend, and adds tooltips.
*/

(function(root){

	if(!root.OI) root.OI = {};
	if(!root.OI.ready){
		root.OI.ready = function(fn){
			// Version 1.1
			if(document.readyState != 'loading') fn();
			else document.addEventListener('DOMContentLoaded', fn);
		};
	}

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
	function InteractiveChart(el){
		var svg = el.querySelector('svg');
		var key = el.querySelector('.legend');
		var serieskey = el.querySelectorAll('.series');
		var s,i,p;
		var pt = el.querySelectorAll('.series circle, .series rect');
		var pts = [];
		var series = {};
		for(s = 0; s < serieskey.length; s++){
			i = serieskey[s].getAttribute('data-series');
			if(i){
				series[i] = {'shapes':[]};
				series[i].series = serieskey[s];
			}
		}
		for(p = 0; p < pt.length; p++){
			s = parseInt(pt[p].getAttribute('data-series'));
			i = parseInt(pt[p].getAttribute('data-i'));
			pts[p] = {'el':pt[p],'series':s,'i':i,'tooltip':pt[p].querySelector('title').innerHTML};
			if(!series[s]) series[s] = {'shapes':[]};
			if(!series[s].pts) series[s].pts = [];
			if(!series[s].pts[i]) series[s].pts[i] = pts[p];
		}
		this.locked = 0;
		
		// A function for setting the x-value of a shape
		function setX(s,r,x){
			if(typeof x==="number") series[s].shapes[r].setAttribute('x',x);
		}

		this.reset = function(e){
			return this.clearSeries(e).clearTooltip(e);
		};
		this.setSeries = function(e){
			for(var s in series){
				if(s==this.locked) series[s].key.classList.add('series-lock');
				else series[s].key.classList.remove('series-lock');
			}
			this.highlightSeries(e);
			return this;
		};
		this.clearSeries = function(e){
			if(this.locked == 0){
				// Make a copy of the data
				e.data = JSON.parse(JSON.stringify(e.data));
				// Set the series to null
				e.data.series = null;
				this.highlightSeries(e);
				//e.target.blur();
			}
			return this;
		};
		this.toggleSeries = function(e){
			this.locked = (this.locked==e.data.series) ? 0 : e.data.series;
			this.setSeries(e);
			if(this.locked==0) this.clearSeries(e);
			return this;
		};
		this.highlightSeries = function(e){
			var selected,typ,origin,s,r,points;
			selected = el.querySelector('.series-'+e.data.series);
			typ = svg.getAttribute('data-type');
			if(typ == "stacked-bar-chart"){
				// Find the origin of the bars by just taking the x-value of the first one in the first series
				origin = parseFloat(serieskey[0].querySelector('rect').getAttribute('x'));
			}
			if(typ == "stacked-bar-chart"){
				for(s in series) series[s].shapes = series[s].series.querySelectorAll('rect');
			}
			for(s in series){
				points = series[s].series.querySelectorAll('circle,rect');

				// If it is a stacked bar chart we will change the left position and store that
				if(typ == "stacked-bar-chart"){
					// Find all the bars
					for(r = 0; r < series[s].shapes.length; r++){
						// Store the x-value if we haven't already done so
						if(!series[s].shapes[r].hasAttribute('data-x')) series[s].shapes[r].setAttribute('data-x',series[s].shapes[r].getAttribute('x')||0);
					}
				}

				// If we aren't locked we will highlight one series
				if(this.locked == 0){

					if(e.data.series==null || s==e.data.series){
						series[s].series.style.opacity = 1;
						// Simulate z-index by moving to the end
						if(typ == "stacked-bar-chart"){
							series[s].series.parentNode.appendChild(series[s].series);
						}
						// Make points selectable
						for(p = 0; p < points.length; p++) points[p].setAttribute('tabindex',0);
					}else{
						// Fade the unselected series
						series[s].series.style.opacity = 0.1;
						// Make points unselectable
						for(p = 0; p < points.length; p++) points[p].removeAttribute('tabindex');
					}

				}else{
					if(s==this.locked){
						series[s].series.style.opacity = 1.0;
						// Make points selectable
						for(p = 0; p < points.length; p++) points[p].setAttribute('tabindex',0);
					}else{
						series[s].series.style.opacity = 0.1;
						// Make points unselectable
						for(p = 0; p < points.length; p++) points[p].removeAttribute('tabindex');
					}
				}
				if(typ == "stacked-bar-chart"){
					// If it is a stacked bar chart we will change the left position and store that
					for(r = 0; r < series[s].shapes.length; r++){
						if(e.data.series===null){
							// Get the stored x-value
							// Update the x-values if we have them
							if(series[s].shapes[r].hasAttribute('data-x')) setX(s,r,parseFloat(series[s].shapes[r].getAttribute('data-x')));
						}else{
							// Update the x-value
							setX(s,r,origin);
						}
					}
				}

			}
			return this;
		};
		this.triggerTooltip = function(e){
			for(var i = 0; i < pts.length; i++){
				if(pts[i].el==e.target){
					return this.showTooltip(pts[i].series,pts[i].i);
				}
			}
			return this;
		};
		this.clearTooltip = function(e){
			if(this.tip && this.tip.parentNode) this.tip.parentNode.removeChild(this.tip);
			return this;
		};
		this.showTooltip = function(s,i){
			el.style.position = 'relative';

			if(this.locked > 0 && s!=this.locked) return this;
			var txt,bb,bbo,bbox,fill,selected,off,pad,wide,shift,typ,tip,box,arr,typ;

			wide = document.body.getBoundingClientRect().width;

			this.tip = el.querySelector('.tooltip');
			if(!this.tip){
				this.tip = document.createElement('div');
				this.tip.innerHTML = '<div class="inner" style="background:#b2b2b2;position:relative;transform:translate3d(50%,0,0);"></div><div class="arrow" style="position: absolute; width: 0; height: 0; border: 0.5em solid transparent; border-bottom: 0; left: 50%; top: calc(100% - 1px); transform: translate3d(-50%,0,0); border-color: transparent; border-top-color: green;"></div>';
				this.tip.classList.add('tooltip');
				add(this.tip,el);
			}

			// Set the contents
			txt = series[s].pts[i].tooltip.replace(/\\n/g,'<br />');

			fill = series[s].pts[i].el.getAttribute('fill');

			// Remove current selections
			selected = el.querySelectorAll('circle.selected, rect.selected');
			for(var j = 0; j < selected.length; j++) selected[j].classList.remove('selected');
			
			// Select this point
			series[s].pts[i].el.classList.add('selected');

			// Set the content
			this.tip.querySelector('.inner').innerHTML = txt;

			// Position the tooltip

			bb = series[s].pts[i].el.getBoundingClientRect();	// Bounding box of the element
			bbo = el.getBoundingClientRect(); // Bounding box of SVG holder

			typ = svg.getAttribute('data-type');
			tip = this.tip;
			box = this.tip.querySelector('.inner');
			arr = this.tip.querySelector('.arrow');
			off = 4;
			pad = 8;
			if(typ=="bar-chart" || typ=="stacked-bar-chart") off = bb.height/2;

			tip.setAttribute('style','position:absolute;left:'+(bb.left + bb.width/2 - bbo.left).toFixed(2)+'px;top:'+(bb.top + bb.height/2 - bbo.top).toFixed(2)+'px;display:'+(txt ? 'block':'none')+';z-index:10000;transform:translate3d(-50%,calc(-100% - '+off+'px),0);');
			box.style.background = fill;
			box.style.transform = 'none';
			arr.style['border-top-color'] = fill;
			tip.style.color = contrastColour(fill);

			// Limit width of tooltip to window width - 2*pad
			tip.style.maxWidth = (tip.offsetWidth.width > wide ? 'calc(100% - '+(2*pad)+'px)' : 'auto');

			// Find out where the tooltip is now
			bbox = tip.getBoundingClientRect();

			// Set tooltip transform
			// If we were to just position the overall tooltip then shift the contents, we 
			// gain a horizontal scroll bar on the page when the tooltip is off the right-hand-side.
			// Instead we calculate the required shift and apply it to the tooltip and the 
			// arrow in opposite senses to keep the arrow where it needs to be
			shift = 0;
			if(bbox.left < pad) shift = (pad-bbox.left);
			else if(bbox.right > wide-pad) shift = -(bbox.right-wide+pad);
			tip.style.transform = 'translate3d('+(shift == 0 ? '-50%' : 'calc(-50% + ' + shift + 'px)')+',calc(-100% - '+off+'px),0)';
			arr.style.transform = 'translate3d(calc(-50% - ' + shift + 'px),0,0)';

			return this;
		};
		// Find the nearest point
		this.findPoint = function(e){
			var i,d,dx,dy,p,idx,min,dist,ok;
			min = 20;
			dist = 1e100;
			var matches = [];
			var typ = svg.getAttribute('data-type');

			for(s in series){
				if(series[s]){
					ok = true;
					if(this.locked > 0 && s!=this.locked) ok = false;
					if(ok){
						dist = 1e100;
						d = -1;
						idx = -1;
						for(i = 0; i < series[s].pts.length; i++){
							p = series[s].pts[i].el.getBoundingClientRect();
							if(typ=="category-chart"){
								dx = Math.abs((p.x+p.width/2)-e.clientX);	// Find distance from circle centre to cursor
								dy = Math.abs((p.y+p.width/2)-e.clientY);
								if(dy < min && dy < dist){
									idx = i;
									dist = dy;
									d = Math.sqrt(dx*dx + dy*dy);
								}
							}else if(typ=="line-chart"){
								dx = Math.abs((p.x+p.width/2)-e.clientX);	// Find distance from circle centre to cursor
								dy = Math.abs((p.y+p.width/2)-e.clientY);
								if(dx < min && dx < dist){
									idx = i;
									dist = dx;
									d = Math.sqrt(dx*dx + dy*dy);
								}
							}else if(typ=="bar-chart"){
								// As the bars run horizontally, we just check if the vertical position lines up with a bar
								if(e.clientY >= p.top && e.clientY <= p.top+p.height){
									idx = i;
								}
							}else if(typ=="stacked-bar-chart"){
								if(s==this.locked){
									// If only one is selected we just check the vertical position
									if(e.clientY >= p.top && e.clientY <= p.top+p.height) idx = i;									
								}else{
									// Check if the vertical position lines up with a bar and the horizontal position is within the bar
									if(e.clientY >= p.top && e.clientY <= p.top+p.height && e.clientX >= p.left && e.clientX <= p.left+p.width) idx = i;
								}
							}
						}
						if(idx >= 0){
							matches.push({'dist':d,'distx':dist,'pt':series[s].pts[idx]});
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
		};
		if(key){
			// We build an HTML version of the key
			var newkey = document.createElement('div');
			newkey.classList.add('legend');
			el.insertBefore(newkey, el.firstChild);

			var lbl = document.createElement('span');
			lbl.innerHTML = "Key:";
			newkey.appendChild(lbl);

			var keyseries = key.querySelectorAll('.data-series');
			var keyitem,icon,txt;
			for(s = 0; s < keyseries.length; s++){
				// Create a key item <div>
				keyitem = document.createElement('div');
				series[keyseries[s].getAttribute('data-series')].key = keyitem;
				keyitem.classList.add('legend-item');
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
				add(keyseries[s],icon);
				setAttr(keyseries[s],{'transform':''});
				setAttr(icon,{'width':17*1.5,'height':17,'viewBox':'0 0 '+(17*1.5)+' 17'});
				setAttr(keyitem,{'data-series':keyseries[s].getAttribute('data-series'),'tabindex':0,'title':'Highlight series: '+txt.innerHTML});

				addEv('mouseover',keyitem,{'this':this,'series':keyseries[s].getAttribute('data-series')},this.highlightSeries);
				addEv('keydown',keyitem,{'this':this,'series':keyseries[s].getAttribute('data-series')},function(e){
					if(e.keyCode==13){
						this.toggleSeries(e);
					}
				});
				addEv('click',keyitem,{'this':this,'series':keyseries[s].getAttribute('data-series')},this.toggleSeries);
				addEv('mouseout',keyitem,{'this':this,'series':null},this.clearSeries);
			}
			// Hide the original key
			key.style.display = 'none';
			addEv('mouseleave',el,{'this':this,'s':''},this.reset);
			addEv('mousemove',svg,{'this':this},this.findPoint);
		}
		if(pts){
			for(p = 0; p < pts.length; p++){
				addEv('focus',pts[p].el,{'this':this},this.triggerTooltip);
			}
		}
		return this;
	}

	root.OI.InteractiveChart = function(el){ return new InteractiveChart(el); };



	// Convert to sRGB colorspace
	// https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
	function sRGBToLinear(v){
		v /= 255;
		if (v <= 0.03928) return v/12.92;
		else return Math.pow((v+0.055)/1.055,2.4);
	}
	function h2d(h) {return parseInt(h,16);}
	// https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
	function relativeLuminance(rgb){ return 0.2126 * sRGBToLinear(rgb[0]) + 0.7152 * sRGBToLinear(rgb[1]) + 0.0722 * sRGBToLinear(rgb[2]); }
	// https://www.w3.org/TR/UNDERSTANDING-WCAG20/visual-audio-contrast-contrast.html#contrast-ratiodef
	function contrastRatio(a, b){
		var L1 = relativeLuminance(a);
		var L2 = relativeLuminance(b);
		if(L1 < L2){
			var temp = L2;
			L2 = L1;
			L1 = temp;
		}
		return (L1 + 0.05) / (L2 + 0.05);
	}	
	function contrastColour(c){
		var rgb = [];
		if(c.indexOf('#')==0){
			rgb = [h2d(c.substring(1,3)),h2d(c.substring(3,5)),h2d(c.substring(5,7))];
		}else if(c.indexOf('rgb')==0){
			var bits = c.match(/[0-9\.]+/g);
			if(bits.length == 4) this.alpha = parseFloat(bits[3]);
			rgb = [parseInt(bits[0]),parseInt(bits[1]),parseInt(bits[2])];
		}
		var cols = {
			"black": [0, 0, 0],
			"white": [255, 255, 255],
		};
		var maxRatio = 0;
		var contrast = "white";
		for(var col in cols){
			var contr = contrastRatio(rgb, cols[col]);
			if(contr > maxRatio){
				maxRatio = contr;
				contrast = col;
			}
		}
		if(maxRatio < 4.5){
			console.warn('Text contrast poor ('+maxRatio.toFixed(1)+') for %c'+c+'%c','background:'+c+';color:'+contrast,'background:none;color:inherit;');
		}else if(maxRatio < 7){
			//console.warn('Text contrast good ('+maxRatio.toFixed(1)+') for %c'+c+'%c','background:'+c+';color:'+contrast,'background:none;color:inherit;');
		}
		return contrast;
	}
	if(!root.OI) root.OI = {};
	if(!root.OI.ready){
		OI.ready = function(fn){
			// Version 1.1
			if(document.readyState != 'loading') fn();
			else document.addEventListener('DOMContentLoaded', fn);
		};
	}
})(window || this);

OI.ready(function(){
	var charts = document.querySelectorAll('.chart');
	for(var i = 0; i < charts.length; i++){
		OI.InteractiveChart(charts[i]);
	}
});