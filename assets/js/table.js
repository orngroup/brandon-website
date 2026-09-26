/* The Clarendon: table booking request, emailed to the hotel via FormSubmit.
   Falls back to the visitor's own email app if the service can't be reached. */
(function () {
  var C = window.BH_CONFIG, T = C.tableBooking, f = document.getElementById("t-form");
  if (!f || !T) return;
  var $ = function (id) { return document.getElementById(id); };
  var pad = function (n) { return (n < 10 ? "0" : "") + n; };
  var toMin = function (s) { var p = s.split(":"); return +p[0] * 60 + +p[1]; };
  var label = function (m) { var h = Math.floor(m / 60), mm = m % 60, h12 = h > 12 ? h - 12 : h; return h12 + (mm ? ":" + pad(mm) : "") + (h >= 12 ? "pm" : "am"); };

  var today = new Date(), iso = function (d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); };
  $("t-date").min = iso(today);
  var max = new Date(); max.setMonth(max.getMonth() + 6); $("t-date").max = iso(max);

  // Guests 1..maxOnline, then "more"
  var g = "";
  for (var i = 1; i <= T.maxOnline; i++) g += '<option value="' + i + '"' + (i === 2 ? " selected" : "") + ">" + i + (i === 1 ? " guest" : " guests") + "</option>";
  $("t-guests").innerHTML = g + '<option value="more">' + (T.maxOnline + 1) + " or more</option>";
  $("t-guests").addEventListener("change", function () {
    var big = this.value === "more";
    $("t-large").hidden = !big; $("t-submit").disabled = big;
  });

  // Time slots; today only shows times at least an hour from now
  function slots() {
    var first = toMin(T.firstSitting), last = toMin(T.lastSitting), opts = "", now = new Date();
    var isToday = $("t-date").value === iso(now), cutoff = now.getHours() * 60 + now.getMinutes() + 60;
    for (var m = first; m <= last; m += T.slotMinutes) {
      if (isToday && m < cutoff) continue;
      opts += '<option value="' + pad(Math.floor(m / 60)) + ":" + pad(m % 60) + '"' + (m === toMin("19:00") ? " selected" : "") + ">" + label(m) + "</option>";
    }
    $("t-time").innerHTML = opts || '<option value="">No more tables today</option>';
  }
  $("t-date").addEventListener("change", slots);
  slots();

  function err(id, msg) { var e = $(id + "-err"); if (e) e.textContent = msg; var el = $(id); if (el) el.setAttribute("aria-invalid", msg ? "true" : "false"); return !msg; }
  function longDate(v) { return new Date(v + "T12:00:00").toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }

  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var v = function (id) { return $(id).value.trim(); };
    var checks = [
      err("t-date", v("t-date") ? "" : "Choose a date"),
      err("t-time", v("t-time") ? "" : "Choose a time"),
      err("t-name", v("t-name") ? "" : "Enter your name"),
      err("t-phone", v("t-phone").replace(/[^0-9]/g, "").length >= 10 ? "" : "Enter a phone number we can reach you on"),
      err("t-email", /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("t-email")) ? "" : "Enter an email address like name@example.co.uk")
    ];
    $("t-consent-err").textContent = $("t-consent").checked ? "" : "Tick to let us contact you about your booking";
    if (checks.indexOf(false) > -1 || !$("t-consent").checked) {
      var bad = f.querySelector('[aria-invalid="true"]'); (bad || $("t-consent")).focus(); return;
    }
    if ($("t-website").value) return; // spam trap

    var time = $("t-time").options[$("t-time").selectedIndex].text;
    var guests = $("t-guests").value;
    var d = {
      "Date": longDate(v("t-date")), "Time": time, "Guests": guests,
      "Name": v("t-name"), "Phone": v("t-phone"), "Email": v("t-email"),
      "Occasion": v("t-occasion") || "None", "High chairs": v("t-highchair"),
      "Dietary needs or requests": v("t-notes") || "None"
    };
    var subject = "Table request: " + guests + " at " + time + ", " + d.Date + " (" + d.Name + ")";
    var payload = Object.assign({
      _subject: subject,
      _replyto: d.Email,
      _template: "table",
      _captcha: "false",
      _autoresponse: "Thank you for your table request at The Clarendon at " + C.hotelName + ". This is not yet a confirmed booking: our team will be in touch to confirm. " + d.Guests + " guests, " + d.Time + ", " + d.Date + "."
    }, d);

    var btn = $("t-submit"); btn.disabled = true; btn.textContent = "Sending…";
    fetch(T.endpoint + encodeURIComponent(T.email), {
      method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(payload)
    })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok || String(j.success) !== "true") throw new Error(j.message || r.status); }); })
      .then(function () { done(true); })
      .catch(function () {
        var body = Object.keys(d).map(function (k) { return k + ": " + d[k]; }).join("\n");
        location.href = "mailto:" + T.email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent("Please could I book a table at The Clarendon.\n\n" + body);
        done(false);
      });

    function done(sent) {
      $("t-done-title").textContent = sent ? "Thank you, " + d.Name.split(" ")[0] + ". Your request is with us." : "Your email is ready to send";
      $("t-done-text").textContent = sent
        ? "We'll confirm your table by email or phone shortly. Your table isn't booked until we've confirmed it."
        : "We've opened your email app with your booking request addressed to us. Press send and we'll confirm your table. If nothing opened, call us on " + C.phone + ".";
      $("t-done-list").innerHTML = ["Date", "Time", "Guests", "Occasion"].filter(function (k) { return k !== "Occasion" || d.Occasion !== "None"; })
        .map(function (k) { return "<div><dt>" + k + "</dt><dd>" + d[k] + "</dd></div>"; }).join("");
      f.hidden = true; $("t-done").hidden = false; $("t-done").focus();
      btn.disabled = false; btn.textContent = "Request my table";
    }
  });
})();
