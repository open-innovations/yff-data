import { assertEquals } from 'https://deno.land/std@0.149.0/testing/asserts.ts';
import {
  assertSpyCall,
  resolvesNext,
  stub,
} from 'https://deno.land/std@0.149.0/testing/mock.ts';
import csvLoader from './csv-loader.ts';

Deno.test('url test', async (t) => {
  const fakeReadTextFile = stub(
    Deno,
    'readTextFile',
    resolvesNext(['a,b\n1,2\n3,4'])
  );
  let result;
  try {
    result = await csvLoader('FAKE_PATH');
  } finally {
    fakeReadTextFile.restore();
  }

  assertSpyCall(fakeReadTextFile, 0, {
    args: ['FAKE_PATH'],
  });

  assertEquals(result.header, [['a', 'b']]);
  assertEquals(result.names, ['a', 'b']);
  console.dir({ data: result.data });
  assertEquals(result.data, [
    ['1', '2'],
    ['3', '4'],
  ]);
  assertEquals(result.rows, [
    { a: '1', b: '2' },
    { a: '3', b: '4' },
  ]);
  assertEquals(result.columns, {
    a: ['1', '3'],
    b: ['2', '4'],
  });
});
