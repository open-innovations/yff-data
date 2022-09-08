import { document } from '/src/_lib/oi/document.ts';
import { textLength } from '/src/_lib/oi/text.js';
import { colourScales, contrastColour } from '/src/_lib/oi/colour.js';

const ns = 'http://www.w3.org/2000/svg';

/*
	Ranking Chart v 0.2
	
	This will make a rankings chart where each row is turned into a line
	that moves up and down depending on the columns used for rankings.
	
	First define the column name that is used to make each series:
		by: "Country"

	To colour the series by a value, you can use the following options:
		scale: "YFF"
		scaleby: "Ranks→2018"
		min: 1
		max: 38
		
	Alternatively, a colour string can be given in the CSV file e.g.:
		scaleby: "Colour"

	It is also possible to change the amount of curvature using 0-1:
		curvature: 0 (straight lines)
		curvature: 1 (fully curvy)

	Optional rank circles can be shown by setting the value of circles e.g.
		circles: 1 (full size)
		circles: 0.5 (half the size)
		circles: 0 (not shown)
*/

export function RankingChart(config,csv){
	
	var svg,id,seriesgroup;

	// Set default options
	this.opt = {
		'type': 'ranking',
		'padding':{'left':0,'top':0,'right':0,'bottom':0},
		'width': 1024,
		'height': 640,
		'font-size': 17,
		'font-family':'"Century Gothic",sans-serif',
		'curvature': 1,
		'circles': 0
	};

	// Update defaults with custom config
	mergeDeep(this.opt,config);

	// Create a random ID number
	id = Math.round(Math.random()*1e8);
	
	// Limit curvature to range
	this.opt.curvature = Math.max(0,Math.min(1,this.opt.curvature));

	this.init = function(){

		var svgopt,clip,rect;

		// Create SVG container
		if(!svg){
			svg = svgEl('svg');
			svgopt = {'xmlns':ns,'version':'1.1','viewBox':'0 0 '+this.opt.width+' '+this.opt.height,'overflow':'visible','style':'max-width:100%;','preserveAspectRatio':'none','data-type':this.opt.type};
			setAttr(svg,svgopt);
			clip = svgEl("clipPath");
			setAttr(clip,{'id':'clip-'+id});
			//add(clip,svg); // Clip to graph area
			rect = svgEl("rect");
			setAttr(rect,{'x':0,'y':0,'width':this.opt.width,'height':this.opt.height});
			add(rect,clip);
			seriesgroup = svgEl('g');
			seriesgroup.classList.add('data');
		}
	};

	this.getSVG = function(){
		this.draw();
		return svg.outerHTML;
	};

	this.draw = function(){

		var dy,y,yv,x,xv,h,w,pad,xoff,yoff,xlbl,dx,delta,r,s,lbl,g,series,fs,v,i,ok,data,path,oldx,oldy,oldrank,rank,orderby,reverse,bg,talign,circle,radius,txt;

		fs = this.opt['font-size'];


		// Create an array of series
		series = [];
		// Loop over the "by" column
		for(r = 0; r < csv.columns[config.by].length; r++){

			// Construct columns for this series
			data = [];
			ok = true;
			for(i = 0; i < config.columns.length; i++){
				// Get the value for this column
				v = csv.rows[r][config.columns[i].name];
				// If the value is a number we use it
				if(typeof v==="number" && !isNaN(v)){
					data[i] = v;
				}else{
					// A bad number means we will ignore this series
					ok = false;
					data[i] = 0;
				}
			}
			
			// If there are values for this series we add the structure for it
			if(ok){

				s = {'title':csv.columns[config.by][r],'data':data,'row':r};

				g = svgEl('g');
				g.classList.add('series');
				s.g = g;
				svg.appendChild(g);

				lbl = svgEl('text');
				lbl.innerHTML = s.title;
				setAttr(lbl,{'dominant-baseline':'middle','text-anchor':'end'});
				s.label = lbl;
				g.appendChild(lbl);

				path = svgEl('path');
				setAttr(path,{'stroke-width':4,'stroke':'red','fill':'transparent'});
				g.appendChild(path);
				s.path = path;

				series.push(s);
			}
		}

		// There's no guarantee that the order of the rows in the CSV matches the first ranking column
		if(config.columns.length > 0){
			// Let's sort the series by the first column
			orderby = csv.colnum[config.columns[0].name];
			// Set the order
			reverse = true;
			// Sort the array
			series = series.sort(function(a, b){
				if(reverse) return a.data[orderby] > b.data[orderby] ? 1 : -1;
				else return a.data[orderby] < b.data[orderby] ? 1 : -1;
			});
		}

		// Calculate some dimensions
		yoff = this.opt['font-size']*1.2;
		delta = (1/6);
		w = this.opt.width;
		h = this.opt.height - yoff;
		dy = h / series.length;
		radius = dy*this.opt.circles*0.5;

		// Shrink the font if the y-spacing is too small
		fs = Math.min(dy,fs);

		// Set the label padding (both sides)
		pad = 5;

		xoff = 0;
		for(s = 0; s < series.length; s++){
			xoff = Math.max(xoff,textLength(series[s].title,fs,"standard",this.opt['font-family'].split(/,/)[0].replace(/\"/g,"")));
		}
		xlbl = xoff + pad;
		xoff = xlbl + pad + radius;

		dx = (w - xoff - radius)/(config.columns.length-1);


		// Let's make some column headers
		for(i = 0; i < config.columns.length; i++){
			lbl = svgEl('text');
			lbl.innerHTML = config.columns[i].rename||config.columns[i].name;
			talign = 'middle';
			if(i==0) talign = 'start';
			if(i==config.columns.length-1) talign = 'end';
			setAttr(lbl,{'x':(xoff + i*dx + (i==0 ? -radius : (i==config.columns.length-1 ? +radius : 0))),'y': fs*0.2,'font-size':fs+'px','dominant-baseline':'hanging','text-anchor':talign});
			svg.appendChild(lbl);
		}


		function getY(v){
			return yoff + ( (v+1)*dy - dy/2 );
		}
		
		// Update label positions and font size
		for(s = 0; s < series.length; s++){

			// Get colour
			bg = 'black';
			if(config.scaleby && csv.rows[series[s].row]){
				// If a "scaleby" is set, we will use that column to define the colours
				// It doesn't have to be one of the data columns
				bg = csv.rows[series[s].row][config.scaleby];
			}else{
				if(config.columns[0].name && csv.columns[config.columns[0].name]){
					// Use the first column provided
					bg = csv.columns[config.columns[0].name][series[s].row];
				}else{
					// Default to the first data value
					bg = series[s].data[0]||0;
				}
			}
			if(typeof bg==="number") bg = colourScales.getColourFromScale(config.scale||'Viridis', bg, config.min, config.max);
			
			// Build path and circles
			v = 0;
			y = getY(s);
			setAttr(series[s].label,{'x':xlbl	,'y':y,'font-size':fs+'px'});
			

			rank = series[s].data[0];
			oldx = xoff;
			oldrank = rank;
			oldy = getY(s);

			// Make path for this series
			path = "";
			for(i = 0; i < series[s].data.length; i++){
				rank = series[s].data[i];
				yv = getY(rank-1);
				xv = xoff + (i)*dx;
				if(i == 0){
					path += 'M'+xv.toFixed(2)+','+yv.toFixed(2);
				}else{
					path += 'C'+(oldx+(dx/2)*this.opt.curvature).toFixed(2)+','+oldy.toFixed(2)+','+(xv-(dx/2)*this.opt.curvature).toFixed(2)+','+yv.toFixed(2)+','+(xv).toFixed(2)+','+yv.toFixed(2);
				}
				
				if(this.opt.circles){
					circle = svgEl('circle');
					setAttr(circle,{'cx':xv.toFixed(2),'cy':yv.toFixed(2),'r':radius,'fill':bg});
					series[s].g.appendChild(circle);

					txt = svgEl('text');
					txt.innerText = rank;
					setAttr(txt,{'font-size':fs+'px','fill':contrastColour(bg),'x':xv.toFixed(2),'y':yv.toFixed(2),'dominant-baseline':'central','text-anchor':'middle','font-size':(radius*1)+'px'});
					series[s].g.appendChild(txt);
				}
				
				oldy = yv;
				oldx = xv;
				oldrank = rank;
			}


			setAttr(series[s].path,{'d':path,'stroke':bg,'stroke-width':(dy*0.5).toFixed(2)});
		}

		return this;
	};

	this.init();

	return this;
}

// Sort the data
function sortBy(arr,i,reverse){
	yaxis = i;
	return arr.sort(function (a, b) {
		if(reverse) return a[i] > b[i] ? 1 : -1;
		else return a[i] < b[i] ? 1 : -1;
	});
}
// Recursively merge properties of two objects 
function mergeDeep(obj1, obj2){
	for(var p in obj2){
		try{
			if(obj2[p].constructor==Object) obj1[p] = mergeDeep(obj1[p], obj2[p]);
			else obj1[p] = obj2[p];
		}catch(e){ obj1[p] = obj2[p]; }
	}
	return obj1;
}
function qs(el,t){ return el.querySelector(t); }
function add(el,to){ return to.appendChild(el); }
function clone(a){ return JSON.parse(JSON.stringify(a)); }
function svgEl(t){ return document.createElement(t);/*return document.createElementNS(ns,t);*/ }
function setAttr(el,prop){
	for(var p in prop) el.setAttribute(p,prop[p]);
	return el;
}