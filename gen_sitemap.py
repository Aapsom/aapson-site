#!/usr/bin/env python3
"""gen_sitemap.py — gera sitemap.xml + robots.txt do aapson-site a partir dos
.html reais. Idempotente. NÃO mexe em test-*/bg-mockup/scroll-world-test.
Uso: python gen_sitemap.py  (cwd = raiz do repo)
"""
import os, re, glob, datetime

ROOT = os.getcwd()
BASE = "https://aapsom.github.io/aapson-site/"
SKIP = ("test-", "bg-mockup", "scroll-world-test", "decks/")

def is_prod(p):
    b = os.path.basename(p)
    if any(b.startswith(s) or p.startswith(s.strip("/")) for s in SKIP if s.endswith("/")):
        return False
    if b.startswith("test-") or b in ("bg-mockup.html", "scroll-world-test.html"):
        return False
    return True

pages = []
for p in glob.glob("*.html") + glob.glob("nicho-fscd/*.html"):
    if is_prod(p):
        pages.append(p.replace("\\", "/"))

# prioridade para homepage
pages.sort(key=lambda x: (x != "index.html", x))

urls = []
for p in pages:
    path = "" if p == "index.html" else p
    urls.append(f"  <url><loc>{BASE}{path}</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>")

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "\n".join(urls) + "\n</urlset>\n"
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap)

robots = "User-agent: *\nAllow: /\n"
robots += f"Sitemap: {BASE}sitemap.xml\n"
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(robots)

print(f"sitemap.xml: {len(pages)} URLs")
print("robots.txt: ok")
print("amostra:", urls[0].strip())
