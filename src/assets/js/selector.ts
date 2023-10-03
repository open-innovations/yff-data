function attachSelector() {
  document.querySelectorAll<HTMLElement>(".selector").forEach((container) => {
    const selector = document.createElement("select");
    selector.id = container.dataset.id!;

    container.querySelectorAll<HTMLElement>(".selector-block").forEach(
      (block) => {
        block.hidden = true;
        const opt = document.createElement("option");
        opt.value = block.id;
        opt.textContent = block.querySelector<HTMLElement>(
          container.dataset.headingLevel || "h2",
        )!.textContent;
        selector.append(opt);
      },
    );
    const options = Array.from(selector.options).map((opt) => opt.value);

    function setVisible() {
      container.querySelectorAll<HTMLElement>(".selector-block").forEach((b) =>
        b.hidden = true
      );
      container.querySelector<HTMLElement>("#" + selector.value)!.hidden =
        false;
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
  });
}
document.addEventListener("DOMContentLoaded", attachSelector);
