var ns = 'http://www.w3.org/2000/svg';
function CategoryChart(config,csv){
	if(!config) config = {};
	var lbl,opt,id,svg,series,axes,xmin,ymin,xmax,ymax,w,h,i,ax,key;
	lbl = 'categorychart';

	opt = {
		'padding':{'left':0,'top':0,'right':0,'bottom':0},
		'left':0,
		'right':0,
		'top':0,
		'bottom':0,
		'tick':5,
		'font-size': 16,
		'key':{
			'show':false,
			'border':{'stroke':'black','stroke-width':1,'fill':'none'},
			'text':{'text-anchor':'start','dominant-baseline':'hanging','font-weight':'bold','fill':'black','stroke-width':0,'font-family':'sans-serif'}
		},
		'axis':{'x':{'padding':10,'grid':{'show':true,'stroke':'#aaa'},'labels':{}},'y':{'padding':10,'labels':{}}},
		'duration': '0.3s'
	};
	mergeDeep(opt,config);


	w = opt.width||960;
	h = opt.height||600;
	id = Math.round(Math.random()*1e8);

	this.updatePadding = function(){
		var l,pad,len,ax,lines,align;
		// Work out padding
		pad = {'l':0,'t':0,'b':0,'r':0};
		for(ax in opt.axis){
			// Work out x-axis padding
			for(l in opt.axis[ax].labels){
				len = 0;
				// Split the label by any new line characters
				lines = opt.axis[ax].labels[l].label.split(/\n/g);
				if(ax=="x"){
					// Length is based on the 
					len = (opt.axis[ax].title && opt.axis[ax].title.label!="" ? opt['font-size']*1.5 : 0) + (opt['font-size']*lines.length) + opt.tick + (opt.axis[ax].labels[l].offset||opt.axis[ax].padding||0);
				}else{
					// Work out the longest line
					for(i = 0; i < lines.length; i++){
						// Roughly calculate the length in pixels
						len = Math.max(len,(opt.axis[ax].title && opt.axis[ax].title.label!="" ? opt['font-size']*1.5 : 0) + opt['font-size']*lines[i].length*0.5 + opt.tick + opt.axis[ax].padding);
					}
				}
				align = opt.axis[ax].labels[l].align||(ax=="x" ? "bottom":"left");
				if(ax=="x"){
					if(align=="bottom") pad.b = Math.max(pad.b,len);
					else pad.t = Math.max(pad.t,len);
				}else{
					if(align=="left") pad.l = Math.max(pad.l,len);
					else pad.r = Math.max(pad.r,len);
				}
			}
		}
		opt.left = opt.padding.left + pad.l;
		opt.right = opt.padding.right + pad.r;
		opt.top = opt.padding.top + pad.t;
		opt.bottom = opt.padding.bottom + pad.b;
		return this;
	};

	// Create SVG container
	if(!svg){
		svg = svgEl('svg');
		var svgopt = {'xmlns':ns,'version':'1.1','viewBox':'0 0 '+w+' '+h,'overflow':'visible','style':'max-width:100%;','preserveAspectRatio':'none'};
		if(opt.width) svgopt.width = opt.width;
		if(opt.height) svgopt.height = opt.height;
		setAttr(svg,svgopt);
		var defs = svgEl('defs');
		add(defs,svg);
		var clip = svgEl("clipPath");
		setAttr(clip,{'id':'clip-'+id});
		add(clip,svg);
		var rect = svgEl("rect");
		setAttr(rect,{'x':0,'y':0,'width':w,'height':h});
		add(rect,clip);
	}

	function getXY(x,y){
		x = opt.left + ((x-xmin)/(xmax-xmin))*(w-opt.left-opt.right);
		y = opt.top + (1-(y-ymin)/(ymax-ymin))*(h-opt.bottom-opt.top);
		return {x:x,y:y};
	}
	function updateRange(){
		xmin = 1e100;
		ymin = 1e100;
		xmax = -1e100;
		ymax = -1e100;			
		// Calculate graph range
		if(typeof axes.x.getProperty('min')==="number") xmin = axes.x.getProperty('min');
		if(typeof axes.x.getProperty('max')==="number") xmax = axes.x.getProperty('max');
		if(typeof axes.y.getProperty('min')==="number") ymin = axes.y.getProperty('min');
		if(typeof axes.y.getProperty('max')==="number") ymax = axes.y.getProperty('max');
		axes.x.updateRange(xmin,xmax,ymin,ymax);
		axes.y.updateRange(xmin,xmax,ymin,ymax);
	}

	// Axes
	// Build x-axis labels
	for(i = 0; i < opt.axis.x.ticks.length; i++) opt.axis.x.labels[opt.axis.x.ticks[i].value] = opt.axis.x.ticks[i];
	// Set y-axis range for categories
	opt.axis.y.min = -0.5;
	opt.axis.y.max = csv.rows.length-0.5;
	// Build y-axis labels
	for(i = 0 ; i < csv.rows.length; i++){
		opt.axis.y.labels[csv.rows.length-i-1.5] = {'label':'','grid':true};
		opt.axis.y.labels[csv.rows.length-i-1] = {'label':csv.rows[i][config.category].replace(/\\n/g,"\n"),'ticksize':0,'grid':false,'data':{'category':csv.rows[i][config.category]}};
		opt.axis.y.labels[csv.rows.length-i-0.5] = {'label':'','grid':true};
	}
	this.updatePadding();
	axes = {x:new Axis("x",opt.left,w-opt.right-opt.left),y:new Axis("y",opt.bottom,h-opt.top-opt.bottom)};
	opt.axis.x.getXY = getXY;
	opt.axis.y.getXY = getXY;
	opt.axis.x.width = w;
	opt.axis.y.width = w;
	opt.axis.x.height = h;
	opt.axis.y.height = h;
	for(ax in axes) axes[ax].setProperties(opt.axis[ax]||{}).addTo(svg);

	// Series
	series = [];
	var data,datum,label;
	for(var s = 0; s < config.series.length; s++){

		mergeDeep(config.series[s],{
			'line':{'show':false},
			'points':{'size':4, 'color': (config.series[s].colour||'black')},
			'errors':{'stroke':(config.series[s].colour||'black'),'stroke-width':2},
			'id':id,
			'lbl':lbl,
			'getXY':getXY
		});
		data = [];
		for(i = 0; i < csv.rows.length; i++){
			categoryoffset = csv.rows.length-i-1;
			seriesoffset = (config.series.length-s-1.5)*(0.8/config.series.length);
			label = config.series[s].title+"\n"+csv.columns[config.category][i].replace(/\\n/g,"")+': '+csv.columns[config.series[s].value][i];
			label += (csv.columns[config.series[s].errors[0]][i]==csv.columns[config.series[s].errors[1]][i] ? ' ±'+csv.columns[config.series[s].errors[0]][i] : ' (+'+csv.columns[config.series[s].errors[1]][i]+' / -'+csv.columns[config.series[s].errors[0]][i]+')');
			if(config.series[s].label && csv.columns[config.series[s].label]) label = csv.columns[config.series[s].label][i];
			datum = {'x':csv.columns[config.series[s].value][i],'y':categoryoffset+seriesoffset,'error':{'x':[csv.columns[config.series[s].errors[0]][i],csv.columns[config.series[s].errors[1]][i]]},'title':label};
			datum.data = {'category':csv.columns[config.category][i],'series':config.series[s].title};
			data.push(datum);
		}

		series.push(new Series(s,config.series[s],data));
		series[series.length-1].addTo(svg);
	}

	this.getSVG = function(){
		return svg.outerHTML;
	};


	this.draw = function(){
		var t,u,i,fs,pd,hkey,wkey,x,y,s,text,line,circ,p,cl,po;

		updateRange();

		// Update axes
		for(ax in axes) axes[ax].update();

		t = '<style>';
		t += '\t.'+lbl+'-series circle { transition: transform '+opt.duration+' linear, r '+opt.duration+' linear; }\n';
		t += '\t.'+lbl+'-series circle:focus { stroke-width: 4; }\n';
		t += '\t.'+lbl+'-series:hover path.line, .'+lbl+'-series.on path.line { cursor:pointer; }\n';
/*
		for(i = 0; i < series.length; i++){
			series[i].draw().addTo(svg);
			t += '\t.'+lbl+'-series-'+(i+1)+':hover path.line, .'+lbl+'-series-'+(i+1)+'.on path.line { stroke-width: '+(series[i].getProperty('stroke-width-hover')||4)+'; }\n';
		}
*/
		if(opt.key.show){
			fs = opt['font-size']||16;
			pd = opt.key.padding||5;
			hkey = (opt.key.label ? 1:0)*fs +(2*pd) + (series.length*fs);
			x = 0;
			y = 0;
			if(!key){
				key = {'el':svgEl("g"),'g':[],'border':svgEl("rect")};
				key.el.classList.add('key');
				setAttr(key.border,{'x':0,'y':opt.top,'width':w,'height':hkey});
				if(typeof opt.key.border==="object"){
					for(p in opt.key.border) key.border.setAttribute(p,opt.key.border[p]);
				}
				add(key.border,key.el);
				add(key.el,svg);
			}

			wkey = 0;
			for(s = 0; s < series.length; s++){
				if(!key.g[s]){
					key.g[s] = svgEl("g");
					key.g[s].setAttribute(lbl+'-series',s);
					// Update class of line
					cl = [lbl+'-series',lbl+'-series-'+(s+1)];
					if(series[s].getProperty('class')) cl.concat(series[s].getProperty('class').split(/ /));
					addClasses(key.g[s],cl);

					add(key.g[s],key.el);
				}
				key.g[s].innerHTML = '<text><tspan dx="'+(fs*2)+'" dy="0">'+(series[s].getProperty('title')||"Series "+(s+1))+'</tspan></text><path d="M0 0 L 1 0" class="line" class="" stroke-width="3" stroke-linecap="round"></path><circle cx="0" cy="0" r="5" fill="silver"></circle>';
				setAttr(key.g[s].querySelector('tspan'),series[s].getProperty('attr'));
				wkey = Math.max(wkey,key.g[s].getBoundingClientRect().width);
			}

			if(!opt.key.position) opt.key.position = 'top right';
			po = opt.key.position.split(/ /);

			x = y = 0;
			for(u = 0; u < po.length; u++){
				if(po[u]=="left") x = opt.left+pd;
				else if(po[u]=="right") x = (w-opt.right-wkey-pd);
				else if(po[u]=="top") y = opt.top+pd;
				else if(po[u]=="bottom") y = h-opt.bottom-pd-hkey;
			}
			setAttr(key.border,{'x':x,'width':wkey+pd,'y':y});
			y += pd;
			x += pd;
			for(s = 0; s < series.length; s++){
				text = qs(key.g[s],'text');
				line = qs(key.g[s],'path');
				circ = qs(key.g[s],'circle');
				text.setAttribute('x',x);
				text.setAttribute('y',(y + s*fs + fs*0.2));
				if(typeof opt.key.text==="object"){
					for(p in opt.key.text) text.setAttribute(p,opt.key.text[p]);
				}
				line.setAttribute('d','M'+(x)+','+(y+(0.5+s)*fs)+' l '+(fs*1.5)+' 0');
				p = series[s].getProperties();
				setAttr(circ,{'cx':(x+fs*0.75),'cy':(y+(0.5+s)*fs),'fill':(p.points.color||""),'stroke-width':p.points['stroke-width']||0,'stroke':p.points.stroke||""});
				if(p.line.color) line.setAttribute('stroke',p.line.color);
			}
		}
		t += '\t.'+lbl+'-grid.'+lbl+'-grid-x .'+lbl+'-grid-title,.'+lbl+'-grid.'+lbl+'-grid-y .'+lbl+'-grid-title { text-anchor: middle; dominant-baseline: central; }\n';
		t += '\t.'+lbl+'-grid.'+lbl+'-grid-y text { dominant-baseline: '+((opt.axis.y.labels ? opt.axis.y.labels.baseline : '')||"middle")+'; }\n';
		t += '\t.'+lbl+'-tooltip { background: black; color: white; padding: 0.25em 0.5em; margin-top: -1em; transition: left 0.1s linear, top 0.1s linear; border-radius: 4px; white-space: nowrap; }\n';
		t += '\t.'+lbl+'-tooltip::after { content: ""; position: absolute; bottom: auto; width: 0; height: 0; border: 0.5em solid transparent; left: 50%; top: 100%; transform: translate3d(-50%,0,0); border-color: transparent; border-top-color: black; }\n';
		t += '\t</style>\n';
		if(defs) defs.innerHTML = t;

		// Update series
		for(i = 0; i < series.length; i++){
			console.log('draw series',i,series[i]);
			series[i].update().addTo(svg);
		}
		return this;
	};
	return this;
}
function Axis(ax,from,to,attr){

	var opt,lbl,fs,xmin,xmax,ymin,ymax;
	
	opt = {
		'left': 0,
		'right': 0,
		'top': 0,
		'bottom': 0,
		'line':{'show':true,stroke:'black','stroke-width':1,'stroke-linecap':'round','stroke-dasharray':''},
		'grid':{'show':false,'stroke':'black','stroke-width':1,'stroke-linecap':'round','stroke-dasharray':''},
		title:{},
		ticks:{'show':true},
		labels:{},
		'getXY':function(x,y){ return {x:x,y:y}; }
	};
	mergeDeep(opt,attr);
	lbl = opt.label||'axis';
	this.ticks = {};
	this.line = {};
	this.el = svgEl("g");
	addClasses(this.el,[lbl+'-grid',lbl+'-grid-'+ax]);
	this.title = svgEl("text");
	this.title.classList.add(lbl+'-grid-title');
	add(this.title,this.el);
	fs = opt['font-size']||16;
	opt.padding = 4;
	xmin = ymin = xmax = ymax = 0;
	this.addTo = function(svg){
		add(this.el,svg);
		return this;
	};
	this.updateRange = function(xmn,xmx,ymn,ymx){
		xmin = xmn;
		xmax = xmx;
		ymin = ymn;
		ymax = ymx;
		return this;
	};
	this.setProperties = function(myopt){
		mergeDeep(opt,myopt);
		return this;
	};
	this.getProperty = function(pid){
		if(opt.hasOwnProperty(pid)) return opt[pid];
		else return null;
	};
	this.update = function(){
		var t,x,y,pos,len,align,talign,baseline,xsign,ysign,lines,l,d;
		if(!opt.labels) opt.labels = {};
		this.title.innerHTML = opt.title.label||"";
		x = (ax=="x" ? (opt.left + (opt.width-opt.right-opt.left)/2):fs/2);
		y = (ax=="y" ? (opt.top + (opt.height-opt.top-opt.bottom)/2):(opt.height-fs/2));
		setAttr(this.title,{'x':x,'y':y,'transform':(ax=="y"?'rotate(-90,'+x+','+y+')':'')});
		this.el.removeAttribute('style');
		// Check if we need to add a line
		if(!this.line.el){
			this.line.el = svgEl("path");
			this.line.el.classList.add('line');
			this.line.el.setAttribute('vector-effect','non-scaling-stroke');
			// Add it to the element
			add(this.line.el,this.el);
			// Create an animation for the line
			this.line.animate = new Animate(this.line.el,{'duration':opt.duration});
		}
		pos = [{x:(opt.left-0.5),y:(opt.height-opt.bottom-0.5)},{x:(ax=="x" ? (opt.width-opt.right) : (opt.left-0.5)),y:(ax=="x" ? (opt.height-opt.bottom-0.5) : (opt.top-0.5))}];
		this.line.animate.set({'d':{'from':'','to':pos}});
		setAttr(this.line.el,{'d':pos,'style':(opt.line.show ? 'display:block':'display:none'),'stroke':opt.line.stroke,'stroke-width':opt.line['stroke-width'],'stroke-dasharray':opt.line['stroke-dasharray']});
		// Loop over existing ticks removing any that no longer exist
		for(t in this.ticks){
			if(t && !opt.ticks.show){
				if(this.ticks[t].line) this.ticks[t].line.parentNode.removeChild(this.ticks[t].line);
				if(this.ticks[t].text) this.ticks[t].text.parentNode.removeChild(this.ticks[t].text);
				delete this.ticks[t];
			}
		}
		// Go through axis label values in order
		var keys = Object.keys(opt.labels);
		var pd,a,b,tspan;
		for(t of keys.sort()){
			// Check if this tick exists
			if(typeof t!=="undefined"){

				if(typeof opt.labels[t]==="undefined") opt.labels[t] = {'label':''};
				align = opt.labels[t].align||(ax=="x" ? "bottom" : "left");
				talign = opt.labels[t]['text-anchor']||(ax=="y" ? (align=="left" ? "end":"start") : "middle");
				baseline = (ax=="x" ? ((align=="bottom") ? "hanging" : "text-bottom") : "middle");
				len = (typeof opt.labels[t].ticksize==="number" ? opt.labels[t].ticksize:5);
				pd = (typeof opt.labels[t].offset==="number" ? opt.labels[t].offset : opt.padding);
				x = (ax=="x" ? parseFloat(t) : (align=="left" ? xmin:xmax));
				y = (ax=="x" ? (align=="bottom" ? ymin:ymax) : parseFloat(t));
				xsign = (opt.labels[t].align=="right" ? 1:-1);
				ysign = (opt.labels[t].align=="top" ? -1:1);

				if(ax=="x"){
					a = opt.getXY(parseFloat(t),(opt.grid.show||opt.labels[t].grid ? (align=="bottom" ? ymax:ymin) : (align=="bottom" ? ymin:ymax)));
					b = opt.getXY(parseFloat(t),(align=="bottom" ? ymin:ymax));
				}else{
					a = opt.getXY((opt.grid.show||opt.labels[t].grid ? (align=="left" ? xmax:xmin) : (align=="left" ? xmin:xmax)),parseFloat(t));
					b = opt.getXY((align=="left" ? xmin:xmax),parseFloat(t));
				}

				if((ax=="x" && (x<xmin || x>xmax)) || (ax=="y" && (y<ymin || y>ymax))){
					if(this.ticks[t]){
						if(this.ticks[t].g) this.ticks[t].g.setAttribute('style','display:none');
					}
				}else{
					if(!this.ticks[t]){
						this.ticks[t] = {'g':{'el':svgEl('g')},'text':{'el':svgEl('text')}};
						this.ticks[t].g.el.setAttribute('data',t);
						// Loop over this label's data attributes
						for(d in opt.labels[t].data){
							this.ticks[t].g.el.setAttribute('data-'+d,opt.labels[t].data[d]);
						}
						this.ticks[t].g.animate = new Animate(this.ticks[t].g.el,{duration:opt.duration});
						add(this.ticks[t].g.el,this.el);
						if(len>0){
							this.ticks[t].line = {'el':svgEl('line')};
							add(this.ticks[t].line.el,this.ticks[t].g.el);
						}
						this.ticks[t].text.el.setAttribute('text-anchor',(opt['text-anchor'] || talign));
						add(this.ticks[t].text.el,this.ticks[t].g.el);
					}else{
						if(this.ticks[t].line) this.ticks[t].line.el.removeAttribute('style');
						this.ticks[t].text.el.removeAttribute('style');
					}
					
					// Split the label by any new line characters and add each as a tspan
					lines = opt.labels[t].label.split(/\n/g);
					for(l = 0; l < lines.length; l++){
						tspan = svgEl('tspan');
						tspan.innerHTML = lines[l];
						if(ax=="x") setAttr(tspan,{'dy':fs*l,'x':0,'y':ysign*(len+pd)});
						if(ax=="y") setAttr(tspan,{'y':fs*((l-(lines.length-1)/2)),'x':xsign*(len+pd)});
						add(tspan,this.ticks[t].text.el);
					}

					// Set some text properties
					setAttr(this.ticks[t].text.el,{'stroke':opt.labels[t].stroke||"black",'stroke-width':opt.labels[t]['stroke-width']||0,'fill':opt.labels[t].fill||"black",'dominant-baseline':baseline});

					if(this.ticks[t].line){
						// Set the position/size of the line
						if(ax=="x") setAttr(this.ticks[t].line.el,{'x1':0,'x2':0,'y1':-xsign*len,'y2':-(b.y-a.y)});
						else if(ax=="y") setAttr(this.ticks[t].line.el,{'x1':-ysign*len,'x2':(a.x-b.x),'y1':0,'y2':0});
						// Set generic properties for the line
						setAttr(this.ticks[t].line.el,{'stroke':opt.grid.stroke,'stroke-width':opt.grid['stroke-width']||1,'stroke-dasharray':opt.grid['stroke-dasharray']||''});
					}
					this.ticks[t].g.animate.set({'transform':{'to':'translate('+b.x+','+b.y+')'}});
				}
			}
		}
		add(this.line.el,this.el); // simulate z-index
	};
	return this;
}
function Series(s,props,data){
	if(!props) return this;
	
	console.log('function Series',s,props,data);
	var id = props.id||Math.round(Math.random()*1e8);
	var lbl = props.lbl||"chart-series";
	var getXY = props.getXY;

	var opt,line,path,pts,o,label;
	opt = {points:{show:true,color:'black','stroke-linecap':'round','stroke':'black','stroke-width':0,'fill-opacity':1},line:{show:true,color:'#000000','stroke-width':4,'stroke-linecap':'round','stroke-linejoin':'round','stroke-dasharray':'','fill':'none'},'opt':props.opt||{}};
	line = {};
	path = "";
	pts = [];
	label = "";


	// Add the output to the SVG
	this.addTo = function(svg){
		add(this.el,svg);
		return this;
	};

	// Build group
	this.el = svgEl("g");
	o = {'clip-path':'url(#clip-'+id+')'};
	o[lbl+'-series'] = (s+1);
	setAttr(this.el,o);
	addClasses(this.el,[lbl+'-series',lbl+'-series-'+(s+1)]);

	this.getStyle = function(t,p){
		if(opt.hasOwnProperty(t)){
			if(opt[t].hasOwnProperty(p)) return opt[t][p];
		}
		return null;
	};
	this.getProperty = function(pid){
		if(opt.hasOwnProperty(pid)) return opt[pid];
		else return null;
	};
	this.getProperties = function(){ return opt; };
	this.setProperties = function(a){
		if(!a) a = {};
		mergeDeep(opt, a);
		if(opt.class){
			var c = opt.class.split(/ /);
			addClasses(this.el,c);
		}
		return this;
	};

	this.update = function(){
		var c,i,pt,txt,p,r,ps,o,ax,a,b;
		// Check if we need to add a line
		if(!line.el){
			line.el = svgEl("path");
			line.el.classList.add('line');
			setAttr(line.el,{'d':'M0 0 L 100,100','stroke':(opt.line.color||'black')});
			add(line.el,this.el); // Add it to the element
			// Create an animation for the line
			line.animate = new Animate(line.el,{'duration':opt.duration});
		}
		setAttr(line.el,{'style':(opt.line.show ? 'display:block':'display:none'),'stroke':(opt.line.color||'black'),'stroke-width':this.getStyle('line','stroke-width'),'stroke-linecap':this.getStyle('line','stroke-linecap'),'stroke-linejoin':this.getStyle('line','stroke-linejoin'),'stroke-dasharray':this.getStyle('line','stroke-dasharray'),'fill':this.getStyle('line','fill'),'vector-effect':'non-scaling-stroke'});

		for(i = pts.length; i < data.length; i++){
			pt = svgEl("g");
			datum = {'data-i':i};
			// Add any data attributes
			for(d in data[i].data) datum['data-'+d] = data[i].data[d];
			setAttr(pt,datum);
			pts[i] = {'el':pt,'point':svgEl('circle'),'title':svgEl("title"),'old':{}};

			o = {'cx':0,'cy':0,'tabindex':0};
			o[lbl+'-series'] = s+1;
			setAttr(pts[i].point,o);

			if(data[i].error) pts[i].errorbar = {};
			if(!data[i].label) data[i].label = "Point "+(i+1);
			txt = (data[i].title || data[i].label+": "+data[i].y.toFixed(2));
			if(pts[i].title){
				pts[i].title.innerHTML = txt;
				add(pts[i].title,pts[i].point);
			}
			if(pts[i].errorbar){
				for(ax in data[i].error){
					pts[i].errorbar[ax] = svgEl("line");
					add(pts[i].errorbar[ax],pt);
				}
			}
			if(pts[i].point){
				add(pts[i].point,pt);
			}

			add(pt,this.el);
			// Add animations
			pts[i].c = new Animate(pts[i].point,{'duration':opt.duration});
		}
		if(opt.line.label){
			label = svgEl("text");
			label.innerHTML = opt.title;
			var nprops = getXY(data[pts.length-1].x,data[pts.length-1].y);
			nprops['dominant-baseline'] = "middle";
			nprops.fill = (opt.line.color||'black');
			if(opt.line.label.padding) nprops.x += opt.line.label.padding;
			setAttr(label,nprops);
			add(label,this.el);
		}

		// Update points
		p = [];
		var old = {};
		for(i = 0; i < pts.length; i++){
			r = (opt['stroke-width']||1)/2;
			if(opt.points){
				if(typeof opt.points.size==="number") r = Math.max(opt.points.size,r);
				if(typeof opt.points.size==="function") r = opt.points.size.call(pt,{'series':s,'i':i,'data':data[i]});
			}
			setAttr(pts[i].point,{'r':r,'fill':opt.points.color,'fill-opacity':opt.points['fill-opacity'],'stroke':opt.points.stroke,'stroke-width':opt.points['stroke-width']});
			ps = getXY(data[i].x,data[i].y);
			p.push(ps);

			// Update error bars
			for(ax in data[i].error){
				a = getXY(data[i].x-data[i].error[ax][0],data[i].y);
				b = getXY(data[i].x+data[i].error[ax][1],data[i].y);
				setAttr(pts[i].errorbar[ax],{'x1':a.x,'y1':a.y,'x2':b.x,'y2':b.y,'stroke':opt.errors.stroke||opt.points.color,'stroke-width':opt.errors['stroke-width']||1,'class':'errorbar'});
			}

			// Keep a copy 
			if(typeof pts[i].old.x==="number" && typeof pts[i].old.y==="number") old = clone(pts[i].old);
			else{
				if(typeof old.x==="number" && typeof old.y==="number") pts[i].old = old;
			}
			// Update point position
			pts[i].c.set({'cx':{'from':pts[i].old.x||null,'to':ps.x},'cy':{'from':pts[i].old.y||null,'to':ps.y}});
			pts[i].old = ps;
		}

		// Update animation
		line.animate.set({'d':{'from':path,'to':p}});

		// Store a copy of the current path
		path = clone(p);

		return this;
	};

	this.setProperties(props);

	return this;
}

function Animate(e,attr){
	var tag,as,opt;
	opt = {'duration':'0.3s'};
	tag = e.tagName.toLowerCase();
	if(!attr) attr = {};
	mergeDeep(opt,attr);
	as = {};
	// Find duration
	if(opt.duration) this.duration = opt.duration;
	if(!this.duration) this.duration = "0.3s";
	this.duration = parseFloat(this.duration);
	this.set = function(props){
		var n,i,a2,b2,a,b;
		e.querySelectorAll('animate').forEach(function(ev){ ev.parentNode.removeChild(ev); });
		for(n in props){
			if(n){
				a = props[n].from||"";
				b = props[n].to;
				if(!a && as[n]) a = as[n].value;
				a2 = null;
				b2 = null;
				if(tag=="path"){
					a2 = "";
					b2 = "";
					for(i = 0; i < a.length; i++) a2 += (i>0 ? 'L':'M')+a[i].x.toFixed(2)+','+a[i].y.toFixed(2);
					for(i = 0; i < b.length; i++) b2 += (i>0 ? 'L':'M')+b[i].x.toFixed(2)+','+b[i].y.toFixed(2);
					if(a.length > 0 && a.length < b.length){
						for(i = 0; i < b.length-a.length; i++) a2 += 'L'+a[a.length-1].x.toFixed(2)+','+a[a.length-1].y.toFixed(2);
					}
					if(b.length > 0 && b.length < a.length){
						for(i = 0; i < a.length-b.length; i++) b2 += 'L'+b[b.length-1].x.toFixed(2)+','+b[b.length-1].y.toFixed(2);
					}
					if(!a2) a2 = null;
				}else{
					if(a) a2 = clone(a);
					b2 = clone(b);
				}
				if(this.duration && a2!==null){
					// Create a new animation
					if(!as[n]) as[n] = {};
					as[n].el = svgEl("animate");
					setAttr(as[n].el,{"attributeName":n,"dur":(this.duration||0),"repeatCount":"1"});
					add(as[n].el,e);
				}
				// Set the final value
				e.setAttribute(n,b2);
				if(this.duration && a2!==null){
					setAttr(as[n].el,{"from":a2,"to":b2,"values":a2+';'+b2}); 
					as[n].el.beginElement();
					as[n].value = b;
				}
			}
		}
		return this;
	};
	return this;
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
function svgEl(t){ return document.createElementNS(ns,t); }
function setAttr(el,prop){
	for(var p in prop) el.setAttribute(p,prop[p]);
	return el;
}
function addClasses(el,cl){
	for(var i = 0; i < cl.length; i++) el.classList.add(cl[i]);
	return el;
}