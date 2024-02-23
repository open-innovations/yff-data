import { consent } from "./tracking-consent.ts";

let tag: string;

function startTracking() {
  // Do nothing if no consent has been given
  if (!consent.hasConsented) return;

  const gtm = document.createElement("script");
  gtm.async = true;
  gtm.src = `https://www.googletagmanager.com/gtag/js?id=${tag}`;
  document.head.appendChild(gtm);

  globalThis.dataLayer = globalThis.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  gtag("js", new Date());
  gtag("config", tag);
}

export function initAnalytics(id: string) {
  // Try to start tracking at the point the document has loaded
  tag = id;
  startTracking();
  consent.addEventListener("consentUpdated", startTracking);
}
