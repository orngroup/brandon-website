/* Brandon Hall Hotel and Spa — shared behaviour */
(function () {
  // Sticky header state
  var header = document.querySelector(".site-header");
  if (header && "IntersectionObserver" in window) {
    var sentinel = document.createElement("div");
    sentinel.style.cssText = "position:absolute;top:0;height:1px;width:1px";
    document.body.prepend(sentinel);
    new IntersectionObserver(function (e) {
      header.classList.toggle("is-stuck", !e[0].isIntersecting);
    }, { rootMargin: "-40px 0px 0px 0px" }).observe(sentinel);
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
