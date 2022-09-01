import * as yaml from 'std/encoding/yaml.ts';
import Ajv from 'https://esm.sh/ajv@8.11.0';
import { ReportSchema } from './schema.ts';

const ajv = new Ajv();
const validate = ajv.compile(ReportSchema);

await Deno.writeTextFile('lib/report.schema.json', JSON.stringify(validate.schema, null, 2));

async function process(filePath: string) {
  const content = await Deno.readTextFile(filePath)

  const document: any = yaml.parse(content, {});

  const valid = validate(document);
  if (!valid) console.log(validate.errors);
}

console.log(Deno.args);

const filePath = Deno.args[0];
if (filePath === undefined) Deno.exit();

process(filePath);
