/*
	Open Innovations Figure Menu
	Helper function that finds <figure> within the class "panes",
	then adds basic menus to them to save/download.
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
  var counter = { "item": 0, "menu": 0 };
  function FigureMenu(el) {
    var opts, opt, menuitems, inp, lbl, svg, li, btn;
    opts = el.querySelector(".figure-options");
    opts.classList.add("added");
    opt = opts.querySelector(".figure-option-list");
    opt.setAttribute("role", "menu");
    opt.setAttribute("id", "menu-" + counter.menu);

    const credit = el.querySelector('.oi-credit');

    // Add screenshot function
    btn = document.createElement("button");
    btn.classList.add("orange-bg", "figure-option");
    btn.setAttribute("role", "menuitem");
    btn.innerHTML =
      '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-image-fill" viewBox="0 0 16 16"><path d="M.002 3a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-12a2 2 0 0 1-2-2V3zm1 9v1a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V9.5l-3.777-1.947a.5.5 0 0 0-.577.093l-3.71 3.71-2.66-1.772a.5.5 0 0 0-.63.062L1.002 12zm5-6.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0z"/></svg> Save figure';
    opt.appendChild(btn);
    btn.addEventListener("click", function (e) {
      var i, ignore, nts, hide;
      // Add menu button
      hide = [opts];
      // Add other elements in the parent
      ignore = el.parentNode.children;
      for (i = 0; i < ignore.length; i++) {
        if (ignore[i] != el) hide.push(ignore[i]);
      }
      nts = el.querySelectorAll(".note");
      for (i = 0; i < nts.length; i++) hide.push(nts[i]);

      // Hide hideable items
      for (i = 0; i < hide.length; i++) hide[i].style.display = "none";
      // Show credit
      credit.hidden = false;
      saveDOMImage(el.parentNode, {
        "file": "figure.png",
        "callback": function (e) {
          // Show hidden items
          for (i = 0; i < hide.length; i++) hide[i].style.display = "";
          // Hide credit
          credit.hidden = true;
        },
      });
    });

    // Save a copy of the SVG if it exists
    svg = el.querySelector(".chart > svg, .svg-map > svg, .hex-map > svg");
    if (svg) {
      // Add "Download SVG" option
      btn = document.createElement("button");
      btn.classList.add("orange-bg", "figure-option");
      btn.setAttribute("role", "menuitem");
      btn.innerHTML =
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-image-fill" viewBox="0 0 16 16"><path d="M4 0h5.293A1 1 0 0 1 10 .293L13.707 4a1 1 0 0 1 .293.707v5.586l-2.73-2.73a1 1 0 0 0-1.52.127l-1.889 2.644-1.769-1.062a1 1 0 0 0-1.222.15L2 12.292V2a2 2 0 0 1 2-2zm5.5 1.5v2a1 1 0 0 0 1 1h2l-3-3zm-1.498 4a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0z"/><path d="M10.564 8.27 14 11.708V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-.293l3.578-3.577 2.56 1.536 2.426-3.395z"/></svg> Save .svg';
      opt.appendChild(btn);
      btn.addEventListener("click", function (e) {
        // Add width/height to SVG
        svg.setAttribute("width", svg.clientWidth + "px");
        svg.setAttribute("height", svg.clientHeight + "px");
        saveSVG(svg);
      });
    }

    menuitems = opts.querySelectorAll(".figure-option");

    // Add the menu selector
    if (menuitems.length > 0) {
      // Make the menu selector
      inp = document.createElement("input");
      inp.setAttribute("type", "checkbox");
      inp.classList.add("figure-menu");
      inp.setAttribute("id", "menu-" + counter.menu + "-item-" + counter.item);
      opt.insertAdjacentElement("beforebegin", inp);

      lbl = document.createElement("label");
      lbl.setAttribute("title", "Toggle figure menu");
      lbl.setAttribute("for", "menu-" + counter.menu + "-item-" + counter.item);
      lbl.setAttribute("aria-label", "Open menu");
      lbl.setAttribute("aria-controls", "menu-" + counter.menu);
      lbl.setAttribute("id", "menu-button-" + counter.menu);
      lbl.classList.add("orange-bg");
      lbl.innerHTML = "&#8801;";
      opt.insertAdjacentElement("beforebegin", lbl);

      // Update the menu toggle aria-labelledby value
      opt.setAttribute("aria-labelledby", "menu-button-" + counter.menu);

      //menuitems[menuitems.length-1].addEventListener('blur',function(e){ inp.checked = false; });

      counter.item++;
    }
    return this;
  }
  function saveSVG(el, opt) {
    if (!opt) opt = {};
    var str = el.outerHTML;
    str = str.replace(/<br>/g, " ");

    var textFileAsBlob = new Blob([str], { type: "text/application/svg+xml" });
    var fileNameToSaveAs = opt.file || "figure.svg";

    function destroyClickedElement(event) {
      document.body.removeChild(event.target);
    }
    var dl = document.createElement("a");
    dl.download = fileNameToSaveAs;
    dl.innerHTML = "Download File";
    if (window.webkitURL != null) {
      // Chrome allows the link to be clicked
      // without actually adding it to the DOM.
      dl.href = window.webkitURL.createObjectURL(textFileAsBlob);
    } else {
      // Firefox requires the link to be added to the DOM
      // before it can be clicked.
      dl.href = window.URL.createObjectURL(textFileAsBlob);
      dl.onclick = destroyClickedElement;
      dl.style.display = "none";
      document.body.appendChild(dl);
    }
    dl.click();
    return this;
  }
  function saveDOMImage(el, opt) {
    var w, h, src, d;
    if (!opt) opt = {};
    if (!opt.file) opt.file = "figure.png";
    if (opt.scale) {
      if (!opt.height) opt.height = el.offsetHeight * 2;
      if (!opt.width) opt.width = el.offsetWidth * 2;
      // Force bigger size for element
      w = el.style.getPropertyValue("width");
      h = el.style.getPropertyValue("height");
      el.style.setProperty("width", (opt.width) + "px");
      el.style.setProperty("height", (opt.height) + "px");
    }
    el.classList.add("capture");
    d = new Date();
    src = document.createElement("p");
    src.classList.add("source");
    // TODO Maybe add OI credit here in some way
    src.innerHTML = "&copy; Youth Futures Foundation " + d.getFullYear();
    el.appendChild(src);

    domtoimage.toPng(el, opt).then(function (dataUrl) {
      var link = document.createElement("a");
      link.download = opt.file;
      link.href = dataUrl;
      link.click();
      // Reset element
      if (opt.scale) {
        el.style.setProperty("width", w);
        el.style.setProperty("height", h);
      }
      el.classList.remove("capture");
      el.removeChild(src);
      if (typeof opt.callback === "function") opt.callback.call();
    });
  }

  OI.FigureMenu = function (el) {
    return new FigureMenu(el);
  };
})(window || this);

OI.ready(function () {
  var figs = document.querySelectorAll(".pane figure");
  for (var i = 0; i < figs.length; i++) OI.FigureMenu(figs[i]);
});

// dom-to-image now separately required.