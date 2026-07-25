/* ============================================================
   AAPSON · motor "marca binária"
   Rasteriza a marca OFICIAL (viewBox 0 0 100 124 — mesmos polígonos
   do acid.css / index.html) num grid de caracteres e deixa os
   binários se organizarem até virar a logo.

   Fonte de verdade da geometria: assets/logo + index.html.
   NÃO redesenhar o símbolo aqui — só rasterizar o que já existe.

   Uso:  MarcaBinaria(canvas, { modo, alturaMarca, densidade })
   modos: 'monta' | 'dissolve' | 'corrente' | 'decodifica' | 'respira'
   ============================================================ */
(function (global) {
  'use strict';

  var MARK_W = 100, MARK_H = 124;
  var TOP  = [[50,2],[91,56],[73,56],[50,25],[27,56],[9,56]];
  var BASE = [[9,68],[27,68],[50,99],[73,68],[91,68],[50,122]];
  var NODE = { cx: 50, cy: 62, r: 9 };

  // 1 = triângulo topo (a2 chartreuse) · 2 = base (a1 violeta) · 3 = nó (a3 terra)
  var CAMADA = { 1: '--a2', 2: '--a1', 3: '--a3' };

  var RM = global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function tokens(el) {
    var cs = getComputedStyle(el);
    var t = {};
    for (var k in CAMADA) t[k] = cs.getPropertyValue(CAMADA[k]).trim() || '#fff';
    t.fraco = cs.getPropertyValue('--bin-fraco').trim() || 'rgba(239,233,255,.13)';
    return t;
  }

  /* Rasteriza a marca num box de `cols` x `rows` células.
     Retorna Uint8Array (0 vazio, 1 topo, 2 base, 3 nó). */
  function mascara(cols, rows) {
    var c = document.createElement('canvas');
    c.width = cols; c.height = rows;
    var x = c.getContext('2d', { willReadFrequently: true });
    var sx = cols / MARK_W, sy = rows / MARK_H;

    function poly(pts, cor) {
      x.beginPath();
      x.moveTo(pts[0][0] * sx, pts[0][1] * sy);
      for (var i = 1; i < pts.length; i++) x.lineTo(pts[i][0] * sx, pts[i][1] * sy);
      x.closePath(); x.fillStyle = cor; x.fill();
    }
    poly(TOP,  '#ff0000');   // canal R = camada 1
    poly(BASE, '#00ff00');   // canal G = camada 2
    x.beginPath();
    x.ellipse(NODE.cx * sx, NODE.cy * sy, NODE.r * sx, NODE.r * sy, 0, 0, Math.PI * 2);
    x.fillStyle = '#0000ff'; x.fill();                       // canal B = camada 3

    var d = x.getImageData(0, 0, cols, rows).data;
    var m = new Uint8Array(cols * rows);
    for (var i = 0; i < cols * rows; i++) {
      var r = d[i * 4], g = d[i * 4 + 1], b = d[i * 4 + 2];
      m[i] = b > 90 ? 3 : (r > 90 ? 1 : (g > 90 ? 2 : 0));
    }
    return m;
  }

  function MarcaBinaria(canvas, opt) {
    opt = opt || {};
    var modo = opt.modo || 'monta';
    var fracaoAltura = opt.alturaMarca || 0.72;   // altura da marca vs altura do canvas
    var corpo = opt.densidade || 13;              // px por linha de caractere

    var ctx = canvas.getContext('2d');
    var cellH, cellW, cols, rows, celulas, dpr, larg, alt;
    var t0 = performance.now(), progressoScroll = 0, raf = null;

    // --- intro: maior atraso (0.85 pontas→centro + 0.3 do nó + 0.12 jitter)
    // somado à viagem de cada dígito. ~2,4s: longo o bastante para ler como
    // nascimento, curto o bastante para não virar pedágio antes do conteúdo.
    var intro = !!opt.intro;
    var VIAGEM = 1.35;
    var FIM_INTRO = 0.85 + 0.3 + 0.12 + VIAGEM;
    var introPulado = false, introEntregue = false;

    function medir() {
      dpr = Math.min(global.devicePixelRatio || 1, 2);
      var r = canvas.getBoundingClientRect();
      larg = Math.max(320, r.width); alt = Math.max(240, r.height);
      canvas.width = larg * dpr; canvas.height = alt * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      cellH = corpo;
      cellW = corpo * 0.6;
      ctx.font = (corpo * 0.82) + 'px "JetBrains Mono", ui-monospace, monospace';
      cellW = ctx.measureText('0').width || cellW;

      cols = Math.ceil(larg / cellW);
      rows = Math.ceil(alt / cellH);

      // caixa da marca, preservando o aspecto 100:124 em px reais
      var hPx = alt * fracaoAltura;
      var mRows = Math.max(6, Math.round(hPx / cellH));
      var mCols = Math.max(6, Math.round((hPx * (MARK_W / MARK_H)) / cellW));
      var m = mascara(mCols, mRows);

      // deslocX move a marca lateralmente (fração da largura). Necessário quando o
      // hero divide o palco com texto: halo de texto não salva sobreposição total.
      var offC = Math.floor((cols - mCols) / 2 + (opt.deslocX || 0) * cols);
      var offR = Math.floor((rows - mRows) / 2);

      celulas = new Array(cols * rows);
      for (var y = 0; y < rows; y++) {
        for (var xx = 0; xx < cols; xx++) {
          var camada = 0;
          var my = y - offR, mx = xx - offC;
          if (my >= 0 && my < mRows && mx >= 0 && mx < mCols) camada = m[my * mCols + mx];
          // atraso radial: a marca se resolve do nó central pra fora
          var dx = (xx - cols / 2) * cellW, dy = (y - rows / 2) * cellH;
          var dist = Math.sqrt(dx * dx + dy * dy) / Math.sqrt(larg * larg + alt * alt);
          // --- INTRO: cada dígito da marca nasce fora da tela e viaja até o lugar.
          // Entra pelo lado MAIS PRÓXIMO (não implode do centro): lê como fluxo de
          // dado chegando, não como explosão genérica.
          var alvoX = xx * cellW, alvoY = y * cellH;
          var lado = alvoX < larg / 2 ? -1 : 1;
          // atraso: as pontas assentam primeiro, o centro por último — assim o nó
          // (que é o miolo da marca) é a ÚLTIMA coisa a acender.
          var dIntro = 0.85 * (1 - Math.min(1, dist * 2.1)) + (camada === 3 ? 0.3 : 0);

          celulas[xx + y * cols] = {
            c: camada,
            bit: Math.random() < 0.5 ? '0' : '1',
            ruido: Math.random() < 0.17,   // só ~1 em 6 células do entorno acende
            atraso: dist,
            fase: Math.random() * Math.PI * 2,
            troca: 0.02 + Math.random() * 0.06,
            // Distância curta DE PROPÓSITO: com origem a ~1,5× a largura o dígito
            // passava a viagem inteira fora do canvas e o voo não existia na tela.
            ox: lado * larg * (0.10 + Math.random() * 0.26),
            oy: (Math.random() - 0.5) * 120,
            aIntro: dIntro + Math.random() * 0.12
          };
        }
      }
    }

    function desenhar(agora) {
      var T = tokens(canvas);
      var t = (agora - t0) / 1000;
      ctx.clearRect(0, 0, larg, alt);
      ctx.textBaseline = 'top';
      ctx.font = (corpo * 0.82) + 'px "JetBrains Mono", ui-monospace, monospace';

      // ---- INTRO (ato de nascimento da marca) --------------------------------
      // 3 atos: (1) os dígitos chegam voando dos lados e assentam nas pontas,
      // (2) o corpo fecha de fora para dentro, (3) o nó terra acende por último.
      // Só depois disso o campo entra no modo vivo ('corrente') e o texto surge.
      var emIntro = intro && !RM && !introPulado && t < FIM_INTRO;
      if (intro && !introEntregue && (!emIntro || RM)) {
        introEntregue = true;
        if (typeof opt.aoTerminar === 'function') opt.aoTerminar();
      }

      for (var i = 0; i < celulas.length; i++) {
        var cel = celulas[i];
        var col = i % cols, lin = (i / cols) | 0;
        var dx = 0, dy = 0, qIntro = 1;

        if (emIntro) {
          qIntro = clamp((t - cel.aIntro) / VIAGEM);
          // Ease mais suave que cubic: com cubic o dígito cobria 80% da distância
          // no primeiro terço do tempo e a viagem ficava invisível.
          var e = 1 - Math.pow(1 - qIntro, 2.2);
          dx = cel.ox * (1 - e);
          dy = cel.oy * (1 - e);
        }

        // quanto esta célula já "resolveu" (0 = ruído, 1 = marca formada)
        var p;
        if (RM) p = 1;
        else if (emIntro) p = qIntro;
        else if (modo === 'dissolve')    p = 1 - clamp((progressoScroll - cel.atraso * 0.5) * 1.8);
        else if (modo === 'corrente')    p = clamp((t * 0.5 + Math.sin(t * 0.7 + col * 0.18) * 0.35) - cel.atraso * 0.4);
        else if (modo === 'respira')     p = 0.55 + 0.45 * Math.sin(t * 0.55 - cel.atraso * 3.2);
        else if (modo === 'decodifica')  p = clamp((t - 0.25 - col / cols * 1.1) * 1.6);
        else                             p = clamp((t - cel.atraso * 2.1) * 0.85);   // 'monta'

        // o bit troca rápido enquanto não resolveu, e congela quando resolve
        if (!RM && Math.random() < cel.troca * (1.15 - p)) cel.bit = cel.bit === '0' ? '1' : '0';

        var dentro = cel.c > 0;
        var alfa, cor;
        if (dentro) {
          // A opacidade sobe MUITO antes da posição chegar — senão o dígito só
          // fica visível já em cima do alvo e ninguém vê o voo (medido: 98% já
          // dentro da caixa aos 900ms, viagem invisível).
          alfa = emIntro ? clamp(qIntro * 3.4) : (0.22 + 0.78 * p);
          cor = T[cel.c];
        } else {
          // Fundo ESPARSO. A referência (AINO) deixa o entorno quase vazio — só a
          // forma tem densidade. Ruído em toda célula vira a poluição que o dono vetou.
          if (!cel.ruido) continue;
          alfa = (0.5 - 0.44 * p) * (0.4 + 0.28 * Math.sin(t * 1.1 + cel.fase));
          // durante a intro o entorno fica calado: o palco é só da marca nascendo
          if (emIntro) alfa *= clamp((t - FIM_INTRO + 0.9) / 0.9);
          cor = T.fraco;
        }
        if (alfa <= 0.012) continue;

        ctx.globalAlpha = Math.min(1, Math.max(0, alfa));
        ctx.fillStyle = cor;
        // o nó central é o ponto focal da marca — só ele ganha brilho.
        // Na chegada leva um estouro curto de brilho (a "ignição" do ato 3).
        if (cel.c === 3) {
          ctx.shadowColor = cor;
          ctx.shadowBlur = emIntro ? 26 * Math.pow(qIntro, 6) : 9 * p;
        }
        ctx.fillText(cel.bit, col * cellW + dx, lin * cellH + dy);
        if (cel.c === 3) ctx.shadowBlur = 0;
      }
      ctx.globalAlpha = 1;
    }

    function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }

    function laco(agora) {
      desenhar(agora);
      if (RM) return;                      // um quadro só: estado final
      raf = requestAnimationFrame(laco);
    }

    var api = {
      // quem rolar ou clicar não deve esperar a intro terminar
      pularIntro: function () { introPulado = true; },
      scroll: function (p) { progressoScroll = p; },
      remedir: function () { medir(); },
      parar: function () { if (raf) cancelAnimationFrame(raf); raf = null; }
    };

    medir();
    laco(performance.now());

    var tmr;
    global.addEventListener('resize', function () {
      clearTimeout(tmr);
      tmr = setTimeout(function () { medir(); if (RM) desenhar(performance.now()); }, 180);
    });

    return api;
  }

  MarcaBinaria.reducedMotion = RM;
  global.MarcaBinaria = MarcaBinaria;
})(window);
