import { Document, initParser } from 'https://deno.land/x/deno_dom/deno-dom-wasm-noinit.ts';

await initParser();
export const document = new Document();
