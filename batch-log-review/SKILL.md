---
name: batch-log-review
description: >
  Analiza logs de procesos agendados (batch-commons-framework: pasos copy_local, upload, execute_command, download, encrypt…) y de cargas Oracle (SQL*Loader + SQL*Plus + PL/SQL con UTL_FILE) para decir en minutos si la corrida funcionó, por qué cargó 0 filas o por qué el reporte salió vacío. Da comandos seguros para validar en el servidor sin exponer PAN ni contraseñas. Activa este skill cuando el mensaje contenga (sin distinguir mayúsculas) palabras como: log del agendado, corrida, agendado, sqlldr, SQL*Loader, rows loaded, cargó 0, reporte vacío, no se generó el reporte, ORA-, FALLIDA, EXITOSA, .bad, batch. Si la intención no es clara, pregunta ¿quieres que analice el log de una corrida?
---

# Batch Log Review — diagnóstico de corridas agendadas y cargas Oracle

## Paso 1 — Leer el log de forma segura

Si el log es un archivo local, leerlo enmascarando dígitos largos:

```bash
grep -c -E '[0-9]{13,19}' <log>          # ¿hay posibles PAN?
sed -E 's/([0-9]{6})[0-9]{3,9}([0-9]{4})/\1******\2/g' <log>
```

En logs de SQL*Loader omitir las líneas de definición de columnas (`FIRST`/`NEXT`).

## Paso 2 — Tabla de la corrida (siempre)

| Paso | Qué buscar | Señal de problema |
|---|---|---|
| copy_local | archivos copiados, **tamaño y líneas** | NP/CTF de **1 línea** = solo encabezado |
| upload | `put X X` hacia `…/data/` | Pisa cualquier archivo dejado a mano con el mismo nombre |
| execute_command / SQL*Loader | `N Rows successfully loaded`, `skipped/read/rejected/discarded` | `read: 0` (entrada vacía), `rejected > 0` (ver `.log` y `.bad`) |
| PL/SQL | `ERRORS ==> …`, `ORA-xxxxx` | Un `WHEN OTHERS` que solo imprime deja `successfully completed` aunque falle |
| download | tamaño y líneas del reporte | Reporte de 1 línea = solo encabezado; `not found` = no se generó |
| correo | `[EXITOSA]` / `[FALLIDA]` | EXITOSA con reporte vacío es posible (valida ≥1 línea) |

Comparar con corridas anteriores en una tabla (fecha, entrada, cargadas, reporte, correo): la causa suele estar en qué cambió entre una y otra.

## Paso 3 — Árbol de diagnóstico

| Síntoma | Causa probable | Cómo confirmarlo |
|---|---|---|
| `0 Rows loaded`, `skipped: 1`, `read: 0` | Archivo de entrada solo con encabezado | Tamaño del respaldo `data/backups/` ≈ tamaño del encabezado |
| Archivo de prueba "dejado en el servidor" no se cargó | El agendado lo pisó en el paso upload, o se dejó en otra ruta | `ls -l --time-style=+%F_%T` del archivo y su respaldo; el origen real es la carpeta del NFS del día |
| `ORA-29280: invalid directory object` | Directorio Oracle de `UTL_FILE.FOPEN` no existe en ese ambiente | `SELECT directory_name, directory_path FROM dba_directories WHERE directory_name = '<NOMBRE>';` |
| N filas cargadas, reporte de 1 línea, sin `ERRORS ==>` | Body compilado sin el cambio, o JOIN sin coincidencias | `all_objects.last_ddl_time` + `all_source` de las líneas del cursor; `COUNT(*)` del JOIN con la tabla cargada |
| `ORA-01722` en una consulta manual | Comparar `VARCHAR2` con un número sin comillas | Usar `'…'` o variable `:pan` |
| `.bad` presente | Puede ser de una corrida antigua (SQL*Loader no lo borra si no hay rechazos) | Ver su fecha; renombrarlo antes de la siguiente prueba |

## Paso 4 — Comandos para el usuario (solo conteos)

```bash
cd <ruta>/cargadores
ls -l --time-style=+%F_%T data/backups/<ARCHIVO>.txt   # ¿qué entró realmente?
tail -n 12 carga/log/<ARCHIVO>.log                     # resumen skipped/read/rejected
ls -l --time-style=+%F_%T carga/bad/<ARCHIVO>.bad 2>&1 # NO hacer cat: tiene PAN
awk -F'|' '{print NR": TC="$1" campos="NF}' <archivo> | head   # estructura sin datos
awk 'NR>1' <archivo> | sort | uniq -d | wc -l           # duplicados exactos
```

Para el reporte generado: `wc -l` y conteo de campos/TC. Nunca pedir que peguen filas completas.

## Reglas

- Si el usuario pega un PAN completo: no repetirlo, enmascararlo y pedir confirmación escrita de que es TEST/UAT antes de seguir.
- Si un script muestra contraseñas, mostrarlas como `<REDACTED>` y avisar.
- Corregirse explícitamente si un log nuevo invalida una conclusión anterior ("me equivoqué: …").
- Cerrar con veredicto: **validado de punta a punta** / **problema de datos** / **problema de código**, y el siguiente paso.
