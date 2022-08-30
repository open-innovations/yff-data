export const css = `
  .download-link {
    display: block;
    padding: 0.5rem 0.7rem;
  }
`;

export default function ({ link }) {
  if (link === undefined) return;
  return `<a class='download-link orange' href="${link}">Download the report</a>`;
}