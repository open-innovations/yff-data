import { applyReplacementFilters } from "/src/_lib/oi/util.js";

// TODO consider checking for old / new lume viz

export default function ({ comp, config, tab, title, caption, type, headingLevel = 3 }) {
  try {
    const heading = title ? `<h${ headingLevel }>${ title }</h${ headingLevel }>` : ""
    const figCaption = caption ? `<figcaption><p>${ applyReplacementFilters(caption, config)}</p></figcaption>` : "";
    const rendered = comp.viz[type]( { config: config });

    return `<span class="tab-title">${ tab ? tab : title }</span>${ heading }${ figCaption }${ rendered }`;
  } catch (e) {
    console.error(e);
    throw e;
  }
}

