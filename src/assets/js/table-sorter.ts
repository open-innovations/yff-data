function reverseBody(table: TableElement) {
  const tbody = table.querySelector("tbody.reverse");
  if (!tbody) return;
  Array.from(tbody.children).toReversed().forEach((row) =>
    tbody.appendChild(row)
  );
}

addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("table").forEach(reverseBody);
});
