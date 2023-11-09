function attachSelector() {
  document.querySelectorAll<HTMLElement>(".selector").forEach((container) => {
    const selector = document.createElement("select");
    selector.id = container.dataset.id!;

    const optionGroupNames: string[] = [];
    container
      .querySelectorAll<HTMLElement>(".selector-block[data-selector-group]")
      .forEach((item) => {
        optionGroupNames.push(item.dataset.selectorGroup!);
      });

    // Get a unique list of elements, in the order they were added
    // and create an option group for each
    const optionGroups = optionGroupNames
      .filter((current, index, list) => index === list.indexOf(current))
      .map((name) => {
        const optionGroup = document.createElement("optgroup");
        optionGroup.label = name;
        return optionGroup;
      });
    // Append each optionGroup to the selector
    optionGroups.forEach((optionGroup) => selector.append(optionGroup));

    container.querySelectorAll<HTMLElement>(".selector-block").forEach(
      (block) => {
        block.hidden = true;
        const opt = document.createElement("option");
        opt.value = block.id;
        opt.textContent = block.querySelector<HTMLElement>(
          container.dataset.headingLevel || "h2",
        )!.textContent;

        // Get the optionGroup that this is to be added to. Default to the root selector;
        const optionGroup = optionGroups.find((x) =>
          x.label === block.dataset.selectorGroup
        ) || selector;
        optionGroup.append(opt);
      },
    );
    const options = Array.from(selector.options).map((opt) => opt.value);

    // Block scoped to mask selected
    {
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
    function updateState() {
      const url = new URL(location.toString());
      url.searchParams.set(selector.id, selector.value);
      history.pushState("", "", url.pathname + url.search);
    }

    setVisible();

    const label = document.createElement("label");
    label.textContent = container.dataset.label!;
    label.setAttribute("for", selector.id);

    const form = document.createElement("form");
    form.append(selector);
    form.insertBefore(label, selector);

    container.append(form);

    selector.addEventListener("change", setVisible);
    selector.addEventListener("change", updateState);
  });
}
document.addEventListener("DOMContentLoaded", attachSelector);
