#!/usr/bin/env python3
"""Probe read-only do site da Mentoria IA (aapson-site).

Recriado 23/07 (ciclo 20) — o probe original sumiu do disco (drift).
Checks:
  1. HTTP 200 na pagina mentoria ao vivo.
  2. Precos travados (MEN-01): R$250 e R$1.500 presentes.
  3. Zero claims proibidos (garantia de resultado, numeros inventados).
  4. DRIFT-GUARD local opcional: se MENTORIA_LOCAL_HTML apontar para o
     mentoria.html da working copy, valida a Regra Fixa '8+' (deve ter
     exatamente 3 ocorrencias: ring-badge + 2x marquee) e os precos.
Nao escreve nada. Exit 0 = VALIDADO, 1 = FALHA.
"""
import os
import re
import sys
import urllib.request

URLS = [
    os.environ.get("MENTORIA_URL", "https://aapson.com.br/mentoria.html"),
    "https://aapsom.github.io/aapson-site/mentoria.html",  # fallback GitHub Pages
]
CLAIMS_PROIBIDOS = [
    r"garantia de resultado",
    r"garantimos",
    r"100% de aprova",
    r"\bROI garantido\b",
]
falhas = []

# 1+2+3: live (tenta cada URL; primeira que responder vale)
html, status, url_ok, last_err = None, None, None, None
for URL in URLS:
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "aapson-probe/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            status = r.status if r.status is not None else 200  # file:// => None
            html = r.read().decode("utf-8", "replace")
        url_ok = URL
        break
    except Exception as e:
        last_err = f"erro ao acessar {URL}: {e}"
if html is None:
    falhas.append(last_err or "nenhuma URL acessivel")
else:
    if status != 200:
        falhas.append(f"HTTP {status} em {url_ok}")
    else:
        print(f"[OK] HTTP 200 {url_ok} ({len(html)} bytes)")
    for num in ("250", "1.500"):
        if re.search(r"R\$\s*" + re.escape(num), html):
            print(f"[OK] preco presente: R$ {num}")
        else:
            falhas.append(f"preco ausente no live: R$ {num}")
    claims_hit = [pat for pat in CLAIMS_PROIBIDOS if re.search(pat, html, re.I)]
    if claims_hit:
        for pat in claims_hit:
            falhas.append(f"claim proibido no live: {pat}")
    else:
        print("[OK] 0 claims proibidos no live")

# 4: drift-guard local (opcional)
local = os.environ.get("MENTORIA_LOCAL_HTML")
if local and os.path.isfile(local):
    txt = open(local, encoding="utf-8", errors="replace").read()
    n8 = txt.count("8+")
    if n8 == 3:
        print("[OK] Regra Fixa '8+' local = 3 (ring + 2x marquee)")
    else:
        falhas.append(f"DRIFT local: '8+' aparece {n8}x (esperado 3) em {local}")
    for num in ("250", "1.500"):
        if not re.search(r"R\$\s*" + re.escape(num), txt):
            falhas.append(f"preco ausente na working copy: R$ {num}")

if falhas:
    print("FALHA:")
    for f in falhas:
        print(" -", f)
    sys.exit(1)
print("VALIDADO")
sys.exit(0)
