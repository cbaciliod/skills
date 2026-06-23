# Estándar de Redacción — GPBD (Gestión de Proyectos de Base de Datos)

## ¿Cuándo usar este tipo?

Un ticket GPBD se crea para gestionar cambios planificados en bases de datos que requieren coordinación formal con el equipo de DBA (Infra BD). Aplica para:
- Scripts DDL: CREATE, ALTER, DROP de tablas, índices, sequences, paquetes, procedimientos
- Scripts DML masivos: INSERT, UPDATE, DELETE que afectan datos de producción
- Migraciones de esquema entre versiones
- Creación o modificación de jobs/schedulers de base de datos
- Optimizaciones de performance (índices, estadísticas, recompilación)
- Backups puntuales o restauraciones parciales controladas

> Si el cambio de BD es parte de un pase a producción, crear subtarea dentro del CDPP usando `cdpp/references/tarea-cdpp.md`.

---

## Flujo de creación

### Paso 0 — Clasificar el cambio

Preguntar al usuario:
- ¿Es DDL (estructura) o DML (datos)?
- ¿Afecta tablas de producción con datos reales?
- ¿Requiere ventana de mantenimiento o puede ejecutarse en línea?
- ¿Hay scripts ya escritos o se deben redactar?

### Paso 1 — Solicitar datos

```
Tipo de cambio       : (DDL / DML / migración / job / optimización / otro)
Motor de BD          : (Oracle / PostgreSQL / MySQL / otro)
Esquema/Base de datos: 
Objetos afectados    : (tablas, índices, paquetes, etc.)
Ambiente             : (PRD / STG / DEV)
Urgencia             : (normal / urgente)
Solicitante          : (nombre + equipo)
Responsable DBA      : (si ya está asignado)
Fecha planificada    : 
Ticket relacionado   : (historia, CDPP, incidente)
Descripción técnica  : (qué se ejecuta y por qué)
Scripts              : (adjuntar o describir los scripts)
Criterio de aceptación: 
Plan de rollback     : (cómo se revierte)
```

### Paso 2 — Generar el ticket GPBD

Usar el template en `gpbd/templates/template.md` como base.

---

## Reglas de redacción

**Título:**
- Formato: `[GPBD][MOTOR][AMBIENTE] Tipo — esquema.objeto`
- Ejemplos:
  - `[GPBD][Oracle][PRD] DDL — schema_payments.TBL_TRANSACTIONS (ALTER)`
  - `[GPBD][Oracle][PRD] DML — schema_reports.PACK_REPORTES_TUPANA (UPDATE masivo)`
  - `[GPBD][PostgreSQL][STG] Migración — novopay_core schema v2.3 → v2.4`

**Secciones obligatorias:**
1. Descripción del cambio
2. Objetos afectados (tabla con esquema, objeto, tipo de cambio, registros estimados)
3. Script(s) de ejecución (o placeholder si están en adjunto)
4. Orden de ejecución
5. Validaciones post-ejecución
6. Plan de rollback
7. Estimación de ventana y tiempo

**Reglas adicionales:**
- Nunca inventar nombres de tablas, esquemas o columnas — usar `*(por definir)*`
- Si el script modifica datos reales, indicar el número estimado de registros afectados
- El plan de rollback debe ser ejecutable independientemente del script principal
