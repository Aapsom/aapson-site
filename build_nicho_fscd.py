#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_nicho_fscd.py — gera a subseção /nicho-fscd/ do site aapson-site.

Integra os 18 artigos de nicho (FS-CD / S/4HANA) como um BLOG dentro do
site das 3 frentes (PME / FS-CD / Mentoria), reusando o design system
Acid Circuit (assets/acid.css) e a mesma nav/footer das landings.

Fontes (vault, PT-BR):
  VAULT/Conteudo - Blog IA Consultores SAP      -> 10 artigos (blog)
  VAULT/Conteudo - Site Saneamento FS-CD        ->  8 artigos (saneamento)

Saída (repo, PT-BR):
  aapson-site/nicho-fscd/index.html             -> hub do blog + estratégia rentabilidade
  aapson-site/nicho-fscd/<slug>.html            -> 18 artigos

Estratégia de monetização (embutida no index, conforme vault
"Blog Nicho - IA para Consultores SAP (SEO _4s1epOcP4U).md"):
  (1) afiliado do próprio SaaS 3a/3b na sidebar  (lead interno)
  (2) AdSense                                      (after E-E-A-T, YMYL-safe)
  (3) CTA p/ Mentoria 3c (contato@aapson.com.br)   (GATE 👤 mailbox)

E-E-A-T: todo artigo carrega callout honesto de "rascunho IA, revisão
humana pendente" — NENHUM byline/URL inventado.
"""
import os, re

VAULT = "C:/Users/kauea/OneDrive/Documentos/AAPSOM.MD/OBSIDIAN/AAPSOM.MD/Trabalho/06-Produto-SaaS"
SRC_BLOG = f"{VAULT}/Conteudo - Blog IA Consultores SAP"
SRC_SITE = f"{VAULT}/Conteudo - Site Saneamento FS-CD"
ROOT = os.path.dirname(os.path.abspath(__file__))          # aapson-site/
OUT = f"{ROOT}/nicho-fscd"

def strip_fm(t):
    if t.startswith("---"):
        return t.split("---", 2)[2].lstrip("\n")
    return t

def inline(s):
    s = s.replace("\\", "")  # sem backslash literal
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[\[(.+?)\]\]", r"\1", s)      # strip obsidian wikilinks
    s = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', s)
    return s

def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60]

# ---- markdown -> html (subset: h1,h2, blockquote, ul, p) ----
def md_to_html(md):
    md = strip_fm(md)
    lines = md.split("\n")
    out, in_ul = [], False
    def close():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>"); in_ul = False
    for ln in lines:
        if ln.startswith("## "):
            close(); out.append(f"<h2>{inline(ln[3:])}</h2>")
        elif ln.startswith("# "):
            close(); out.append(f"<h1>{inline(ln[2:])}</h1>")
        elif ln.startswith("> "):
            close(); out.append(f"<blockquote class=\"eeat\">{inline(ln[2:])}</blockquote>")
        elif ln.startswith("- "):
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append(f"<li>{inline(ln[2:])}</li>")
        elif ln.strip() == "":
            close()
        else:
            close(); out.append(f"<p>{inline(ln)}</p>")
    close()
    return "\n".join(out)

# ---- nav + footer compartilhados (idênticos às landings) ----
NAV = """
<nav>
  <div class="wrap">
    <a class="brand" href="../index.html" aria-label="AAPSON — início">
      <span class="mark"><svg viewBox="0 0 100 124" aria-hidden="true"><polygon fill="#B2F120" points="50,2 91,56 73,56 50,25 27,56 9,56"/><polygon fill="#FE2266" points="9,68 27,68 50,99 73,68 91,68 50,122"/><circle fill="#484AF0" cx="50" cy="62" r="9"/></svg></span>
      <span class="word"><span class="a1">A</span><span class="a2">A</span><span class="rest">PSON</span></span>
    </a>
    <div class="navright">
      <a class="nlink" href="../pme.html">PME</a>
      <a class="nlink" href="../fscd.html">FS-CD</a>
      <a class="nlink" href="../mentoria.html">Mentoria</a>
      <a class="nlink" href="./index.html" style="color:var(--lime)">Blog FS-CD</a>
      <span class="status"><span class="dot" aria-hidden="true"></span>Disponível</span>
    </div>
  </div>
</nav>"""

FOOTER = """
<footer>
  <div class="colorbar"><span class="c1"></span><span class="c2"></span><span class="c3"></span></div>
  <div class="wrap foot-inner">
    <span>AAPSON · Confiabilidade de cobrança recorrente sobre Pix Automático</span>
    <span class="mono">© 2026 · não é recomendação</span>
  </div>
</footer>"""

# sidebar de monetização (afiliado SaaS + CTA Mentoria)
SIDEBAR = """
<aside class="rail">
  <div class="rail-card saas">
    <span class="eyebrow blue">Produto AAPSON</span>
    <h3>SaaS de Confiabilidade de Cobrança</h3>
    <p>Recuperação automática de Pix, dunning e conciliação FS-CD/S4HANA. Reduce inadimplência sem operação manual.</p>
    <a class="btn btn-solid" href="../pme.html">Conhecer o SaaS →</a>
  </div>
  <div class="rail-card ment">
    <span class="eyebrow pink">Mentoria 3c</span>
    <h3>Vire consultor SAP independente</h3>
    <p>Formato 1:1 + in-company em FS-CD, S/4HANA e dunning automático. Credencial real de quem entrega em equipes.</p>
    <a class="btn btn-outline" href="../mentoria.html">Ver mentoria →</a>
  </div>
  <div class="rail-card cons">
    <span class="eyebrow">AdSense</span>
    <h3>Receita de mídia</h3>
    <p>Este blog roda AdSense após passar no pente E-E-A-T (YMYL-safe). Conteúdo de nicho SAP = RPM alto em finanças/tech.</p>
    <span class="tag cons">em revisão</span>
  </div>
</aside>"""

def article_page(title, body_html, section, slug_url):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AAPSON · {title}</title>
<meta name="description" content="{title} — artigo do blog de nicho FS-CD / S/4HANA da AAPSON, com base em fontes oficiais SAP.">
<link rel="canonical" href="https://aapsom.github.io/aapson-site/nicho-fscd/{slug_url}">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-8 -10 116 144'%3E%3Crect x='-8' y='-10' width='116' height='144' rx='20' fill='%230B0B0F'/%3E%3Cpolygon fill='%23B2F120' points='50,2 91,56 73,56 50,25 27,56 9,56'/%3E%3Cpolygon fill='%23FE2266' points='9,68 27,68 50,99 73,68 91,68 50,122'/%3E%3Ccircle fill='%23484AF0' cx='50' cy='62' r='9'/%3E%3C/svg%3E">
<link rel="stylesheet" href="../assets/acid.css">
</head>
<body>
{NAV}
<header class="hero">
  <div class="wrap">
    <span class="eyebrow cons">{section}</span>
    <h1 class="rise">{title}</h1>
  </div>
</header>
<div class="wrap blog-grid">
  <main class="blog-main">
{body_html}
<div class="eeat-note">
  <strong>Status de publicação:</strong> rascunho gerado por IA com base em fontes oficiais SAP.
  Requer (1) revisão de consultor SAP sênior, (2) substituição de citações genéricas por
  <strong>URLs reais do help.sap.com/OSS</strong>, (3) byline com autor experiente (E-E-A-T).
  Não publicar em YMYL sem isso.
</div>
  </main>
{SIDEBAR}
</div>
{FOOTER}
</body>
</html>"""

def index_page(blog_items, site_items):
    def card_list(items):
        return "\n".join(
            f'<a class="pcard post" href="./{u}"><span class="eyebrow cons">{sec}</span><h3>{t}</h3>'
            f'<p>Leitura técnica com base em fontes oficiais SAP (help.sap.com).</p></a>'
            for t, u, sec in items
        )
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AAPSON · Blog FS-CD / S/4HANA — IA para Consultores SAP</title>
<meta name="description" content="Blog de nicho FS-CD / S/4HANA da AAPSON: artigos técnicos para consultores SAP, com estratégia de rentabilidade (SaaS, AdSense, Mentoria).">
<link rel="canonical" href="https://aapsom.github.io/aapson-site/nicho-fscd/index.html">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-8 -10 116 144'%3E%3Crect x='-8' y='-10' width='116' height='144' rx='20' fill='%230B0B0F'/%3E%3Cpolygon fill='%23B2F120' points='50,2 91,56 73,56 50,25 27,56 9,56'/%3E%3Cpolygon fill='%23FE2266' points='9,68 27,68 50,99 73,68 91,68 50,122'/%3E%3Ccircle fill='%23484AF0' cx='50' cy='62' r='9'/%3E%3C/svg%3E">
<link rel="stylesheet" href="../assets/acid.css">
</head>
<body>
{NAV}
<header class="hero">
  <div class="wrap">
    <span class="eyebrow blue">Topo de funil orgânico</span>
    <h1 class="rise">Blog FS-CD / S/4HANA</h1>
    <p class="lede rise d1">IA aplicada à consultoria SAP — aquisição orgânica sem depender de algoritmo.
    Cada artigo cita fontes oficiais SAP e alimenta o funil da AAPSON (SaaS, AdSense, Mentoria).</p>
  </div>
</header>

<section class="reveal">
  <div class="wrap">
    <span class="eyebrow pink">Como este blog é rentável</span>
    <h2>Três frentes de receita, uma base de conteúdo</h2>
    <p class="sec-lede">O blog é capital-zero (IA gera, humano revisa E-E-A-T). A monetização é em camadas —
    do tráfego orgânico até o lead qualificado:</p>
    <div class="tracks">
      <a class="track saas" href="../pme.html">
        <span class="eyebrow blue">Frente 1 · Afiliado próprio</span>
        <h2>SaaS de Confiabilidade de Cobrança</h2>
        <p>Barra lateral e CTAs levam para o SaaS 3a/3b (Pix automático, dunning, conciliação). Lead interno, sem custo de mídia.</p>
        <span class="go">Conhecer o SaaS →</span>
      </a>
      <a class="track cons" href="#adsense">
        <span class="eyebrow">Frente 2 · AdSense</span>
        <h2>Receita de mídia (RPM alto)</h2>
        <p>Nicho SAP = finanças/tech, faixa de RPM mais alta do AdSense. Ativo <strong>após</strong> passar no pente E-E-A-T (YMYL-safe).</p>
        <span class="go">Ver critério →</span>
      </a>
      <a class="track mentoria" href="../mentoria.html">
        <span class="eyebrow pink">Frente 3 · Mentoria 3c</span>
        <h2>CTA para consultor independente</h2>
        <p>O leitor vira lead para a Mentoria IA 3c (1:1 + in-company). Conversão de leitor técnico em aluno pagante.</p>
        <span class="go">Ver mentoria →</span>
      </a>
    </div>

    <div id="adsense" class="wedge-panel reveal">
      <span class="eyebrow pink">Gate de receita · AdSense</span>
      <p>Google penaliza IA genérica em YMYL (HCU). Por isso o AdSense <b>só entra após</b>:
      (1) revisão técnica humana em 100% dos artigos, (2) byline com autor experiente,
      (3) URLs reais do <strong>help.sap.com/OSS</strong> em cada claim. Até lá, o blog roda
      só com as frentes 1 e 3 — que não dependem de volume de tráfego para converter.</p>
    </div>
  </div>
</section>

<section class="reveal">
  <div class="wrap">
    <span class="eyebrow cons">Acervo</span>
    <h2>Artigos publicados (rascunhos IA, em revisão E-E-A-T)</h2>
    <div class="posts">
      {card_list(blog_items)}
      {card_list(site_items)}
    </div>
    <p class="sec-lede" style="margin-top:var(--s-xl)">São 18 artigos (10 de blog + 8 de saneamento FS-CD).
    Todos em revisão técnica humana antes de ativar AdSense.</p>
  </div>
</section>
{FOOTER}
</body>
</html>"""

# ---- build ----
os.makedirs(OUT, exist_ok=True)
blog, site = [], []
for d, sec in ((SRC_BLOG, "Blog — IA para Consultores SAP"),
              (SRC_SITE, "Site — Saneamento FS-CD")):
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        t = open(f"{d}/{fn}", encoding="utf-8").read()
        m = re.search(r'titulo: "(.+?)"', t)
        title = m.group(1) if m else fn[:-3]
        body = md_to_html(t)
        s = slug(title)
        with open(f"{OUT}/{s}.html", "w", encoding="utf-8") as f:
            f.write(article_page(title, body, sec, f"{s}.html"))
        (blog if sec.startswith("Blog") else site).append((title, f"{s}.html", sec))

with open(f"{OUT}/index.html", "w", encoding="utf-8") as f:
    f.write(index_page(blog, site))

print(f"blog={len(blog)} site={len(site)} index=1 -> {OUT}")
