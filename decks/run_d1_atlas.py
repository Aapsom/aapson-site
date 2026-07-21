#!/usr/bin/env python3
# ATLAS PO - Semana 1, Dia 1 (8h autônomo). Gera evidência em disco; para em GATE 👤.
import os, sys, datetime, textwrap

VAULT = r"C:\Users\kauea\OneDrive\Documentos\AAPSOM.MD\OBSIDIAN\AAPSOM.MD\Trabalho"
DECKS = r"C:\Users\kauea\dev\aapson-site\decks"
LOG = os.path.join(VAULT, "06-Produto-SaaS", "Log - PO ATLAS Autonomo D1 2026-07-18.md")
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

# ---------- BLOCO A (2h): re-verificar decks ----------
log(f"# Log — PO ATLAS Autônomo | D1 | {now}")
log("\n## BLOCO A — Re-verificação dos decks (sem toque visual)")
checks = []
for name in ["deck-atlas-pme.html", "deck-atlas-wl.html"]:
    p = os.path.join(DECKS, name)
    t = open(p, encoding="utf-8").read()
    violeta = t.count("#A78BFA"); terra = t.count("#C8743C"); chart = t.count("#D9F03A")
    verde = t.count("#2DD4BF"); lime = t.count("#C6FF00")
    brand = t.count("brandmark"); powered = t.lower().count("powered by")
    cod = 1 if ("emerald sentry" in t.lower() or "acid circuit" in t.lower()) else 0
    ok = (violeta==0 and terra==0 and chart==0 and verde>0 and lime>0 and brand>0 and powered>0 and cod==0)
    checks.append((name, ok, f"violeta={violeta} terra={terra} chart={chart} verde={verde} lime={lime} brand={brand} powered={powered} codinome={cod}"))
    log(f"  [{'OK' if ok else 'FAIL'}] {name}: {checks[-1][2]}")
log("  >> Decks mantêm Emerald Sentry + brandmark + powered by. Sem rótulo de codinome.")

# ---------- BLOCO B (2h): One-Pager ATLAS interno (Emerald Sentry) ----------
log("\n## BLOCO B — One-Pager ATLAS (interno, Emerald Sentry)")
onepager = f"""---
tipo: one-pager
titulo: "ATLAS — One-Pager Interno (PO)"
frente: "ATLAS (powered by AAPSON)"
tags: [atlas, one-pager, interno, emerald-sentry]
data: {now}
status: interno-sem-pii
identidade: "Emerald Sentry (verde #2DD4BF / lime #C6FF00)"
relacionado: "[[ATLAS - Spec do Produto (PO)]] · [[Aristoteles - One-Pager Interno]]"
---

# ATLAS — One-Pager Interno

**O que é:** marca de produto AAPSON para PME. Duas frentes:
- **ATLAS PME** — SaaS de Confiabilidade de Cobrança (Pix Automático + recorrência + retry + WhatsApp). Preços: Entry R$147 · Core R$347 · Scale R$797/mês.
- **ATLAS White-label (Aristóteles)** — 5/6 funcionários de IA 24/7 com a marca do parceiro. Preços: BASE R$997+697/mês · PREMIUM R$1497+997/mês.

**Wedge:** recuperar receita que a PME deixa escapar (62% chamadas perdidas, 27% follow-up perdido, +400% conversão se responder <5min).

**Estado:** decks comerciais corrigidos p/ Emerald Sentry (18-jul). MVP SaaS fechado (F1-F3). Roadmap F4-F6 em construção. 1º cliente = GATE 👤 (Mom Test ≥5 verdes + HITL/LGPD + Stripe live).

**Não fazer:** nunca usar paleta violeta/chartreuse/terra do Acid Circuit nos decks ATLAS. Sempre brandmark ATLAS + "powered by AAPSON".
"""
op_path = os.path.join(VAULT, "06-Produto-SaaS", "ATLAS - One-Pager Interno.md")
open(op_path, "w", encoding="utf-8").write(onepager)
log(f"  >> Escrito: {op_path} ({len(onepager)} bytes)")

# ---------- BLOCO C (2h): consolidar spec dos 5 funcionários ----------
log("\n## BLOCO C — Consolidação da spec dos 5 funcionários (ATLAS)")
dest = os.path.join(VAULT, "03-Sistema-Agentes-IA", "ATLAS - Spec dos 5 Funcionarios.md")
func_spec = f"""---
tipo: spec-funcionarios
titulo: "ATLAS — Spec dos 5 Funcionários de IA (BASE)"
frente: "ATLAS White-label (Aristóteles)"
tags: [atlas, aristoteles, funcionarios, spec, pt-br]
data: {now}
status: consolidado-do-vault (fontes: Aristoteles - Produto Servico / Manual Tecnico / Tiers)
compliance: "Sem PII. Nomes em pt-BR obrigatórios nos decks. HITL/LGPD antes de uso real (GATE 👤)."
---

# ATLAS — Spec dos 5 Funcionários de IA (pacote BASE)

> Consolidação das fontes reais do vault (Aristóteles - *) para a marca ATLAS. Nomes em pt-BR (regra de deck).

## 1. Receptionista
- **Dor:** lead chega, ninguém responde na hora → fecha com concorrente.
- **Faz:** recebe msg/ligação perdida (WhatsApp/Telegram); qualifica; propõe horário; confirma/reagenda no-show por cron.
- **Métrica:** responde <10s.

## 2. Reativação de Base
- **Dor:** 27% dos leads nunca recebem follow-up (receita enterrada na planilha).
- **Faz:** importa CSV de CRM (qualquer layout); gera msg personalizada por lead (GLM 5.2 NIM); dispara e nutre por cron.
- **Métrica:** reativa base inativa sem tráfego pago.

## 3. Nutrição de Leads
- **Dor:** follow-up médio 42h; <5min = +400% conversão (Harvard).
- **Faz:** responde lead de formulário <5min no WhatsApp; qualifica; agenda; reagenda no-show.
- **Métrica:** mantém interessado quente até fechar.

## 4. Avaliações e Indicações
- **Dor:** 98% leem reviews, só 11% pedem; indicação é tráfego mais barato.
- **Faz:** pede review pós-atendimento; responde reviews (positivas/negativas); solicita indicação.
- **Métrica:** prova social + indicação.

## 5. Treinador de Vendas
- **Dor:** ~30% treinam vendas; time treinado vende +50%; treinar é caro/parcial.
- **Faz:** gera roteiro por vertical (GLM 5.2); role-play com cliente simulado; avalia call (nota 1-10 + feedback).
- **Métrica:** time mais preparado, sem custo de consultoria.

## PREMIUM (nº6): Captador / Lead Engine
- Topo do funil: Apify → Ollama → Airtable. Só no PREMIUM e no Add-on do SaaS.

## GATE 👤
- HITL/LGPD aprovado antes de cobrança real.
- Migração Stripe test→live.
- 1º cliente após Mom Test ≥5 verdes.
"""
os.makedirs(os.path.dirname(dest), exist_ok=True)
open(dest, "w", encoding="utf-8").write(func_spec)
log(f"  >> Escrito: {dest} ({len(func_spec)} bytes)")

# ---------- BLOCO D (2h): verificação + registro na spec ----------
log("\n## BLOCO D — Verificação final + link na spec")
spec = os.path.join(VAULT, "06-Produto-SaaS", "ATLAS - Spec do Produto (PO).md")
if os.path.exists(spec):
    s = open(spec, encoding="utf-8").read()
    if "ATLAS - Spec dos 5 Funcionarios" not in s:
        s = s.replace("## 5. Próximos passos imediatos (PO)",
                      "## 5. Próximos passos imediatos (PO)\n- Spec dos 5 funcionários consolidada: `[[ATLAS - Spec dos 5 Funcionarios]]` (Bloco C, D1 18-jul).\n- One-Pager interno: `[[ATLAS - One-Pager Interno]]` (Bloco B, D1 18-jul).")
        open(spec, "w", encoding="utf-8").write(s)
        log("  >> Spec do PO atualizada com links D1.")
    else:
        log("  >> Spec do PO já tem link D1.")
log("\n=== D1 CONCLUÍDO (autônomo) — sem GATE travado. Próximo: D2 (MVP E2E real). ===")
print("D1_DONE")
