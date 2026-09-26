/* Contact form: sends the message into HOSPRO's enquiries,
   or opens the visitor's email app if HOSPRO can't be reached. */
(function () {
  var C = window.BH_CONFIG, f = document.getElementById("c-form");
  if (!f) return;
  var $ = function (id) { return document.getElementById(id); };
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
    if (ok.indexOf(false) > -1 || !$("c-consent").checked) { f.querySelector('[aria-invalid="true"]') ? f.querySelector('[aria-invalid="true"]').focus() : $("c-consent").focus(); return; }
    var topic = $("c-topic").value, phone = $("c-phone").value.trim();
    var done = $("c-done"), btn = $("c-submit");
    if ($("c-website").value) { done.hidden = false; done.textContent = "Thank you."; return; }
    btn.disabled = true; btn.textContent = "Sending…";
    var map = { "A wedding": "wedding", "A meeting or event": "meeting", "Christmas and New Year": "christmas" };
    toHospro({ name: name, email: email, phone: phone, event: map[topic] || "other", eventLabel: topic,
      notes: "Website contact form: " + topic + " · " + msg, summary: msg, source: "Website contact form",
      stage: "Contact form", status: "new", pax: null, date: "", room: "", created: new Date().toISOString() })
      .then(function () {
        done.textContent = "Thank you, " + name.split(" ")[0] + ". Your message is with our team and we'll be in touch soon.";
      })
      .catch(function () {
        location.href = "mailto:" + C.eventsEmail + "?subject=" + encodeURIComponent("Website enquiry: " + topic) + "&body=" + encodeURIComponent(msg + "\n\n" + name + (phone ? "\n" + phone : "") + "\n" + email);
        done.textContent = "We've opened your email app with your message ready to send to " + C.eventsEmail + ". Press send and we'll be in touch soon.";
      })
      .then(function () { done.hidden = false; done.focus(); btn.disabled = false; btn.textContent = "Send message"; f.reset(); });
  });
})();
