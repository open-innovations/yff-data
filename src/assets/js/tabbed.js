/*
	Open Innovations Tabbed Interface v0.1
	Helper function that find elements with the class "panes",
	looks for elements with "pane" within them,
	finds their <h3> elements, 
	then builds a simple tabbed interface.
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
	function TabbedInterface(el){
		var tabs,panes,li,p,h,b,l;
		this.selectTab = function(t){
			var tab,pane;
			tab = tabs[t].tab;
			pane = tabs[t].pane;

			// Remove existing selection and set all tabindex values to -1
			tab.parentNode.querySelectorAll('button').forEach(function(el){ el.removeAttribute('aria-selected'); el.setAttribute('tabindex',-1); });

			// Update the selected tab
			tab.setAttribute('aria-selected','true');
			tab.setAttribute('tabindex',0);
			tab.focus();

			pane.closest('.panes').querySelectorAll('.pane').forEach(function(el){ el.style.display = "none"; el.setAttribute('hidden',true); });
			pane.style.display = "";
			pane.removeAttribute('hidden');
			// Loop over any potentially visible leaflet maps that haven't been sized and set the bounds
			if(OI.maps){
				for(var m = 0; m < OI.maps.length; m++){
					if(OI.maps[m].map._container==pane.querySelector('.leaflet')){
						OI.maps[m].map.invalidateSize(true);
						if(!OI.maps[m].set){
							if(OI.maps[m].bounds) OI.maps[m].map.fitBounds(OI.maps[m].bounds);
							OI.maps[m].set = true;
						}
					}
				}
			}
			return this;
		};
		this.enableTab = function(tab,t){
			var _obj = this;

			// Set the tabindex of the tab panel
			panes[t].setAttribute('tabindex',0);

			// Add a focus event
			tab.addEventListener('focus',function(e){ e.preventDefault(); var t = parseInt(e.target.getAttribute('data-tab')); _obj.selectTab(t); });

			// Store the tab number in the tab (for use in the keydown event)
			tab.setAttribute('data-tab',t);

			// Add keyboard navigation to arrow keys following https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/Tab_Role
			tab.addEventListener('keydown',function(e){

				// Get the tab number from the attribute we set
				t = parseInt(e.target.getAttribute('data-tab'));

				if(e.keyCode === 39 || e.keyCode === 40){
					e.preventDefault();
					// Move right or down
					t++;
					if(t >= tabs.length) t = 0;
					_obj.selectTab(t);
				}else if(e.keyCode === 37 || e.keyCode === 38){
					e.preventDefault();
					// Move left or up
					t--;
					if(t < 0) t = tabs.length-1;
					_obj.selectTab(t);
				}
			});
		};
		tabs = [];

		l = document.createElement('div');
		l.classList.add('grid','tabs');
		l.setAttribute('role','tablist');
		l.setAttribute('aria-label','Visualisations');
		panes = el.querySelectorAll('.pane');
		for(p = 0; p < panes.length; p++){
			h = panes[p].querySelector('.tab-title');
			b = document.createElement('button');
			b.classList.add('tab');
			b.setAttribute('role','tab');
			if(h) b.appendChild(h);
			l.appendChild(b);
			tabs[p] = {'tab':b,'pane':panes[p]};
			this.enableTab(b,p);
		}
		el.insertAdjacentElement('beforebegin', l);
		this.selectTab(0);
		return this;
	}
	root.OI.TabbedInterface = function(el){ return new TabbedInterface(el); };

})(window || this);

OI.ready(function(){
	var tabbed = document.querySelectorAll('.panes.tabbed');
	for(var i = 0; i < tabbed.length; i++) OI.TabbedInterface(tabbed[i]);
});