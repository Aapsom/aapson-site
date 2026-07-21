#!/usr/bin/env python3
"""inject_jsonld.py — injeta JSON-LD (Organization + WebSite) nos .html de producao.
Idempotente: pula se ja tem application/ld+json. NÃO mexe em test-*/bg-mockup.
Uso: python inject_jsonld.py  (cwd = raiz do repo)
"""
import os, re, glob

ROOT = os.getcwd()
SKIP_BASENAME = ("bg-mockup.html", "scroll-world-test.html")
SKIP_PREFIX = ("test-",)

def is_prod(p):
    b = os.path.basename(p)
    if b in SKIP_BASENAME or b.startswith(SKIP_PREFIX):
        return False
    return True

ORG = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "AAPSON",
  "url": "https://aapsom.github.io/aapson-site/",
  "description": "Tres frentes, uma base tecnica FS-CD: cobranca recorrente Pix PME, mentoria de IA para consultores SAP, e diagnostico & migracao FS-CD para S/4HANA.",
  "sameAs": []
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "AAPSON",
  "url": "https://aapsom.github.io/aapson-site/"
}
</script>"""

ARTICLE = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "%s",
  "publisher": {"@type": "Organization", "name": "AAPSON"}
}
</script>"""

changed = 0
for p in glob.glob("*.html") + glob.glob("nicho-fscd/*.html"):
    if not is_prod(p):
        continue
    fp = os.path.join(ROOT, p)
    t = open(fp, encoding="utf-8", errors="ignore").read()
    if "application/ld+json" in t:
        continue
    # pega o title
    m = re.search(r"<title>(.*?)</title>", t, re.S)
    title = m.group(1).strip() if m else "AAPSON"
    block = ORG if p == "index.html" else ARTICLE % title
    if "</head>" in t:
        t = t.replace("</head>", block + "\n</head>", 1)
    else:
        t = t.replace("</html>", block + "\n</html>", 1)
    open(fp, "w", encoding="utf-8").write(t)
    changed += 1
    print(f"+ JSON-LD -> {p} ({'Org+WebSite' if p=='index.html' else 'Article'})")

print(f"\nTotal alterados: {changed}")
