/* =========================================================
   Reflex Services — interactions
   Mobile menu · FAQ accordion · Before/After slider ·
   Scroll reveal · Contact form · Active nav
   Progressive enhancement: everything works without JS too.
   ========================================================= */
(function () {
  "use strict";

  /* ---- Mobile navigation ---- */
  var toggle = document.querySelector(".nav__toggle");
  var menu = document.getElementById("mobile-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    // close on link click
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        menu.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ---- Active nav link (current page) ---- */
  var here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("[data-nav]").forEach(function (link) {
    if (link.getAttribute("data-nav") === here) {
      link.setAttribute("aria-current", "page");
      link.style.color = "var(--blue-800)";
      link.style.fontWeight = "600";
    }
  });

  /* ---- FAQ accordion ---- */
  document.querySelectorAll(".faq__q").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var expanded = btn.getAttribute("aria-expanded") === "true";
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      btn.setAttribute("aria-expanded", expanded ? "false" : "true");
      if (panel) {
        panel.style.maxHeight = expanded ? null : panel.scrollHeight + "px";
      }
    });
  });

  /* ---- Before / After sliders ---- */
  document.querySelectorAll(".ba").forEach(function (ba) {
    var before = ba.querySelector(".ba__before");
    var handle = ba.querySelector(".ba__handle");
    var knob = ba.querySelector(".ba__knob");
    var range = ba.querySelector(".ba__range");
    function setPos(pct) {
      pct = Math.max(0, Math.min(100, pct));
      if (before) before.style.clipPath = "inset(0 " + (100 - pct) + "% 0 0)";
      if (handle) handle.style.left = pct + "%";
      if (knob) knob.style.left = pct + "%";
      if (range) range.value = pct;
    }
    if (range) {
      range.addEventListener("input", function () { setPos(parseFloat(range.value)); });
    }
    // drag support (pointer)
    var dragging = false;
    function pctFromEvent(e) {
      var rect = ba.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
      return (x / rect.width) * 100;
    }
    function start(e) { dragging = true; setPos(pctFromEvent(e)); }
    function move(e) { if (dragging) { setPos(pctFromEvent(e)); e.preventDefault(); } }
    function end() { dragging = false; }
    ba.addEventListener("mousedown", start);
    window.addEventListener("mousemove", move);
    window.addEventListener("mouseup", end);
    ba.addEventListener("touchstart", start, { passive: true });
    ba.addEventListener("touchmove", move, { passive: false });
    ba.addEventListener("touchend", end);
    setPos(50);
  });

  /* ---- Scroll reveal ---- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- Contact form (client-side demo handler) ---- */
  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var success = document.getElementById("form-success");
      // NOTE: connect this to your CRM / email endpoint (Formspree, Netlify, GA4 event, etc.)
      if (window.gtag) {
        window.gtag("event", "generate_lead", { form_id: "contact-form" });
      }
      if (success) {
        success.classList.add("show");
        success.setAttribute("tabindex", "-1");
        success.focus();
      }
      form.reset();
    });
  }

  /* ---- Track click-to-call for analytics (GA4-ready) ---- */
  document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
    a.addEventListener("click", function () {
      if (window.gtag) { window.gtag("event", "click_to_call"); }
    });
  });

  /* ---- Footer year ---- */
  var yearEl = document.getElementById("year");
  if (yearEl) { yearEl.textContent = new Date().getFullYear(); }
})();
