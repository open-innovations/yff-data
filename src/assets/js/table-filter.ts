import search from "lume/plugins/search.ts";
import filter from "./src/_components/filter.js";

function inflateTable(table: HTMLTableElement) {
  const rows = table.querySelectorAll('tr')
  const tableData = Array.from(rows).map(row => {
    const cols = Array.from(row.querySelectorAll('td')).map(c => ({ text: c.innerText, span: c.rowSpan }))
    return cols
  }).filter(r => r.length > 0);

  tableData.forEach((row, rowIndex) => {
    const rowBefore = tableData[rowIndex - 1]!;
    if (!rowBefore) return;
    rowBefore.forEach((cell, cellIndex) => {
      if (cell.span == 1) return;
      row.splice(cellIndex, 0, { span: cell.span - 1, text: cell.text });
    })
  });
  return tableData.map(row => row.map(cell => cell.text));
}

const uniqueValues = <T>(value: T, index: number, self: T[]) => self.indexOf(value) === index;

const addOption = (select: HTMLSelectElement, value: string, text?: string) => {
  const opt = document.createElement('option');
  opt.value = value;
  opt.innerText = text || value;
  select.append(opt);
}

const EVENT_FILTER_CHANGE = 'filter-change';

function initialise() {
  const filters = document.querySelectorAll<HTMLTableElement>('[data-filter-col]');
  filters.forEach((filterRoot, filterIndex) => {
    const table = filterRoot.querySelector('table');
    if (!table) return;

    // Update table
    {
      const filterCol = parseInt(filterRoot.dataset.filterCol!) - 1;
      const tableData = inflateTable(table);
      table.querySelectorAll<HTMLTableCellElement>('tr:has(td)').forEach((row, index)=> {
        row.dataset.filterValue = tableData[index][filterCol];
      });
    }

    const filterGroup = filterRoot.dataset.filterGroup;

    // Create picker
    const targets = Array.from(table.querySelectorAll<HTMLTableRowElement>('tr[data-filter-value]'));
    const values = targets.map(row => row.dataset.filterValue).filter(uniqueValues);
    const container = document.createElement('form')
    const picker = document.createElement('select');
    addOption(picker, "", filterRoot.dataset.filterDefault || "- select a value -");
    values.forEach(v => addOption(picker, v!));
    if (filterGroup) {
      const currentValue = new URLSearchParams(location.search).get(filterGroup) || "";
      picker.value = currentValue;
    }
    picker.id = `filter-picker-${filterIndex}`;
    const label = document.createElement('label');
    label.setAttribute('for', picker.id);
    label.innerText = filterRoot.dataset.filterLabel || 'Filter table';
    container.append(label);
    container.append(picker);
    table.parentNode!.insertBefore(container, table);

    function updateState() {
      const url = new URL(location.toString());
      url.searchParams.set(filterGroup!, picker.value);
      history.pushState("", "", url.pathname + url.search);
    }      

    function setTargets() {
      const value = picker.value;
      if (value == '') {
        targets.forEach(t => t.hidden = false);
      } else {
        targets.forEach(t => t.hidden = t.dataset.filterValue != value);
      }
      if (filterGroup) {
        globalThis.dispatchEvent(new CustomEvent(EVENT_FILTER_CHANGE, { detail: { value, group: filterGroup } }))
        updateState();
      }
    }

    if (filterGroup) {
      globalThis.addEventListener(EVENT_FILTER_CHANGE, (event) => {
        const { group, value } = (<CustomEvent>event).detail!;
        if (group !== filterGroup ) return;
        if (value === picker.value ) return;
        picker.value = value;
        console.log({
          group,
          value,
          filterGroup,
          currentValue: picker.value,
        });
      })
    }
    setTargets();
    picker.addEventListener('change', setTargets);
  });

}

addEventListener('DOMContentLoaded', initialise);