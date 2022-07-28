import { HexMap } from '/oi/oi.hexmap.js';
import { loadDataFile } from '/oi/util.js'

export default function ({ config, sources }) {
  const layout = loadDataFile(config.layout, sources);

  console.log(layout);
  const hexmap = new HexMap({
    hexjson: layout,
  });

  return hexmap.getSVG();
}