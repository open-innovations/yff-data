import { createSelectorElements, hydrateSelectorElements } from "../../_lib/ui/selector.ts";

document.addEventListener("DOMContentLoaded", () => {
  createSelectorElements(document);
  hydrateSelectorElements();
});
