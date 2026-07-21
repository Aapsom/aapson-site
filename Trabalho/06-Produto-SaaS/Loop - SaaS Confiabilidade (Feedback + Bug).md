---
tags: [loop, saas, feedback, bug, produto]
video_origem: "[[Referencia - Loop Engineering (5p_BBdfvzgQ)]]"
data: 2026-07-21
status: esqueleto de loop agentic (FASE 4 — respeitar decisão 11: MVP ZERO IA)
---

# Loop — SaaS Confiabilidade (Product Feedback + Bug)

> Instanciado do `references/loop-template.md` (Loop Engineering, 5p_BBdfvzgQ).
> ⚠️ IMPORTANTE: o SaaS tem **MVP ZERO IA determinístico** (decisão 11 da spec).
> Este loop agentic é **Fase 4** — NÃO injetar no MVP. Documentado aqui para adoção pós-Mom Test.

## Product Feedback loop (crescimento)
- **KPI:** retenção de cobrança (clientes que recuperaram débito e seguem ativos), DAU/MAU do painel.
- **Dados:** analytics do produto (eventos de retry/recuperação) + feedback de clientes.
- **Ação:** priorizar fix de UX onde a retenção cai → prototipar → medir de novo.
- **STOP:** retenção estabilizada no alvo OU sem ganho após N rodadas.
- **Memória:** `loop_feedback_memory.md`.

## Bug loop (uptime)
- **KPI:** uptime do retry-runner / webhook Pix.
- **Dados:** Sentry-style (logs de falha do Edge Function `retry-runner`).
- **Ação:** auto-corrigir gatilho de falha com stop condition (uptime alvo).
- **STOP:** uptime ≥ SLA.
- **Memória:** `loop_bug_memory.md`.

## Motor
`hermes cron` (execução esparsa) + `memory` (relê memória a cada run). Modelo barato (GLM 5.2 NIM) p/ iteração.
