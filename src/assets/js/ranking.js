/*
	Open Innovations Ranking Chart Interactivity v0.1
	Helper function that find ".ranking" elements 
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
	
	function InteractiveRankingChart(el){
		console.log(el);
		return this;
	}

	root.OI.InteractiveRankingChart = function(el){ return new InteractiveRankingChart(el); };

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
	var charts = document.querySelectorAll('.ranking');
	for(var i = 0; i < charts.length; i++){
		OI.InteractiveRankingChart(charts[i]);
	}
});