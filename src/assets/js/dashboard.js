/*
	Open Innovations Dashboard Interactivity v0.1.1
	Adds "animation" to numbers in ".dashboard" elements of the form:
	<div class="dashboard">
		<div class="panel">
			<span class="bignum" data="37" data-prefix="£" data-postfix="p" data-precision="0.01">£37.00p</span>
		</div>
	</div>
*/

(function (root) {
	if (!root.OI) root.OI = {};
	if (!root.OI.ready) {
	root.OI.ready = function (fn) {
		// Version 1.1
		if (document.readyState != "loading") fn();
		else document.addEventListener("DOMContentLoaded", fn);
	};
	}

	if (!window.requestAnimFrame) {
	// shim layer with setTimeout fallback
	window.requestAnimFrame = (function () {
		return window.requestAnimationFrame ||
		window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame ||
		function (callback) {
			window.setTimeout(callback, 1000 / 60);
		};
	})();
	}

	function AugmentDashboards() {
	// Find all the dashboards on the page
	var dashboards = document.querySelectorAll(".dashboard");
	// A function to "animate" the number when first seen
	function animateNumber(el, val, duration) {
		var start, pre, post, v, prec;
		// Get the number from the data attribute (or the HTML content if not set)
		if (typeof val !== "number") {
		val = el.getAttribute("data") || el.innerHTML;
		if (val) val = parseFloat(val);
		// Just stop processing if it's not a number
		if (isNaN(val)) return;
		el.innerHTML = "";
		}
		start = new Date();
		pre = el.getAttribute("data-prefix") || "";
		post = el.getAttribute("data-postfix") || "";
		prec = el.getAttribute("data-precision") ? parseFloat(el.getAttribute("data-precision")) : "";
		if (typeof duration !== "number") duration = 500;
		function frame() {
			var now, f;
			now = new Date();
			// Set the current time in milliseconds
			f = (now - start) / duration;
			if (f < 1) {
				v = formatNumber(Math.round(val * f),prec);
				el.innerHTML = pre + v + post;
				window.requestAnimFrame(frame);
			} else {
				el.innerHTML = (pre || "") + formatNumber(val,prec) + (post || "");
			}
		}
		// If the value is a number we animate it
		if (typeof val === "number") frame();
		return;
	}
	function countDecimals(v){
		var txt = v.toString();
		// If it is in scientific notation
		if(txt.indexOf('e-') > -1){
			var [base, trail] = txt.split('e-');
			return parseInt(trail, 10);
		}
		// Otherwise count decimals
		if(Math.floor(v) !== v) return v.toString().split(".")[1].length || 0;
		return 0;
	}
	function toPrecision(v,prec){
		if(typeof prec!=="number") return v;
		var n = Math.round(v/prec);
		var dp = countDecimals(prec);
		// Rebuild the number
		v = prec*n;
		if(prec < 1) v = v.toFixed(dp);
		return v;
	}
	// Shorten big numbers
	function formatNumber(v,precision) {
		if (typeof v !== "number") return v;
		if (v > 1e7) return toPrecision(v / 1e6,(precision ? precision/1e6 : 1)) + "M";
		if (v > 1e6) return toPrecision(v / 1e6,(precision ? precision/1e6 : 0.1)) + "M";
		if (v > 1e4) return toPrecision(v / 1e3,(precision ? precision/1e3 : 1)) + "k";
		if (v > 1e3) return toPrecision(v / 1e3,(precision ? precision/1e3 : 0.1)) + "k";
		return toPrecision(v,precision);
	}
	// Check if the element is within the viewport
	function inViewport(el) {
		var b, w, h;
		b = el.getBoundingClientRect();
		h = el.offsetHeight;
		w = el.offsetWidth;
		return (b.top >= -h && b.left >= -w &&
		b.right <=
			(window.innerWidth || document.documentElement.clientWidth) + w &&
		b.bottom <=
			(window.innerHeight || document.documentElement.clientHeight) + h);
	}
	// For each dashboard, check if "activated" is set. If not, animate the panels and set the attribute.
	function activateDashboards() {
		var d, p, panels;
		for (d = 0; d < dashboards.length; d++) {
		if (
			!dashboards[d].getAttribute("activated") && inViewport(dashboards[d])
		) {
			dashboards[d].setAttribute("activated", true);
			// Now trigger the number animations
			panels = dashboards[d].querySelectorAll(".bignum");
			for (p = 0; p < panels.length; p++) animateNumber(panels[p]);
		}
		}
	}
	// Attach the scroll event
	document.addEventListener("scroll", activateDashboards);
	// See if any dashboards need to be activated
	activateDashboards();
	}
	root.OI.AugmentDashboards = AugmentDashboards;
})(window || this);

OI.ready(function () {
	OI.AugmentDashboards();
});
