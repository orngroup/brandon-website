/* ==========================================================
   Floor plans drawn to scale, in metres.
   bhPlan(room, layoutId, guests, opts) -> SVG string
   The front of the room (screen / stage / top table) is the
   left-hand wall. Plans are indicative; the events team
   confirms the final set-up.
   ========================================================== */
(function () {
  var NAVY = "#2C3E50", GOLD = "#BB9979", BURNT = "#AB3C0C";
  var TABLE = "#E5DBCB", PAPER = "#FBF9F5";

  function r2(n) { return Math.round(n * 100) / 100; }

  // Small seeded random so reception plans don't jump around.
  function seeded(seed) {
    var s = seed % 2147483647; if (s <= 0) s += 2147483646;
    return function () { s = s * 16807 % 2147483647; return (s - 1) / 2147483646; };
  }

  function chair(x, y, rot) {
    return '<rect x="' + r2(x - .22) + '" y="' + r2(y - .22) + '" width=".44" height=".44" rx=".08" fill="#fff" stroke="' + NAVY + '" stroke-width=".05"' +
      (rot ? ' transform="rotate(' + rot + ' ' + r2(x) + ' ' + r2(y) + ')"' : '') + '/>';
  }

  function plan(room, layout, guests, opts) {
    opts = opts || {};
    var d = window.bhRoomDims(room), L = d.L, W = d.W;
    var cap = room.cap[layout] || 0;
    var n = Math.max(0, Math.min(guests || cap, cap));
    var pad = Math.max(L, W) * 0.09 + 0.6;
    var fs = Math.max(L, W) / 34 + 0.12;
    var out = [], seats = 0;

    // Front of room
    function front(label) {
      out.push('<rect x=".12" y="' + r2(W * .28) + '" width=".22" height="' + r2(W * .44) + '" fill="' + BURNT + '"/>');
      if (!opts.compact) out.push('<text x=".55" y="' + r2(W / 2) + '" font-size="' + r2(fs * .8) + '" fill="' + BURNT + '" font-style="italic" dominant-baseline="middle" transform="rotate(-90 .55 ' + r2(W / 2) + ')" text-anchor="middle">' + label + '</text>');
    }

    if (layout === "theatre") {
      front("Screen");
      var x0 = Math.min(2.2, L * .22), aisle = W > 5 ? 1.1 : 0.8;
      var usableW = W - 1.0 - aisle;
      var perSide = Math.max(1, Math.floor(usableW / 2 / .55));
      var perRow = perSide * 2;
      var rows = Math.ceil(n / perRow);
      var pitch = Math.min(1.1, (L - x0 - .6) / Math.max(rows, 1));
      for (var r = 0; r < rows; r++) {
        var x = x0 + r * pitch;
        for (var s = 0; s < perRow && seats < n; s++) {
          var side = s < perSide ? 0 : 1, k = s % perSide;
          var y = side === 0 ? (W / 2 - aisle / 2 - .3 - k * .55) : (W / 2 + aisle / 2 + .3 + k * .55);
          out.push(chair(x, y, 90)); seats++;
        }
      }
    }
    else if (layout === "boardroom") {
      front("Screen");
      var perLong = Math.ceil(Math.max(n - 2, 0) / 2);
      var tl = Math.min(L - 2.2, Math.max(1.8, perLong * .7 + .4));
      var tw = n > 16 ? 1.5 : 1.2;
      var tx = (L - tl) / 2 + .3, ty = (W - tw) / 2;
      out.push('<rect x="' + r2(tx) + '" y="' + r2(ty) + '" width="' + r2(tl) + '" height="' + r2(tw) + '" rx=".12" fill="' + TABLE + '" stroke="' + NAVY + '" stroke-width=".05"/>');
      var heads = n > 4 ? 2 : 0;
      var along = n - heads, top = Math.ceil(along / 2), bottom = along - top;
      for (var i = 0; i < top; i++) { out.push(chair(tx + (i + .5) * tl / top, ty - .38, 0)); seats++; }
      for (var j = 0; j < bottom; j++) { out.push(chair(tx + (j + .5) * tl / bottom, ty + tw + .38, 0)); seats++; }
      if (heads) { out.push(chair(tx - .38, W / 2, 90)); out.push(chair(tx + tl + .38, W / 2, 90)); seats += 2; }
    }
    else if (layout === "ushape") {
      front("Screen");
      var depth = .6;
      var ux0 = Math.min(2.4, L * .24), ux1 = L - .9;
      var uy0 = Math.max(.9, W * .14), uy1 = W - uy0;
      // base (far end) and two arms
      out.push('<rect x="' + r2(ux1 - depth) + '" y="' + r2(uy0) + '" width="' + depth + '" height="' + r2(uy1 - uy0) + '" fill="' + TABLE + '" stroke="' + NAVY + '" stroke-width=".05"/>');
      out.push('<rect x="' + r2(ux0) + '" y="' + r2(uy0) + '" width="' + r2(ux1 - ux0 - depth) + '" height="' + depth + '" fill="' + TABLE + '" stroke="' + NAVY + '" stroke-width=".05"/>');
      out.push('<rect x="' + r2(ux0) + '" y="' + r2(uy1 - depth) + '" width="' + r2(ux1 - ux0 - depth) + '" height="' + depth + '" fill="' + TABLE + '" stroke="' + NAVY + '" stroke-width=".05"/>');
      var baseLen = uy1 - uy0 - 2 * depth, armLen = ux1 - ux0 - depth;
      var baseN = Math.min(Math.max(1, Math.floor(baseLen / .65)), Math.round(n * baseLen / (baseLen + 2 * armLen)));
      var armN = n - baseN, armA = Math.ceil(armN / 2), armB = armN - armA;
      for (var a = 0; a < baseN; a++) { out.push(chair(ux1 + .38, uy0 + depth + (a + .5) * baseLen / baseN, 90)); seats++; }
      for (var b = 0; b < armA; b++) { out.push(chair(ux0 + (b + .5) * armLen / armA, uy0 - .38, 0)); seats++; }
      for (var c = 0; c < armB; c++) { out.push(chair(ux0 + (c + .5) * armLen / armB, uy1 + .38, 0)); seats++; }
    }
    else if (layout === "cabaret") {
      front("Stage");
      var perTable = 8, tables = Math.ceil(n / perTable);
      var cx0 = Math.min(2.6, L * .2), areaL = L - cx0 - .8, areaW = W - 1.2;
      var cols = Math.max(1, Math.round(Math.sqrt(tables * areaL / areaW)));
      var rowsC = Math.ceil(tables / cols);
      while (rowsC * cols < tables) cols++;
      var gx = areaL / cols, gy = areaW / rowsC;
      var tr = Math.max(.45, Math.min(.8, Math.min(gx, gy) * .27));
      var placed = 0;
      for (var rr = 0; rr < rowsC; rr++) for (var cc = 0; cc < cols; cc++) {
        if (placed >= tables) break;
        var cxT = cx0 + (cc + .5) * gx, cyT = .6 + (rr + .5) * gy;
        out.push('<circle cx="' + r2(cxT) + '" cy="' + r2(cyT) + '" r="' + r2(tr) + '" fill="' + TABLE + '" stroke="' + NAVY + '" stroke-width=".05"/>');
        var here = Math.min(perTable, n - placed * perTable);
        // leave the side facing the front open
        for (var q = 0; q < here; q++) {
          var ang = Math.PI * (0.32 + 1.36 * (here === 1 ? .5 : q / (here - 1)));
          var chx = cxT - Math.cos(ang) * (tr + .32), chy = cyT + Math.sin(ang) * (tr + .32);
          out.push(chair(chx, chy, 0)); seats++;
        }
        placed++;
      }
    }
    else { // reception
      var rnd = seeded(room.id.length * 997 + n * 13 + Math.round(L * 10));
      var poseurs = Math.max(2, Math.round(n / 14));
      var pc = Math.ceil(Math.sqrt(poseurs * L / W)), pr = Math.ceil(poseurs / pc), p = 0;
      for (var pi = 0; pi < pr; pi++) for (var pj = 0; pj < pc; pj++) {
        if (p++ >= poseurs) break;
        out.push('<circle cx="' + r2((pj + .5) * L / pc) + '" cy="' + r2((pi + .5) * W / pr) + '" r=".35" fill="' + TABLE + '" stroke="' + NAVY + '" stroke-width=".05"/>');
      }
      var dots = Math.min(n, 220);
      for (var g = 0; g < dots; g++) {
        out.push('<circle cx="' + r2(.4 + rnd() * (L - .8)) + '" cy="' + r2(.4 + rnd() * (W - .8)) + '" r=".16" fill="' + NAVY + '" fill-opacity=".55"/>');
      }
      seats = n;
    }

    // Scale bar
    var bar = L > 12 ? 5 : (L > 6 ? 2 : 1);
    var sb = '<g transform="translate(0 ' + r2(W + pad * .55) + ')">' +
      '<rect x="0" y="0" width="' + bar + '" height=".12" fill="' + NAVY + '"/>' +
      '<rect x="0" y="-.12" width=".04" height=".36" fill="' + NAVY + '"/><rect x="' + r2(bar - .04) + '" y="-.12" width=".04" height=".36" fill="' + NAVY + '"/>' +
      '<text x="' + r2(bar + .25) + '" y=".1" font-size="' + r2(fs * .85) + '" fill="' + NAVY + '" dominant-baseline="middle">' + bar + ' m</text></g>';

    var dims = opts.compact ? '' :
      '<text x="' + r2(L / 2) + '" y="' + r2(-pad * .35) + '" font-size="' + r2(fs) + '" fill="' + NAVY + '" text-anchor="middle">' + L + ' m</text>' +
      '<text x="' + r2(L + pad * .42) + '" y="' + r2(W / 2) + '" font-size="' + r2(fs) + '" fill="' + NAVY + '" text-anchor="middle" transform="rotate(90 ' + r2(L + pad * .42) + ' ' + r2(W / 2) + ')">' + W + ' m</text>';

    var vb = [-pad, -pad, L + pad * 2, W + pad * 2 + (opts.compact ? 0 : pad * .3)].map(r2).join(" ");
    var title = room.name + ", " + (window.BH_LAYOUTS.find(function (l) { return l.id === layout; }) || {}).label + " layout for " + seats + " guests";

    return '<svg viewBox="' + vb + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="' + title + '" font-family="Lato, sans-serif">' +
      '<title>' + title + '</title>' +
      '<rect x="0" y="0" width="' + L + '" height="' + W + '" fill="' + PAPER + '"/>' +
      '<rect x="0" y="0" width="' + L + '" height="' + W + '" fill="none" stroke="' + NAVY + '" stroke-width=".16"/>' +
      '<rect x=".2" y=".2" width="' + r2(L - .4) + '" height="' + r2(W - .4) + '" fill="none" stroke="' + GOLD + '" stroke-width=".03"/>' +
      out.join("") + dims + (opts.compact ? '' : sb) + '</svg>';
  }

  // Small pictogram for each layout (used in pickers and table headers)
  function icon(layout) {
    var s = '<svg viewBox="0 0 42 30" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" fill="none" stroke="' + NAVY + '" stroke-width="1.3">';
    var dot = function (x, y) { return '<rect x="' + (x - 1.6) + '" y="' + (y - 1.6) + '" width="3.2" height="3.2" fill="' + NAVY + '" stroke="none"/>'; };
    s += '<rect x=".7" y=".7" width="40.6" height="28.6"/>';
    s += '<line x1="3.5" y1="9" x2="3.5" y2="21" stroke="' + BURNT + '" stroke-width="2"/>';
    var i, j;
    if (layout === "theatre") { for (i = 0; i < 4; i++) for (j = 0; j < 5; j++) s += dot(11 + i * 7.5, 6 + j * 4.5); }
    else if (layout === "boardroom") { s += '<rect x="11" y="11" width="22" height="8" fill="' + TABLE + '"/>'; for (i = 0; i < 4; i++) { s += dot(14 + i * 5.3, 7.5); s += dot(14 + i * 5.3, 22.5); } }
    else if (layout === "ushape") { s += '<path d="M10 7H34V23H10" stroke-width="3" stroke="' + GOLD + '"/>'; for (i = 0; i < 4; i++) { s += dot(12 + i * 5.5, 3.6); s += dot(12 + i * 5.5, 26.4); } s += dot(37.6, 11) + dot(37.6, 19); }
    else if (layout === "cabaret") { [[15, 10], [29, 10], [15, 21], [29, 21]].forEach(function (p) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="3.6" fill="' + TABLE + '"/>'; s += dot(p[0] + 5, p[1]) + dot(p[0], p[1] - 5.2) + dot(p[0], p[1] + 5.2); }); }
    else { [[13, 9], [30, 20], [22, 14]].forEach(function (p) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="2.6" fill="' + TABLE + '"/>'; }); [[9, 18], [17, 22], [26, 7], [35, 11], [33, 25], [18, 7], [24, 24], [11, 25], [36, 5]].forEach(function (p) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="1.4" fill="' + NAVY + '" stroke="none"/>'; }); }
    return s + '</svg>';
  }

  window.bhPlan = plan;
  window.bhLayoutIcon = icon;
})();
