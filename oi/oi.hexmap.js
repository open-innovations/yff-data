import { document } from '/oi/document.ts';

/**
  Originally adapted from oi.hexmap.js 0.6.1
 */

// Input structure:
//    attr: an object defining various parameters:
//      id: an ID to use for clipping (it matters if there are multiple hexmaps on a page)
//      width: the width of the SVG element created
//      height: the height of the SVG element created
//      padding: an integer number of hexes to leave as padding around the displayed map
//      grid: do we show the background grid?
//      clip: do we clip the text to the hex?
//      formatLabel: a function to format the hex label
//      size: the size of a hexagon in pixels
export function HexMap(attr) {

  this.version = "0.6.1-deno";
  if (!attr) attr = {};
  this._attr = attr;
  this.title = "OI HexMap";
  this.log = function () {
    // Version 1.1
    if (this.logging || arguments[0] == "ERROR" || arguments[0] == "WARNING") {
      const args = Array.prototype.slice.call(arguments, 0);
      // Build basic result
      const extra = ['%c' + this.title + '%c: ' + args[1], 'font-weight:bold;', ''];
      // If there are extra parameters passed we add them
      if (args.length > 2) extra = extra.concat(args.splice(2));
      if (console && typeof console.log === "function") {
        if (arguments[0] == "ERROR") console.error.apply(null, extra);
        else if (arguments[0] == "WARNING") console.warn.apply(null, extra);
        else if (arguments[0] == "INFO") console.info.apply(null, extra);
        else console.log.apply(null, extra);
      }
    }
    return this;
  };

  if (!attr.label) attr.label = {};
  if (!attr.grid) attr.grid = {};
  if (typeof attr.label.show !== "boolean") attr.label.show = false;
  if (typeof attr.label.clip !== "boolean") attr.label.clip = false;
  if (typeof attr.grid.show !== "boolean") attr.grid.show = false;

  let wide = attr.width || 300;
  let tall = attr.height || 150;
  this.maxw = wide;
  this.maxh = tall;
  const aspectratio = wide / tall;
  let constructed = false;
  let svg;
  let range = {};
  const fs = attr['font-size'] || 16;
  this.areas = {};
  this.padding = (typeof attr.padding === "number" ? attr.padding : 0);
  this.properties = { 'size': attr.size };
  this.callback = {};
  this.mapping = {};

  // Add an inner element
  this.el = document.createElement('div');
  this.el.classList.add('hexmap-inner');

  this.options = {
    'clip': attr.label.clip,
    'showgrid': attr.grid.show,
    'showlabel': attr.label.show,
    'formatLabel': (typeof attr.label.format === "function" ? attr.label.format : function (txt, _attr) { return txt.substr(0, 3); }),
    'minFontSize': (typeof attr.minFontSize === "number" ? attr.minFontSize : 4)
  };

  this.style = {
    'default': { 'fill': '#cccccc', 'fill-opacity': 1, 'font-size': fs, 'stroke-width': 1.5, 'stroke-opacity': 1, 'stroke': '#ffffff' },
    'highlight': { 'fill': '#1DD3A7' },
    'grid': { 'fill': '#aaa', 'fill-opacity': 0.1 }
  };

  for (const s in attr.style) {
    if (attr.style[s]) {
      if (!this.style[s]) this.style[s] = {};
      if (attr.style[s].fill) this.style[s].fill = attr.style[s].fill;
      if (attr.style[s]['fill-opacity']) this.style[s]['fill-opacity'] = attr.style[s]['fill-opacity'];
      if (attr.style[s]['font-size']) this.style[s]['font-size'] = attr.style[s]['font-size'];
      if (attr.style[s].stroke) this.style[s].stroke = attr.style[s].stroke;
      if (attr.style[s]['stroke-width']) this.style[s]['stroke-width'] = attr.style[s]['stroke-width'];
      if (attr.style[s]['stroke-opacity']) this.style[s]['stroke-opacity'] = attr.style[s]['stroke-opacity'];
    }
  }
  this.setHexSize = function (s) {
    if (typeof s !== "number") s = 10;
    s = Math.round(100 * s) / 100;
    attr.size = s;
    this.properties.size = s;
    return this;
  };

  // Can load a hexjson data structure
  this.load = function (data, prop, fn) {
    if (typeof data !== "object") throw "Can't load - not an object";
    if (typeof prop === "function" && !fn) {
      fn = prop;
      prop = "";
    }
    this.setMapping(data);
    this.updateColours();
    if (typeof fn === "function") fn.call(this, { 'data': prop });
    return this;
  };

  this.setHexStyle = function (r) {
    let cls, p;
    const h = this.areas[r];
    const style = clone(this.style['default']);
    cls = "";
    if (h.active) style.fill = h.fillcolour;
    if (h.hover) cls += ' hover';
    if (h.selected) {
      for (p in this.style.selected) {
        if (this.style.selected[p]) style[p] = this.style.selected[p];
      }
      cls += ' selected';
    }
    if (this.mapping.hexes[r]['class']) cls += " " + this.mapping.hexes[r]['class'];
    style['class'] = 'hex-cell' + cls;
    setAttr(h.hex, style);
    if (h.label) setAttr(h.label, { 'class': 'hex-label' + cls });
    return h;
  };

  function setClip(h) {
    const sty = getComputedStyle(h.hex);
    const s = {};
    if (sty.transform) s.transform = sty.transform;
    if (s.transform == "none") s.transform = "";
    if (sty['transform-origin']) s['transform-origin'] = sty['transform-origin'];
    setAttr(h.clip, s);
  }

  this.size = function (w, h) {
    if (!this.el.style) this.el.style = {}
    this.el.style.height = '';
    this.el.style.width = '';
    if (svg) setAttr(svg, { 'width': 0, 'height': 0 });
    w = Math.min(this.maxw, wide);
    this.el.style.height = (w / aspectratio) + 'px';
    this.el.style.width = w + 'px';
    h = this.maxh;

    // Create SVG container
    if (!svg) {
      svg = svgEl('svg');
      setAttr(svg, { 'class': 'hexmap-map', 'xmlns': ns, 'version': '1.1', 'overflow': 'visible', 'viewBox': (attr.viewBox || '0 0 ' + w + ' ' + h), 'style': 'max-width:100%;', 'preserveAspectRatio': 'xMinYMin meet', 'vector-effect': 'non-scaling-stroke' });
      add(svg, this.el);
    }
    setAttr(svg, { 'width': w, 'height': h });

    const scale = w / wide;
    this.properties.size = attr.size * scale;
    wide = w;
    tall = h;
    this.el.style.height = '';
    this.el.style.width = '';

    return this;
  };

  this.create = function () {
    // Clear the canvas
    svg.innerHTML = "";
    this.areas = {};
    constructed = false;
    return this;
  };

  function updatePos(q, r, layout) {
    if (layout == "odd-r" && (r % 2) != 0) q += 0.5;  // "odd-r" horizontal layout shoves odd rows right
    if (layout == "even-r" && (r % 2) == 0) q += 0.5; // "even-r" horizontal layout shoves even rows right
    if (layout == "odd-q" && (q % 2) != 0) r += 0.5;  // "odd-q" vertical layout shoves odd columns down
    if (layout == "even-q" && (q % 2) == 0) r += 0.5; // "even-q" vertical layout shoves even columns down
    return { 'q': q, 'r': r };
  }

  this.setMapping = function (mapping) {
    let region, p, s;
    this.mapping = mapping;
    if (!this.properties) this.properties = { "x": 100, "y": 100 };
    p = mapping.layout.split("-");
    this.properties.shift = p[0];
    this.properties.orientation = p[1];

    range = { 'r': { 'min': 1e100, 'max': -1e100 }, 'q': { 'min': 1e100, 'max': -1e100 } };
    for (region in this.mapping.hexes) {
      if (this.mapping.hexes[region]) {
        p = updatePos(this.mapping.hexes[region].q, this.mapping.hexes[region].r, this.mapping.layout);
        if (p.q > range.q.max) range.q.max = p.q;
        if (p.q < range.q.min) range.q.min = p.q;
        if (p.r > range.r.max) range.r.max = p.r;
        if (p.r < range.r.min) range.r.min = p.r;
      }
    }
    // Find range and mid points
    range.q.d = range.q.max - range.q.min;
    range.r.d = range.r.max - range.r.min;
    range.q.mid = range.q.min + range.q.d / 2;
    range.r.mid = range.r.min + range.r.d / 2;
    this.range = clone(range);

    if (this.properties.orientation == "r") s = Math.min(0.5 * tall / (range.r.d * 0.75 + 1), (1 / Math.sqrt(3)) * wide / (range.q.d + 1));	// Pointy-topped
    else s = Math.min((1 / Math.sqrt(3)) * tall / (range.r.d + 1), 0.5 * wide / (range.q.d * 0.75 + 1));	// Flat-topped

    if (typeof attr.size !== "number") this.setHexSize(s);
    this.setSize();

    return this.create().draw();
  };

  this.setSize = function (size) {
    if (size) this.properties.size = size;
    this.properties.s = { 'cos': Math.round(10 * this.properties.size * Math.sqrt(3) / 2) / 10, 'sin': this.properties.size * 0.5 };
    this.properties.s.c = this.properties.s.cos.toFixed(2);
    this.properties.s.s = this.properties.s.sin.toFixed(2);
    return this;
  };

  this.drawHex = function (q, r) {
    if (this.properties) {
      let x, y;
      const cs = this.properties.s.cos;
      const ss = this.properties.s.sin;

      const p = updatePos(q, r, this.mapping.layout);

      if (this.properties.orientation == "r") {
        // Pointy topped
        x = (wide / 2) + ((p.q - this.range.q.mid) * cs * 2);
        y = (tall / 2) - ((p.r - this.range.r.mid) * ss * 3);
      } else {
        // Flat topped
        x = (wide / 2) + ((p.q - this.range.q.mid) * ss * 3);
        y = (tall / 2) - ((p.r - this.range.r.mid) * cs * 2);
      }
      x = parseFloat(x.toFixed(1));
      const path = [['M', [x, y]]];
      if (this.properties.orientation == "r") {
        // Pointy topped
        path.push(['m', [cs, -ss]]);
        path.push(['l', [0, 2 * ss, -cs, ss, -cs, -ss, 0, -2 * ss, cs, -ss, cs, ss]]);
        path.push(['z', []]);
      } else {
        // Flat topped
        path.push(['m', [-ss, cs]]);
        path.push(['l', [2 * ss, 0, ss, -cs, -ss, -cs, -2 * ss, 0, -ss, cs]]);
        path.push(['z', []]);
      }
      return { 'array': path, 'path': toPath(path), 'x': x, 'y': y };
    }
    return this;
  };

  this.updateColours = function (fn) {
    let r;
    if (typeof fn !== "function") {
      fn = function () {
        let fill = this.style['default'].fill;
        if (this.mapping.hexes[r].colour) fill = this.mapping.hexes[r].colour;
        if (typeof attr.colours === "string") fill = attr.colours;
        return fill;
      };
    }
    for (r in this.mapping.hexes) {
      if (this.mapping.hexes[r]) {
        this.areas[r].fillcolour = fn.call(this, r);
        this.setHexStyle(r);
      }
    }
    return this;
  };

  this.draw = function () {
    let r, q, h, hex, region;

    const range = this.range;
    for (region in this.mapping.hexes) {
      if (this.mapping.hexes[region]) {
        q = this.mapping.hexes[region].q;
        r = this.mapping.hexes[region].r;
        if (q > range.q.max) range.q.max = q;
        if (q < range.q.min) range.q.min = q;
        if (r > range.r.max) range.r.max = r;
        if (r < range.r.min) range.r.min = r;
      }
    }

    // Add padding to range
    range.q.min -= this.padding;
    range.q.max += this.padding;
    range.r.min -= this.padding;
    range.r.max += this.padding;

    // q,r coordinate of the centre of the range
    const qp = (range.q.max + range.q.min) / 2;
    const rp = (range.r.max + range.r.min) / 2;

    this.properties.x = (this.w / 2) - (this.properties.s.cos * 2 * qp);
    this.properties.y = (this.h / 2) + (this.properties.s.sin * 3 * rp);

    // Store this for use elsewhere
    this.range = clone(range);

    if ((this.options.showgrid || this.options.clip) && !this.grid) {
      this.grid = svgEl('g');
      setAttr(this.grid, { 'class': 'hex-grid-holder' });
      for (q = range.q.min - 1; q <= range.q.max + 1; q++) {
        for (r = range.r.min - 1; r <= range.r.max + 1; r++) {
          h = this.drawHex(q, r);
          if (this.options.showgrid) {
            hex = svgEl('path');
            setAttr(hex, { 'd': h.path, 'class': 'hex-grid', 'data-q': q, 'data-r': r, 'fill': (this.style.grid.fill || ''), 'fill-opacity': (this.style.grid['fill-opacity'] || 0.1), 'stroke': (this.style.grid.stroke || '#aaa'), 'stroke-opacity': (this.style.grid['stroke-opacity'] || 0.2) });
            add(hex, this.grid);
          }
        }
      }
      add(this.grid, svg);
    }

    let path, label, hexclip, g;
    const min = 50000;
    const max = 80000;
    const defs = svgEl('defs');
    add(defs, svg);
    const id = (attr.id || 'hex');

    for (r in this.mapping.hexes) {
      if (this.mapping.hexes[r]) {

        h = this.drawHex(this.mapping.hexes[r].q, this.mapping.hexes[r].r);

        if (!constructed) {
          g = svgEl('g');
          setAttr(g, { 'data': r });
          svg.appendChild(g);
          path = svgEl('path');
          path.innerHTML = '<title>' + (this.mapping.hexes[r].n || r) + '</title>';
          setAttr(path, { 'd': h.path, 'class': 'hex-cell', 'transform-origin': h.x + 'px ' + h.y + 'px', 'data-q': this.mapping.hexes[r].q, 'data-r': this.mapping.hexes[r].r });
          g.appendChild(path);
          this.areas[r] = { 'g': g, 'hex': path, 'selected': false, 'active': true, 'data': this.mapping.hexes[r], 'orig': h };

          if (this.options.showlabel) {
            if (this.style['default']['font-size'] >= this.options.minFontSize) {
              if (this.options.clip) {
                // Make all the clipping areas
                this.areas[r].clipid = (id) + '-clip-' + r;
                this.areas[r].clip = svgEl('clipPath');
                this.areas[r].clip.setAttribute('id', this.areas[r].clipid);
                hexclip = svgEl('path');
                setAttr(hexclip, { 'd': h.path, 'transform-origin': h.x + 'px ' + h.y + 'px' });
                add(hexclip, this.areas[r].clip);
                add(this.areas[r].clip, defs);
              }
              label = svgEl('text');
              // Add to DOM
              g.appendChild(label);
              label.innerHTML = this.options.formatLabel(this.mapping.hexes[r].n || this.mapping.hexes[r].msoa_name_hcl, { 'x': h.x, 'y': h.y, 'hex': this.mapping.hexes[r], 'size': this.properties.size, 'font-size': parseFloat(getComputedStyle(label)['font-size']) });
              setAttr(label, { 'x': h.x, 'y': h.y, 'transform-origin': h.x + 'px ' + h.y + 'px', 'dominant-baseline': 'central', 'clip-path': 'url(#' + this.areas[r].clipid + ')', 'data-q': this.mapping.hexes[r].q, 'data-r': this.mapping.hexes[r].r, 'class': 'hex-label', 'text-anchor': 'middle', 'font-size': this.style['default']['font-size'] + 'px', 'title': (this.mapping.hexes[r].n || r), '_region': r });
              this.areas[r].label = label;
              this.areas[r].labelprops = { x: h.x, y: h.y };
            }
          }

        }
        this.setHexStyle(r);
        setAttr(this.areas[r].hex, { 'stroke': this.style['default'].stroke, 'stroke-opacity': this.style['default']['stroke-opacity'], 'stroke-width': this.style['default']['stroke-width'], 'title': this.mapping.hexes[r].n, 'data-regions': r, 'style': 'cursor: pointer;' });
      }
    }

    constructed = true;

    return this;
  };
  
  // Return the SVG string for the hexmap
  this.getSVG = function(){ return svg.outerHTML; };

  this.size();
  if (attr.hexjson) this.load(attr.hexjson, attr.ready);

  return this;
}

// Helper functions
const ns = 'http://www.w3.org/2000/svg';
function prepend(el, to) { to.insertBefore(el, to.firstChild); }
function add(el, to) { return to.appendChild(el); }
function clone(a) { return JSON.parse(JSON.stringify(a)); }
function setAttr(el, prop) {
  for (const p in prop) {
    if (prop[p]) el.setAttribute(p, prop[p]);
  }
  return el;
}
function svgEl(t) { return document.createElement(t); }
function toPath(p) {
  let str = '';
  for (let i = 0; i < p.length; i++) str += ((p[i][0]) ? p[i][0] : ' ') + (p[i][1].length > 0 ? p[i][1].join(',') : ' ');
  return str;
}
