import { document } from '/src/_lib/oi/document.ts';

const ns = 'http://www.w3.org/2000/svg';


export function Dashboard(config,csv){

	this.getHTML = function(){
		var html,i,panel,r,cls,p,idx;
		
		html = ['<div class="dashboard" data-scroll="visible" style="grid-template-columns: repeat('+(config.columns||4)+', 1fr);">'];

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

				panel = '<div class="panel'+(cls ? ' '+cls : '')+'">';
				panel += '<h3>'+config.panels[p].name+'</h3>';
				if(config.value && csv.columns[config.value]) panel += '<span class="bignum" data="'+csv.rows[idx][config.value]+'">'+csv.rows[idx][config.value].toLocaleString()+'</span>';
				if(config.note && csv.columns[config.note]) panel += '<span class="note">'+csv.rows[idx][config.note]+'</span>';
				panel += '</div>';

				html.push(panel);
				
			}
		}
		html.push('</div>');

		return html.join('');
	};
	return this;
}