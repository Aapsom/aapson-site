#!/usr/bin/env python3
"""seo_audit.py — auditor offline do loop SEO do site AAPSON.
Verifica quick-wins do "Loop Engineering" (5p_BBdfvzgQ) sem precisar de GSC:
sitemap.xml, robots.txt, JSON-LD, <title>/description por página, e interlink
dos artigos nicho-fscd/. Gera relatório + sugestões. Idempotente.
Uso: python seo_audit.py  (roda em cwd = raiz do repo aapson-site)
"""
import os, re, glob, sys

ROOT = os.getcwd()
html_files = [f for f in glob.glob("*.html")] + \
            [f for f in glob.glob("nicho-fscd/*.html")]

def read(p):
    try:
        with open(os.path.join(ROOT, p), encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except Exception as e:
        return ""

report = []
report.append("=== AUDITOR SEO OFFLINE — aapson-site ===")
report.append(f"páginas .html encontradas: {len(html_files)}")

# 1) sitemap / robots
for f in ["sitemap.xml", "robots.txt"]:
    ok = os.path.exists(os.path.join(ROOT, f))
    report.append(f"[{'OK ' if ok else 'FALTA'}] {f}")

# 2) JSON-LD em qualquer html
has_jsonld = 0
for p in html_files:
    if 'application/ld+json' in read(p):
        has_jsonld += 1
report.append(f"[{'OK ' if has_jsonld else 'FALTA'}] JSON-LD (application/ld+json) em {has_jsonld}/{len(html_files)} páginas")

# 3) title / description por página
missing_meta = []
for p in html_files:
    t = read(p)
    title = re.search(r"<title>(.*?)</title>", t, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', t, re.S)
    if not title or not title.group(1).strip():
        missing_meta.append(f"{p}: sem <title>")
    if not desc:
        missing_meta.append(f"{p}: sem meta description")
report.append(f"meta tags: {len(html_files)-len(set(m.split(':')[0] for m in missing_meta)) if False else len(html_files)} páginas; problemas={len(missing_meta)}")
for m in missing_meta[:20]:
    report.append(f"   - {m}")

# 4) interlink nicho-fscd (cannibalization / isolamento)
artigos = glob.glob(os.path.join(ROOT, "nicho-fscd", "*.html"))
isolados = 0
for a in artigos:
    nome = os.path.basename(a)
    if nome == "index.html":
        continue
    txt = read(a)
    # conta links internos para OUTROS artigos nicho-fscd
    outros = [n for n in glob.glob("nicho-fscd/*.html") if os.path.basename(n) != nome and os.path.basename(n) != "index.html"]
    links = 0
    for o in outros:
        if os.path.basename(o) in txt:
            links += 1
    if links == 0:
        isolados += 1
report.append(f"[{'OK ' if isolados==0 else 'FALTA'}] interlink nicho-fscd: {isolados}/{len(artigos)-1} artigos sem link p/ outro artigo do cluster")

# Veredito
faltas = (not os.path.exists(os.path.join(ROOT,"sitemap.xml"))) + \
         (not os.path.exists(os.path.join(ROOT,"robots.txt"))) + \
         (has_jsonld == 0) + (isolados > 0)
verdict = "SAUDÁVEL" if faltas == 0 else f"{faltas} categoria(s) de quick-win pendente(s)"
report.append(f"\nVEREDITO: {verdict}")

out = "\n".join(report)
print(out)
# grava relatório p/ memória do loop
with open(os.path.join(ROOT, "seo_audit_last.txt"), "w", encoding="utf-8") as fh:
    fh.write(out + f"\n[gerado por seo_audit.py em {__import__('datetime').datetime.now().isoformat(timespec='seconds')}]\n")
sys.exit(0)
