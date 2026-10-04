/* Shared form sender: emails a form straight to the hotel through
   FormSubmit, without opening the visitor's email program.
   bhSendForm(toKey, subject, replyTo, fields, autoReply)
     toKey   "reservations" or "events" (addresses in venue-data.js)
     fields  { "Label": "value", ... } shown as a table in the email
   Resolves on success. Rejects with err.code = "activation" when the
   address hasn't been activated yet, or "failed" otherwise. */
(function () {
  window.bhSendForm = function (toKey, subject, replyTo, fields, autoReply) {
    var C = window.BH_CONFIG || {};
    var to = (C.formEmails && C.formEmails[toKey]) || C.eventsEmail;
    var body = Object.assign({ _subject: subject, _template: "table", _captcha: "false" }, fields);
    if (replyTo) body._replyto = replyTo;
    if (autoReply) body._autoresponse = autoReply;
    return fetch((C.formEndpoint || "https://formsubmit.co/ajax/") + encodeURIComponent(to), {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(body)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (r.ok && String(j.success) === "true") return j;
        var e = new Error(j.message || ("HTTP " + r.status));
        e.code = /activat/i.test(j.message || "") ? "activation" : "failed";
        console.warn("Form not sent:", e.message);
        throw e;
      });
    });
  };
  /* Create a HOSPRO lead (Firestore "enquiries"), same route as the planner. */
  function load(src) { return new Promise(function (res, rej) { if (document.querySelector('script[src="' + src + '"]')) return res(); var s = document.createElement("script"); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); }
  window.bhHosproLead = function (rec) {
    var C = window.BH_CONFIG || {}, H = C.hospro;
    if (!H || !H.enabled) return Promise.reject(new Error("HOSPRO off"));
    return load(H.sdk + "firebase-app-compat.js")
      .then(function () { return Promise.all([load(H.sdk + "firebase-auth-compat.js"), load(H.sdk + "firebase-firestore-compat.js")]); })
      .then(function () {
        var app = firebase.apps.find(function (a) { return a.name === "bh-web"; }) || firebase.initializeApp(H.firebase, "bh-web");
        var auth = app.auth();
        return (auth.currentUser ? Promise.resolve() : auth.signInAnonymously()).then(function () {
          rec.uid = auth.currentUser.uid; rec.status = "new"; rec.created = new Date().toISOString();
          return app.firestore().collection("enquiries").add(rec);
        });
      });
  };

  window.bhSendError = function (C, toKey) {
    var C2 = C || window.BH_CONFIG || {};
    return "Sorry, we couldn't send that just now. Please call us on " + C2.phone + " and we'll be happy to help.";
  };
})();
