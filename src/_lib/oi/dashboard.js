import { document } from '/src/_lib/oi/document.ts';
import { colours, scales } from '/src/_data/colours.js';
import { Colour, ColourScale } from 'local/oi/colours.js';


// This component uses "/assets/js/dashboard.js" to make things interactive in the browser.
// It will only get included in pages that need it by using the "data-dependencies" attribute.

const ns = 'http://www.w3.org/2000/svg';

export function Dashboard(config,csv){

	this.getHTML = function(){
		var html,i,panel,r,cls,p,idx,col,v,c,scale;
		
		html = ['<div class="dashboard" data-dependencies="/assets/js/dashboard.js" style="grid-template-columns: repeat(auto-fill, minmax(min(100%, '+(config.width||'250px')+'), 1fr));">'];

		// Loop over the user-specified panels
		for(p = 0 ; p < config.panels.length; p++){

			// Find the matching row
			idx = -1;
			if(config.title && csv.columns[config.title]){
				for(r = 0; r < csv.rows.length; r++){
					if(csv.rows[r][config.title]==config.panels[p].name){
						idx = r;
					}
				}
			}
			if(idx >= 0){
				// Build classes
				cls = config.class||'';
				cls += (cls ? " ":"")+(config.panels[p].class||'');
				col = (config.panels[p].colour||'');
				v = "";

				// Get the value for this panel
				if(config.value && csv.columns[config.value]) v = csv.rows[idx][config.value];

				// If we haven't set a colour explicitly but we have set a colour scale
				if(!typeof config.panels[p].colour==="string" && config.panels[p].scale){
					// If a scale value has been given, use that instead of the value of the panel
					if(typeof config.panels[p]['scale-value']==="number") v = config.panels[p]['scale-value'];

					// Get the ColourScale from either:
					// string - a key referencing a scale
					// object:
					//     function: 'round'
					//     stops:
					//         - { value: 0, colour: name1 }
					//         - { value: 50, colour: name2 }
					//         - { value: 100, colour: name3 }
					scale = (typeof config.panels[p].scale==="string") ? scales[(scales[config.panels[p].scale] ? config.panels[p].scale : 'Viridis')] : ColourScale(config.panels[p].scale);

					// Find the background colour
					col = scale(table.data[r][c2],config.columns[c].min,config.columns[c].max);

				}
				
				// Update with any named colours
				if(colours[col]) col = colours[col];

				var color = new Colour(col);
				c = color.contrast;

				panel = '<div class="panel'+(cls ? ' '+cls : '')+'"'+(col ? ' style="background-color:'+col+';color:'+c+'"' : '')+'>';
				panel += '<h3>'+config.panels[p].name+'</h3>';
				if(config.value && csv.columns[config.value]){
					panel += '<span class="bignum" data="'+csv.rows[idx][config.value]+'"';
					if(config.panels[p].precision) panel += ' data-precision="'+config.panels[p].precision+'"';
					if(config.units){
						if(config.units.prefix && csv.rows[idx][config.units.prefix]) panel += ' data-prefix="'+csv.rows[idx][config.units.prefix]+'"';
						if(config.units.postfix && csv.rows[idx][config.units.postfix]) panel += ' data-postfix="'+csv.rows[idx][config.units.postfix]+'"';
					}
					panel += '>';
					panel += csv.rows[idx][config.value].toLocaleString();
					panel += '</span>';
				}else{
					console.error('WARNING: No column named "'+config.value+'" in panel '+p+' ('+config.file+')');
				}

				var note = config.panels[p].note || config.note;
				if(note){
					if(csv.columns[note]) panel += '<span class="footnote">'+csv.rows[idx][config.note]+'</span>';
					else panel += '<span class="footnote">'+note+'</span>';
				}
				panel += '</div>';

				html.push(panel);
				
			}else{
				console.error('WARNING: Unable to find matching row for panel '+p+' "'+config.panels[p].name+'" ('+config.file+').');
			}
		}
		html.push('</div>');

		return html.join('');
	};
	return this;
}