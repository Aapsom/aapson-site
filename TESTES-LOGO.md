# Testes de Logo AAPSON — histórico (não apagar)

**Data:** 2026-07-14
**Decisão final:** a *logo atual* (mark "Á": triângulo topo + chevron base + círculo) é a **oficial**, apenas recolorida pro duotone aprovado. Não entra símbolo novo na final.
**Regra dos A's (dura, vale pra sempre):** cada A da wordmark AAPSON recebe a cor de 1 triângulo do símbolo →
- A1 (1º A) = cor do triângulo do topo = `a2` (chartreuse `#D9F03A` no dark / teal `#1B6E7A` no light)
- A2 (2º A) = cor do triângulo da base = `a1` (violeta `#A78BFA` no dark / vinho `#B4472B` no light)
- demais letras (P, S, O, N) = foreground (`--fg`)
- círculo central = `a3` terra `#C8743C` (mesmo nos dois tons)

## Arquivos de teste nesta pasta
| Arquivo | Conteúdo | Status |
|---|---|---|
| `test-logos.html` / `.png` | 1ª leva — 12 concepts focados no duplo-AA | **rejeitada**: "muito parecidas, todas focadas nos AA" |
| `test-logos-v2.html` / `.png` | 2ª leva — 13 concepts (A duplo-A / B abstrato / C esconde-A / D wordmark + ATUAL recolorida) | verificado por vision: **bons = ATUAL, 09, 11** · **fracos = 01,02,03,04,05,06,07,08** |
| `test-duotone.html` / `.png` | paleta duotone aprovada (Dark 10 Ultraviolet + Light 04 Editorial Cream) | **aprovada** |
| `test-palettes.html` / `.png` | 10 paletas candidatas | arquivado |
| `test-hero.html` / `.png` | matriz tipografia × cor | arquivado |
| `MOODBOARD.md` | moodboard consolidado (refs: NOUS / Stripe / Apple / Anthropic / Resend) | vivo |

## Próximos passos (pós-decisão)
1. Lock duotone em `assets/acid.css` (`:root` = dark10, `@media (prefers-color-scheme: light)` = light04) — **liberado** (antes adiado p/ validar logo).
2. Logo oficial como assets (`logo-mark-dark.svg` / `logo-mark-light.svg`) + wordmark com A's coloridos no header de `index/pme/mentoria/fscd` + favicon + og-image.
3. Mark reativo ao scroll (estilo Anthropic, aprovado) em `assets/main.js`.
4. Fundo Nano Banana (Phase A, opacity ~0.12) no hero.
5. Validação visual final (render + vision).
