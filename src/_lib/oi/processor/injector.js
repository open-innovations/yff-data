export default function injector(page) {
  // This works only on elements with both data-injector-url and data-injector-selector attributes set
  page.document.querySelectorAll('[data-injector-url][data-injector-selector]').forEach((insertionPoint) => {
    // Get the source url and selector
    const sourceUrl = insertionPoint.getAttribute('data-injector-url');
    if (!sourceUrl) return;
    const sourceSelector = insertionPoint.getAttribute('data-injector-selector')
    if (!sourceSelector) return;

    // Find the page which matches that URL
    const targetPage = page.data.search.page("url="+sourceUrl);
    if (!targetPage) return;

    // Get the first instance of the seletor from that page.
    // Clone that so we can operate on it with no fear of breaking the original.
    const featuredContent = targetPage.page.document.querySelector(sourceSelector).cloneNode(true);
    if (!featuredContent) return;

    // Remove any links
    // TODO maybe make this optional
    featuredContent.querySelectorAll('a').forEach(a => a.parentNode.removeChild(a));

    // Set the content of the insertion point
    insertionPoint.innerHTML = featuredContent.innerHTML;
  });
}