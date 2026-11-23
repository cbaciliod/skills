#!/usr/bin/env python3
"""Compara los mismos archivos entre carpetas de ambiente (test / uat / prd).

Uso:
    python compare.py sql/test sql/uat sql/prd
    python compare.py baseii/prd baseii/uat --file baseii.sh
    python compare.py a/ b/ --diff          # muestra las líneas que difieren (lógico)

Para cada archivo presente en las carpetas:
- tamaño, hash md5 corto, fin de línea (CRLF/LF), salto final, terminador '/'
- diff EXACTO (cantidad de líneas) y diff LÓGICO: ignora CRLF, espacios,
  líneas vacías y el esquema en `CREATE OR REPLACE ... [ESQ.]"OBJ"`
Nunca imprime contraseñas: las líneas con PASS/PASSWORD/USERID/IDENTIFIED BY
se muestran como <REDACTED>. No compara archivos de datos (.txt, .bad, .csv, .dat),
que pueden contener PAN.
"""
import argparse
import difflib
import hashlib
import os
import re
import sys

CODE_EXT = {".sql", ".pks", ".pkb", ".ctl", ".sh", ".ksh", ".json", ".yaml", ".yml",
            ".properties", ".xml", ".conf", ".env", ".py", ".go", ".java", ".md"}
DATA_EXT = {".txt", ".bad", ".dsc", ".csv", ".dat", ".log"}
SECRET = re.compile(r"(PASS(WORD|_ORA)?\s*=|PASSWORD|IDENTIFIED\s+BY|USERID=|Bearer\s+\S{8,})", re.I)
HEADER = re.compile(r'^CREATE OR REPLACE (PACKAGE BODY|PACKAGE|PROCEDURE|FUNCTION|TRIGGER|VIEW)\s+(\w+\.)?"?(\w+)"?', re.I)


def redact(line):
    return re.sub(r"(=|BY\s+|Bearer\s+).*", r"\1<REDACTED>", line, flags=re.I) if SECRET.search(line) else line


def info(path):
    raw = open(path, "rb").read()
    text = raw.decode("utf-8", errors="replace")
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return {
        "bytes": len(raw),
        "md5": hashlib.md5(raw).hexdigest()[:8],
        "eol": "CRLF" if b"\r\n" in raw else "LF",
        "final_nl": raw.endswith(b"\n"),
        "slash": any(l.strip() == "/" for l in lines[-3:]),
        "lines": lines,
    }


def logical(lines):
    out = []
    for l in lines:
        s = re.sub(r"\s+", " ", l).strip()
        if not s or s == "/":
            continue
        m = HEADER.match(s)
        if m:
            s = f"CREATE OR REPLACE {m.group(1).upper()} {m.group(3).upper()}"
        out.append(s)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dirs", nargs="+", help="Carpetas a comparar (2 o más)")
    ap.add_argument("--file", action="append", help="Comparar solo este archivo (repetible)")
    ap.add_argument("--diff", action="store_true", help="Mostrar las diferencias lógicas")
    args = ap.parse_args()
    if len(args.dirs) < 2:
        sys.exit("Indica al menos 2 carpetas")
    sys.stdout.reconfigure(encoding="utf-8")

    names = set(args.file or [])
    if not names:
        for d in args.dirs:
            names |= {f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))}
    tags = [os.path.basename(os.path.normpath(d)) or d for d in args.dirs]

    for name in sorted(names):
        ext = os.path.splitext(name)[1].lower()
        print(f"\n## {name}")
        if ext in DATA_EXT:
            print("   (archivo de datos: no se compara contenido; puede tener PAN)")
            continue
        found = {t: info(os.path.join(d, name)) for t, d in zip(tags, args.dirs) if os.path.isfile(os.path.join(d, name))}
        print("| ambiente | bytes | md5 | EOL | salto final | '/' final |")
        print("|---|---|---|---|---|---|")
        for t in tags:
            if t in found:
                f = found[t]
                print(f"| {t} | {f['bytes']} | {f['md5']} | {f['eol']} | {'sí' if f['final_nl'] else 'no'} | {'sí' if f['slash'] else 'no'} |")
            else:
                print(f"| {t} | — no existe — | | | | |")
        keys = list(found)
        for a_i in range(len(keys)):
            for b_i in range(a_i + 1, len(keys)):
                a, b = keys[a_i], keys[b_i]
                fa, fb = found[a], found[b]
                if fa["md5"] == fb["md5"]:
                    print(f"- {a} vs {b}: IDÉNTICOS byte a byte")
                    continue
                exact = sum(1 for l in difflib.unified_diff(fa["lines"], fb["lines"], n=0, lineterm="")
                            if l[:1] in "+-" and not l.startswith(("+++", "---")))
                la, lb = logical(fa["lines"]), logical(fb["lines"])
                if la == lb:
                    print(f"- {a} vs {b}: MISMO CÓDIGO (solo formato: {exact} líneas por espacios/EOL/encabezado)")
                    continue
                d = [l for l in difflib.unified_diff(la, lb, a, b, n=0, lineterm="") if not l.startswith(("+++", "---"))]
                changed = sum(1 for l in d if l[:1] in "+-")
                print(f"- {a} vs {b}: DIFERENTE ({changed} líneas de código, {exact} exactas)")
                if args.diff:
                    for l in d:
                        print("    " + redact(l)[:200])


if __name__ == "__main__":
    main()
