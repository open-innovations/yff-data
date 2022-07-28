export const css = `
  .tag-cloud {
    list-style: none;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    font-size: 0.8em;
  }
  .tag-cloud li {
    padding: 0.3rem 0.7rem;
    border-radius: 0.3rem;
  }
`;

export default function ({ tags = [] }) {
  if (tags.length < 1) return;
  let items = tags;
  items = tags.map(t => `<li>${t}</li>`);
  return `<ul class='tag-cloud'>${items.join('')}</ul>`;
}
