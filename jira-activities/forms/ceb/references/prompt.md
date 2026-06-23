# Estándar de Redacción — CEB (Story)

## ¿Qué es un CEB?

**CEB es el project key del proyecto Jira "POD 1 - Legión de Zeus"** (equipo de desarrollo interno de Novo). Un ticket CEB es una **Story** de desarrollo dentro de ese proyecto. No es un formulario de cambio — es un ticket técnico con descripción detallada, fases de implementación y criterios de aceptación.

Se crea para cualquier iniciativa técnica del equipo: features, deuda técnica, bugs, migraciones, mejoras de performance, etc.

---

## Flujo de creación

### Paso 1 — Solicitar datos

```text
Producto/Cliente     : (ej: Billet, Zinli, DBS, MIO, COOP29)
Tipo                 : (ej: DEUDA TECNICA, FEATURE, BUG, MIGRACION)
Scope                : (ej: INTERNO, EXTERNO)
Componente/Repo      : (nombre del microservicio o sistema)
Descripción corta    : (qué se va a hacer)
Repo de referencia   : (si aplica — repo del que se toman cambios ya validados)
Tickets origen       : (tickets relacionados, ej: CEB-XXXX, CEB-YYYY)
Epic padre           : (CEB-XXXX)
Sprint               : (si aplica)
Responsable técnico  :
Fecha límite         :
Canal de seguimiento : (link hilo Teams/Slack si aplica)
```

### Paso 2 — Construir la descripción

Usar el template en `ceb/templates/template.md`. La descripción tiene 9 secciones fijas:

1. Header con repos, fecha, tickets origen y canal
2. Contexto — por qué existe y qué problemas resuelve
3. Alcance — dentro y fuera de scope
4. Fases / entregables — cada fase es un PR independiente con sub-tareas y criterios de aceptación
5. Inventario de diferencias estructurales — tabla comparativa (si aplica)
6. Riesgos y mitigaciones — tabla
7. Plan de rollout — orden de despliegue por ambientes
8. Backlog — mejoras fuera del alcance del ticket actual
9. Definición de Done — checkboxes por fase

### Paso 3 — Crear el ticket en Jira

Crear como **Story** en el proyecto **CEB** con:

- Summary construido con el formato de título
- Descripción completa según template
- Epic parent asignado
- Sprint asignado si corresponde

---

## Reglas de redacción

### Título (summary)

```text
[PRODUCTO] [TIPO] [SCOPE] Componente — descripción corta
```

Ejemplos reales:

- `[BILLET] [DEUDA TECNICA] [INTERNO] Mejoras de RabbitMQ, performance y robustez en api-tbs-dbs-orchestrator-microservice`
- `[ZINLI] [FEATURE] [EXTERNO] Migración endpoint getTotalAmount en Go`
- `[MIO] [BUG] SDK Visa — error CVV en transacciones tokenizadas contactless`

### Descripción

- Usar Markdown con encabezados numerados (`## 1.`, `## 2.`, etc.)
- Cada fase de implementación incluye: archivo a modificar, referencia (repo/commit), síntoma que resuelve, criterios de aceptación con `[ ]`
- Tablas para comparativos y riesgos
- Nunca inventar datos — usar placeholder `*(por definir)*`
- Referenciar commits concretos cuando los cambios vienen de otro repo
