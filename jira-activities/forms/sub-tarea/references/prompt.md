# Estándar de Redacción — Sub-tarea CEB

## ¿Cuándo usar este tipo?

Una sub-tarea es un ticket hijo de un CEB (Story del proyecto POD 1 - Legión de Zeus). Representa una unidad de trabajo técnico que mapea 1:1 con una rama de código y un PR.

Puede ser de tipo:

- **feat** — nueva funcionalidad o implementación
- **fix** — corrección de bug
- **chore** — tarea técnica sin impacto funcional (migración, refactor, configuración)
- **test** — pruebas unitarias, de carga o integración
- **docs** — documentación o plan de desarrollo

> Si la sub-tarea es parte de un CDPP, usar `cdpp/references/tarea-cdpp.md` en su lugar.

---

## Flujo de creación

### Paso 1 — Solicitar datos

```text
Ticket padre (CEB)  : (ej. CEB-6222)
Tipo                : (feat / fix / chore / test / docs)
Descripción corta   : (qué se va a cambiar — verbo + objeto)
Repo                : (nombre del repositorio afectado)
Responsable         : (nombre del asignado)
Contexto/motivación : (por qué se hace este cambio)
Criterios aceptación: (cuándo se considera lista)
```

### Paso 2 — Generar la sub-tarea

Usar el template en `sub-tarea/templates/template.md` como base.

---

## Reglas de redacción

### Título (summary)

```text
[TIPO] — descripción corta del cambio
```

Ejemplos:

- `[FEAT] — activar automaticAck en consumer de respuestas`
- `[FIX] — corregir tipo AMQP en propiedades numéricas de cola`
- `[CHORE] — migrar SpringFox a SpringDoc OpenAPI`
- `[TEST] — agregar suite de pruebas de carga k6`

Reglas:

- El tipo va en mayúsculas entre corchetes
- La descripción es concisa, en minúsculas, empieza con verbo en infinitivo
- El nombre del repo va dentro de la descripción del ticket, no en el título

### Descripción

- Incluir el repo afectado como primer dato
- Puede tener formato user story (`Como / Quisiera / Para`) o directo según complejidad
- Siempre incluir criterios de aceptación con `[ ]`
- Incluir antes/después en snippet de código cuando aplique
- Nunca inventar datos técnicos — usar `*(por definir)*`
