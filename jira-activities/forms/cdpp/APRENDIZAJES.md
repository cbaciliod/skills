# Memoria de Aprendizaje — CDPP Skill

Registro de tipos de pase validados, patrones aprendidos y artefactos
disponibles. Se actualiza cada vez que un nuevo tipo de pase es revisado y
aprobado por el Líder Técnico.

---

## Cómo usar este archivo

- Antes de generar un CDPP, consultar este registro para ver si existe un
  playbook validado para el tipo de pase solicitado.
- Si existe → ir a `playbooks/<nombre>/` y usar las plantillas.
- Si no existe → generar con `references/prompt-cdpp.md` y, una vez aprobado
  por el Líder Técnico, registrar aquí el nuevo tipo.

---

## Registro de Tipos de Pase

| ID | Tipo | Subtipo | Estado | Ticket modelo | Playbook | Fecha |
|---|---|---|---|---|---|---|
| PT-001 | Microservicio | Emergente — K8s Rolling Update + migración de dependencias | ✅ Validado | [CDPP-35117](https://jira4novo.atlassian.net/browse/CDPP-35117) | `playbooks/emergente-microservicio-k8s/` | 2026-06-19 |

---

## PT-001 — Microservicio Emergente (K8s Rolling Update)

**Validado por:** Gustavo Lopez — Líder Técnico Backend  
**Fecha de validación:** 2026-06-19  
**Ticket modelo:** [CDPP-35117](https://jira4novo.atlassian.net/browse/CDPP-35117)  
**Subtareas modelo:** [CDPP-35124](https://jira4novo.atlassian.net/browse/CDPP-35124) (config), [CDPP-35132](https://jira4novo.atlassian.net/browse/CDPP-35132) (deploy)

### Cuándo usar este playbook

- Despliegue de un microservicio Spring Boot / Java en Kubernetes.
- El cambio atiende un incidente crítico o bug en producción (tipo EMERGENTE).
- Puede incluir: migración de Java version, migración de broker/integraciones,
  variables de entorno nuevas, actualización de librerías.
- No genera indisponibilidad (rolling update).

### Artefactos validados

| Artefacto | Archivo | Estado |
|---|---|---|
| CDPP (ticket principal) | `playbooks/emergente-microservicio-k8s/cdpp-template.md` | ✅ |
| Subtarea PASO 1 — Configuración y variables | `playbooks/emergente-microservicio-k8s/subtarea-config-template.md` | ✅ |
| Subtarea PASO 2 — Ejecución del despliegue | `playbooks/emergente-microservicio-k8s/subtarea-deploy-template.md` | ✅ |
| Anexo 1 — Plan de Pase a Producción | *(generar con `references/prompt-anexo1.md`)* | ✅ probado |
| Anexo 4 — Plan de Pruebas Postproducción | *(generar con `references/prompt-anexo4.md`)* | ✅ probado |

### Estructura de subtareas real (2 pasos)

```
CDPP-35117 (padre)
├── CDPP-35124 — PASO 1: [Infra Middleware] Config + variables + prep  → Done ✅
└── CDPP-35132 — PASO 2: Desplegar microservicio (tabla simple + GitHub Actions) → Done ✅
```

### Patrones aprendidos

- **Situación Inicial:** nombrar cada incidente con fecha y síntoma concreto. Si
  hay más de uno, un bloque por incidente. Al final, lista de problemas
  adicionales identificados (no solo los incidentes que detonaron el pase).
- **Situación Final:** un bullet por cada mejora técnica. Terminar siempre con
  la frase de alcance acotado.
- **Plan de Rollback:** 3 bloques obligatorios: Consideraciones, Acciones
  numeradas, Alcance. Si hay variables nuevas en el ConfigMap → el rollback de
  imagen siempre va acompañado del rollback del ConfigMap.
- **Subtarea PASO 1 (config):** separar las variables en dos grupos:
  "Variables nuevas (requieren configuración antes del despliegue)" y
  "Variables existentes ahora validadas en startup". Incluir el bloque YAML
  completo del ConfigMap listo para aplicar.
- **Subtarea PASO 2 (deploy):** formato simple. Solo la tabla de despliegue con
  POD, APPSERVER, NOMBRE WAR (N/A para micros), job (N/A), y el link del run de
  GitHub Actions. Asignado al equipo de Infra Middleware (no al desarrollador).
- **Assignee real del despliegue:** Guillermo Infante Martinez (Infra). El
  desarrollador (cbacilio) es quien crea el CDPP y la subtarea de configuración.
- **Namespace:** confirmar siempre con el usuario — puede ser `uat-api-backend`,
  `prd-api-backend` u otro según el ambiente y el cliente.
- **Variables OTEL:** el ConfigMap real incluye también las variables de
  OpenTelemetry (`ENV_OTEL_DISABLED`, `ENV_OTEL_EXPORTER_OTLP_ENDPOINT`,
  `ENV_OTEL_EXPORTER_OTLP_PROTOCOL`) aunque no se documenten explícitamente en
  el CDPP como variables "del cambio".

### Lecciones aprendidas

- No asumir `prd-api-backend` como namespace. Leer la subtarea o preguntar.
- No asumir el host de RabbitMQ. CDPP-35117 menciona `rabbitmq.novopayment.net`
  pero CDPP-35124 muestra `prod-rabbitmq.novopayment.net`. La fuente de verdad
  es la subtarea de configuración, no el CDPP.
- `ENV_RABBIT_PASSWORD` se valida en startup pero nunca se loguea. En la tabla
  de variables mostrar `*(sensible — gestionar vía Secret K8s)*`.
- El título del CDPP en Jira real usa `[PRD][CLIENTE]` sin país ni tipo. El
  formato del prompt incluye país y tipo — ajustar al estilo del proyecto.

---

## Tipos pendientes de registrar

Los siguientes tipos son conocidos pero aún no tienen un ticket modelo validado:

| Tipo | Observación |
|---|---|
| Standard — Microservicio K8s | Similar a PT-001 pero sin urgencia de incidente |
| Normal — Base de Datos DDL Oracle | Basado en CDPP-34680 — pendiente de documentar como playbook |
| WAR / JBoss | Pendiente de primer caso real |
| Configuración pura (solo ConfigMap) | Pendiente de primer caso real |
| Proceso Agendado / Batch | Pendiente de primer caso real |
| Infraestructura (certificados, LB) | Pendiente de primer caso real |

---

## Lecciones — Base de Datos Oracle + Proceso Batch (BASE II MIO, nov-2026)

Pase en 2 subtareas: PASO 1 BD (tabla de paso + recompilación del body) bloquea
PASO 2 servidor del cargador (`.ctl` + `.sh`). Aún no es playbook validado.

### Armado de los archivos del pase

- Partir **siempre del vigente de producción** (pedirlo por CDSI a BD) y aplicar
  **solo el delta**. Nunca subir a PRD el archivo de UAT: rutas, `ORACLE_SID`,
  conexión (PRD usa `'/ as sysdba'`) y directorios Oracle difieren.
- Guardar el vigente como rollback **antes** de editar (ej. `prd/data/`).
- Comparar test / uat / prd con diff **lógico** (ignorando CRLF, espacios y
  encabezado `ESQUEMA."OBJETO"`) y clasificar cada diferencia: *delta*,
  *propio del ambiente* o *formato*. Ver skill `env-compare`.
- Spec del package: si no cambia, **no se ejecuta**; decirlo en el CDPP.
- Body PL/SQL: debe terminar en `/` + salto de línea para SQL*Plus y Flyway.
- `.ctl` con tabla calificada (`ESQUEMA.TABLA`) cuando el cargador conecta como sysdba.
- `.sh`: validar con `bash -n`; no tocar bloques ajenos al delta, pero avisar si
  contienen contraseñas.

### Directorios Oracle (`UTL_FILE`)

- `ORA-29280: invalid directory object` = el nombre del directorio no existe en
  ese ambiente. Homologar el **nombre** del directorio entre ambientes (CDSI a BD)
  para que el mismo body sirva en UAT y PRD.

### Validación en UAT antes del pase

- La certificación es válida solo con **datos**: verificar en el log de
  SQL*Loader `read: N`, `rejected: 0` y que el reporte generado tenga N+1 líneas.
  Un reporte de 1 línea = solo encabezado (o entrada vacía, o JOIN sin match, o
  body sin el delta). Ver skill `batch-log-review`.
- Confirmar qué versión del body está compilada: `all_objects.last_ddl_time` +
  `all_source` filtrando las líneas del delta.

### Flyway (repo de migraciones de BD)

- Estructura `flyway/oracle/{tst,stg,prd}/<ESQUEMA>/migrations/V<yyyyMMddHHmm>__<TICKET>_<desc>.sql`;
  el mismo archivo se replica en los 3 ambientes. Merge a `main` dispara la migración.
- Verificar que la carpeta del esquema exista antes de proponerlo en el CDPP.
- DDL de tabla y body en **migraciones separadas** (el DDL hace commit implícito).
- Rollback = **nueva migración** con el body vigente; nunca editar una migración aplicada.

---

## Cómo registrar un nuevo tipo

Cuando un nuevo CDPP sea aprobado por el Líder Técnico:

1. Leer el ticket principal y todas sus subtareas.
2. Crear el directorio `playbooks/<tipo-nombre>/`.
3. Extraer las plantillas del ticket real → crear `cdpp-template.md`,
   `subtarea-*-template.md`.
4. Crear el `README.md` del playbook con: cuándo usarlo, artefactos,
   estructura de subtareas, patrones y lecciones.
5. Agregar la entrada en la tabla "Registro de Tipos" de este archivo.
6. Agregar el bloque de detalle con patrones y lecciones aprendidas.
