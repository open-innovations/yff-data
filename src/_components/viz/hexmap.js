import { HexMap } from '/oi/oi.hexmap.js';
import { loadDataFile } from '/oi/util.js'

export const css = `
.hexmap {
  border: 1px solid black;
  max-width: 30rem;
  margin: 0 auto;
}
.hexmap svg {
}
`;

export default function ({ config, sources }) {
  const layout = loadDataFile(config.layout, sources);

  console.log(layout);
  const hexmap = new HexMap({
    hexjson: layout,
    width: config?.width,
    height: config?.height,
  });

  return ['<div class="hexmap">',
    hexmap.getSVG(),
    '</div>'
  ].join('');
}