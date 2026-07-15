/* AAPSON — toggle de tema (segue o sistema por padrão, botão sobrescreve)
   Sem dependências. Carregue no <head> (sem defer) para evitar flash de cor. */
(function () {
  "use strict";
  var STORE = "aapson-theme"; // "light" | "dark" | ausente = segue o sistema

  var SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.5M12 19.5V22M4.2 4.2l1.8 1.8M18 18l1.8 1.8M2 12h2.5M19.5 12H22M4.2 19.8l1.8-1.8M18 6l1.8-1.8"/></svg>';
  var MOON = '<svg viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';

  function systemPref() {
    return (window.matchMedia && matchMedia("(prefers-color-scheme:light)").matches) ? "light" : "dark";
  }
  function forced() {
    try { return localStorage.getItem(STORE); } catch (e) { return null; }
  }
  function resolved() {
    return forced() || systemPref();
  }
  function applyTheme() {
    var f = forced();
    if (f === "light" || f === "dark") {
      document.documentElement.setAttribute("data-theme", f);
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
  }
  function save(next) {
    try { localStorage.setItem(STORE, next); } catch (e) {}
  }

  // Aplica ANTES do primeiro paint (script roda no <head>, sem defer).
  applyTheme();

  function buildButton() {
    if (document.querySelector(".theme-toggle")) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "theme-toggle";

    function paint() {
      var t = resolved();
      btn.innerHTML = (t === "light") ? MOON : SUN;
      btn.setAttribute("aria-label",
        (t === "light") ? "Mudar para tema escuro" : "Mudar para tema claro");
      btn.setAttribute("title",
        (t === "light") ? "Tema claro — clica para escuro" : "Tema escuro — clica para claro");
      btn.setAttribute("aria-pressed", (t === "light") ? "true" : "false");
    }
    paint();

    btn.addEventListener("click", function () {
      var next = (resolved() === "light") ? "dark" : "light";
      save(next);
      applyTheme();
      paint();
    });

    // Se o sistema mudar e o usuário não escolheu manualmente, acompanha.
    if (window.matchMedia) {
      var mq = matchMedia("(prefers-color-scheme:light)");
      var onChange = function () { if (!forced()) { applyTheme(); paint(); } };
      if (mq.addEventListener) mq.addEventListener("change", onChange);
      else if (mq.addListener) mq.addListener(onChange);
    }

    (document.body || document.documentElement).appendChild(btn);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", buildButton);
  } else {
    buildButton();
  }
})();
