# MOODBOARD · Redesign AAPSON (PME / FS-CD / Mentoria)

/* Hallmark · macrostructure: Index-First (moodboard) · brief: técnico-editorial QUENTE + vibe research */
/* Fonte de verdade de marca: Acid Circuit. Não copiar pixel — extrair DNA. Textos do site serão reescritos depois. */

## TESE (fechada com o user)
"Técnico-editorial quente" + vibe **research**. Público = PME (pilates, psico, música, cursos)
— precisa de premium contido, não terminal cru. Interseção alvo:
**estrutura editorial-técnica (Nous/Anthropic/Resend) + energia Acid Circuit (lime/pink/blue)
+ "máquina operando" já presente na status bar.** Paleta: USER ABRIU — admite 1 cor de apoio fria.

## Paleta em discussão (user abriu a cor)
Base atual (manter como fundo): `--bg:#0B0B0F` · `--surface:#121218`.
Quentes (marca): `--lime:#B2F120` · `--pink:#FE2266` · `--blue:#484AF0`.
Apoio frio PROPOSTO (do DNA do Nous/Anthropic): `--petrol:#0E6E8C` ou `--ink-blue:#1B3A4B`
— usado SÓ como linha/divisor/acento secundário, nunca como cor principal.
→ decidir no final do moodboard.

=====================================================================
## ÂNCORAS DO USER (analisadas)
=====================================================================

### 1. Nous Research — https://nousresearch.com  [VERIFICADO: screenshot+vision real]
- DNA: Brutalist Technical / Academic. Branco + azul-petróleo; CORPO em MONOSPACE;
  grid de "record blocks" 3-col (img/texto/metadados); SEEDs espalhados; linhas tracejadas;
  cantos vivos; sem hero de venda.
- Borrow: índice/record como esqueleto alt.; mono como acento; metadados (seed/output) como
  decoração de máquina; cantos vivos; restrição de paleta.
- Avoid: frieza total pro PME; duotone azul (nossa paleta é Acid Circuit).
- Fit: 4/5.

### 2. Stripe — https://stripe.com  [VERIFICADO: snapshot estrutural + domínio]
- DNA: fintech authority. Hero dark com gradiente sutil (navy→preto) e brilho; tipografia
  grotesca (Sohne/Inter-like) com hierarquia forte; métricas GRANDES como prova ($1.9T, 99.999%);
  dashboards reais como mock no hero; cantos arredondados suaves (radius ~8-12px); motion refinado.
- Borrow: confiança técnica + calor; "métrica como hero"; precisão sem ser fria; grau de cantos
  (nosso site hoje usa cantos vivos — Stripe sugere escalar pra 8-12px em cards).
- Avoid: virou template (Hallmark gate 8 — não vira color-swap de Stripe); gradiente roxo deles.
- Fit: 4.5/5 — fintech que o PME respeita.

### 3. Apple — https://www.apple.com  [VERIFICADO: snapshot estrutural + domínio]
- DNA: premium por RESTRIÇÃO. Fundo branco/quase-branco; SF Pro (grotesca nua); hero POR PRODUTO
  (um produto = uma tela cheia, tipo grande); espaço negativo enorme; imagem de produto flutuando
  com sombra suave; scroll "encena" o produto.
- Borrow: disciplina de ESPAÇO (respiro); um foco por seção; objetos flutuando com sombra;
  "encenação no scroll" (parallax/scroll-driven — já temos scrub, alinha).
- Avoid: fundo branco (nosso é dark — manter dark, pegar o RESPIRO não o branco); fotos de produto
  físico (não temos produto físico).
- Fit: 4/5 — o "feel premium por restrição" é o pulo do gato.

### 4. Anthropic — https://www.anthropic.com  [VERIFICADO: snapshot + domínio]
- DNA: research sério porém quente. Fundo off-white/creme; accent terra/ochre (#D97757-ish) +
  espinha de peixe (herringbone) como marca; tipografia editorial (serifada de display + grotesca);
  SEÇÕES de "releases" em lista com DATE/CATEGORY (metadados como estrutura).
- ANIMAÇÃO DA LOGO (pedido do user): a marca no canto sup-esq é o "burst" de espinha de peixe que
  REAGE AO SCROLL — conforme rola, os feixes se expandem/retraem (scroll-linked transform).
  Implementável via `scroll-driven animation` (animation-timeline: scroll()) ou JS scroll listener.
- Borrow: (a) logo reativa ao scroll = assinatura de marca viva; (b) metadados DATE/CATEGORY como
  estrutura de lista; (c) calor sem ser "friendly" (terra/ochre, não pastel).
- Avoid: fundo creme (nosso é dark); cor terra como primária (usar como acento só).
- Fit: 5/5 — research + calor + animação de marca é EXATAMENTE o brief.

### 5. Resend — https://resend.com  [VERIFICADO: snapshot + domínio]
- DNA: técnico-porém-amigável. Fundo claro; accent índigo; CORPO/headings em MONO (JetBrains/Similar);
  "código como decoração" (blocos de código/terminal no hero); restrição; limpo.
- Borrow: acento mono; "código/terminal como identidade"; restrição que não afuga leigo.
- Avoid: fundo claro (manter dark); mono como TUDO (usar mono só como acento/tag, não corpo todo).
- Fit: 3.5/5 — tempero, não prato principal.

=====================================================================
## SÍNTESE → DIREÇÃO AAPSON
=====================================================================
Esqueleto (macroestrutura): manter **Split Studio (15)** já no acid.css, MAS injetar
atitude de ÍNDICE/RECORD do Nous+Anthropic em seções de "prova" (ex: lista de releases/casos
com DATE/CATEGORY/SEED-like metadata). Quebra o SaaS template sem perder o editorial.

Tipografia: manter Space Grotesk (display) + JetBrains Mono (tags/metadata). ADICIONAR:
- uma serifada editorial de DISPLAY pro hero (ex: "Newsreader" ou "Fraunces") — dá o calor
  "técnico-editorial" da Anthropic. [NOVO — precisa de teste]
- Mono SÓ para metadados (DATE/CATEGORY/SEED/OUTPUT), nunca corpo.

Cor: fundo #0B0B0F + Acid Circuit (lime/pink/blue). ADICIONAR 1 apoio frio (petrol/ink-blue)
OU calor (terra/ochre do Anthropic) como acento de seção. USER DECIDE.

Motion (a grande novidade):
- (a) LOGO REATIVA AO SCROLL estilo Anthropic: o mark duplo-A "respira"/expande feixes no scroll.
  Usa scroll-driven animation (CSS) com fallback JS. Respeita prefers-reduced-motion.
- (b) Fundo Nano Banana sutil (Fase A) + canvas p5.js (Fase B) + vídeo no hero (Fase C).
- (c) Encenação no scroll estilo Apple (já temos scrub — reforçar).

Anti-refs (slop — Hallmark gate 8): Recurly, Chargebee, Paddle, Hotmart (hero→3cards→CTA→footer).
Nosso Split Studio + índice já foge; manter.

=====================================================================
## PENDENTE (decisões do user)
=====================================================================
- [ ] Cor de apoio: petrol/ink-blue (frio, research) OU terra/ochre (quente, Anthropic)? OU nenhuma?
- [ ] Serifada editorial de hero? (Newsreader/Fraunces) — sim/não/qual
- [ ] Logo reativa ao scroll (Anthropic-style): aprova implementar no mark duplo-A?
- [ ] Prioridade de implementação: Fase A (fundo) → B (canvas) → C (vídeo) ainda vale?
- [ ] Quais seções do pme.html viram "índice/record" (DATE/CATEGORY) vs Split Studio?
