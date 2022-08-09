import { HexMap } from './hexmap.js';

Deno.test('it should load', () => {
  const hexmap = new HexMap();
});

Deno.test('it should load a hexjson layout', () => {
  const fakeLayout = {
    layout: 'odd-r',
    hexes: {
      E05011395: { n: 'Guiseley and Rawdon', q: 0, r: 3, colour: '#00B6FF' },
    },
  };
  const hexmap = new HexMap({
    hexjson: fakeLayout,
  });
});
