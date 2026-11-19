// Runs before first paint (loaded synchronously in <head>) to apply the saved theme
// without a flash. Kept as a file, not inline, so the CSP can forbid inline scripts.
(function () {
  var d = document.documentElement;
  d.classList.add('js');
  try {
    var t = localStorage.getItem('theme');
    if (t === 'dark' || t === 'light') d.setAttribute('data-theme', t);
  } catch (e) {}
})();
