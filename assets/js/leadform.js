/* Lead forms (Corporate Stays, Group Tours).
   <form data-leadform data-team="corporate|groups" data-tag="Corporate|Group" data-subject="...">
   Every field with a <label> is sent. Fields marked required are checked.
   Sends the email directly (FormSubmit) and creates a HOSPRO lead.
   Never opens the visitor's email program. */
(function () {
  var C = window.BH_CONFIG || {};
  document.querySelectorAll("form[data-leadform]").forEach(function (f) {
    var done = f.parentNode.querySelector(".lead-done");
    var err = f.querySelector(".lead-err");
    var btn = f.querySelector("button[type=submit]");

    function labelFor(el) {
      if (el.dataset.label) return el.dataset.label;
      var l = f.querySelector('label[for="' + el.id + '"]');
      return l ? (l.firstChild && l.firstChild.nodeType === 3 ? l.firstChild.textContent : l.textContent).trim() : el.name;
    }
    function setErr(el, msg) {
      var e = document.getElementById(el.id + "-err");
      if (e) e.textContent = msg;
      el.setAttribute("aria-invalid", msg ? "true" : "false");
      return !msg;
    }

    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (f.querySelector("[name=_hp]") && f.querySelector("[name=_hp]").value) return;   // spam trap
      var ok = true, first = null;
      f.querySelectorAll("[required]").forEach(function (el) {
        var v = (el.value || "").trim(), msg = "";
        if (el.type === "checkbox") msg = el.checked ? "" : "Please tick to continue";
        else if (!v) msg = "Please complete this field";
        else if (el.type === "email" && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) msg = "Enter an email address like name@company.co.uk";
        else if (el.type === "tel" && v.replace(/[^0-9]/g, "").length < 10) msg = "Enter a phone number we can reach you on";
        if (!setErr(el, msg)) { ok = false; first = first || el; }
      });
      if (!ok) { first.focus(); return; }

      // Collect labelled answers, in page order
      var fields = {}, groups = {};
      f.querySelectorAll("input, select, textarea").forEach(function (el) {
        if (!el.id && !el.dataset.group) return;
        if (el.name === "_hp" || el.type === "submit") return;
        if (el.dataset.group) {           // checkbox groups, e.g. nights of the week
          groups[el.dataset.group] = groups[el.dataset.group] || [];
          if (el.checked) groups[el.dataset.group].push(el.value);
          return;
        }
        if (el.type === "checkbox") return;   // consent
        fields[labelFor(el)] = (el.value || "").trim() || "–";
      });
      Object.keys(groups).forEach(function (g) { fields[g] = groups[g].length ? groups[g].join(", ") : "–"; });

      var name = fields["Your name"] || fields["Contact name"] || "";
      var email = fields["Email"] || "";
      var org = fields["Company name"] || fields["Company or club name"] || "";
      var tag = f.dataset.tag, team = f.dataset.team;
      var subject = (f.dataset.subject || "Website enquiry") + ": " + (org || name) + (name && org ? " (" + name + ")" : "");

      btn.disabled = true; var label = btn.textContent; btn.textContent = "Sending…"; err.textContent = "";
      var notes = Object.keys(fields).map(function (k) { return k + ": " + fields[k]; }).join(" · ");
      var mail = window.bhSendForm(team, subject, email, fields,
        "Thank you for your enquiry to " + C.hotelName + ". Our team will reply within one working hour.")
        .then(function () { return true; }, function () { return false; });
      var lead = window.bhHosproLead({
        name: name, email: email, phone: fields["Phone"] || "", company: org,
        event: "meeting", eventLabel: tag + " enquiry", tag: tag,
        pax: parseInt(fields["Group size"], 10) || null, date: fields["Preferred arrival dates"] || "",
        room: "", notes: "Website " + tag + " enquiry · " + notes, summary: notes,
        source: "Website", stage: tag + " enquiry"
      }).then(function () { return true; }, function (e) { console.warn("HOSPRO not reached:", e && e.message); return false; });

      Promise.all([mail, lead]).then(function (r) {
        if (r[0] || r[1]) {
          f.hidden = true; done.hidden = false; done.focus();
        } else {
          err.textContent = window.bhSendError(C);
        }
        btn.disabled = false; btn.textContent = label;
      });
    });
  });
})();
