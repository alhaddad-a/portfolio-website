// Progressive enhancement only: without JavaScript every investigation is listed as plain HTML.
(function () {
  var list = document.getElementById('r-list');
  if (!list) return;
  var rows = Array.prototype.slice.call(list.children);
  var limit = parseInt(list.getAttribute('data-preview') || '0', 10);
  var expanded = false;
  var moreWrap = document.querySelector('.r-more-wrap');
  var moreBtn = document.querySelector('[data-show-all]');
  var countEl = document.querySelector('[data-count]');
  var empty = document.querySelector('.r-empty');
  var reset = document.querySelector('.f-reset');
  var caseSel = document.getElementById('f-case');
  var statusSel = document.getElementById('f-status');
  var params = new URLSearchParams(window.location.search);
  var state = { case: params.get('case') || '', status: params.get('status') || '' };

  function matches(r) {
    var st = r.getAttribute('data-status');
    return (!state.case || (' ' + r.getAttribute('data-src') + ' ').indexOf(' ' + state.case + ' ') > -1) &&
      (!state.status || st === state.status || (state.status === 'open' && st === 'reopened'));
  }

  function apply(updateUrl) {
    var filtered = Boolean(state.case || state.status);
    var total = 0;
    var visible = 0;
    rows.forEach(function (r) {
      var ok = matches(r);
      if (ok) total++;
      var show = ok && (filtered || expanded || visible < limit);
      r.hidden = !show;
      if (show) visible++;
    });
    if (caseSel) caseSel.value = state.case;
    if (statusSel) statusSel.value = state.status;
    if (countEl) countEl.textContent = visible;
    if (moreWrap) moreWrap.hidden = filtered || expanded || total <= limit;
    if (empty) empty.hidden = total !== 0;
    if (reset) reset.hidden = !filtered;
    if (updateUrl) {
      var q = new URLSearchParams();
      if (state.case) q.set('case', state.case);
      if (state.status) q.set('status', state.status);
      var qs = q.toString();
      history.replaceState(null, '', (qs ? '?' + qs : window.location.pathname) + '#register');
    }
  }

  if (moreBtn) moreBtn.addEventListener('click', function () {
    expanded = true;
    apply(false);
    var next = rows[limit] && rows[limit].querySelector('a');
    if (next) next.focus();
  });
  if (caseSel) caseSel.addEventListener('change', function () { state.case = caseSel.value; apply(true); });
  if (statusSel) statusSel.addEventListener('change', function () { state.status = statusSel.value; apply(true); });
  if (reset) reset.addEventListener('click', function () { state = { case: '', status: '' }; apply(true); });
  apply(false);
})();
