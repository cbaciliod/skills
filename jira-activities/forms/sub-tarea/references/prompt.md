# Estándar de Redacción — Sub-tarea

## ¿Cuándo usar este tipo?

Una sub-tarea es un ticket hijo dentro de un ticket padre en Jira. Puede ser subtarea de:
- Una Historia de usuario
- Un CDPP (pases a producción)
- Un CDSI (solicitudes de infraestructura)
- Un GPBD (proyectos de BD)
- Cualquier epic o tarea padre

> Si la sub-tarea es parte de un CDPP, usar `cdpp/references/tarea-cdpp.md` en su lugar.

---

## Flujo de creación

### Paso 0 — Identificar el ticket padre

Preguntar al usuario:
- ¿Cuál es el ticket padre? (número Jira)
- ¿Cuál es el propósito de la sub-tarea?
- ¿Quién será el responsable/asignado?

### Paso 1 — Solicitar datos

Completar este formulario si el usuario no los proporciona:

```
Ticket padre    : (ej. NOVA-1234 / CDPP-XXXX)
Título          : (acción concreta — verbo + objeto)
Equipo/Squad    : (ej. Backend, Infra Middleware, QA)
Responsable     : (nombre del asignado)
Estimación      : (horas o story points)
Sprint/Versión  : (opcional)
Descripción     : (qué se hace y por qué)
Criterio aceptación: (cuándo se considera lista)
```

### Paso 2 — Generar la sub-tarea

Usar el template en `sub-tarea/templates/template.md` como base.

---

## Reglas de redacción

**Título:**
- Formato: `[EQUIPO] Acción — descripción corta`
- Usar verbos de acción: *Configurar, Desplegar, Validar, Crear, Actualizar, Revisar*
- Ejemplos:
  - `[Infra Middleware] Configurar variables de entorno — microservicio api-tbs-payment`
  - `[QA] Validar flujo de pago recurrente en ambiente staging`
  - `[Backend] Actualizar dependencia hikari-cp a 5.1.0`

**Descripción:**
- Explicar QUÉ se hace, POR QUÉ se hace, y CÓMO se valida
- Incluir pasos de ejecución si es una tarea técnica
- Incluir criterio de aceptación claro
- Nunca inventar datos técnicos — usar `*(por definir)*`

**Secciones obligatorias (tareas técnicas):**
1. ¿Qué se va a hacer?
2. ¿Por qué se hace?
3. Pasos de ejecución
4. Validación / Criterio de aceptación
5. Dependencias (si las hay)
