/**
 * This class encapsulates all the logic related to tracking consent.
 *
 * It uses localStorage (stored under the `consentKey`) to record the timestamp
 * for the date consent was granted. This is persistent for a given browser.
 *
 * It uses sessionStorage (stored under the `responseKey`) to record in-session
 * response. This can be used to avoid showing popups within a session.
 *
 * When it starts up, it checks if the consent is over a certain age, and removes
 * consent if it has expired.
 *
 * It raises a `consentUpdated` event when the consent status changes. Code can
 * listen to an event on this element to respond to changes. The event detail is
 * the new consent status (true or false).
 */
class TrackingConsent extends EventTarget {
  /** Consent key name - used in localStorage */
  private consentKey: string;
  /** Response key name - used in sessionStorage */
  private responseKey: string;
  /** Maxiumum age for consent in milliseconds for consent - 90 days */
  private maxAge = 90 * 24 * 60 * 60 * 1000;

  constructor(key: string) {
    super();
    // Set the keys
    this.consentKey = key;
    this.responseKey = key + ".responded";

    // On creation, check if the token has expired
    if (this.expired) {
      this.consentToken = null;
      this.responseToken = null;
    }

    // If storage changes, send an event to anyone listening
    // NB this doesn't trigger in the same session - primarily useful if something changes elsewhere
    addEventListener("storage", (event) => {
      console.dir(event)
      // If the key that changed was ours
      if (event.key == this.consentKey) {
        this.raiseUpdateEvent();
      }
    });
  }
  /* Public getters */
  /**
   * Check if the token is older than the maxAge. Return true if expired.
   */
  get expired() {
    if (this.consentToken == null) return false;
    const age = Date.now() - parseInt(this.consentToken);
    return age > this.maxAge;
  }

  /**
   * Check if the site user has consented
   */
  get hasConsented() {
    return this.consentToken !== null;
  }
  /**
   * Check if the site user has responded in this browser session
   */
  get hasResponded() {
    return this.responseToken !== null;
  }

  /**
   * Record acceptance of tracking consent
   */
  accept() {
    this.consentToken = `${Date.now()}`;
    this.raiseUpdateEvent();
  }
  /**
   * Record acceptance of tracking consent
   */
  reject() {
    this.consentToken = null;
    this.responseToken = `${Date.now()}`;
    this.raiseUpdateEvent();
  }

  /** Private getters and setters */
  private get consentToken() {
    return globalThis.localStorage.getItem(this.consentKey);
  }
  private set consentToken(token: string | null) {
    if (token == null) {
      globalThis.localStorage.removeItem(this.consentKey);
      return;
    }
    globalThis.localStorage.setItem(this.consentKey, token);
  }
  private get responseToken() {
    return globalThis.sessionStorage.getItem(this.responseKey);
  }
  private set responseToken(value: string | null) {
    if (value == null) {
      globalThis.sessionStorage.removeItem(this.responseKey);
      return;
    }
    globalThis.sessionStorage.setItem(this.responseKey, value);
  }

  /** Event triggering */
  private raiseUpdateEvent() {
    return this.dispatchEvent(
      new CustomEvent<boolean>("consentUpdated", {
        bubbles: false,
        detail: this.hasConsented,
      }),
    );
  }
}

export const consent = new TrackingConsent("yff.tracking.consent");

globalThis.oi = {
  ...globalThis.oi,
  tracking: consent,
};
