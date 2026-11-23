#!/usr/bin/env python3
"""Convierte Markdown (subconjunto) a ADF de Jira con títulos en color.

Uso:
    python md2adf.py borrador.md                > descripcion.json
    python md2adf.py borrador.md --color none   > descripcion.json
    python md2adf.py borrador.md --check            # solo valida, no imprime

Soporta: ## / ### títulos (color verde #36b37e por defecto), párrafos,
listas con viñetas y numeradas (anidadas por indentación), bloques de
código con lenguaje, citas (>), tablas Markdown, separador (---),
**negrita**, *cursiva* / _cursiva_, `código`, [texto](url) y URLs de
Jira (…/browse/KEY-123) como smart link (inlineCard).

Reglas de ADF que aplica para evitar INVALID_INPUT:
- La marca `code` no se combina con strong/em/textColor: se emite sola.
- Nodos de texto vacíos se descartan.
"""
import argparse
import json
import re
import sys

GREEN = "#36b37e"
JIRA_URL = re.compile(r"^https?://[\w.-]+\.atlassian\.net/browse/[A-Z][A-Z0-9]+-\d+$")
INLINE = re.compile(
    r"\*\*(?P<b>.+?)\*\*"
    r"|`(?P<c>[^`]+)`"
    r"|\[(?P<lt>[^\]]+)\]\((?P<lu>[^)\s]+)\)"
    r"|(?P<url>https?://[^\s)<>|]+)"
    r"|(?<![\w*])\*(?P<i1>[^*\s][^*]*?)\*(?![\w*])"
    r"|(?<![\w_])_(?P<i2>[^_\s][^_]*?)_(?![\w_])"
)


def text(t, marks=None):
    if not t:
        return []
    node = {"type": "text", "text": t}
    if marks:
        node["marks"] = marks
    return [node]


def inline(s, marks=None):
    marks = list(marks or [])
    out, pos = [], 0
    for m in INLINE.finditer(s):
        out += text(s[pos:m.start()], marks)
        if m.group("b") is not None:
            out += inline(m.group("b"), marks + [{"type": "strong"}])
        elif m.group("c") is not None:
            link = [x for x in marks if x["type"] == "link"]
            out += text(m.group("c"), link + [{"type": "code"}])
        elif m.group("lt") is not None:
            out += inline(m.group("lt"), marks + [{"type": "link", "attrs": {"href": m.group("lu")}}])
        elif m.group("url") is not None:
            url = m.group("url").rstrip(".,;:")
            tail = m.group("url")[len(url):]
            if JIRA_URL.match(url) and not marks:
                out.append({"type": "inlineCard", "attrs": {"url": url}})
            else:
                out += text(url, marks + [{"type": "link", "attrs": {"href": url}}])
            out += text(tail, marks)
        else:
            out += inline(m.group("i1") or m.group("i2"), marks + [{"type": "em"}])
        pos = m.end()
    out += text(s[pos:], marks)
    return out


def para(s):
    content = inline(s.strip())
    return {"type": "paragraph", "content": content} if content else {"type": "paragraph"}


LIST_ITEM = re.compile(r"^(?P<ind>\s*)(?P<mk>[-*+]|\d+[.)])\s+(?P<txt>.*)$")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")


def cells(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]


def parse_list(lines, i, base):
    """Parsea una lista desde lines[i] con indentación >= base."""
    first = LIST_ITEM.match(lines[i])
    ordered = first.group("mk")[0].isdigit()
    node = {"type": "orderedList", "attrs": {"order": 1}, "content": []} if ordered else {"type": "bulletList", "content": []}
    ind = len(first.group("ind"))
    while i < len(lines):
        m = LIST_ITEM.match(lines[i])
        if not m or len(m.group("ind")) != ind or m.group("mk")[0].isdigit() != ordered:
            break
        buf = [m.group("txt")]
        item = {"type": "listItem", "content": []}
        i += 1
        # Líneas de continuación (sin línea en blanco) se unen al texto del ítem.
        while i < len(lines) and lines[i].strip() and len(lines[i]) - len(lines[i].lstrip()) > ind \
                and not LIST_ITEM.match(lines[i]) and not lines[i].strip().startswith("```"):
            buf.append(lines[i].strip())
            i += 1
        item["content"].append(para(" ".join(buf)))
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                nxt = next((l for l in lines[i:] if l.strip()), "")
                if len(nxt) - len(nxt.lstrip()) > ind:
                    i += 1
                    continue
                break
            lead = len(line) - len(line.lstrip())
            if lead <= ind:
                break
            sub = LIST_ITEM.match(line)
            if sub:
                child, i = parse_list(lines, i, lead)
                item["content"].append(child)
            elif line.strip().startswith("```"):
                block, i = parse_code(lines, i)
                item["content"].append(block)
            else:
                item["content"].append(para(line))
                i += 1
        node["content"].append(item)
    return node, i


def parse_code(lines, i):
    lang = lines[i].strip()[3:].strip() or None
    lead = len(lines[i]) - len(lines[i].lstrip())
    body = []
    i += 1
    while i < len(lines) and not lines[i].strip().startswith("```"):
        body.append(lines[i][lead:] if lines[i][:lead].strip() == "" else lines[i])
        i += 1
    node = {"type": "codeBlock", "content": text("\n".join(body))}
    if lang:
        node["attrs"] = {"language": lang}
    return node, i + 1


def convert(md, color):
    lines = md.replace("\r\n", "\n").split("\n")
    doc, i = [], 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", s)
        if h:
            level = len(h.group(1))
            marks = [{"type": "textColor", "attrs": {"color": color}}] if color and level <= 3 else []
            # Los títulos llevan texto plano: color y marcas de código no se combinan.
            title = re.sub(r"[*`]", "", h.group(2)).strip()
            doc.append({"type": "heading", "attrs": {"level": level}, "content": text(title, marks)})
            i += 1
        elif s.startswith("```"):
            node, i = parse_code(lines, i)
            doc.append(node)
        elif re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            doc.append({"type": "rule"})
            i += 1
        elif s.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            paras = [p for p in "\n".join(quote).split("\n\n") if p.strip()]
            doc.append({"type": "blockquote", "content": [para(" ".join(p.split("\n"))) for p in paras]})
        elif s.startswith("|") and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1]):
            head = cells(lines[i])
            rows = []
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1

            def row(values, kind):
                values = (values + [""] * len(head))[: len(head)]
                return {"type": "tableRow", "content": [{"type": kind, "content": [para(v)]} for v in values]}

            doc.append({
                "type": "table",
                "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
                "content": [row(head, "tableHeader")] + [row(r, "tableCell") for r in rows],
            })
        elif LIST_ITEM.match(line):
            node, i = parse_list(lines, i, 0)
            doc.append(node)
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6}\s|```|>|\|)", lines[i].strip()) and not LIST_ITEM.match(lines[i]):
                buf.append(lines[i].strip())
                i += 1
            doc.append(para(" ".join(buf)))
    return {"type": "doc", "version": 1, "content": doc}


def check(node, path="doc"):
    """Valida reglas de ADF que Jira rechaza con INVALID_INPUT."""
    errors = []
    if node.get("type") == "text":
        kinds = [m["type"] for m in node.get("marks", [])]
        if "code" in kinds and set(kinds) - {"code", "link"}:
            errors.append(f"{path}: 'code' combinado con {kinds}")
        if not node.get("text"):
            errors.append(f"{path}: nodo de texto vacío")
    for n, child in enumerate(node.get("content", []) or []):
        errors += check(child, f"{path}/{child.get('type')}[{n}]")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("archivo", help="Markdown de entrada ('-' para stdin)")
    ap.add_argument("--color", default=GREEN, help="Color de títulos H1-H3 (hex) o 'none'")
    ap.add_argument("--check", action="store_true", help="Solo validar y reportar")
    args = ap.parse_args()
    src = sys.stdin.read() if args.archivo == "-" else open(args.archivo, encoding="utf-8").read()
    adf = convert(src, None if args.color.lower() == "none" else args.color)
    errors = check(adf)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    if args.check:
        print(f"OK: {len(adf['content'])} bloques", file=sys.stderr)
        return
    sys.stdout.reconfigure(encoding="utf-8")
    json.dump(adf, sys.stdout, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main()
