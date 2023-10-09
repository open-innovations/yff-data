export default function injector(page) {
  page.document.querySelectorAll('[data-injector-url][data-injector-selector]').forEach((insertionPoint) => {
    const sourceUrl = insertionPoint.getAttribute('data-injector-url');
    if (!sourceUrl) return;

    const sourceSelector = insertionPoint.getAttribute('data-injector-selector')
    if (!sourceSelector) return;

    const targetPage = page.data.search.page("url="+sourceUrl);
    if (!targetPage) return;

    const featuredContent = targetPage.document.querySelector(sourceSelector).cloneNode(true);
    if (!featuredContent) return;

    // Remove any links
    featuredContent.querySelectorAll('a').forEach(a => a.parentNode.removeChild(a));

    insertionPoint.innerHTML = featuredContent.innerHTML;
  });
}