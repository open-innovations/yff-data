import { parse } from 'std/encoding/csv.ts';
import { transpose } from '/oi/util.js';

const FLOAT = 'float';
const INTEGER = 'integer';
const YEAR = 'year';
const BOOLEAN = 'boolean';
const URL = 'url';
const DATETIME = 'datetime';
const STRING = 'string';
const TIME = 'time';
const HEADER_SEPARATOR = '---';

const urlMatcher =
  /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)/;
const timeMatcher = /^[0-2]?[0-9]\:[0-5][0-9]$/;

function guessType(value: string) {
  if (typeof value === 'undefined') return undefined;

  // Remove any quotes around the column value
  const cleaned = value.trim().replace(/(^\"|\"$)/, '');

  if (isFinite(parseFloat(value))) {
    // if (parseInt(value).toString() === value) {
    //   const intValue = parseInt(value);
    //   if (intValue > 1700 && intValue < 2100) return YEAR;
    //   return INTEGER;
    // }
    return FLOAT;
  }
  // if (value.match(/^(true|false)$/i)) return BOOLEAN;
  // if (value.match(urlMatcher)) return URL;
  // if (!isNaN(Date.parse(value))) return DATETIME;
  // if (value.match(timeMatcher)) return TIME;
  // Default to a string
  return STRING;
}

export default async function csvLoader(path: string) {
  const text = await Deno.readTextFile(path);
  const raw = await (<Promise<[string[]]>>parse(text));

  const separatorRow = raw.findIndex(x => x[0] === HEADER_SEPARATOR);
  if (separatorRow > 0) raw.splice(separatorRow, 1);
  
  // Calculate types for all cells
  const types = raw.map((rows) => rows.map(guessType));

  const headerRowCount = separatorRow > 1 ? separatorRow : 1;
  // Grab the header
  const header = raw.slice(0, headerRowCount);
  // Construct the column names by concatenating columns
  const names: string[] = transpose(header).map((r: string[]) => r.join('.'));
  // Grab the data
  const data = raw.slice(headerRowCount);

  // Construct a list of objects as key / value pairs
  const rows = data.map((row) =>
    names.reduce(
      (a, k, i) => ({
        ...a,
        [k]: row[i],
      }),
      {}
    )
  );

  // Create an object with data lists
  const columns = names.reduce(
    (a, k, i) => ({ ...a, [k]: data.map((r) => r[i]) }),
    {}
  );

  return { header, names, data, rows, columns, types, raw };
}
