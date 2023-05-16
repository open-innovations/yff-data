export const js = `
  addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-list-selector]').forEach((filter) => {
      const theList = document.querySelector(filter.dataset.listSelector);

      const clearFilter = () => {
        Array.from(theList.children).forEach(i => i.hidden = false);
      }
      const setFilter = (filter) => {
        Array.from(theList.children).forEach(i => {
          const matches = i.innerText.toUpperCase().match(filter.toUpperCase()) === null;
          i.hidden = matches;
        });
      }
      function updateFilter() {
        const filter = this.value;
        if (!filter) {
          clearFilter();
          return;
        }
        setFilter(this.value);
      }
      filter.addEventListener('input', updateFilter);
    });
  });
`;

export const css = `
.filter-container {
  display: flex;
  gap: 1em;
  align-items: baseline;
}
.filter-container input {
  flex-grow: 1;
}
`;

export default function ({ label, selector }) {
  const id = crypto.randomUUID();
  return `<div class="filter-container">
    <label for="${ id }">${ label }</label><input id="${ id }" data-list-selector="${ selector }" type="text"/>
  </div>`;
}
