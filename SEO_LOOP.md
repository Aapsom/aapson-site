---
tags: [loop, seo, aapson-site, real, gsc-gate]
video_origem: "[[Referencia - Loop Engineering (5p_BBdfvzgQ)]]"
data: 2026-07-21
status: loop REAL instanciado p/ aapson-site (GitHub Pages)
repo: "C:/Users/kauea/dev/aapson-site"
public_url: "https://aapsom.github.io/aapson-site/"
---

# Loop — SEO do Site AAPSON (instanciado, REAL)

> 1º loop real do `references/loop-template.md` (Loop Engineering, 5p_BBdfvzgQ).
> Motor sugerido: `hermes cron` mensal + `memory` (relê `seo_loop_memory.md`).

## Estado atual do site (auditado 21/jul, ground truth)
- ✅ HTML estático GitHub Pages, já com `<title>`, `meta description`, `canonical`, OpenGraph em `index.html`/`fscd.html`/`mentoria.html`/`pme.html`.
- ✅ Pasta `nicho-fscd/` com 18 artigos FS-CD (conteúdo real, autoridade).
- ❌ **FALTAM** (quick wins do vídeo) — BASELINE do `seo_audit.py` (21/jul, exit 0):
  - `sitemap.xml` (FALTA)
  - `robots.txt` (FALTA)
  - **JSON-LD** (`application/ld+json`) — 0/30 páginas (FALTA)
  - Interlink entre os 18 artigos `nicho-fscd/` — 18/18 isolados (FALTA)
  - 9 páginas sem meta description/title (maioria test/mockup: bg-mockup, scroll-world-test, test-duotone, test-hero, test-logos, test-logos-v2, test-palettes)
  - GSC conectado (GATE 👤)
- 🔧 **Automatizado:** `seo_audit.py` (offline, idempotente) roda a auditoria sem GSC e grava `seo_audit_last.txt`. Veredito: "4 categoria(s) de quick-win pendente(s)".

## O que o loop faz (cada rodada mensal)
1. **Ler memória** (`seo_loop_memory.md`): mudanças anteriores + posição GSC.
2. **Auditar offline** (`seo_audit.py`): checa sitemap/robots/JSON-LD/interlink nos .html reais.
3. **Conectar GSC** (GATE 👤: credencial do CEO via `gcloud`/OAuth) → ler posição para termos-alvo.
4. **Aplicar 1 melhoria**: ex. adicionar JSON-LD Org/Article, criar sitemap.xml, interlinkar artigos.
5. **KPI objetivo**: posição no Google para termos-alvo (ex.: "consultoria FS-CD", "cobrança Pix PME", "mentoria IA SAP").
6. **STOP CONDITION**: topo da 1ª página OU plateau após N rodadas.
7. **Reverter** se piorou.
8. **Ping** (Telegram) + **GATE 👤**: aprovação antes de aplicar em produção (push pro GitHub Pages).

## Termos-alvo sugeridos (KPI)
- "consultoria FS-CD S/4HANA"
- "cobrança recorrente Pix PME"
- "mentoria IA consultor SAP"
- "saneamento dados FS-CD"

## GATE 👤 (não autônomo)
- Credencial Google Search Console (owner do `aapsom.github.io`).
- Aprovação do push pro GitHub Pages.
- `setx` de qualquer token (NUNCA no vault).

## Custo
<$5/run (GLM 5.2 NIM barato p/ gerar JSON-LD/sitemap). Execução esparsa.
