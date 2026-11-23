---
name: jira-activities
description: >
  Crea, redacta y ACTUALIZA tickets Jira de NovoPayment siguiendo los estándares del equipo: CEB (story), sub-tarea, CDSI (solicitudes a Cloud-DevOps, BD e Infra) y CDPP (pase a producción). Publica directo en Jira con títulos verdes (ADF) usando scripts/md2adf.py. Activa este skill cuando el mensaje contenga (sin distinguir mayúsculas) un link o clave de Jira (CEB-, CDSI-, CDPP-, …/browse/) o palabras como: jira, ticket, actividad, crear tarea, actualiza el ticket, redacta el ticket, sub-tarea, subtarea, ceb, cdsi, cdpp, solicitud infraestructura, solicitud a base de datos, control de solicitudes. Si la intención no es clara, pregunta ¿quieres crear o actualizar una actividad en Jira?
---

# Skill: Jira Activities

## Modo rápido — actualizar o redactar un ticket existente (caso más frecuente)

Si el mensaje trae un link o clave de ticket (ej. "actualiza CDSI-13779 en base a CDSI-13778"), **no muestres el menú ni el formulario**:

1. **Leer en paralelo** el ticket destino y los tickets de referencia (`getJiraIssue`, `responseContentFormat: markdown`; agrega `comment` e `issuelinks` en `fields` cuando la respuesta del otro equipo importe).
2. **Identificar el tipo** por la clave (CEB / CDSI / CDPP / sub-tarea) y leer **solo** la referencia de ese tipo (tabla del Paso 1).
3. **Redactar** en Markdown siguiendo el ticket de referencia que dio el usuario (estructura, tono, nivel de detalle). Si el usuario dice "similar a X", imitar X, no el template genérico.
4. **Checklist de seguridad** (sección abajo) antes de publicar.
5. **Publicar** con ADF y títulos en verde (sección "Publicar en Jira").
6. **Responder corto**: link, qué cambió y qué quedó como *(por definir)*. Ofrecer como mucho 1 siguiente paso.

Correcciones del usuario ("no es para homologar", "no pongas la config") → rehacer **solo** la parte señalada y republicar; no reabrir el resto.

---

## Flujo de creación (ticket nuevo sin referencia)

### Paso 0 — Mostrar menú de tipos

Si el usuario no especificó el tipo, presenta este menú:

```
¿Qué tipo de actividad Jira quieres crear?

1. CEB       — Story de desarrollo (POD 1 - Legión de Zeus)
2. Sub-tarea — Subtarea técnica de un CEB (1 rama = 1 sub-tarea)
3. CDSI      — Solicitud a Cloud-DevOps / BD / Infra
4. CDPP      — Pase a producción (ver forms/cdpp/SKILL.md)

Responde con el número o el nombre del tipo.
```

Si el usuario ya mencionó el tipo, ir directo al flujo sin mostrar el menú.

### Paso 1 — Ejecutar flujo del tipo seleccionado

| Tipo | Referencia | Template |
|------|-----------|----------|
| CEB | `forms/ceb/references/prompt.md` | `forms/ceb/templates/template.md` |
| Sub-tarea | `forms/sub-tarea/references/prompt.md` | `forms/sub-tarea/templates/template.md` |
| CDSI | `forms/cdsi/references/prompt.md` | `forms/cdsi/templates/template.md` |
| CDPP | `forms/cdpp/SKILL.md` | `forms/cdpp/playbooks/` |

---

## Publicar en Jira (ADF con títulos verdes)

Las descripciones del equipo usan **títulos H2 en verde `#36b37e`**. Markdown plano pierde el color, así que se publica en ADF:

```bash
# 1. Escribe el borrador en Markdown (## títulos, tablas, listas, ```sql, > notas)
# 2. Convierte y valida
python3 -I jira-activities/scripts/md2adf.py borrador.md --check
python3 -I jira-activities/scripts/md2adf.py borrador.md > descripcion.json
# 3. editJiraIssue con contentFormat: "adf" y fields.description = contenido de descripcion.json
```

Reglas aprendidas (Jira responde `INVALID_INPUT` si se rompen):

- La marca `code` **no se combina** con `strong`/`em`/`textColor`: `**\`X\`**` no es válido. El script ya lo resuelve; si armas ADF a mano, separa los nodos.
- Links a Jira (`…/browse/KEY-123`) van como `inlineCard` (smart link); el script lo hace solo.
- Al **leer** un ticket, el MCP siempre devuelve Markdown: no se puede verificar el color leyendo. Confía en el ADF enviado.
- `addCommentToJiraIssue` puede estar bloqueado por permisos: si falla, entrega el texto listo para pegar y no reintentes.
- Comentarios y textos cortos pueden ir en Markdown; la **descripción** siempre en ADF.

---

## Checklist de seguridad (antes de publicar o responder)

- **PAN** → `BBBBBB******LLLL`; cuenta → `BB********LLLL`; vencimiento → `*M/*Y`; CVV → `**X`. Nunca completos, tampoco en consultas SQL de ejemplo (usar `:pan` / `<NUMERO_DE_TARJETA>`).
- **Contraseñas, tokens, llaves**: nunca. En ejemplos `curl` usar `Bearer <token>`. Si aparecen en logs o scripts, redactar como `<REDACTED>` y avisar.
- Si el usuario pega datos de tarjeta, pedir confirmación explícita de que son de TEST/UAT antes de procesarlos.
- No abrir con `cat` archivos `.bad`, NP/CTF o reportes con PAN: usar conteos (`wc -l`, `awk -F'|' '{print NF}'`).

---

## Reglas generales

- **Nunca inventar datos**: usar `*(por definir)*` cuando no esté disponible (puerto, PR, link de Keeper, CDPP del pase).
- **Pedir, no prescribir** (CDSI): decir qué se necesita (desde → hacia, resultado esperado); el equipo ejecutor ya sabe cómo configurarlo.
- **Mantener coherencia** entre el ticket principal, sus subtareas y los archivos del pase.
- **Contexto correcto**: si es para un pase a producción, decirlo así (no "homologación"); si es apoyo a otro equipo, redactar como solicitud de apoyo.
- **Un ticket por ambiente** cuando el cambio es de infraestructura (TEST / UAT / PRD).

## Estructura del directorio

```
jira-activities/
├── SKILL.md              ← este archivo (modo rápido, menú, publicación, seguridad)
├── README.md
├── scripts/
│   └── md2adf.py         ← Markdown → ADF con títulos verdes + validación
└── forms/
    ├── cdpp/             ← Control de Pase a Producción (SKILL.md, playbooks, APRENDIZAJES)
    ├── cdsi/             ← Solicitudes a Cloud-DevOps / BD / Infra
    ├── ceb/
    ├── sub-tarea/
    ├── historia/
    └── gpbd/
```
