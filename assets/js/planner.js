/* ==========================================================
   Event Planner
   Builds a full event specification, draws the chosen room
   to scale, estimates package cost and carbon, and sends the
   request to the events team.
   ========================================================== */
(function () {
  var C = window.BH_CONFIG, ROOMS = window.BH_ROOMS, LAYOUTS = window.BH_LAYOUTS;
  var TYPES = window.BH_EVENT_TYPES, PKGS = window.BH_PACKAGES;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var money = function (n) { return "£" + n.toLocaleString("en-GB", { minimumFractionDigits: 0, maximumFractionDigits: 0 }); };
  var byId = function (list, id) { return list.find(function (x) { return x.id === id; }); };

  var q = new URLSearchParams(location.search);
  var S = {
    type: "meeting",
    date: "",
    days: 1,
    guests: parseInt(q.get("guests"), 10) || 20,
    layout: q.get("layout") || "boardroom",
    room: q.get("room") || "",
    pkg: "ddr",
    catering: [],
    extras: [],
    breakoutRoom: "",
    stay: false,
    bedrooms: 10,
    nights: 1,
    singles: 10, doubles: 0, twins: 0,
    board: "bb",
    arrival: "",
    name: "", company: "", email: "", phone: "", notes: "", source: ""
  };
  if (!byId(LAYOUTS, S.layout)) S.layout = "boardroom";

  /* ---------- Step 1: event type ---------- */
  function renderTypes() {
    $("#p-type").innerHTML = TYPES.map(function (t) {
      return '<button type="button" class="chip" data-type="' + t.id + '" aria-pressed="' + (t.id === S.type) + '">' + t.label + '</button>';
    }).join("");
  }

  /* ---------- Step 2: layout + room ---------- */
  function renderLayouts() {
    var rec = byId(TYPES, S.type).layouts;
    $("#p-layout").innerHTML = LAYOUTS.map(function (l) {
      return '<button type="button" data-layout="' + l.id + '" aria-pressed="' + (l.id === S.layout) + '">' +
        window.bhLayoutIcon(l.id) + l.label + (rec.indexOf(l.id) > -1 ? '<small>Suggested</small>' : '') + '</button>';
    }).join("");
    $("#p-layout-desc").textContent = byId(LAYOUTS, S.layout).desc;
  }

  function fitting() {
    return ROOMS.filter(function (r) { return (r.cap[S.layout] || 0) >= S.guests; })
      .sort(function (a, b) { return a.cap[S.layout] - b.cap[S.layout]; });
  }

  function ensureRoom() {
    var room = byId(ROOMS, S.room);
    if (!room || (room.cap[S.layout] || 0) < S.guests) {
      var f = fitting();
      S.room = f.length ? f[0].id : "";
    }
  }

  function renderRooms() {
    var f = fitting();
    var others = ROOMS.filter(function (r) { return f.indexOf(r) < 0 && r.cap[S.layout]; });
    var html = f.map(function (r) {
      var spare = r.cap[S.layout] - S.guests;
      var note = spare <= Math.max(4, S.guests * .15) ? "A snug fit" : (spare > S.guests ? "Plenty of space" : "Comfortable");
      return '<label class="opt' + (r.id === S.room ? ' is-on' : '') + '"><input type="radio" name="room" value="' + r.id + '"' + (r.id === S.room ? ' checked' : '') + '>' +
        '<span class="opt-main"><strong>' + r.name + '</strong><span>' + r.m2 + ' m², seats ' + r.cap[S.layout] + ' ' + byId(LAYOUTS, S.layout).label.toLowerCase() + '</span></span>' +
        '<span class="opt-side">' + note + '</span></label>';
    }).join("");
    if (!f.length) {
      html = '<p class="notice">No single room seats ' + S.guests + ' in a ' + byId(LAYOUTS, S.layout).label.toLowerCase() +
        ' layout. Try another layout, or <a href="mailto:' + C.eventsEmail + '">ask our events team</a> about using the grounds or combining spaces.</p>';
    }
    if (others.length && f.length) {
      html += '<p class="small mt-1">Too small for ' + S.guests + ' in this layout: ' + others.map(function (r) { return r.name + ' (' + r.cap[S.layout] + ')'; }).join(", ") + '.</p>';
    }
    $("#p-rooms").innerHTML = html;
  }

  /* ---------- Step 3: package ---------- */
  function isWeekend() {
    if (!S.date) return false;
    var d = new Date(S.date + "T12:00:00").getDay();
    return d === 0 || d === 6;
  }
  function pkgPrice(p) { return isWeekend() ? p.weekend : p.midweek; }

  function renderPackages() {
    $("#p-pkg").innerHTML = PKGS.map(function (p) {
      var price = pkgPrice(p);
      return '<label class="opt opt--pkg' + (p.id === S.pkg ? ' is-on' : '') + '"><input type="radio" name="pkg" value="' + p.id + '"' + (p.id === S.pkg ? ' checked' : '') + '>' +
        '<span class="opt-main"><strong>' + p.name + '</strong><span>' + p.includes.slice(0, 3).join(", ") + (p.includes.length > 3 ? " and more" : "") + '</span></span>' +
        (C.showPackagePrices && price ? '<span class="opt-side">from <b>' + money(price) + '</b> pp</span>' : '<span></span>') + '</label>';
    }).join("");
    $("#p-pkg-note").textContent = C.showPackagePrices
      ? (S.date ? (isWeekend() ? "Weekend rates shown for your date." : "Midweek rates shown for your date.") : "Choose a date to see midweek or weekend rates.") + " Rates include VAT."
      : "Choose what suits you best. Our events team will confirm the price in your proposal.";
  }

  /* ---------- Steps 4 & 5: catering and extras ---------- */
  function renderChecks(target, list, key) {
    $(target).innerHTML = list.map(function (c) {
      return '<label class="check"><input type="checkbox" value="' + c.id + '"' + (S[key].indexOf(c.id) > -1 ? ' checked' : '') + '><span>' + c.name + '</span></label>';
    }).join("");
  }
  function renderCateringNote() {
    $("#p-cat-note").textContent = S.pkg === "hire"
      ? "Pick what you'd like and we'll price it for you."
      : "Your package already includes all-day tea and coffee, two rounds of refreshments and lunch. Add anything extra here.";
  }
  function renderBreakout() {
    var wrap = $("#p-breakout-wrap");
    var on = S.extras.indexOf("breakout") > -1;
    wrap.hidden = !on;
    if (!on) return;
    var opts = ROOMS.filter(function (r) { return r.id !== S.room; });
    if (!S.breakoutRoom || S.breakoutRoom === S.room) S.breakoutRoom = opts[opts.length - 1].id;
    $("#p-breakout").innerHTML = opts.map(function (r) {
      return '<option value="' + r.id + '"' + (r.id === S.breakoutRoom ? ' selected' : '') + '>' + r.name + ' (boardroom ' + (r.cap.boardroom || "–") + ')</option>';
    }).join("");
  }

  /* ---------- Step 6: bedrooms ---------- */
  function syncStay() {
    $("#p-stay-fields").hidden = !S.stay;
    $("#p-stay").checked = S.stay;
    var mix = S.singles + S.doubles + S.twins;
    $("#p-mix-note").textContent = mix !== S.bedrooms
      ? "Your room mix adds up to " + mix + ", not " + S.bedrooms + ". We'll check this with you."
      : "";
    $("#p-stay-24").hidden = S.pkg !== "24hr";
  }

  /* ---------- Summary, plan and estimates ---------- */
  function carbon() {
    var room = byId(ROOMS, S.room), K = window.BH_CARBON;
    if (!room) return null;
    var energy = room.m2 * K.kwhPerM2Day * K.kgPerKwh * S.days;
    var br = S.extras.indexOf("breakout") > -1 ? byId(ROOMS, S.breakoutRoom) : null;
    if (br) energy += br.m2 * K.kwhPerM2Day * K.kgPerKwh * S.days;
    var food = byId(TYPES, S.type).carbonPerHead * S.guests * S.days;
    var nights = S.stay ? S.bedrooms * S.nights : (S.pkg === "24hr" ? S.guests : 0);
    var stay = nights * K.kgPerRoomNight;
    var total = energy + food + stay;
    return { total: Math.round(total), perHead: (total / Math.max(S.guests, 1)).toFixed(1), energy: Math.round(energy), food: Math.round(food), stay: Math.round(stay) };
  }

  function estimate() {
    var p = byId(PKGS, S.pkg), price = pkgPrice(p);
    if (!C.showPackagePrices || !price) return null;
    var units = S.pkg === "24hr" ? S.guests : S.guests * S.days;
    return { total: price * units, line: money(price) + " × " + units + (S.pkg === "24hr" ? " delegates" : (S.days > 1 ? " delegate days" : " delegates")) };
  }

  function dateText() {
    if (!S.date) return "Date to be confirmed";
    var d = new Date(S.date + "T12:00:00");
    return d.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long", year: "numeric" }) + (S.days > 1 ? " for " + S.days + " days" : "");
  }

  function names(list, ids) { return ids.map(function (id) { return byId(list, id).name; }); }

  function renderSummary() {
    var room = byId(ROOMS, S.room), lay = byId(LAYOUTS, S.layout);
    $("#s-plan").innerHTML = room
      ? window.bhPlan(room, S.layout, Math.min(S.guests, room.cap[S.layout] || 0))
      : '<p class="notice">Choose a layout and number of guests that one of our rooms can seat.</p>';
    $("#s-caption").textContent = room ? room.name + ", " + lay.label.toLowerCase() + " for " + S.guests + (S.guests === 1 ? " guest" : " guests") : "";

    var rows = [
      ["Event", byId(TYPES, S.type).label],
      ["When", dateText()],
      ["Guests", S.guests],
      ["Room", room ? room.name + " (" + lay.label.toLowerCase() + ")" : "No room fits yet"],
      ["Package", byId(PKGS, S.pkg).name]
    ];
    if (S.catering.length) rows.push(["Food and drink", names(window.BH_CATERING, S.catering).join(", ")]);
    if (S.extras.length) rows.push(["Extras", names(window.BH_EXTRAS, S.extras).map(function (n, i) {
      return S.extras[i] === "breakout" && byId(ROOMS, S.breakoutRoom) ? n + ": " + byId(ROOMS, S.breakoutRoom).name : n;
    }).join(", ")]);
    if (S.stay) rows.push(["Bedrooms", S.bedrooms + " rooms × " + S.nights + (S.nights > 1 ? " nights" : " night") + ", " + (S.board === "dbb" ? "dinner, bed and breakfast" : "bed and breakfast")]);
    else if (S.pkg === "24hr") rows.push(["Bedrooms", "Included in the 24-hour package"]);

    $("#s-list").innerHTML = rows.map(function (r) { return '<div><dt>' + r[0] + '</dt><dd>' + r[1] + '</dd></div>'; }).join("");

    var est = estimate();
    $("#s-estimate").hidden = !est;
    if (est) {
      $("#s-est-total").textContent = money(est.total);
      $("#s-est-line").textContent = byId(PKGS, S.pkg).name + " package, " + est.line + ". Bedrooms, extras and any à la carte items are added in your quote.";
    }

    var c = carbon();
    $("#s-carbon").hidden = !c;
    if (c) {
      $("#s-co2").textContent = c.total.toLocaleString("en-GB") + " kg CO₂e";
      $("#s-co2-line").textContent = "About " + c.perHead + " kg per guest: room energy " + c.energy + " kg, catering " + c.food + " kg" + (c.stay ? ", bedrooms " + c.stay + " kg" : "") + ".";
    }
  }

  /* ---------- Render everything ---------- */
  function renderAll() {
    ensureRoom();
    renderTypes(); renderLayouts(); renderRooms(); renderPackages();
    renderCateringNote(); renderBreakout(); syncStay(); renderSummary();
  }

  /* ---------- Events ---------- */
  $("#p-type").addEventListener("click", function (e) {
    var b = e.target.closest("[data-type]"); if (!b) return;
    S.type = b.dataset.type;
    var rec = byId(TYPES, S.type).layouts;
    if (rec.indexOf(S.layout) < 0) S.layout = rec[0];
    if (S.type === "dinner" || S.type === "celebration" || S.type === "christmas") { if (S.pkg !== "hire") S.pkg = "hire"; }
    renderAll();
  });
  $("#p-layout").addEventListener("click", function (e) {
    var b = e.target.closest("[data-layout]"); if (!b) return;
    S.layout = b.dataset.layout; renderAll();
  });
  $("#p-rooms").addEventListener("change", function (e) { if (e.target.name === "room") { S.room = e.target.value; renderRooms(); renderBreakout(); renderSummary(); } });
  $("#p-pkg").addEventListener("change", function (e) { if (e.target.name === "pkg") { S.pkg = e.target.value; renderPackages(); renderCateringNote(); syncStay(); renderSummary(); } });

  function num(el, min, max) { var v = parseInt(el.value, 10); if (isNaN(v)) v = min; return Math.max(min, Math.min(max, v)); }

  $("#p-guests").addEventListener("input", function () { S.guests = num(this, 1, 300); renderAll(); });
  $("#p-guests").addEventListener("change", function () { this.value = S.guests; });
  $("#p-date").addEventListener("change", function () { S.date = this.value; if (!S.arrival) { S.arrival = S.date; $("#p-arrival").value = S.date; } renderPackages(); renderSummary(); });
  $("#p-days").addEventListener("change", function () { S.days = num(this, 1, 5); renderSummary(); });

  $("#p-cat").addEventListener("change", function () { S.catering = $$("#p-cat input:checked").map(function (i) { return i.value; }); renderSummary(); });
  $("#p-extras").addEventListener("change", function () { S.extras = $$("#p-extras input:checked").map(function (i) { return i.value; }); renderBreakout(); renderSummary(); });
  $("#p-breakout").addEventListener("change", function () { S.breakoutRoom = this.value; renderSummary(); });

  $("#p-stay").addEventListener("change", function () { S.stay = this.checked; if (S.stay && S.bedrooms === 10 && S.singles === 10) { S.bedrooms = S.singles = Math.min(S.guests, 60); $("#p-bedrooms").value = S.bedrooms; $("#p-singles").value = S.singles; } syncStay(); renderSummary(); });
  ["bedrooms", "nights", "singles", "doubles", "twins"].forEach(function (k) {
    $("#p-" + k).addEventListener("input", function () { S[k] = num(this, 0, k === "nights" ? 14 : 120); syncStay(); renderSummary(); });
  });
  $("#p-board").addEventListener("change", function () { S.board = this.value; renderSummary(); });
  $("#p-arrival").addEventListener("change", function () { S.arrival = this.value; });

  ["name", "company", "email", "phone", "notes", "source"].forEach(function (k) {
    var el = $("#p-" + k); if (el) el.addEventListener("input", function () { S[k] = el.value.trim(); });
  });

  /* ---------- Build the enquiry ---------- */
  function specText() {
    var room = byId(ROOMS, S.room), lay = byId(LAYOUTS, S.layout), est = estimate(), c = carbon();
    var L = [];
    L.push("EVENT ENQUIRY: " + C.hotelName, "");
    L.push("Name: " + S.name, "Company: " + (S.company || "–"), "Email: " + S.email, "Phone: " + (S.phone || "–"), "");
    L.push("Event: " + byId(TYPES, S.type).label);
    L.push("Date: " + dateText());
    L.push("Guests: " + S.guests);
    L.push("Room: " + (room ? room.name : "To advise") + ", " + lay.label + " layout");
    L.push("Package: " + byId(PKGS, S.pkg).name);
    if (S.catering.length) L.push("Food and drink: " + names(window.BH_CATERING, S.catering).join("; "));
    if (S.extras.length) L.push("Extras: " + names(window.BH_EXTRAS, S.extras).join("; ") + (S.extras.indexOf("breakout") > -1 && byId(ROOMS, S.breakoutRoom) ? " (breakout: " + byId(ROOMS, S.breakoutRoom).name + ")" : ""));
    if (S.stay) {
      L.push("", "Bedrooms: " + S.bedrooms + " rooms for " + S.nights + (S.nights > 1 ? " nights" : " night") + (S.arrival ? " from " + S.arrival : ""));
      L.push("Room mix: " + S.singles + " single occupancy, " + S.doubles + " double, " + S.twins + " twin");
      L.push("Board: " + (S.board === "dbb" ? "Dinner, bed and breakfast" : "Bed and breakfast"));
    }
    if (est) L.push("", "Indicative package cost: " + money(est.total) + " (" + est.line + ")");
    if (c) L.push("Estimated footprint: " + c.total + " kg CO2e (" + c.perHead + " kg per guest)");
    if (S.notes) L.push("", "Notes: " + S.notes);
    if (S.source) L.push("Heard about us: " + S.source);
    return L.join("\n");
  }

  /* ---------- Send to HOSPRO (Firestore) ---------- */
  function loadScript(src) {
    return new Promise(function (res, rej) {
      if (document.querySelector('script[src="' + src + '"]')) return res();
      var s = document.createElement("script"); s.src = src; s.onload = res; s.onerror = function () { rej(new Error("Could not load " + src)); };
      document.head.appendChild(s);
    });
  }
  function hosproRecord(body) {
    var room = byId(ROOMS, S.room), lay = byId(LAYOUTS, S.layout), est = estimate(), c = carbon(), t = byId(TYPES, S.type);
    var notes = [
      "Website planner: " + t.label,
      S.company ? "Company: " + S.company : "",
      S.days > 1 ? "Days: " + S.days : "",
      "Layout: " + lay.label,
      "Package: " + byId(PKGS, S.pkg).name,
      S.catering.length ? "Catering: " + names(window.BH_CATERING, S.catering).join(", ") : "",
      S.extras.length ? "Extras: " + names(window.BH_EXTRAS, S.extras).join(", ") + (S.extras.indexOf("breakout") > -1 && byId(ROOMS, S.breakoutRoom) ? " (breakout " + byId(ROOMS, S.breakoutRoom).name + ")" : "") : "",
      S.notes ? "Notes: " + S.notes : "",
      S.source ? "Heard via: " + S.source : ""
    ].filter(Boolean).join(" · ");
    return {
      name: S.name, email: S.email, phone: S.phone || "",
      company: S.company || "",
      event: t.hospro, eventLabel: t.label,
      date: S.date || "", days: S.days,
      pax: S.guests,
      room: room ? room.id : "", layout: S.layout,
      package: S.pkg,
      catering: S.catering, extras: S.extras,
      breakoutRoom: S.extras.indexOf("breakout") > -1 ? S.breakoutRoom : "",
      accommodation: S.stay
        ? S.bedrooms + " rooms x " + S.nights + " night(s) from " + (S.arrival || S.date || "TBC") + ", " + S.singles + " single / " + S.doubles + " double / " + S.twins + " twin, " + (S.board === "dbb" ? "DBB" : "B&B")
        : (S.pkg === "24hr" ? "Included in 24-hour package" : ""),
      budget: est ? "Package estimate " + money(est.total) : "",
      carbonKg: c ? c.total : null,
      notes: notes,
      summary: body,
      source: "Website",
      status: "new",
      created: new Date().toISOString()
    };
  }
  function hosproDb() {
    var H = C.hospro;
    if (!H || !H.enabled) return Promise.reject(new Error("HOSPRO disabled"));
    return loadScript(H.sdk + "firebase-app-compat.js")
      .then(function () { return Promise.all([loadScript(H.sdk + "firebase-auth-compat.js"), loadScript(H.sdk + "firebase-firestore-compat.js")]); })
      .then(function () {
        var app = (firebase.apps.find(function (a) { return a.name === "bh-web"; })) || firebase.initializeApp(H.firebase, "bh-web");
        var auth = app.auth();
        return (auth.currentUser ? Promise.resolve() : auth.signInAnonymously()).then(function () {
          return { db: app.firestore(), uid: auth.currentUser ? auth.currentUser.uid : "" };
        });
      });
  }
  // Called when someone passes the gate: records them in HOSPRO straight away,
  // so the team can follow up even if they don't finish the plan.
  function createLead() {
    return hosproDb().then(function (h) {
      return h.db.collection("enquiries").add({
        name: CT.name, email: CT.email, phone: CT.phone, company: CT.company || "",
        event: "meeting", pax: null, date: "", room: "",
        notes: "Started the online event planner" + (CT.company ? " · Company: " + CT.company : ""),
        source: "Website", stage: "Planner started", status: "new",
        uid: h.uid, created: new Date().toISOString()
      }).then(function (ref) { CT.leadId = ref.id; saveContact(); });
    });
  }
  function sendToHospro(body) {
    return hosproDb().then(function (h) {
      var rec = hosproRecord(body); rec.uid = h.uid; rec.stage = "Quote requested";
      if (CT.leadId) {
        return h.db.collection("enquiries").doc(CT.leadId).update(rec)
          .catch(function () { return h.db.collection("enquiries").add(rec); });
      }
      return h.db.collection("enquiries").add(rec);
    });
  }

  function validate() {
    var errs = [];
    var need = [["p-name", S.name, "Enter your name"], ["p-email", S.email, "Enter your email address"]];
    need.forEach(function (n) { setErr(n[0], n[1] ? "" : n[2]); if (!n[1]) errs.push(n[0]); });
    if (S.email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(S.email)) { setErr("p-email", "Enter an email address like name@company.co.uk"); errs.push("p-email"); }
    return errs;
  }
  function setErr(id, msg) {
    var el = $("#" + id), e = $("#" + id + "-err");
    if (e) e.textContent = msg;
    if (el) el.setAttribute("aria-invalid", msg ? "true" : "false");
  }

  $("#p-form").addEventListener("submit", function (e) {
    e.preventDefault();
    ["name", "company", "email", "phone", "notes", "source"].forEach(function (k) { var el = $("#p-" + k); if (el) S[k] = el.value.trim(); });
    var errs = validate();
    if (errs.length) { $("#" + errs[0]).focus(); return; }
    var body = specText();
    var done = $("#p-done");
    var btn = $("#p-submit");

    btn.disabled = true; btn.textContent = "Sending…";
    $("#p-send-err").textContent = "";
    if ($("#p-website").value) { showDone(true); return; } // spam trap

    sendToHospro(body).then(function () { showDone(true); })
      .catch(function (err) {
        console.warn("HOSPRO unavailable, using email:", err && err.message);
        var subject = "Event enquiry: " + byId(TYPES, S.type).label + ", " + S.guests + " guests" + (S.date ? ", " + S.date : "");
        location.href = "mailto:" + C.eventsEmail + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
        showDone(false);
      })
      .then(function () { btn.disabled = false; btn.textContent = "Request my quote"; });

    function showDone(sent) {
      $("#p-done-title").textContent = sent ? "Thank you, your request has been sent" : "Your email is ready to send";
      $("#p-done-text").textContent = sent
        ? "It's with our events team now, and they'll be in touch with a tailored proposal. A copy of your specification is below for your records."
        : "We've opened your email app with your full specification addressed to our events team. Press send and we'll come back to you with a tailored proposal. If nothing opened, copy the details below into an email to " + C.eventsEmail + ".";
      $("#p-done-copy").textContent = body;
      done.hidden = false; done.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  $("#p-copy").addEventListener("click", function () {
    var t = $("#p-done-copy").textContent;
    if (navigator.clipboard) navigator.clipboard.writeText(t).then(function () { $("#p-copy").textContent = "Copied"; });
  });
  $("#p-print").addEventListener("click", function () { window.print(); });


  /* ---------- Gate: contact details before planning ---------- */
  var CT = {};
  var CT_KEY = "bh_planner_contact";
  function saveContact() { try { localStorage.setItem(CT_KEY, JSON.stringify(CT)); } catch (e) {} }
  function loadContact() { try { return JSON.parse(localStorage.getItem(CT_KEY)) || null; } catch (e) { return null; } }

  function fillContact() {
    ["name", "company", "email", "phone"].forEach(function (k) { S[k] = CT[k] || ""; var el = $("#p-" + k); if (el) el.value = S[k]; });
    $("#who").textContent = CT.name + (CT.company ? ", " + CT.company : "");
  }
  function openPlanner(focus) {
    $("#gate").hidden = true; $("#planner-wrap").hidden = false;
    fillContact();
    if (focus) { $("#step-1 .step-t").setAttribute("tabindex", "-1"); $("#step-1 .step-t").focus(); window.scrollTo({ top: $("#planner-wrap").offsetTop - 90, behavior: "smooth" }); }
  }
  function gateErr(id, msg) { var e = $("#" + id + "-err"); if (e) e.textContent = msg; var el = $("#" + id); if (el) el.setAttribute("aria-invalid", msg ? "true" : "false"); return !msg; }

  $("#gate-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var v = function (id) { return $("#" + id).value.trim(); };
    var ok = true, first = null;
    function need(id, cond, msg) { var good = gateErr(id, cond ? "" : msg); if (!good && !first) first = id; ok = ok && good; }
    need("g-name", v("g-name"), "Enter your name");
    need("g-email", /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("g-email")), "Enter an email address like name@company.co.uk");
    need("g-phone", v("g-phone").replace(/[^0-9]/g, "").length >= 10, "Enter a phone number we can reach you on");
    need("g-consent", $("#g-consent").checked, "Tick to let us contact you about your event");
    if (!ok) { $("#" + first).focus(); return; }
    CT = { name: v("g-name"), company: v("g-company"), email: v("g-email"), phone: v("g-phone"), consent: new Date().toISOString() };
    saveContact();
    openPlanner(true);
    if (!$("#g-website").value) createLead().catch(function (err) { console.warn("Lead not saved to HOSPRO:", err && err.message); });
  });
  $("#not-you").addEventListener("click", function (e) {
    e.preventDefault();
    try { localStorage.removeItem(CT_KEY); } catch (x) {}
    CT = {};
    ["g-name", "g-company", "g-email", "g-phone"].forEach(function (id) { $("#" + id).value = ""; });
    $("#g-consent").checked = false;
    $("#planner-wrap").hidden = true; $("#gate").hidden = false; $("#g-name").focus();
  });

  var saved = loadContact();
  if (saved && saved.name && saved.email) { CT = saved; openPlanner(false); }
  else { $("#gate").hidden = false; }

  /* ---------- Initial values ---------- */
  $("#p-guests").value = S.guests;
  var today = new Date(); today.setDate(today.getDate() + 1);
  $("#p-date").min = today.toISOString().slice(0, 10);
  renderChecks("#p-cat", window.BH_CATERING, "catering");
  renderChecks("#p-extras", window.BH_EXTRAS, "extras");
  if (q.get("room")) {
    var rr = byId(ROOMS, q.get("room"));
    if (rr && !q.get("guests")) { S.guests = Math.min(S.guests, rr.cap[S.layout] || S.guests); $("#p-guests").value = S.guests; }
  }
  renderAll();
})();
