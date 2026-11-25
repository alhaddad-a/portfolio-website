// Runs before first paint: marks that JavaScript is available, so progressive
// enhancements (register filters) can show their controls. Kept as a file, not
// inline, so the Content-Security-Policy can forbid inline scripts.
document.documentElement.classList.add('js');
