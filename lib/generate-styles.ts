import { namedColours } from "../yff-config.ts"
import { encode } from 'std/encoding/base64.ts';

const sanitizeName = (n: string) => n.toLowerCase().replace(/[^a-z0-9\-]/g, '-').replace(/\-+/g, '-')

const generateStyleSheet = () => {
  const vars = Object.entries(namedColours).map(([name, colour]) => {
    return `  --yff-${sanitizeName(name)}:${colour};`;
  });
  const css = `:root {
${ vars.join('\n') }
}`;
  return css;
}

export const getNamedColourStyles = () => {
  const stylesheet = generateStyleSheet();
  return `data:text/css;base64,${ encode(stylesheet) }`;
}