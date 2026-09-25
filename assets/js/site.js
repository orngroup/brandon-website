/* Brandon Hall Hotel and Spa — shared behaviour */
(function () {
  // Mobile splash: hold the gold logo briefly, then fade to the page.
  var root = document.documentElement;
  if (root.classList.contains("splash")) {
    var sp = document.querySelector(".splash-screen");
    try { sessionStorage.setItem("bhSplash", "1"); } catch (e) {}
    setTimeout(function () {
      if (sp) sp.classList.add("is-leaving");
      setTimeout(function () { root.classList.remove("splash"); }, 750);
    }, 1400);
  }

  // Sticky header: shrink only once the visitor has actually scrolled.
  // Set the starting state without animation so the logo never "jumps"
  // when a page opens.
  var header = document.querySelector(".site-header");
  if (header) {
    var stuck = null;
    function update() {
      var s = window.scrollY > 60;
      if (s !== stuck) { stuck = s; header.classList.toggle("is-stuck", s); }
    }
    header.classList.add("no-anim");
    update();
    requestAnimationFrame(function () { requestAnimationFrame(function () { header.classList.remove("no-anim"); }); });
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(function () { update(); ticking = false; }); }
    }, { passive: true });
  }

  // Mobile drawer
  var drawer = document.getElementById("drawer");
  var openBtn = document.querySelector(".menu-toggle");
  if (drawer && openBtn) {
    var closeBtn = drawer.querySelector(".close");
    openBtn.addEventListener("click", function () {
      drawer.classList.add("open"); openBtn.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden"; closeBtn.focus();
    });
    function close() {
      drawer.classList.remove("open"); openBtn.setAttribute("aria-expanded", "false");
      document.body.style.overflow = ""; openBtn.focus();
    }
    closeBtn.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && drawer.classList.contains("open")) close(); });
  }

  // Book direct: open the Profitroom panel when it has loaded,
  // otherwise follow the link to the booking engine.
  document.addEventListener("click", function (e) {
    var a = e.target.closest("[data-book]");
    if (!a) return;
    if (window.Booking && typeof window.Booking.Open === "function") {
      e.preventDefault();
      window.Booking.Open();
    }
  });

  // Meeting photo galleries (local copy first, hotel website as fallback)
  if (window.BH_MEETING_PHOTOS) {
    document.querySelectorAll("[data-meeting-photos]").forEach(function (g) {
      var root = g.getAttribute("data-root") || "";
      g.innerHTML = window.BH_MEETING_PHOTOS.map(function (ph) {
        return '<figure><img src="' + root + ph.src + '" alt="' + ph.alt + '" loading="lazy" data-fallback="' + ph.remote + '"></figure>';
      }).join("");
      g.querySelectorAll("img").forEach(function (img) {
        img.addEventListener("error", function () {
          if (img.dataset.fallback && img.src !== img.dataset.fallback) { img.src = img.dataset.fallback; img.dataset.fallback = ""; }
          else { img.closest("figure").remove(); }
        });
      });
    });
  }

  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
})();
