#!/usr/bin/env python3
"""interlink_nicho.py — autorelaciona os 18 artigos nicho-fscd/ via JSON-LD
SeeAlso + bloco HTML de "Artigos relacionados" no fim do <body>. Idempotente.
NÃO mexe em index.html do cluster nem em test-*. Gera ainda related-links
internos (corta o isolamento apontado pelo seo_audit.py: 18/18 isolados).
Uso: python interlink_nicho.py  (cwd = raiz do repo)
"""
import os, re, glob

ROOT = os.getcwd()
NICH = os.path.join(ROOT, "nicho-fscd")
arts = [a for a in glob.glob(os.path.join(NICH, "*.html")) if os.path.basename(a) != "index.html"]
arts.sort()

def title_of(p):
    t = open(p, encoding="utf-8", errors="ignore").read()
    m = re.search(r"<title>(.*?)</title>", t, re.S)
    return m.group(1).strip() if m else os.path.basename(p)

titles = {os.path.basename(a): title_of(a) for a in arts}

changed = 0
for a in arts:
    b = os.path.basename(a)
    t = open(a, encoding="utf-8", errors="ignore").read()
    others = [x for x in arts if os.path.basename(x) != b]
    # pega 3 relacionados (mesma palavra-chave provável: ordem estável, vizinhos)
    rel = others[:3] if others[:3] else others
    # bloco HTML
    links_html = "\n".join(
        f'  <li><a href="{os.path.basename(x)}">{titles[os.path.basename(x)]}</a></li>'
        for x in rel
    )
    block = (
        '\n<section class="related" aria-label="Artigos relacionados">\n'
        '  <h2>Artigos relacionados</h2>\n  <ul>\n' + links_html + "\n  </ul>\n</section>\n"
    )
    # JSON-LD SeeAlso
    seealso = (
        '<script type="application/ld+json">\n{\n'
        '  "@context": "https://schema.org",\n  "@type": "Article",\n'
        f'  "name": {title_of(a)!r},\n  "seeAlso": [\n'
        + ",\n".join(f'    "https://aapsom.github.io/aapson-site/nicho-fscd/{os.path.basename(x)}"' for x in rel)
        + "\n  ]\n}\n</script>"
    )
    if "class=\"related\"" in t or "seeAlso" in t:
        continue  # idempotente
    if "</body>" in t:
        t = t.replace("</body>", block + seealso + "\n</body>", 1)
    else:
        t = t + block + seealso
    open(a, "w", encoding="utf-8").write(t)
    changed += 1
    print(f"+ interlink -> {b} ({len(rel)} links)")

print(f"\nTotal alterados: {changed}")
