import { parse } from "https://deno.land/std@0.192.0/yaml/parse.ts";

export async function patchVisualisation<T>(filename: string, patchFunction: (config: T) => T) {
  const text = await Deno.readTextFile(filename);
  
  const viz = parse(text) as T;
  return patchFunction(viz);
}

