import { HexMap } from '/oi/oi.hexmap.js';

export default function ({ config }) {
  const hexmap = new HexMap({});

  return hexmap.getSVG();
}