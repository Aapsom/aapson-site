#!/usr/bin/env python3
"""Teste negativo/positivo do probe verificar_site_mentoria.py (ciclo 22).

Nao toca na rede: usa MENTORIA_URL=file://... para servir HTML controlado.
Casos:
  NEG-1: HTML com claim proibido ("garantia de resultado") => probe DEVE sair 1.
  NEG-2: HTML sem preco R$250 => probe DEVE sair 1.
  POS-1: HTML limpo com precos MEN-01 => probe DEVE sair 0.
Exit 0 = todos os casos passaram.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.join(HERE, "verificar_site_mentoria.py")

BASE_OK = "<html><body>Mentoria IA. R$250/sessao. In-company R$1.500/turma.</body></html>"

CASOS = [
    ("NEG-1 claim proibido", BASE_OK.replace("Mentoria IA.", "Mentoria IA com garantia de resultado."), 1),
    ("NEG-2 preco ausente", "<html><body>Mentoria IA. In-company R$1.500/turma.</body></html>", 1),
    ("POS-1 html limpo", BASE_OK, 0),
]

falhou = False
for nome, html, esperado in CASOS:
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        path = f.name
    try:
        url = "file:///" + path.replace("\\", "/").lstrip("/")
        env = dict(os.environ, MENTORIA_URL=url)
        env.pop("MENTORIA_LOCAL_HTML", None)
        r = subprocess.run([sys.executable, PROBE], env=env, capture_output=True, text=True)
        ok = r.returncode == esperado
        print(f"[{'OK' if ok else 'FALHA'}] {nome}: exit {r.returncode} (esperado {esperado})")
        if not ok:
            falhou = True
            print(r.stdout)
    finally:
        os.unlink(path)

sys.exit(1 if falhou else 0)
