/* Christmas competition 2026
   Five-question quiz; when every answer is right the entry form opens.
   Entries go straight into HOSPRO (Firestore "competition"), with no email
   step that could hold them up. HOSPRO > HosSTUDIO > Competition shows the
   entries, the mailing-list opt-ins and picks a winner. */
(function () {
  var C = window.BH_CONFIG || {};
  var $ = function (id) { return document.getElementById(id); };
  var CAMPAIGN = "xmas2026";
  var CLOSES = new Date("2026-12-14T23:59:59+00:00");
  var Q = [
    { q: "What is the name of our restaurant at Brandon Hall?", a: ["The Orangery", "The Clarendon", "The Warwick Room", "The Brandon Grill"], c: 1, hint: '<a href="../dining/" target="_blank">Find it on our Dining page</a>' },
    { q: "How many acres of Warwickshire grounds surround the hotel?", a: ["7 acres", "17 acres", "70 acres", "170 acres"], c: 1, hint: '<a href="../christmas/" target="_blank">Find it on our Christmas page</a>' },
    { q: "What can you enjoy beneath a glazed roof in our Leisure and Wellness area?", a: ["An ice rink", "A bowling alley", "An indoor swimming pool", "A climbing wall"], c: 2, hint: '<a href="../spa-leisure/" target="_blank">Find it on our Leisure page</a>' },
    { q: "Which country gives London the Christmas tree in Trafalgar Square every year?", a: ["Sweden", "Finland", "Denmark", "Norway"], c: 3, hint: "It's been a thank-you gift since 1947." },
    { q: "In The Twelve Days of Christmas, what is given on the first day?", a: ["Two turtle doves", "A partridge in a pear tree", "Five gold rings", "Three French hens"], c: 1, hint: "It's sitting in a tree." }
  ];

  var qf = $("q-form");
  qf.innerHTML = Q.map(function (x, i) {
    return '<fieldset class="qq" id="qq' + i + '"><legend><span class="qn">' + (i + 1) + '</span>' + x.q + '</legend><div class="qa">' +
      x.a.map(function (t, j) { return '<label class="qopt"><input type="radio" name="q' + i + '" value="' + j + '"><span>' + t + '</span></label>'; }).join("") +
      '</div><p class="qhint" hidden></p></fieldset>';
  }).join("");

  var closed = new Date() > CLOSES;
  if (closed) {
    $("q-actions").hidden = true;
    $("q-msg").innerHTML = "This competition has now closed. Thank you to everyone who entered.";
  }

  var answers = [];
  $("q-check").addEventListener("click", function () {
    var wrong = 0, missing = 0;
    answers = Q.map(function (x, i) {
      var r = qf.querySelector('input[name="q' + i + '"]:checked'), box = $("qq" + i), h = box.querySelector(".qhint");
      box.classList.remove("ok", "no");
      if (!r) { missing++; h.hidden = false; h.innerHTML = "Choose an answer."; box.classList.add("no"); return null; }
      var v = +r.value;
      if (v === x.c) { box.classList.add("ok"); h.hidden = true; }
      else { wrong++; box.classList.add("no"); h.hidden = false; h.innerHTML = "Not quite. Have another go. " + x.hint; }
      return x.a[v];
    });
    if (missing || wrong) {
      $("q-msg").textContent = missing ? "Please answer every question." : (wrong === 1 ? "One answer isn't right yet. Change it and check again." : wrong + " answers aren't right yet. Change them and check again.");
      var first = qf.querySelector(".qq.no"); if (first) first.scrollIntoView({ behavior: "smooth", block: "center" });
      return;
    }
    $("q-msg").textContent = "";
    $("q-actions").hidden = true;
    var e = $("entry"); e.hidden = false; e.focus(); e.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  function err(id, msg) { var e = $(id + "-err"); if (e) e.textContent = msg; var el = $(id); if (el) el.setAttribute("aria-invalid", msg ? "true" : "false"); return !msg; }
  function load(src) { return new Promise(function (res, rej) { if (document.querySelector('script[src="' + src + '"]')) return res(); var s = document.createElement("script"); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); }
  function save(rec) {
    var H = C.hospro; if (!H || !H.enabled) return Promise.reject(new Error("HOSPRO off"));
    return load(H.sdk + "firebase-app-compat.js")
      .then(function () { return load(H.sdk + "firebase-firestore-compat.js"); })
      .then(function () {
        var app = firebase.apps.find(function (a) { return a.name === "bh-comp"; }) || firebase.initializeApp(H.firebase, "bh-comp");
        return app.firestore().collection("competition").add(rec);
      });
  }

  $("e-form").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var v = function (id) { return $(id).value.trim(); };
    var ok = [err("e-first", v("e-first") ? "" : "Enter your first name"),
      err("e-last", v("e-last") ? "" : "Enter your last name"),
      err("e-email", /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("e-email")) ? "" : "Enter an email address like name@example.co.uk"),
      err("e-age", $("e-age").checked ? "" : "Please confirm you're 18 or over, live in the UK and agree to the terms")];
    if (ok.indexOf(false) > -1) { $(["e-first", "e-last", "e-email", "e-age"][ok.indexOf(false)]).focus(); return; }
    if ($("e-website").value) { done(); return; }
    var btn = $("e-submit"); btn.disabled = true; btn.textContent = "Entering…"; $("e-send-err").textContent = "";
    var src = new URLSearchParams(location.search).get("src") || (document.referrer ? new URL(document.referrer).hostname : "direct");
    var rec = {
      campaign: CAMPAIGN, firstName: v("e-first"), lastName: v("e-last"), email: v("e-email").toLowerCase(),
      phone: v("e-phone"), town: v("e-town"), optIn: $("e-optin").checked, terms: true,
      answers: answers, score: Q.length, allCorrect: true, source: String(src).slice(0, 60),
      created: new Date().toISOString()
    };
    function attempt(n) {
      return save(rec).catch(function (e) { if (n > 1) return new Promise(function (r) { setTimeout(r, 1500); }).then(function () { return attempt(n - 1); }); throw e; });
    }
    attempt(2).then(function () {
      try { localStorage.setItem("bh_comp_" + CAMPAIGN, "1"); } catch (x) {}
      done();
    }, function (e) {
      console.warn("Entry not saved:", e && e.message);
      $("e-send-err").textContent = "Sorry, we couldn't save your entry just now. Please try again in a moment, or call us on " + (C.phone || "024 7710 2555") + ".";
      btn.disabled = false; btn.textContent = "Enter the competition";
    });
  });

  var URL_ = "https://www.brandonhallhotelandspa.com/christmas-competition/";
  var MSG = "I've just entered the Brandon Hall Hotel and Spa Christmas competition to win a night for two with dinner. Enter here: ";
  $("sh-wa").href = "https://wa.me/?text=" + encodeURIComponent(MSG + URL_ + "?src=whatsapp");
  $("sh-fb").href = "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(URL_ + "?src=facebook-share");
  $("sh-copy").addEventListener("click", function () {
    var b = this; (navigator.clipboard ? navigator.clipboard.writeText(URL_) : Promise.reject()).then(function () { b.textContent = "Link copied"; }, function () { prompt("Copy this link:", URL_); });
  });

  function done() {
    $("e-form").hidden = true; $("entry").querySelector("h3").hidden = true; $("entry").hidden = true;
    var d = $("done"); d.hidden = false; d.focus(); d.scrollIntoView({ behavior: "smooth", block: "center" });
  }
})();
