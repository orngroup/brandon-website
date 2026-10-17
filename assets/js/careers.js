/* Careers page: "Apply" buttons pick the team in the form, and the
   application (with CV attached) is posted to the careers inbox through
   FormSubmit in a hidden frame. The visitor only sees a thank-you box. */
(function () {
  var C = window.BH_CONFIG || {}, f = document.getElementById("cv-form");
  if (!f) return;
  var $ = function (id) { return document.getElementById(id); };
  var to = (C.formEmails && C.formEmails.careers) || "laith.hardy@brandonhallhotelandspa.com";
  f.action = "https://formsubmit.co/" + to;

  document.querySelectorAll("[data-dept]").forEach(function (a) {
    a.addEventListener("click", function () { $("cv-dept").value = a.dataset.dept; });
  });

  function err(id, msg) { var e = $(id + "-err"); if (e) e.textContent = msg; var el = $(id); if (el) el.setAttribute("aria-invalid", msg ? "true" : "false"); return !msg; }

  f.addEventListener("submit", function (e) {
    var name = $("cv-name").value.trim(), email = $("cv-email").value.trim(), phone = $("cv-phone").value.trim();
    var file = $("cv-file").files[0];
    var okType = file && /\.(pdf|docx?)$/i.test(file.name);
    var ok = [
      err("cv-name", name ? "" : "Enter your name"),
      err("cv-phone", phone.replace(/[^0-9]/g, "").length >= 10 ? "" : "Enter a phone number we can reach you on"),
      err("cv-email", /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) ? "" : "Enter an email address like name@example.co.uk"),
      err("cv-file", !file ? "Attach your CV" : !okType ? "Attach your CV as a PDF or Word document" : file.size > 5 * 1024 * 1024 ? "Your CV must be 5 MB or smaller" : ""),
      err("cv-consent", $("cv-consent").checked ? "" : "Tick to let us keep your details and contact you")
    ];
    if (ok.indexOf(false) > -1) {
      e.preventDefault();
      var first = ["cv-name", "cv-phone", "cv-email", "cv-file", "cv-consent"][ok.indexOf(false)];
      $(first).focus();
      return;
    }
    if (f.querySelector('[name="_honey"]').value) { e.preventDefault(); done(); return; }
    $("cv-replyto").value = email;
    $("cv-subject").value = "Job application: " + $("cv-dept").value + " (" + name + ")";
    $("cv-submit").disabled = true; $("cv-submit").textContent = "Sending…";
    // The browser posts the form into the hidden frame; show the thank-you box.
    setTimeout(done, 900);
  });

  function done() {
    f.hidden = true;
    var d = $("cv-done"); d.hidden = false; d.focus();
    d.scrollIntoView({ behavior: "smooth", block: "center" });
  }
})();
