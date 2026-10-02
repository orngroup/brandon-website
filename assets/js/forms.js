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
  window.bhSendError = function (C, toKey) {
    var C2 = C || window.BH_CONFIG || {};
    return "Sorry, we couldn't send that just now. Please call us on " + C2.phone + " and we'll be happy to help.";
  };
})();
