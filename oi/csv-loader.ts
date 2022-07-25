import { parse } from 'std/encoding/csv.ts';
import { transpose } from '/oi/util.js';

export default async function csvLoader(path: string) {
  const text = await Deno.readTextFile(path);
  const raw = await (<Promise<[string[]]>>parse(text));

  const headerRowCount = 1;
  const header = raw.slice(0, headerRowCount);
  const data = raw.slice(headerRowCount);
  const names: string[] = transpose(header).map((r: string[]) => r.join('.'));

  const rows = data.map((row) =>
    names.reduce(
      (a, k, i) => ({
        ...a,
        [k]: row[i],
      }),
      {}
    )
  );

  const columns = names.reduce(
    (a, k, i) => ({ ...a, [k]: data.map((r) => r[i]) }),
    {}
  );

  return { header, names, data, rows, columns };
}
