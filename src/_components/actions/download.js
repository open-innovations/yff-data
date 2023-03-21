import { existsSync } from "https://deno.land/std/fs/mod.ts";

export const css = `
  .download-link {
    display: block;
    padding: 0.5rem 0.7rem;
  }
`;

export default function ({ link, note }) {
  if (link === undefined) return;
  // Create a note if the download file doesn't exist
  if (note === undefined) { 
    return `<a class='download-link orange' href="${link}">Get the report</a>`;
  }
  else return  `<a class='download-link orange' href="${link}">${note}</a>`;
     
  /*if (!existsSync(link)) {
    console.error('WARNING: Download file '+link+' does not exist.');
    note = '<span class="note">No PDF yet</span>';
  }*/
  return `<a class='download-link orange' href="${link}">${note}Get the report</a>`;
}