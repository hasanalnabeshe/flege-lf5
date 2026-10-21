#!/usr/bin/env python3
"""Baut index.html aus content/*.txt  (Lernseite LF 5 – Pflege)."""
import re, html, os, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))

def inline(s):
    s = html.escape(s.strip(), quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", s)
    return s

def split(s):
    if " | " in s:
        de, ar = s.split(" | ", 1)
        return de, ar
    return s, ""

def bi(s, tag="span"):
    de, ar = split(s)
    out = f'<{tag} class="de" lang="de">{inline(de)}</{tag}>'
    if ar.strip():
        out += f'<{tag} class="ar" lang="ar" dir="rtl">{inline(ar)}</{tag}>'
    return out

def cell(s, th=False):
    t = "th" if th else "td"
    return f"<{t}>{bi(s)}</{t}>"

def img(path):
    return f"img/{path}.jpg"

def render_page(lines):
    out, listtype, table, boxes = [], None, None, None
    def close():
        nonlocal listtype, table, boxes
        if listtype: out.append(f"</{listtype}>"); listtype = None
        if table is not None:
            out.append('<div class="tablewrap"><table>' + "".join(table) + "</table></div>"); table = None
        if boxes is not None:
            html_boxes = "".join(f'<div class="box c-{c}"><div class="bt">{bi(t)}</div>' + (f'<ul>{"".join(items)}</ul>' if items else "") + "</div>" for c, t, items in boxes)
            out.append(f'<div class="boxes">{html_boxes}</div>'); boxes = None
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            close(); continue
        if line.startswith("box: "):
            if listtype or table is not None:
                b = boxes; boxes = None; close(); boxes = b
            if boxes is None: boxes = []
            color, rest = line[5:].split(" | ", 1)
            boxes.append((color.strip(), rest, [])); continue
        if line.startswith("+ ") and boxes:
            boxes[-1][2].append(f"<li>{bi(line[2:])}</li>"); continue
        if boxes is not None:
            close()
        m = re.match(r"^(\s*)(- |\d+\. )(.*)$", line)
        if m and not line.startswith(("th:", "tr:")):
            kind = "ol" if m.group(2)[0].isdigit() else "ul"
            if table is not None: close()
            if listtype != kind:
                if listtype: out.append(f"</{listtype}>")
                out.append(f"<{kind}>"); listtype = kind
            cls = ' class="sub"' if m.group(1) else ""
            out.append(f"<li{cls}>{bi(m.group(3))}</li>"); continue
        if line.startswith(("th:", "tr:")):
            if listtype: out.append(f"</{listtype}>"); listtype = None
            if table is None: table = []
            th = line.startswith("th:")
            cells = re.split(r"\s*;;\s*", line[3:].strip())
            table.append("<tr>" + "".join(cell(c, th) for c in cells) + "</tr>"); continue
        close()
        if line.strip() == "↓":
            out.append('<div class="flowarrow" aria-hidden="true">↓</div>')
        elif line.startswith("### "):
            out.append(f"<h4>{bi(line[4:])}</h4>")
        elif line.startswith("## "):
            out.append(f"<h3>{bi(line[3:])}</h3>")
        elif line.startswith("# "):
            de, _ = split(line[2:])
            sid = re.sub(r"[^a-z0-9]+", "-", de.lower()).strip("-")[:40]
            out.append(f'<h2 id="{sid}">{bi(line[2:])}</h2>')
        elif line.startswith("p: "):
            de, ar = split(line[3:])
            out.append(f'<p class="de" lang="de">{inline(de)}</p>')
            if ar.strip(): out.append(f'<p class="ar" lang="ar" dir="rtl">{inline(ar)}</p>')
        elif line.startswith("ar: "):
            out.append(f'<p class="ar only" lang="ar" dir="rtl">{inline(line[4:])}</p>')
        elif line.startswith(("note: ", "tip: ", "warn: ", "fix: ")):
            kind, rest = line.split(": ", 1)
            label = {"note": ("Hinweis", "ملاحظة"), "tip": ("Merke", "تذكّر"), "warn": ("Achtung", "انتبه"), "fix": ("Korrektur", "تصحيح")}[kind]
            out.append(f'<div class="callout {kind}"><div class="lbl"><span class="de">{label[0]}</span><span class="ar" dir="rtl">{label[1]}</span></div>{bi(rest, "div")}</div>')
        elif line.startswith("q: "):
            out.append(f'<div class="q">{bi(line[3:], "div")}</div>')
        elif line.startswith("img: "):
            parts = line[5:].split(" | ")
            f = parts[0].strip(); cde = parts[1] if len(parts) > 1 else ""; car = parts[2] if len(parts) > 2 else ""
            out.append(f'<figure><a href="{img(f)}" class="zoom"><img src="{img(f)}" loading="lazy" alt="{html.escape(cde)}"></a>'
                       f'<figcaption><span class="de">{inline(cde)}</span>' + (f'<span class="ar" dir="rtl">{inline(car)}</span>' if car else "") + "</figcaption></figure>")
        elif line.startswith("gallery: "):
            parts = line[9:].split(" | ")
            prefix = parts[0].strip()
            files = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, "public", "img", prefix + "*.jpg")))
            cde = parts[1] if len(parts) > 1 else ""; car = parts[2] if len(parts) > 2 else ""
            items = "".join(f'<a href="{img(f)}" class="zoom" data-n="{i+1}"><img src="{img(f)}" loading="lazy" alt="{html.escape(cde)} {i+1}"><span>{i+1}</span></a>' for i, f in enumerate(files))
            out.append(f'<details class="gallery"><summary><span class="de">{inline(cde)} ({len(files)})</span>' + (f'<span class="ar" dir="rtl">{inline(car)}</span>' if car else "") + f'</summary><div class="grid">{items}</div></details>')
        elif line.startswith("cards:"):
            out.append("@@CARDS@@")
        else:
            out.append(f"<p>{bi(line)}</p>")
    close()
    return "\n".join(out)

def main():
    pages = []
    for path in sorted(glob.glob(os.path.join(ROOT, "content", "*.txt"))):
        cur = None
        for line in open(path, encoding="utf-8"):
            if line.startswith("@page "):
                pid, nde, nar, grp = [x.strip() for x in line[6:].split(" | ")]
                cur = {"id": pid, "de": nde, "ar": nar, "grp": grp, "lines": []}
                pages.append(cur)
            elif cur is not None:
                cur["lines"].append(line)
    groups, nav = [], []
    for p in pages:
        if p["grp"] not in groups: groups.append(p["grp"])
    for g in groups:
        gde, gar = g.split(" / ") if " / " in g else (g, "")
        nav.append(f'<div class="navgrp"><span class="de">{gde}</span><span class="ar" dir="rtl">{gar}</span></div>')
        for p in pages:
            if p["grp"] == g:
                nav.append(f'<a href="#{p["id"]}" data-page="{p["id"]}"><span class="de">{p["de"]}</span><span class="ar" dir="rtl">{p["ar"]}</span></a>')
    cards = '<div class="cards">' + "".join(
        f'<a class="card" href="#{p["id"]}"><b>{p["de"]}</b><span class="ar" dir="rtl">{p["ar"]}</span></a>'
        for p in pages if p["id"] != "start") + "</div>"
    body = ""
    for p in pages:
        body += f'<section class="page" id="p-{p["id"]}" data-title="{html.escape(p["de"])}">' + render_page(p["lines"]).replace("@@CARDS@@", cards) + "</section>\n"
    tpl = open(os.path.join(ROOT, "template.html"), encoding="utf-8").read()
    out = tpl.replace("{{NAV}}", "\n".join(nav)).replace("{{BODY}}", body)
    os.makedirs(os.path.join(ROOT, "public"), exist_ok=True)
    open(os.path.join(ROOT, "public", "index.html"), "w", encoding="utf-8").write(out)
    print("pages:", len(pages), "bytes:", len(out))

main()
