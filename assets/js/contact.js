/* Contact form: emails the message straight to the right team.
   Stays, dining and anything else go to reservations; weddings,
   meetings, Christmas and celebrations go to events, and also
   into HOSPRO. Never opens the visitor's email program.
   Pre-select a topic with ?topic=wedding|meeting|christmas|celebration|stay|dining
   and an optional ?about=... to start the message. */
(function () {
  var C = window.BH_CONFIG, f = document.getElementById("c-form");
  if (!f) return;
  var $ = function (id) { return document.getElementById(id); };

  // Topic from the link (e.g. "Book a tour" on the weddings page)
  var q = new URLSearchParams(location.search);
  var TOPICS = { wedding: "A wedding", meeting: "A meeting or event", christmas: "Christmas and New Year",
                 celebration: "A meeting or event", stay: "A stay", dining: "Dining" };
  if (q.get("topic") && TOPICS[q.get("topic")]) $("c-topic").value = TOPICS[q.get("topic")];
  if (q.get("about")) $("c-msg").value = q.get("about") + "\n\n";

  function err(id, msg) { $(id + "-err").textContent = msg; $(id).setAttribute("aria-invalid", msg ? "true" : "false"); return !msg; }
  function load(src) { return new Promise(function (res, rej) { if (document.querySelector('script[src="' + src + '"]')) return res(); var s = document.createElement("script"); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); }
  function toHospro(rec) {
    var H = C.hospro; if (!H || !H.enabled) return Promise.reject(new Error("off"));
    return load(H.sdk + "firebase-app-compat.js")
      .then(function () { return Promise.all([load(H.sdk + "firebase-auth-compat.js"), load(H.sdk + "firebase-firestore-compat.js")]); })
      .then(function () {
        var app = firebase.apps.find(function (a) { return a.name === "bh-web"; }) || firebase.initializeApp(H.firebase, "bh-web");
        var auth = app.auth();
        return (auth.currentUser ? Promise.resolve() : auth.signInAnonymously()).then(function () {
          rec.uid = auth.currentUser.uid;
          return app.firestore().collection("enquiries").add(rec);
        });
      });
  }

  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var name = $("c-name").value.trim(), email = $("c-email").value.trim(), msg = $("c-msg").value.trim();
    var ok = [err("c-name", name ? "" : "Enter your name"),
      err("c-email", /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) ? "" : "Enter an email address like name@example.co.uk"),
      err("c-msg", msg ? "" : "Enter your message")];
    $("c-consent-err").textContent = $("c-consent").checked ? "" : "Tick to let us contact you about your message";
    if (ok.indexOf(false) > -1 || !$("c-consent").checked) { (f.querySelector('[aria-invalid="true"]') || $("c-consent")).focus(); return; }
    var topic = $("c-topic").value, phone = $("c-phone").value.trim();
    var done = $("c-done"), btn = $("c-submit"), sendErr = $("c-send-err");
    if ($("c-website").value) { done.hidden = false; done.textContent = "Thank you."; return; }

    var hosproType = { "A wedding": "wedding", "A meeting or event": "meeting", "Christmas and New Year": "christmas" }[topic];
    var team = hosproType ? "events" : "reservations";
    btn.disabled = true; btn.textContent = "Sending…"; sendErr.textContent = "";

    var mail = window.bhSendForm(team, "Website enquiry: " + topic + " (" + name + ")", email,
      { "Topic": topic, "Name": name, "Email": email, "Phone": phone || "–", "Message": msg },
      "Thank you for contacting " + C.hotelName + ". We've received your message and our team will be in touch soon.");
    var hospro = hosproType
      ? toHospro({ name: name, email: email, phone: phone, event: hosproType, eventLabel: topic,
          notes: "Website contact form: " + topic + " · " + msg, summary: msg, source: "Website contact form",
          stage: "Contact form", status: "new", pax: null, date: "", room: "", created: new Date().toISOString() }).catch(function () {})
      : Promise.resolve();

    mail.then(function () {
      return hospro.then(function () {
        done.textContent = "Thank you, " + name.split(" ")[0] + ". Your message is with our team and we'll be in touch soon.";
        done.hidden = false; done.focus(); f.reset();
      });
    }).catch(function () {
      sendErr.textContent = window.bhSendError(C);
    }).then(function () { btn.disabled = false; btn.textContent = "Send message"; });
  });
})();
