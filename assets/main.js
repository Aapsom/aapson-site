/* AAPSON · Acid Circuit — motion runtime
   Lenis smooth-scroll + scrub com spring + reveals de seção + parallax.
   Honra prefers-reduced-motion: sem smooth-scroll, sem observers, estado final. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- Lenis: inércia de scroll (o "feel Apple") --- */
  if (!reduce && typeof Lenis !== "undefined") {
    var lenis = new Lenis({ lerp: 0.1, wheelMultiplier: 1, smoothWheel: true });
    function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
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

  /* ============================================================
     1) REVEALS de seção (IntersectionObserver) — dirige .in
     ============================================================ */
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window && !reduce) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); ro.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.12 });
    reveals.forEach(function (r) { ro.observe(r); });
  } else {
    reveals.forEach(function (r) { r.classList.add("in"); });
  }

  /* ============================================================
     2) FLOW-STEP ativo (linha de tempo da seção "Como funciona")
        dirige .is-active (highlight de borda) — mais robusto que opacity
     ============================================================ */
  var steps = document.querySelectorAll(".flow-step");
  var count = document.querySelector("[data-flow-count]");
  var now = document.querySelector("[data-flow-now]");
  if (steps.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          steps.forEach(function (s) { s.classList.remove("is-active"); });
          en.target.classList.add("is-active");
          if (count && now) {
            var i = en.target.getAttribute("data-i");
            var label = en.target.getAttribute("data-label") || "";
            count.firstChild.nodeValue = (i < 10 ? "0" : "") + i;
            now.textContent = label;
          }
        }
      });
    }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
    steps.forEach(function (s) { io.observe(s); });
    if (reduce) steps[0].classList.add("is-active");
  }

  /* flow-mark: respiro ao entrar na view */
  var fmark = document.querySelector(".flow-mark");
  if (fmark && "IntersectionObserver" in window && !reduce) {
    var mo = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); mo.unobserve(en.target); }
      });
    }, { threshold: 0.3 });
    mo.observe(fmark);
  } else if (fmark) { fmark.classList.add("in"); }

  /* ============================================================
     3) SCRUB PME — progresso com SPRING (lerp contínuo no rAF)
        feel suave/robusto, não linear. Labels com fade ao trocar.
     ============================================================ */
  var scrub = document.querySelector(".scrub");
  var pipe = document.querySelector("[data-pipe]");
  var vpipe = document.querySelector("[data-vpipe]");
  var label = document.querySelector("[data-scrub-label]");
  var nodes = document.querySelectorAll(".scrub .node");
  var vnodes = document.querySelectorAll(".vtimeline .vstages li");
  var vlabels = document.querySelectorAll(".vtimeline .vstages li");
  var STAGES = (scrub && scrub.getAttribute("data-stages"))
    ? scrub.getAttribute("data-stages").split(",").map(function (s) { return s.trim(); })
    : ["Detecta", "Tenta de novo", "Avisa", "Confere"];
  var sub = (label && label.querySelector(".sub")) ? label.querySelector(".sub") : null;

  function setFinal() {
    if (pipe) pipe.style.width = "100%";
    if (vpipe) vpipe.style.height = "100%";
    if (label) label.firstChild.nodeValue = STAGES[STAGES.length - 1];
    nodes.forEach(function (n) { n.classList.add("on"); });
    vnodes.forEach(function (n, i) { n.classList.toggle("on", i === STAGES.length - 1); });
    vlabels.forEach(function (n, i) { n.classList.toggle("on", i === STAGES.length - 1); });
  }

  if (scrub && vpipe && label) {
    if (reduce) {
      setFinal();
    } else {
      var cur = 0, target = 0, raf2 = null, lastIdx = -1;
      function computeTarget() {
        var total = scrub.offsetHeight - window.innerHeight;
        if (total <= 0) { target = 1; return; }
        var top = scrub.getBoundingClientRect().top;
        target = Math.min(1, Math.max(0, -top / total));
      }
      function apply() {
        /* spring: aproxima cur de target (suaviza o salto do scroll) */
        cur += (target - cur) * 0.06;
        if (Math.abs(target - cur) < 0.0005) cur = target;
        if (pipe) pipe.style.width = (cur * 100).toFixed(2) + "%";
        if (vpipe) vpipe.style.height = (cur * 100).toFixed(2) + "%";
        if (window.__aapsonScrubProg) window.__aapsonScrubProg(cur);
        var idx = Math.min(STAGES.length - 1, Math.floor(cur * STAGES.length));
        if (idx !== lastIdx) {
          /* fade out/in no label ao trocar de etapa */
          if (label) {
            label.style.opacity = "0";
            label.style.transform = "translateY(6px)";
            setTimeout(function () {
              label.firstChild.nodeValue = STAGES[idx];
              label.style.opacity = "1";
              label.style.transform = "none";
            }, 140);
          }
          nodes.forEach(function (n) {
            var at = parseFloat(n.getAttribute("data-at"));
            var on = at >= 1 ? (idx >= STAGES.length - 1) : (cur >= at - 0.001);
            n.classList.toggle("on", on);
          });
          vnodes.forEach(function (n) {
            var at = parseFloat(n.getAttribute("data-vat"));
            var i = Math.round(at * (STAGES.length - 1));
            n.classList.toggle("on", i === idx);   /* so o atual aberto */
          });
          vlabels.forEach(function (n, i) {
            n.classList.toggle("on", i === idx);
          });
          lastIdx = idx;
        }
        if (cur !== target) { raf2 = requestAnimationFrame(apply); }
        else { raf2 = null; }
      }
      function kick() {
        computeTarget();
        if (!raf2) raf2 = requestAnimationFrame(apply);
      }
      window.addEventListener("scroll", kick, { passive: true });
      window.addEventListener("resize", kick);
      window.addEventListener("load", kick);
      kick();
    }
  }

  /* ============================================================
     4) PARALLAX do fundo Nano Banana (hub) — --py conforme scroll
     ============================================================ */
  var hero = document.querySelector(".hub-hero");
  if (hero && !reduce) {
    var py = 0, pyt = 0, raf3 = null;
    function computePy() {
      var r = hero.getBoundingClientRect();
      var prog = Math.min(1, Math.max(0, -r.top / (r.height || 1)));
      pyt = prog * 60; /* desloca até 60px p/ baixo */
    }
    function tick() {
      py += (pyt - py) * 0.1;
      if (Math.abs(pyt - py) < 0.1) py = pyt;
      hero.style.setProperty("--py", py.toFixed(2) + "px");
      if (py !== pyt) raf3 = requestAnimationFrame(tick); else raf3 = null;
    }
    function kickPy() { computePy(); if (!raf3) raf3 = requestAnimationFrame(tick); }
    window.addEventListener("scroll", kickPy, { passive: true });
    window.addEventListener("resize", kickPy);
    kickPy();
  }

  /* ============================================================
     4b) COLLAPSE DA MARCA NO SCROLL (estilo Anthropic)
         no topo: marca completa (logo + wordmark) | ao descer: só o logo
     ============================================================ */
  var navEl = document.querySelector("nav");
  if (navEl) {
    var navScrolled = false;
    function navUpdate() {
      var next = window.scrollY > 60;
      if (next !== navScrolled) {
        navScrolled = next;
        navEl.classList.toggle("scrolled", next);
      }
    }
    var navTicking = false;
    window.addEventListener("scroll", function () {
      if (!navTicking) {
        navTicking = true;
        requestAnimationFrame(function () { navUpdate(); navTicking = false; });
      }
    }, { passive: true });
    window.addEventListener("resize", navUpdate);
    window.addEventListener("load", navUpdate);
    navUpdate();
  }

  /* ============================================================
     5) STATUS BAR global — sessão (tempo real) + heartbeat pings
     ============================================================ */
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
  if (sessEl) { setInterval(function () { sessEl.textContent = fmt(Date.now() - t0); }, 1000); }
  if (pingEl && !reduce) {
    var pings = 0;
    setInterval(function () { pings++; pingEl.textContent = pings; }, 3000);
  }

  /* ============================================================
     6) PARALLAX DE CURSOR COM SPRING (técnica do vídeo XEIMIfJb5d0)
        floaters seguem o cursor (spring lerp); um contra-move na
        direção oposta e mais devagar (estilo "lata" do vídeo).
        Só em ponteiro fino; respeita prefers-reduced-motion.
     ============================================================ */
  var fx = document.querySelectorAll(".hub-hero .hero-fx, .scrub .hero-fx");
  var scrubProg = 0; /* 0..1 progresso do .scrub (hero pme) — alimenta drift no scroll */
  if (fx.length && !reduce && window.matchMedia("(pointer:fine)").matches) {
    var items = [];
    fx.forEach(function (el) {
      items.push({
        el: el,
        depth: parseFloat(el.getAttribute("data-depth")) || 0.03,
        dir: parseFloat(el.getAttribute("data-dir")) || 1,
        scroll: el.getAttribute("data-scroll") === "1",
        cx: 0, cy: 0, tx: 0, ty: 0,   /* cursor (spring) */
        sx: 0, sy: 0                    /* scroll drift */
      });
    });
    var rafFx = null;
    function onMove(e) {
      var nx = (e.clientX / window.innerWidth) - 0.5;  /* -0.5..0.5 */
      var ny = (e.clientY / window.innerHeight) - 0.5;
      items.forEach(function (t) {
        t.tx = nx * t.dir * t.depth * 220;  /* px */
        t.ty = ny * t.dir * t.depth * 220;
      });
      if (!rafFx) rafFx = requestAnimationFrame(tickFx);
    }
    function tickFx() {
      var moving = false;
      items.forEach(function (t) {
        t.cx += (t.tx - t.cx) * 0.08;  /* spring cursor */
        t.cy += (t.ty - t.cy) * 0.08;
        if (t.scroll) { t.sx = scrubProg * t.dir * 40; t.sy = -scrubProg * t.dir * 30; }
        if (Math.abs(t.tx - t.cx) > 0.05 || Math.abs(t.ty - t.cy) > 0.05 ||
            (t.scroll && (Math.abs(t.sx) > 0.05 || Math.abs(t.sy) > 0.05))) moving = true;
        var x = (t.cx + t.sx), y = (t.cy + t.sy);
        t.el.style.transform = "translate3d(" + x.toFixed(2) + "px," + y.toFixed(2) + "px,0)";
      });
      rafFx = moving ? requestAnimationFrame(tickFx) : null;
    }
    window.addEventListener("mousemove", onMove, { passive: true });
    /* expõe o progresso do scrub p/ o drift no scroll (hero pme) */
    window.__aapsonScrubProg = function (p) { scrubProg = p; if (!rafFx) rafFx = requestAnimationFrame(tickFx); };
  }

  /* ============================================================
     7) SCROLL-PROGRESS fina no topo (IDEIA 7)
        respeita prefers-reduced-motion (sem transição, mas mantém o traço)
     ============================================================ */
  var bar = document.querySelector(".scroll-progress");
  if (bar) {
    var progTicking = false;
    function progUpdate() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var p = h > 0 ? (window.scrollY / h) * 100 : 0;
      bar.style.width = Math.min(100, Math.max(0, p)).toFixed(2) + "%";
      progTicking = false;
    }
    window.addEventListener("scroll", function () {
      if (!progTicking) { progTicking = true; requestAnimationFrame(progUpdate); }
    }, { passive: true });
    window.addEventListener("resize", progUpdate);
    window.addEventListener("load", progUpdate);
    progUpdate();
  }
})();
