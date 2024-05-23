export function createSelectorElements(page: Document) {
  page.querySelectorAll<HTMLElement>(".selector").forEach((container) => {
    // Create the selector
    const selector = page.createElement("select");
    selector.id = container.getAttribute('data-id')!;

    // Get the list of option group names requested
    const optionGroupNames: string[] = [];
    container
      .querySelectorAll<HTMLElement>(".selector-block[data-selector-group]")
      .forEach((item) => {
        optionGroupNames.push(item.getAttribute('data-selector-group')!);
      });

    optionGroupNames
      // Get the first instance in the list, in the order they were added
      .filter((current, index, list) => index === list.indexOf(current))
      .forEach((name) => {
        // and create an option group for each
        const optionGroup = page.createElement("optgroup");
        optionGroup.setAttribute('label', name);
        // Append each optionGroup to the selector
        selector.append(optionGroup);
      });

    container.querySelectorAll<HTMLElement>(".selector-block").forEach(
      (block) => {
        const opt = page.createElement("option");
        opt.setAttribute('value', block.getAttribute('id')!);
        opt.textContent = block.querySelector<HTMLElement>(
          container.getAttribute('data-heading-level') || "h2"
        )!.textContent;

        // Get the optionGroup that this is to be added to. Default to the root selector;
        const selectorGroup = block.getAttribute('data-selector-group')
        const optionGroup = selectorGroup
          ? selector.querySelector(
              `optgroup[label="${selectorGroup}"]`
          )!
          : selector;
        optionGroup.append(opt);
      },
    );

    const label = page.createElement("label");
    label.textContent = container.getAttribute('data-label')!;
    label.setAttribute("for", selector.id);

    const form = page.createElement("form");
    form.setAttribute('style', 'display:none');
    form.append(selector);
    form.insertBefore(label, selector);

    container.insertBefore(
      form,
      container.getAttribute('data-selector-position') === "top"
        ? container.firstChild
        : null,
    );

  });
}

export function selectorProcessor(page) {
  createSelectorElements(page.document);
}

export function hydrateSelectorElements() {
  document.querySelectorAll<HTMLSelectElement>(".selector select").forEach((selector) => {
    const form = selector.parentElement as HTMLFormElement;
    if (form === null) return;
    const container = form.parentElement;
    if (container === null) return;

    // Block scoped to mask options and selected
    {
      const options = Array.from(selector.options).map((opt) => opt.value);
      const selected = new URLSearchParams(location.search).get(selector.id);
      if (selected && options.includes(selected)) {
        selector.value = selected;
      }
    }

    function setVisible() {
      container!.querySelectorAll<HTMLElement>(".selector-block").forEach((b) =>
        b.hidden = true
      );
      container!.querySelector<HTMLElement>("#" + selector.value)!.hidden =
        false;
    }
    setVisible();
    form.style.display = '';

    function updateState() {
      const url = new URL(location.toString());
      url.searchParams.set(selector.id, selector.value);
      history.pushState("", "", url.pathname + url.search);
    }

    selector.addEventListener("change", setVisible);
    selector.addEventListener("change", updateState);
  });
}
