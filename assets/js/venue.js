/* Our spaces: capacity table, finder and room details */
(function () {
  var ROOMS = window.BH_ROOMS, LAYOUTS = window.BH_LAYOUTS;
  var state = { guests: 0, layout: "theatre" };
  var params = new URLSearchParams(location.search);
  if (params.get("guests")) state.guests = parseInt(params.get("guests"), 10) || 0;
  if (params.get("layout")) state.layout = params.get("layout");

  var tableEl = document.getElementById("cap-table");
  var cardsEl = document.getElementById("room-cards");
  var guestsEl = document.getElementById("f-guests");
  var pickEl = document.getElementById("f-layout");
  var countEl = document.getElementById("f-count");
  var dialog = document.getElementById("room-dialog");

  function fits(room) { return !state.guests || (room.cap[state.layout] || 0) >= state.guests; }
  function capCell(v) { return v ? v : "–"; }

  function renderPick() {
    pickEl.innerHTML = LAYOUTS.map(function (l) {
      return '<button type="button" data-layout="' + l.id + '" aria-pressed="' + (l.id === state.layout) + '">' + window.bhLayoutIcon(l.id) + l.label + '</button>';
    }).join("");
  }

  function renderTable() {
    var head = '<thead><tr><th scope="col">Room</th><th scope="col">Size</th>' +
      LAYOUTS.map(function (l) { return '<th scope="col">' + window.bhLayoutIcon(l.id) + l.label + '</th>'; }).join("") + '</tr></thead>';
    var body = '<tbody>' + ROOMS.map(function (r) {
      var ok = fits(r);
      return '<tr data-room="' + r.id + '" class="' + (ok ? '' : 'dim') + '" tabindex="0" aria-label="View ' + r.name + '">' +
        '<td class="room">' + r.name + (r.group !== "Meeting rooms" && r.group !== r.name.split(" ")[0] ? '' : '') + '</td>' +
        '<td>' + r.m2 + ' m²</td>' +
        LAYOUTS.map(function (l) {
          var v = r.cap[l.id];
          var cls = !v ? 'na' : (l.id === state.layout && state.guests && v >= state.guests ? 'fit' : '');
          return '<td class="' + cls + '">' + capCell(v) + '</td>';
        }).join("") + '</tr>';
    }).join("") + '</tbody>';
    tableEl.innerHTML = head + body;
  }

  function renderCards() {
    var list = ROOMS.slice().sort(function (a, b) { return (fits(b) - fits(a)); });
    var nFit = ROOMS.filter(fits).length;
    countEl.textContent = state.guests
      ? nFit + (nFit === 1 ? " room fits " : " rooms fit ") + state.guests + " guests in " + label(state.layout).toLowerCase()
      : "Showing all " + ROOMS.length + " rooms";
    cardsEl.innerHTML = list.map(function (r) {
      var ok = fits(r), cap = r.cap[state.layout] || 0;
      var show = cap ? (state.guests ? Math.min(state.guests, cap) : cap) : 0;
      var plan = cap ? window.bhPlan(r, state.layout, show, { compact: true }) : '<svg viewBox="0 0 10 6"><text x="5" y="3.2" font-size=".55" text-anchor="middle" fill="#52606D" font-style="italic" font-family="Lato">Not offered in ' + label(state.layout).toLowerCase() + '</text></svg>';
      return '<article class="room-card' + (ok ? '' : ' is-out') + '">' +
        '<div class="plan">' + plan + '</div>' +
        '<div class="body">' +
          (state.guests ? '<div class="fit-note ' + (ok ? 'ok">Fits your ' + state.guests + ' guests' : 'no">Seats ' + (cap || 0) + ' in this layout') + '</div>' : '') +
          '<h3>' + r.name + '</h3>' +
          '<div class="meta">' + r.m2 + ' m²' + (r.length ? ', ' + window.bhRoomDims(r).L + ' × ' + window.bhRoomDims(r).W + ' m' : '') + '</div>' +
          '<dl>' + LAYOUTS.map(function (l) { var v = r.cap[l.id]; return '<div><dt>' + l.label + '</dt><dd class="' + (v ? '' : 'na') + '">' + capCell(v) + '</dd></div>'; }).join("") + '</dl>' +
          '<div class="actions"><button class="btn btn--line" data-open="' + r.id + '">Room details</button>' +
          '<a class="btn btn--navy" href="../planner/?room=' + r.id + '&layout=' + state.layout + (state.guests ? '&guests=' + state.guests : '') + '">Plan in this room</a></div>' +
        '</div></article>';
    }).join("");
  }

  function label(id) { return (LAYOUTS.find(function (l) { return l.id === id; }) || {}).label || id; }

  function openRoom(id, layout) {
    var r = ROOMS.find(function (x) { return x.id === id; }); if (!r) return;
    layout = layout || (r.cap[state.layout] ? state.layout : LAYOUTS.find(function (l) { return r.cap[l.id]; }).id);
    var d = window.bhRoomDims(r);
    dialog.innerHTML =
      '<div class="rd-head"><div><span class="kicker">' + (r.group === "Meeting rooms" ? "Meeting room" : r.group + " rooms") + '</span><h2>' + r.name + '</h2></div>' +
      '<button class="rd-close" data-close>Close</button></div>' +
      '<div class="rd-body">' +
        '<div><div class="rd-plan">' + window.bhPlan(r, layout, r.cap[layout]) + '</div>' +
        '<div class="layout-pick mt-1" role="group" aria-label="Layout">' + LAYOUTS.filter(function (l) { return r.cap[l.id]; }).map(function (l) {
          return '<button type="button" data-rl="' + l.id + '" aria-pressed="' + (l.id === layout) + '">' + window.bhLayoutIcon(l.id) + l.label + ' · ' + r.cap[l.id] + '</button>';
        }).join("") + '</div>' +
        '<p class="small mt-1">Plans are drawn to the room\'s measurements and show the maximum for each layout. Our events team will confirm the final set-up with you.</p></div>' +
        '<div><p>' + r.summary + '</p>' +
        '<p class="small">' + r.m2 + ' m² · ' + d.L + ' × ' + d.W + ' m' + (r.length ? '' : ' (approximate)') + '</p>' +
        '<h4>In the room</h4><ul class="techlist">' + r.tech.map(function (t) { return '<li>' + t + '</li>'; }).join("") + '</ul>' +
        '<div class="btn-row"><a class="btn btn--book" href="../planner/?room=' + r.id + '&layout=' + layout + '">Plan an event here</a></div></div>' +
      '</div>';
    dialog.dataset.room = r.id;
    if (!dialog.open) dialog.showModal();
  }

  function all() { renderPick(); renderTable(); renderCards(); }

  guestsEl.value = state.guests || "";
  guestsEl.addEventListener("input", function () { state.guests = parseInt(guestsEl.value, 10) || 0; renderTable(); renderCards(); });
  pickEl.addEventListener("click", function (e) { var b = e.target.closest("[data-layout]"); if (!b) return; state.layout = b.dataset.layout; all(); });
  cardsEl.addEventListener("click", function (e) { var b = e.target.closest("[data-open]"); if (b) openRoom(b.dataset.open); });
  tableEl.addEventListener("click", function (e) { var tr = e.target.closest("tr[data-room]"); if (tr) openRoom(tr.dataset.room); });
  tableEl.addEventListener("keydown", function (e) { var tr = e.target.closest("tr[data-room]"); if (tr && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); openRoom(tr.dataset.room); } });
  dialog.addEventListener("click", function (e) {
    if (e.target.closest("[data-close]") || e.target === dialog) dialog.close();
    var b = e.target.closest("[data-rl]"); if (b) openRoom(dialog.dataset.room, b.dataset.rl);
  });
  all();
  if (params.get("room")) openRoom(params.get("room"));
})();
