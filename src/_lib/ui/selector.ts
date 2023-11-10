export function createSelectorElements(page: Document) {
  page.querySelectorAll<HTMLElement>(".selector").forEach((container) => {
    // Create the selector
    const selector = page.createElement("select");
    selector.id = container.dataset.id!;

    // Get the list of option group names requested
    const optionGroupNames: string[] = [];
    container
      .querySelectorAll<HTMLElement>(".selector-block[data-selector-group]")
      .forEach((item) => {
        optionGroupNames.push(item.dataset.selectorGroup!);
      });

    optionGroupNames
      // Get the first instance in the list, in the order they were added
      .filter((current, index, list) => index === list.indexOf(current))
      .forEach((name) => {
        // and create an option group for each
        const optionGroup = page.createElement("optgroup");
        optionGroup.label = name;
        // Append each optionGroup to the selector
        selector.append(optionGroup);
      });

    container.querySelectorAll<HTMLElement>(".selector-block").forEach(
      (block) => {
        const opt = page.createElement("option");
        opt.value = block.id;
        opt.textContent = block.querySelector<HTMLElement>(
          container.dataset.headingLevel || "h2",
        )!.textContent;

        // Get the optionGroup that this is to be added to. Default to the root selector;
        const optionGroup = block.dataset.selectorGroup
          ? selector.querySelector(
            `optgroup[label="${block.dataset.selectorGroup}"]`,
          )!
          : selector;
        optionGroup.append(opt);
      },
    );

    const label = page.createElement("label");
    label.textContent = container.dataset.label!;
    label.setAttribute("for", selector.id);

    const form = page.createElement("form");
    form.style.display = 'none';
    form.append(selector);
    form.insertBefore(label, selector);

    container.insertBefore(
      form,
      container.dataset.selectorPosition === "top"
        ? container.firstChild
        : null,
    );

  });
}

export function hydrateSelectorElements() {
  document.querySelectorAll<HTMLElement>(".selector").forEach((container) => {
    const selector = container.querySelector('select')!;

    // Block scoped to mask options and selected
    {
      const options = Array.from(selector.options).map((opt) => opt.value);
      const selected = new URLSearchParams(location.search).get(selector.id);
      if (selected && options.includes(selected)) {
        selector.value = selected;
      }
    }

    function setVisible() {
      container.querySelectorAll<HTMLElement>(".selector-block").forEach((b) =>
        b.hidden = true
      );
      container.querySelector<HTMLElement>("#" + selector.value)!.hidden =
        false;
    }
    setVisible();
    selector.parentElement.style.display = null;

    function updateState() {
      const url = new URL(location.toString());
      url.searchParams.set(selector.id, selector.value);
      history.pushState("", "", url.pathname + url.search);
    }

    selector.addEventListener("change", setVisible);
    selector.addEventListener("change", updateState);
  });
}
