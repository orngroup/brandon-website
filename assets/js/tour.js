/* ==========================================================
   Take a tour: a click-through photo walk around
   Brandon Hall Hotel and Spa. Each stop is a photo with
   hotspots that lead to the next room, a short description,
   extra photos and a link to book or enquire.
   Hotspot x/y are percentages of the photo itself.
   ========================================================== */
(function () {
  var IMG = "../assets/img/", T = IMG + "tour/";
  var BOOK = "https://booking.profitroom.com/en/brandonhallhotelspawarwickshire/home?no-cache=&currency=GBP";
  var S = {
    welcome: { name: "Welcome", title: "Welcome to Brandon Hall Hotel and Spa",
      text: "A country house hotel set in 17 acres of Warwickshire grounds, a short drive from Coventry, Rugby and Warwick. Let's walk up to the house.",
      photos: [IMG + "exterior-lawn.jpg", IMG + "exterior-summer.jpg"],
      spots: [{ x: 22, y: 54, to: "front", label: "Walk to the front entrance" }, { x: 80, y: 66, to: "gardens", label: "Explore the gardens" }] },
    front: { name: "Front entrance", title: "The front entrance",
      text: "Our pillared porch welcomes you in, with parking right outside. Step through the front door to reception.",
      photos: [T + "front-entrance.jpg", IMG + "exterior-front.jpg"],
      spots: [{ x: 47, y: 58, to: "reception", label: "Step inside" }, { x: 90, y: 72, to: "terrace", label: "Round to the terrace" }] },
    reception: { name: "Reception", title: "Reception",
      text: "Our reception team is here 24 hours a day to check you in, book your table and help with anything you need during your stay.",
      photos: [IMG + "reception.jpg"],
      spots: [{ x: 90, y: 44, to: "lounge", label: "The lounge" }, { x: 66, y: 34, to: "bar", label: "The bar" },
              { x: 34, y: 20, to: "bedroom", label: "Up to the bedrooms" }, { x: 52, y: 78, to: "events", label: "Event suites" },
              { x: 80, y: 80, to: "pool", label: "Leisure and wellness" }] },
    lounge: { name: "Lounge", title: "The lounge",
      text: "Sink into a sofa by the open fire with a coffee or a glass of something. A favourite spot on a winter's afternoon.",
      photos: [IMG + "lounge-fireplace.jpg"],
      spots: [{ x: 74, y: 56, to: "reception", label: "Back to reception" }, { x: 10, y: 38, to: "bar", label: "Through to the bar" }] },
    bar: { name: "The bar", title: "The bar",
      text: "Light and elegant by day, cosy by night. Meet friends for a drink, a cocktail before dinner or a nightcap.",
      photos: [T + "bar-1.jpg", T + "bar-2.jpg", T + "bar-3.jpg", IMG + "bar-lounge.jpg"],
      spots: [{ x: 92, y: 60, to: "clarendon", label: "The Clarendon restaurant" }, { x: 12, y: 74, to: "lounge", label: "The lounge" }] },
    clarendon: { name: "The Clarendon", title: "The Clarendon restaurant",
      text: "Lunch and dinner every day beneath tall arched windows, with grill dishes, classics and a wine list to match.",
      photos: [IMG + "restaurant.jpg", T + "clarendon-2.jpg", IMG + "site/dine-restaurant.jpg", T + "clarendon-3.jpg"],
      spots: [{ x: 36, y: 26, to: "terrace", label: "Out to the terrace" }, { x: 7, y: 74, to: "bar", label: "Back to the bar" }],
      cta: { href: "../dining/#book-table", label: "Book a table" } },
    bedroom: { name: "Bedrooms", title: "Our bedrooms",
      text: "Comfortable, calm rooms with everything you need for a good night's sleep, with doubles, twins and suites to choose from.",
      photos: [T + "bedroom-1.jpg", T + "bedroom-2.jpg", T + "bedroom-3.jpg", IMG + "bedroom-teal.jpg", IMG + "bedroom-yellow.jpg"],
      spots: [{ x: 88, y: 44, to: "suite", label: "See a suite" }, { x: 8, y: 62, to: "reception", label: "Back to reception" }],
      cta: { href: BOOK, label: "Book your stay", ext: true } },
    suite: { name: "Suites", title: "Our suites",
      text: "More space to relax, with generous beds and seating areas. Perfect for a special occasion or a wedding night.",
      photos: [IMG + "suite-bay.jpg", T + "junior-suite.jpg", IMG + "bedroom-suite.jpg"],
      spots: [{ x: 10, y: 60, to: "bedroom", label: "Back to the bedrooms" }],
      cta: { href: "../rooms-suites/", label: "See all rooms" } },
    pool: { name: "Pool", title: "The swimming pool",
      text: "An indoor pool beneath a glazed roof, bright in every season. A lovely way to start the day or unwind after a meeting.",
      photos: [IMG + "site/leisure-pool.jpg", IMG + "pool.jpg"],
      spots: [{ x: 86, y: 58, to: "gym", label: "The gym" }, { x: 8, y: 70, to: "reception", label: "Back to reception" }],
      cta: { href: "../spa-leisure/", label: "Leisure and wellness" } },
    gym: { name: "Gym", title: "Gym and fitness centre",
      text: "Cardio and resistance equipment and space to stretch, so you can keep your routine going while you stay.",
      photos: [IMG + "site/leisure-gym.jpg", IMG + "site/leisure-fitness.jpg"],
      spots: [{ x: 10, y: 64, to: "pool", label: "Back to the pool" }] },
    events: { name: "Event suites", title: "Our event suites",
      text: "The Brandon Suite and the Woodlands Suite host weddings, celebrations, dinners and conferences, each set up exactly the way you want it.",
      photos: [IMG + "suite-banquet.jpg", T + "wedding-breakfast.jpg", IMG + "table-setting.jpg", T + "wedding-table.jpg", T + "wedding-chairs.jpg"],
      spots: [{ x: 86, y: 50, to: "ceremony", label: "A ceremony set-up" }, { x: 12, y: 40, to: "gardens", label: "Out to the gardens" }, { x: 50, y: 86, to: "reception", label: "Back to reception" }],
      cta: { href: "../meetings-events/planner/", label: "Plan your event" } },
    ceremony: { name: "Ceremonies", title: "Wedding ceremonies",
      text: "Say \"I do\" in one of our elegant suites, then step outside for photographs in the grounds.",
      photos: [IMG + "suite-theatre.jpg", T + "ceremony-couple.jpg"],
      spots: [{ x: 10, y: 60, to: "events", label: "Back to the event suites" }, { x: 88, y: 60, to: "gardens", label: "Out to the gardens" }],
      cta: { href: "../weddings/", label: "Weddings at Brandon Hall" } },
    terrace: { name: "Terrace", title: "The terrace",
      text: "Garden seating on the terrace beside the house: a sunny spot for a drink on a summer evening.",
      photos: [IMG + "terrace.jpg", IMG + "exterior-terrace.jpg"],
      spots: [{ x: 84, y: 72, to: "gardens", label: "Into the gardens" }, { x: 30, y: 52, to: "clarendon", label: "The Clarendon" }] },
    gardens: { name: "Gardens", title: "The gardens and grounds",
      text: "Seventeen acres of lawns, woodland and mature trees, and a beautiful setting for an outdoor ceremony.",
      photos: [T + "garden-ceremony.jpg", T + "garden-ceremony-2.jpg", IMG + "grounds-lawn.jpg", T + "garden-couple.jpg"],
      spots: [{ x: 50, y: 32, to: "farewell", label: "Back towards the house" }, { x: 10, y: 74, to: "terrace", label: "The terrace" }] },
    farewell: { name: "Thank you", title: "Thank you for visiting",
      text: "We hope you enjoyed your tour. We'd love to welcome you in person, whether for a stay, a meal, a celebration or a meeting.",
      photos: [IMG + "exterior-summer.jpg", IMG + "exterior-dusk.jpg"],
      spots: [{ x: 26, y: 60, to: "welcome", label: "Start the tour again" }],
      cta: { href: BOOK, label: "Book your stay", ext: true }, cta2: { href: "../contact/", label: "Contact us" } }
  };
  var ORDER = ["welcome", "front", "reception", "lounge", "bar", "clarendon", "bedroom", "suite", "pool", "gym", "events", "ceremony", "terrace", "gardens", "farewell"];

  var $ = function (id) { return document.getElementById(id); };
  var stage = $("t-stage"), img = $("t-img"), bg = $("t-bg"), spots = $("t-spots"), panel = $("t-panel");
  var cur = null, photoIdx = 0, busy = false;

  // Where a point on the photo appears on screen, given object-fit: cover.
  function place() {
    var s = S[cur]; if (!s || !img.naturalWidth) return;
    var W = stage.clientWidth, H = stage.clientHeight, iw = img.naturalWidth, ih = img.naturalHeight;
    var sc = Math.max(W / iw, H / ih), dw = iw * sc, dh = ih * sc, ox = (W - dw) / 2, oy = (H - dh) / 2;
    Array.prototype.forEach.call(spots.children, function (b, i) {
      var p = s.spots[i]; if (!p) return;
      var x = ox + dw * p.x / 100, y = oy + dh * p.y / 100;
      x = Math.max(26, Math.min(W - 26, x)); y = Math.max(100, Math.min(H - 70, y));
      // keep hotspots clear of the description panel and the buttons
      var pr = panel.classList.contains("min") ? null : panel.getBoundingClientRect(), sr = stage.getBoundingClientRect();
      if (pr && x > pr.left - sr.left - 30 && x < pr.right - sr.left + 30 && y > pr.top - sr.top - 26) y = pr.top - sr.top - 34 - (i % 2) * 46;
      if (y > H - 90 && x > W - 320) y = H - 110;
      b.style.left = x + "px"; b.style.top = y + "px";
      b.classList.toggle("lab-left", x > W * 0.55);
    });
    // nudge apart any hotspots whose labels overlap (mostly on phones)
    var bs = Array.prototype.slice.call(spots.children);
    for (var pass = 0; pass < 4; pass++) {
      for (var a = 0; a < bs.length; a++) for (var c = a + 1; c < bs.length; c++) {
        var A = bs[a].getBoundingClientRect(), B = bs[c].getBoundingClientRect();
        if (A.left < B.right && B.left < A.right && A.top < B.bottom + 8 && B.top < A.bottom + 8) {
          var up = parseFloat(bs[a].style.top) <= parseFloat(bs[c].style.top);
          bs[up ? a : c].style.top = (parseFloat(bs[up ? a : c].style.top) - 26) + "px";
          bs[up ? c : a].style.top = (parseFloat(bs[up ? c : a].style.top) + 26) + "px";
        }
      }
    }
  }

  function show(id, from) {
    var s = S[id]; if (!s || busy) return;
    busy = true;
    var go = function () {
      cur = id; photoIdx = 0;
      setPhoto(0, true);
      $("t-name").textContent = s.title;
      $("t-text").textContent = s.text;
      $("t-step").textContent = (ORDER.indexOf(id) + 1) + " of " + ORDER.length;
      var c = "";
      if (s.cta) c += '<a class="btn btn--book" href="' + s.cta.href + '"' + (s.cta.ext ? ' target="_blank" rel="noopener"' : "") + ">" + s.cta.label + "</a>";
      if (s.cta2) c += '<a class="btn btn--light" href="' + s.cta2.href + '">' + s.cta2.label + "</a>";
      $("t-cta").innerHTML = c; $("t-cta").hidden = !c;
      $("t-thumbs").innerHTML = s.photos.length > 1 ? s.photos.map(function (p, i) {
        return '<button type="button" data-i="' + i + '"' + (i ? "" : ' aria-current="true"') + ' aria-label="Photo ' + (i + 1) + '"><img src="' + p + '" alt="" loading="lazy"></button>';
      }).join("") : "";
      spots.innerHTML = s.spots.map(function (p) {
        return '<button type="button" class="t-spot" data-to="' + p.to + '"><span class="dot" aria-hidden="true"></span><span class="lab">' + p.label + "</span></button>";
      }).join("");
      Array.prototype.forEach.call(document.querySelectorAll("#t-map button"), function (b) { b.setAttribute("aria-current", b.dataset.to === id ? "true" : "false"); });
      try { history.replaceState(null, "", "#" + id); } catch (e) {}
      // preload the next stops
      s.spots.forEach(function (p) { var n = S[p.to]; if (n) { var im = new Image(); im.src = n.photos[0]; } });
    };
    if (from && from.spot) {
      // "walk" towards the hotspot, then fade into the next room
      var r = from.spot.getBoundingClientRect(), sr = stage.getBoundingClientRect();
      img.style.transformOrigin = (r.left + r.width / 2 - sr.left) + "px " + (r.top + r.height / 2 - sr.top) + "px";
      stage.classList.add("walking");
      setTimeout(function () { go(); }, 520);
    } else { go(); }
  }

  function setPhoto(i, entering) {
    var s = S[cur]; photoIdx = i;
    var src = s.photos[i];
    var pre = new Image();
    pre.onload = function () {
      // jump back to the starting frame without animating, then fade the new room in
      img.style.transition = "none";
      stage.classList.remove("walking", "in");
      img.style.transformOrigin = "50% 50%";
      img.src = src; bg.style.backgroundImage = "url('" + src + "')";
      void img.offsetWidth;
      img.style.transition = "";
      stage.classList.toggle("has-spots", i === 0);
      requestAnimationFrame(function () { place(); stage.classList.add("in"); busy = false; });
    };
    pre.onerror = function () { busy = false; };
    stage.classList.remove("in");
    pre.src = src;
    Array.prototype.forEach.call(document.querySelectorAll("#t-thumbs button"), function (b) { b.setAttribute("aria-current", +b.dataset.i === i ? "true" : "false"); });
  }

  spots.addEventListener("click", function (e) { var b = e.target.closest(".t-spot"); if (b) show(b.dataset.to, { spot: b.querySelector(".dot") }); });
  $("t-thumbs").addEventListener("click", function (e) { var b = e.target.closest("button"); if (b && !busy) setPhoto(+b.dataset.i); });
  $("t-next").addEventListener("click", function () { show(ORDER[(ORDER.indexOf(cur) + 1) % ORDER.length]); });
  $("t-prev").addEventListener("click", function () { show(ORDER[(ORDER.indexOf(cur) - 1 + ORDER.length) % ORDER.length]); });
  $("t-mapbtn").addEventListener("click", function () { var m = $("t-map"); m.hidden = !m.hidden; this.setAttribute("aria-expanded", String(!m.hidden)); });
  $("t-map").innerHTML = '<p class="t-map-h">Jump to</p>' + ORDER.map(function (id, i) { return '<button type="button" data-to="' + id + '">' + (i + 1) + ". " + S[id].name + "</button>"; }).join("");
  $("t-map").addEventListener("click", function (e) { var b = e.target.closest("button[data-to]"); if (b) { $("t-map").hidden = true; show(b.dataset.to); } });
  $("t-hide").addEventListener("click", function () { var p = $("t-panel"); p.classList.toggle("min"); this.textContent = p.classList.contains("min") ? "Show details" : "Hide"; place(); });
  document.addEventListener("keydown", function (e) {
    if ($("t-intro") && !$("t-intro").hidden) return;
    if (e.key === "ArrowRight") $("t-next").click();
    if (e.key === "ArrowLeft") $("t-prev").click();
    if (e.key === "Escape") $("t-map").hidden = true;
  });
  window.addEventListener("resize", place);

  // Start screen
  var start = (location.hash || "").slice(1);
  $("t-start").addEventListener("click", function () {
    $("t-intro").classList.add("gone");
    setTimeout(function () { $("t-intro").hidden = true; }, 600);
    show("welcome");
  });
  if (S[start]) { $("t-intro").hidden = true; show(start); }
})();
