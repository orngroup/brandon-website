/* ==========================================================
   Event quote links
   The planner packs the event specification into a link such as
   /meetings-events/quote/?q=...  so the guest, the events team and
   HOSPRO can all open the same branded quote and download it as a PDF.
   No email address or phone number is put in the link.
   ========================================================== */
(function () {
  var BASE = "https://www.brandonhallhotelandspa.com/meetings-events/quote/";

  function b64urlEncode(str) {
    var b = btoa(unescape(encodeURIComponent(str)));
    return b.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }
  function b64urlDecode(s) {
    s = String(s || "").replace(/-/g, "+").replace(/_/g, "/");
    while (s.length % 4) s += "=";
    return decodeURIComponent(escape(atob(s)));
  }

  // Reference such as BH-261015-7KQ4
  window.bhQuoteRef = function () {
    var d = new Date(), p = function (n) { return (n < 10 ? "0" : "") + n; };
    var abc = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789", r = "";
    for (var i = 0; i < 4; i++) r += abc[Math.floor(Math.random() * abc.length)];
    return "BH-" + String(d.getFullYear()).slice(2) + p(d.getMonth() + 1) + p(d.getDate()) + "-" + r;
  };

  var KEYS = ["type", "date", "days", "guests", "layout", "room", "pkg", "catering", "extras", "breakoutRoom",
    "stay", "bedrooms", "nights", "singles", "doubles", "twins", "board", "arrival", "name", "company", "notes"];

  window.bhQuoteLink = function (S, ref) {
    var o = { v: 1, ref: ref, ts: new Date().toISOString() };
    KEYS.forEach(function (k) { if (S[k] !== undefined && S[k] !== "" && !(Array.isArray(S[k]) && !S[k].length)) o[k] = S[k]; });
    if (!o.stay) { ["bedrooms", "nights", "singles", "doubles", "twins", "board", "arrival"].forEach(function (k) { delete o[k]; }); }
    return BASE + "?q=" + b64urlEncode(JSON.stringify(o));
  };

  window.bhQuoteRead = function (search) {
    var q = new URLSearchParams(search || location.search).get("q");
    if (!q) return null;
    try { var o = JSON.parse(b64urlDecode(q)); return o && o.v === 1 ? o : null; } catch (e) { return null; }
  };

  /* Guide "from" price for the event, matching the prices shown on the site.
     Returns null when the price is on request. */
  window.bhGuidePrice = function (S) {
    var P = (window.BH_CONFIG && window.BH_CONFIG.fromPrices) || {};
    var meet = ["meeting", "conference", "training"].indexOf(S.type) > -1;
    var map = meet
      ? (S.pkg === "ddr" ? ["dayDelegate", "per delegate, day delegate package"] : S.pkg === "24hr" ? ["twentyFourHour", "per delegate, 24-hour package"] : null)
      : ({
          wedding: ["wedding", "per guest"],
          celebration: ["party", "per person"],
          "baby-shower": ["babyShower", "per person"],
          "celebration-of-life": ["celebrationOfLife", "per person"],
          masonic: ["masonic", "per person, two nights"],
          christmas: ["christmasParty", "per person for party nights"],
          dinner: ["awardsDinner", "per person"],
          awards: ["awardsDinner", "per person"]
        })[S.type];
    if (!map || !P[map[0]]) return null;
    return { price: P[map[0]], suffix: map[1] };
  };
})();
