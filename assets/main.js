/* AAPSON · Acid Circuit — motion runtime
   Lenis smooth-scroll + contador do bloco pinado "Como funciona".
   Honra prefers-reduced-motion: sem smooth-scroll, sem observers. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- Lenis: inércia de scroll (o "feel Apple") --- */
  if (!reduce && typeof Lenis !== "undefined") {
    var lenis = new Lenis({ lerp: 0.1, wheelMultiplier: 1, smoothWheel: true });
    function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
    /* âncoras internas continuam funcionando com o smooth-scroll */
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener("click", function (e) {
        var id = a.getAttribute("href");
        if (id.length > 1) {
          var el = document.querySelector(id);
          if (el) { e.preventDefault(); lenis.scrollTo(el, { offset: -72 }); }
        }
      });
    });
  }

  /* --- contador do bloco pinado: qual passo está ativo --- */
  var steps = document.querySelectorAll(".flow-step");
  var count = document.querySelector("[data-flow-count]");
  var now = document.querySelector("[data-flow-now]");
  if (steps.length && count && now && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          var i = en.target.getAttribute("data-i");
          var label = en.target.getAttribute("data-label") || "";
          count.firstChild.nodeValue = "0" + i;
          now.textContent = label;
        }
      });
    }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
    steps.forEach(function (s) { io.observe(s); });
  }

  /* --- PME scrub hero: o scroll dirige a animação do fluxo --- */
  var scrub = document.querySelector(".scrub");
  var pipe = document.querySelector("[data-pipe]");
  var label = document.querySelector("[data-scrub-label]");
  var nodes = document.querySelectorAll(".scrub .node");
  var STAGES = ["Detecta", "Tenta de novo", "Avisa", "Confere"];
  if (scrub && pipe && label) {
    if (reduce) {
      /* reduced-motion: estado final estático */
      pipe.style.width = "100%";
      label.textContent = STAGES[STAGES.length - 1];
      nodes.forEach(function (n) { n.classList.add("on"); });
    } else {
      var ticking = false;
      function update() {
        ticking = false;
        var total = scrub.offsetHeight - window.innerHeight;
        if (total <= 0) {            /* mobile: hero estático */
          pipe.style.width = "100%";
          label.textContent = STAGES[STAGES.length - 1];
          nodes.forEach(function (n) { n.classList.add("on"); });
          return;
        }
        var top = scrub.getBoundingClientRect().top;
        var p = Math.min(1, Math.max(0, -top / total));
        pipe.style.width = (p * 100).toFixed(2) + "%";
        var idx = Math.min(STAGES.length - 1, Math.floor(p * STAGES.length));
        if (label.textContent !== STAGES[idx]) label.textContent = STAGES[idx];
        var lastIdx = STAGES.length - 1;
        nodes.forEach(function (n) {
          var at = parseFloat(n.getAttribute("data-at"));
          /* último nó acende ao entrar na etapa final (não só em p=1) */
          var on = at >= 1 ? (idx >= lastIdx) : (p >= at - 0.001);
          n.classList.toggle("on", on);
        });
      }
      window.addEventListener("scroll", function () {
        if (!ticking) { ticking = true; requestAnimationFrame(update); }
      }, { passive: true });
      window.addEventListener("resize", update);
      update();
    }
  }

  /* --- global status bar: sessão (tempo real) + heartbeat pings --- */
  var t0 = Date.now();
  var sessEl = document.querySelector("[data-sessão]");
  var pingEl = document.querySelector("[data-pings]");
  function fmt(ms) {
    var s = Math.floor(ms / 1000);
    var h = Math.floor(s / 3600); s -= h * 3600;
    var m = Math.floor(s / 60); s -= m * 60;
    var p = function (n) { return (n < 10 ? "0" : "") + n; };
    return (h ? h + "h " : "") + p(m) + "m " + p(s) + "s";
  }
  if (sessEl) {
    setInterval(function () { sessEl.textContent = fmt(Date.now() - t0); }, 1000);
  }
  if (pingEl && !reduce) {
    var pings = 0;
    setInterval(function () { pings++; pingEl.textContent = pings; }, 3000);
  }
})();
