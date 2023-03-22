/*
	Open Innovations SVG map Interactivity v0.1
	Helper function that find ".map.svg-map" elements 
	looks for <path> in the ".data-layer" group,
	then creates a tooltip
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

	function add(el,to){ return to.appendChild(el); }

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

	function InteractiveSVGMap(el){
		var svg,pt,pts,tt,p;

		svg = el.querySelector('svg');
		pt = svg.querySelectorAll('.data-layer path');
		pts = [];

		this.showTooltip = function(e){
			//console.log('showTooltip',e.data,this);
			el.style.position = 'relative';

			var txt,bb,bbo,fill,hsv,hsl,selected,off;
			this.tip = el.querySelector('.tooltip');
			if(!this.tip){
				this.tip = document.createElement('div');
				this.tip.innerHTML = '<div class="inner" style="background: #b2b2b2;position:relative;"></div><div class="arrow" style="position: absolute; width: 0; height: 0; border: 0.5em solid transparent; border-bottom: 0; left: 50%; top: calc(100% - 1px); transform: translate3d(-50%,0,0); border-color: transparent; border-top-color: green;"></div>';
				addClasses(this.tip,['tooltip']);
				add(this.tip,el);
			}

			// Set the contents
			txt = e.data.title;

			// Get the fill colour
			fill = e.data.el.getAttribute('fill');

			this.tip.querySelector('.inner').innerHTML = (txt);

			// Position the tooltip
			bb = e.data.el.getBoundingClientRect();	// Bounding box of the element
			bbo = el.getBoundingClientRect(); // Bounding box of SVG holder

			var typ = svg.getAttribute('data-type');
			off = 4;
			//if(typ=="hex-map") off = bb.height/2;
			
			this.tip.setAttribute('style','position:absolute;left:'+(bb.left + bb.width/2 - bbo.left).toFixed(2)+'px;top:'+(bb.top + bb.height/2 - bbo.top).toFixed(2)+'px;transform:translate3d(-50%,calc(-100% - '+off+'px),0);display:'+(txt ? 'block':'none')+';');
			this.tip.querySelector('.inner').style.background = fill;
			this.tip.querySelector('.arrow').style['border-top-color'] = fill;
			this.tip.style.color = contrastColour(fill);

			return this;
		};

		this.reset = function(e){
			return this.clearTooltip(e);
		};
		this.clearTooltip = function(e){
			if(this.tip && this.tip.parentNode) this.tip.parentNode.removeChild(this.tip);
			return this;
		};
		for(p = 0; p < pt.length; p++){
			tt = pt[p].querySelector('title')
			pts[p] = {'el':pt[p],'tooltip':(tt ? tt.innerHTML : "")};
			addEv('mouseover',pt[p],{'this':this,'title':pts[p].tooltip,'el':pt[p]},this.showTooltip);
		}
		addEv('mouseleave',el,{'this':this,'s':''},this.reset);

		return this;
	}

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
	root.OI.contrastColour = contrastColour;
	root.OI.InteractiveSVGMap = function(el){ return new InteractiveSVGMap(el); };

})(window || this);

OI.ready(function(){
	var svgs = document.querySelectorAll('.map.svg-map, .map.hex-map');
	for(var i = 0; i < svgs.length; i++){
		OI.InteractiveSVGMap(svgs[i]);
	}
});