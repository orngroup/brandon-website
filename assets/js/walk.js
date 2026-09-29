/* A country walk from Brandon Hall
   - clickable pins on the illustrated map, linked to the step list
   - scenery photo on hover (or tap on phones)
   - "Walk it virtually": a step-by-step photo tour of the route
   - Google Maps / Street View links, with verified coordinates:
       Hotel      52.38326,-1.40643  (address register, CV8 3FW)
       Crossing   52.40590,-1.40757  (Geograph SP 404 788, Twelve O'Clock Ride at the B4428)
       Visitor C. 52.41200,-1.40906  (Coventry City Council directions link)            */
(function () {
  var root = document.getElementById("walk");
  if (!root) return;
  var P = root.getAttribute("data-root") || "../";
  var GM = "https://www.google.com/maps/";
  var HOTEL = "52.38326,-1.40643", CROSS = "52.40590,-1.40757", VC = "52.41200,-1.40906";
  var place = function (q) { return GM + "search/?api=1&query=" + encodeURIComponent(q); };
  var pano = function (ll, heading) { return GM + "@?api=1&map_action=pano&viewpoint=" + ll + (heading != null ? "&heading=" + heading : ""); };
  var dir = function (from, to) { return GM + "dir/?api=1&origin=" + from + "&destination=" + to + "&travelmode=walking"; };
  var commons = function (file) { return "https://commons.wikimedia.org/wiki/Special:FilePath/" + encodeURIComponent(file) + "?width=800"; };
  var commonsPage = function (file) { return "https://commons.wikimedia.org/wiki/File:" + encodeURIComponent(file.replace(/ /g, "_")); };

  // Scenery photographs. local = copy in the repo (added by the "Fetch hotel photos" Action);
  // remote = original source, used until then.
  var PH = {
    hall:   { local: "assets/img/exterior-summer.jpg", alt: "Brandon Hall across the lawn", credit: "" },
    ride:   { local: "assets/img/walk/twelve-oclock-ride.jpg", remote: "https://s0.geograph.org.uk/geophotos/02/00/26/2002679_3adee2e3.jpg", alt: "The Twelve O'Clock Ride, a straight bridleway through the fields towards the trees", credit: "Twelve O'Clock Ride, northwards © E Gammie, Geograph, CC BY-SA 2.0", link: "https://www.geograph.org.uk/photo/2002679" },
    drive:  { local: "assets/img/walk/coombe-drive.jpg", remote: commons("The drive, Coombe Park - geograph.org.uk - 920007.jpg"), alt: "The long straight drive into Coombe Park", credit: "The drive, Coombe Park, Geograph contributor via Wikimedia Commons, CC BY-SA 2.0", link: commonsPage("The drive, Coombe Park - geograph.org.uk - 920007.jpg") },
    approach: { local: "assets/img/walk/coombe-approach.jpg", remote: commons("The approach to Coombe Abbey - geograph.org.uk - 1232122.jpg"), alt: "The approach to Coombe Abbey", credit: "The approach to Coombe Abbey, Geograph contributor via Wikimedia Commons, CC BY-SA 2.0", link: commonsPage("The approach to Coombe Abbey - geograph.org.uk - 1232122.jpg") },
    lake:   { local: "assets/img/walk/coombe-lake.jpg", remote: commons("Lake, Coombe Abbey - geograph.org.uk - 190502.jpg"), alt: "Coombe Pool framed by trees", credit: "Lake, Coombe Abbey, Geograph contributor via Wikimedia Commons, CC BY-SA 2.0", link: commonsPage("Lake, Coombe Abbey - geograph.org.uk - 190502.jpg") },
    birds:  { local: "assets/img/walk/coombe-ducks.jpg", remote: commons("Ducks on the lake at Coombe Abbey Country Park - geograph.org.uk - 1478533.jpg"), alt: "Ducks on Coombe Pool", credit: "Ducks on the lake at Coombe Abbey Country Park, Geograph contributor via Wikimedia Commons, CC BY-SA 2.0", link: commonsPage("Ducks on the lake at Coombe Abbey Country Park - geograph.org.uk - 1478533.jpg") },
    vc:     { local: "assets/img/walk/coombe-visitor-centre.jpg", remote: commons("The visitor centre at Coombe Country Park - geograph.org.uk - 1232125.jpg"), alt: "The visitor centre at Coombe Country Park", credit: "The visitor centre at Coombe Country Park, Geograph contributor via Wikimedia Commons, CC BY-SA 2.0", link: commonsPage("The visitor centre at Coombe Country Park - geograph.org.uk - 1232125.jpg") },
    fields: { local: "assets/img/walk/coombe-farmland.jpg", remote: commons("Farmland by Coombe Abbey park - geograph.org.uk - 2480146.jpg"), alt: "Open farmland beside Coombe Abbey park", credit: "Farmland by Coombe Abbey park, Geograph contributor via Wikimedia Commons, CC BY-SA 2.0", link: commonsPage("Farmland by Coombe Abbey park - geograph.org.uk - 2480146.jpg") },
    lawn:   { local: "assets/img/exterior-lawn.jpg", alt: "Brandon Hall and its lawns", credit: "" }
  };

  var STOPS = [
    { id: "hall", n: "1", x: 47.1, y: 14.4, ph: "hall", kicker: "Your starting point", title: "Brandon Hall",
      text: "Step outside and discover one of Warwickshire's most beautiful walks. Leave from the hotel on Main Street, Brandon, CV8 3FW.",
      links: [["Open in Google Maps", place("Brandon Hall Hotel and Spa, Main Street, Brandon CV8 3FW")], ["Street View", pano(HOTEL)]] },
    { id: "ride", n: "2", x: 74.6, y: 36.9, ph: "ride", kicker: "Centenary Way", title: "The Twelve O'Clock Ride",
      text: "A scenic bridleway linking Brandon to Coombe Abbey. It runs in a dead-straight line through the woods and fields, named after its position to the noonday sun.",
      links: [["Open in Google Maps", place("Twelve O'Clock Ride, Brandon, Warwickshire")]] },
    { id: "road", n: "!", x: 68.4, y: 48.2, ph: "ride", warn: true, kicker: "Please note", title: "Crossing the Brinklow Road (B4428)",
      text: "Where the ride meets the trees, it crosses the Brinklow Road (B4428). Please take care when crossing, then carry straight on along the drive to Coombe Abbey.",
      links: [["Street View of the crossing", pano(CROSS, 0)], ["Open in Google Maps", GM + "search/?api=1&query=" + CROSS]] },
    { id: "coombe", n: "3", x: 67.7, y: 52.2, ph: "approach", kicker: "Approx. 4.5 km from the hotel", title: "Coombe Abbey Country Park",
      text: "Reach Coombe Abbey via countryside footpaths and the Twelve O'Clock Ride (Centenary Way): 500 acres of gardens, woodland and lakeside walks.",
      links: [["Open in Google Maps", place("Coombe Abbey Park, Brinklow Road, Binley CV3 2AB")], ["Walking route from the hotel", dir(HOTEL, VC)]] },
    { id: "herons", n: "4", x: 64.8, y: 61.6, ph: "lake", kicker: "2-mile lakeside trail", title: "Heron's Way",
      text: "Walk around Coombe Pool through woodland, past the bird hide, and enjoy beautiful lake views. The pool is home to Warwickshire's largest heronry.",
      links: [["Open in Google Maps", place("Heron's Way, Coombe Abbey Park")]] },
    { id: "hide", n: "", x: 79.0, y: 60.3, ph: "birds", icon: true, kicker: "On Heron's Way", title: "Bird hide",
      text: "Look out over Coombe Pool and the heronry. Bring binoculars for a closer view of the herons, swans and ducks.",
      links: [["Open in Google Maps", place("Coombe Abbey Park Bird Hide")]] },
    { id: "vc", n: "", x: 59.4, y: 71.0, ph: "vc", icon: true, kicker: "Coombe Abbey Park", title: "Visitor Centre",
      text: "Café, toilets and information. The Visitor Centre is usually open 10am to 4pm daily.",
      links: [["Open in Google Maps", place("Coombe Country Park Visitor Centre, Coventry CV3 2AB")], ["Street View", pano(VC)]] },
    { id: "goape", n: "", x: 80.9, y: 68.8, icon: true, kicker: "Coombe Abbey Park", title: "Go Ape",
      text: "Treetop adventures and zip wires in the park, for anyone with energy to spare.",
      links: [["Open in Google Maps", place("Go Ape Coventry, Coombe Abbey Park")]] },
    { id: "return", n: "5", x: 46.9, y: 78.1, ph: "fields", kicker: "Complete your circular walk", title: "Return to Brandon Hall",
      text: "Head back through the countryside to the hotel for lunch in The Clarendon, a drink in the bar, or a swim in the leisure club.",
      links: [["Walking route back to the hotel", dir(VC, HOTEL)]] }
  ];
  // The virtual walk follows the route in order
  var TOUR = [
    { stop: "hall", ph: "hall", cap: "Set off from Brandon Hall and head for the start of the bridleway at the edge of the village." },
    { stop: "ride", ph: "ride", cap: "The Twelve O'Clock Ride runs dead straight towards Coombe Abbey, through woodland and open fields." },
    { stop: "road", ph: "ride", cap: "At the line of trees the ride meets the Brinklow Road (B4428). Take care crossing." },
    { stop: "coombe", ph: "drive", cap: "Carry straight on along the drive into Coombe Park, on the same line as the ride." },
    { stop: "coombe", ph: "approach", cap: "The approach to Coombe Abbey, where the Heron's Way trail begins." },
    { stop: "vc", ph: "vc", cap: "The Visitor Centre, with its café, is a good place for a break." },
    { stop: "herons", ph: "lake", cap: "Heron's Way circles Coombe Pool, Capability Brown's 80-acre lake." },
    { stop: "hide", ph: "birds", cap: "From the bird hide, look out for herons, swans and ducks on the water." },
    { stop: "return", ph: "fields", cap: "Retrace your steps through the countryside for the return to Brandon Hall." },
    { stop: "hall", ph: "lawn", cap: "Back at the hotel for lunch, afternoon tea or a swim." }
  ];

  function src(ph) { return ph.local ? P + ph.local : ph.remote; }
  function imgTag(key, cls) {
    var ph = PH[key]; if (!ph) return "";
    var fb = ph.remote ? ' onerror="if(this.dataset.fb){this.src=this.dataset.fb;this.dataset.fb=\'\'}else{this.closest(\'figure\').classList.add(\'no-img\')}" data-fb="' + ph.remote + '"' : "";
    return '<figure class="' + (cls || "") + '"><img src="' + src(ph) + '" alt="' + ph.alt + '" loading="lazy"' + fb + ">" +
      (ph.credit ? '<figcaption><a href="' + ph.link + '" target="_blank" rel="noopener">' + ph.credit + "</a></figcaption>" : "") + "</figure>";
  }
  var byId = function (id) { return STOPS.find(function (x) { return x.id === id; }); };

  var pins = root.querySelector(".walk-pins"), panel = root.querySelector(".walk-panel"), steps = root.querySelectorAll("[data-stop]");
  var tip = document.createElement("div"); tip.className = "walk-tip"; tip.hidden = true; root.querySelector(".walk-map").appendChild(tip);

  pins.innerHTML = STOPS.map(function (s) {
    return '<button type="button" class="walk-pin' + (s.warn ? " is-warn" : "") + (s.icon ? " is-small" : "") + '" style="left:' + s.x + "%;top:" + s.y + '%" data-id="' + s.id + '" aria-label="' + s.title + '"><span>' + (s.n || "") + "</span></button>";
  }).join("");

  function mark(id) {
    pins.querySelectorAll(".walk-pin").forEach(function (b) { var on = b.dataset.id === id; b.classList.toggle("is-on", on); b.setAttribute("aria-pressed", on); });
    steps.forEach(function (li) { li.classList.toggle("is-on", li.dataset.stop === id); });
  }
  function show(id, scroll) {
    var s = byId(id); if (!s) return;
    mark(id);
    panel.innerHTML = (s.ph ? imgTag(s.ph, "walk-photo") : "") +
      '<div class="walk-panel-body"><span class="kicker">' + s.kicker + "</span><h3>" + s.title + "</h3><p>" + s.text + "</p>" +
      '<div class="walk-links">' + s.links.map(function (l) { return '<a class="btn btn--line" href="' + l[1] + '" target="_blank" rel="noopener">' + l[0] + "</a>"; }).join("") + "</div></div>";
    panel.classList.toggle("is-warn", !!s.warn);
    if (scroll && window.matchMedia("(max-width: 980px)").matches) panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  // Hover / focus preview of the scenery
  var canHover = window.matchMedia("(hover: hover)").matches;
  function showTip(btn) {
    var s = byId(btn.dataset.id); if (!s || !s.ph) return;
    var ph = PH[s.ph];
    tip.innerHTML = '<img src="' + src(ph) + '" alt=""' + (ph.remote ? ' onerror="if(this.dataset.fb){this.src=this.dataset.fb;this.dataset.fb=\'\'}" data-fb="' + ph.remote + '"' : "") + '><span>' + s.title + "</span>";
    tip.hidden = false;
    var x = parseFloat(btn.style.left), y = parseFloat(btn.style.top);
    tip.style.left = Math.min(Math.max(x, 22), 78) + "%";
    tip.style.top = y + "%";
    tip.classList.toggle("below", y < 30);
  }
  if (canHover) {
    pins.addEventListener("mouseover", function (e) { var b = e.target.closest(".walk-pin"); if (b) showTip(b); });
    pins.addEventListener("mouseout", function (e) { if (e.target.closest(".walk-pin")) tip.hidden = true; });
  }
  pins.addEventListener("focusin", function (e) { var b = e.target.closest(".walk-pin"); if (b && canHover) showTip(b); });
  pins.addEventListener("focusout", function () { tip.hidden = true; });
  pins.addEventListener("click", function (e) { var b = e.target.closest(".walk-pin"); if (b) { tip.hidden = true; show(b.dataset.id, true); } });
  steps.forEach(function (li) { var btn = li.querySelector("button"); if (btn) btn.addEventListener("click", function () { show(li.dataset.stop, true); }); });

  // Virtual walk
  var tour = document.getElementById("walk-tour");
  if (tour) {
    var i = 0, timer = null;
    var stage = tour.querySelector(".tour-stage"), capEl = tour.querySelector(".tour-cap"), count = tour.querySelector(".tour-count"),
      bar = tour.querySelector(".tour-bar span"), prev = tour.querySelector("[data-tour=prev]"), next = tour.querySelector("[data-tour=next]"),
      play = tour.querySelector("[data-tour=play]"), dots = tour.querySelector(".tour-dots");
    dots.innerHTML = TOUR.map(function (t, k) { return '<button type="button" aria-label="Stop ' + (k + 1) + '" data-k="' + k + '"></button>'; }).join("");
    // preload the photos so the tour feels smooth
    TOUR.forEach(function (t) { var im = new Image(); im.src = src(PH[t.ph]); if (PH[t.ph].remote) im.onerror = function () { new Image().src = PH[t.ph].remote; }; });
    function render() {
      var t = TOUR[i], s = byId(t.stop);
      stage.innerHTML = imgTag(t.ph, "tour-photo");
      capEl.innerHTML = '<span class="kicker">' + (i + 1) + " of " + TOUR.length + " · " + s.title + "</span><p>" + t.cap + "</p>";
      count.textContent = (i + 1) + " / " + TOUR.length;
      bar.style.width = ((i + 1) / TOUR.length * 100) + "%";
      prev.disabled = i === 0; next.textContent = i === TOUR.length - 1 ? "Start again" : "Next";
      dots.querySelectorAll("button").forEach(function (d, k) { d.classList.toggle("is-on", k === i); });
      mark(t.stop);
    }
    function go(k) { i = (k + TOUR.length) % TOUR.length; render(); }
    function stop() { clearInterval(timer); timer = null; play.textContent = "Play"; play.setAttribute("aria-pressed", "false"); }
    prev.addEventListener("click", function () { stop(); go(i - 1); });
    next.addEventListener("click", function () { stop(); go(i + 1); });
    dots.addEventListener("click", function (e) { var d = e.target.closest("[data-k]"); if (d) { stop(); go(+d.dataset.k); } });
    play.addEventListener("click", function () {
      if (timer) return stop();
      play.textContent = "Pause"; play.setAttribute("aria-pressed", "true");
      timer = setInterval(function () { if (i === TOUR.length - 1) return stop(); go(i + 1); }, 4500);
    });
    tour.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") { stop(); go(i + 1); } if (e.key === "ArrowLeft") { stop(); go(i - 1); } });
    render();
  }

  show("hall");
})();
