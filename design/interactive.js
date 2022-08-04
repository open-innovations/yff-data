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
			txt = series[s][i].tooltip.replace(/\n/g,"<br />");

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
})(window || this);