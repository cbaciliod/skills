---
name: env-compare
description: >
  Compara archivos de un cambio entre carpetas de ambiente (test / uat / prd, vigente vs nuevo, rollback) — SQL (packages, DDL), .ctl de SQL*Loader, .sh, configs — y arma el archivo para producción aplicando solo el delta. Distingue diferencias de código, propias del ambiente y de formato; nunca muestra contraseñas ni contenido con PAN. Activa este skill cuando el mensaje contenga (sin distinguir mayúsculas) palabras como: compara, comparar, comparación, valida en los tres ambientes, son iguales, diferencias, diff, vs, prd vs uat, test vs uat, toma como referencia, actualiza a los demás. Si la intención no es clara, pregunta ¿quieres comparar archivos entre ambientes?
---

# Env Compare — comparar y alinear archivos entre ambientes

## Paso 1 — Comparar (siempre con el script)

```bash
python3 -I <ruta-skill>/env-compare/scripts/compare.py <dir1> <dir2> [dir3 …] [--file X] [--diff]
```

- Sin `--diff`: tabla por archivo (bytes, md5, EOL, salto final, `/` final) + veredicto por par: **IDÉNTICOS**, **MISMO CÓDIGO** (solo formato) o **DIFERENTE**.
- Con `--diff`: líneas de código que difieren (ignora CRLF, espacios, líneas vacías y el esquema del encabezado `CREATE OR REPLACE`). Las credenciales salen como `<REDACTED>`.
- Archivos de datos (`.txt`, `.bad`, `.csv`, `.log`) no se comparan por contenido: pueden contener PAN.
- Si el usuario pide "otra vez" / "ahora compara": volver a ejecutar el script (el usuario suele haber editado). Mencionar qué archivo cambió y a qué hora (`ls -l --time-style=+%F_%T`).

## Paso 2 — Clasificar cada diferencia y responder en tabla

| Clase | Ejemplos | Qué hacer |
|---|---|---|
| **Delta** (el cambio del ticket) | tabla origen, JOIN, filtro eliminado, `APPEND`→`TRUNCATE`, bloque nuevo | Es lo único que va al pase |
| **Propio del ambiente** | `ORACLE_SID`, rutas `/…UAT/…`, conexión (`user/pass@sid` vs `'/ as sysdba'`), nombre de directorio Oracle, hosts | Se conserva el valor de PRD; nunca copiar el de UAT |
| **Formato** | CRLF/LF, tabs vs espacios, espacios finales, `ESQ."OBJ"` vs `OBJ`, `/` final | No cambia la lógica; alinear solo si el usuario quiere archivos idénticos |

Formato de respuesta: tabla de archivos (bytes / hash / fecha) → tabla de diferencias por línea con columna "¿Delta?" → conclusión de 1-2 líneas ("sirve tal cual para PRD" / "no sirve, usar vigente + delta").

## Paso 3 — Armar el archivo para PRD (cuando lo pidan)

1. **Respaldar el vigente** antes de tocar nada: `prd/data/<archivo>` con `cp -p` (es el rollback). No sobrescribir si ya existe.
2. Partir del **vigente de PRD** y aplicar **solo el delta** (no copiar el archivo de UAT si tiene diferencias propias del ambiente).
3. "Toma X como referencia y actualiza los demás": confirmar primero que el **código** es idéntico (veredicto MISMO CÓDIGO); respaldar los que se sobrescriben en el scratchpad; copiar; verificar hashes iguales.
4. Validar: `.sh` → `bash -n`; PL/SQL → termina en `/` + salto de línea; `.ctl` → tabla calificada `ESQUEMA.TABLA` si se carga como sysdba.
5. No tocar bloques ajenos al delta (ej. bloques comentados) sin pedirlo; si contienen contraseñas, avisar sin mostrarlas.

## Reglas de seguridad

- Nunca imprimir líneas con `PASS`, `PASSWORD`, `USERID=`, `IDENTIFIED BY`, tokens: usar el script o `sed` que reemplace por `<REDACTED>`.
- Nunca `cat` de archivos de datos/reportes: solo `wc -l`, `md5sum`, `awk -F'|' '{print NF}'`, conteo de duplicados.
- Si aparece un PAN completo, enmascararlo (`BBBBBB******LLLL`) y pedir confirmación de que es TEST/UAT.
