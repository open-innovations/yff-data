document.addEventListener('DOMContentLoaded', () => {
  var navButton = document.querySelector('#navigation button');
  navButton.addEventListener('click', function() {
    let expanded = this.getAttribute('aria-expanded') === 'true' || false;
    this.setAttribute('aria-expanded', !expanded);
  });
})
