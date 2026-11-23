# Estándar de Redacción — CDSI (Control de Solicitudes Infraestructura)

## ¿Qué es un CDSI?

**CDSI** es el proyecto Jira donde se hacen solicitudes formales al equipo **Cloud - DevOps**.
El tipo de issue es **"Solicitud de configuración"** — tipo custom del proyecto.

Se usa para cualquier configuración que requiera intervención de infraestructura:

- Variables de entorno en K8s (el caso más frecuente)
- Secrets / ConfigMaps
- Namespaces, permisos, accesos
- Configuración de pipelines CI/CD
- Certificados, balanceadores, firewall

---

## Flujo de creación

### Paso 1 — Solicitar datos

```text
Tipo de configuración : (ej: variables de entorno, secret, namespace, acceso)
Repo / Microservicio  : (nombre del repo en GitHub)
Sistema/Herramienta   : (ej: New Relic, RabbitMQ, Kubernetes, ArgoCD)
Ambientes             : (TEST / UAT / PRD — puede ser uno o varios)
Variables / Config    : (lista de variables con nombre y valor por ambiente)
Ticket CEB relacionado: (ej: CEB-6222 — si aplica)
```

### Paso 2 — Generar el ticket

- Se crea **un ticket por ambiente** (TEST, UAT, PRD por separado)
- Los tickets de ambientes adicionales se marcan como clones del primero
- Usar el template en `cdsi/templates/template.md` como base

---

## Reglas de redacción

### Título (summary)

```text
Solicita configuración de <tipo> <AMBIENTE> - <nombre-del-repo> - <sistema>
```

Ejemplos reales:

- `Solicita configuración de variables de entorno TEST - api-tbs-zinli-orchestrator-microservice - New Relic`
- `Solicita configuración de variables de entorno UAT - api-tbs-zinli-orchestrator-microservice - New Relic`
- `Solicita configuración de variables de entorno PRD - api-tbs-dbs-orchestrator-microservice - RabbitMQ`
- `Solicita configuración de secret TEST - api-tbs-payment-microservice - credenciales DB`

Reglas:

- El ambiente va en mayúsculas: `TEST`, `UAT`, `PRD`
- El nombre del repo va completo
- El sistema o herramienta afectada va al final

### Descripción

- Tono directo: "Estimados, se solicita..."
- Incluir link al repo en GitHub
- Las variables en bloque de código YAML (`- name: / value:`)
- Un bloque por ambiente si se piden varios en el mismo ticket
- Sin secciones elaboradas — el equipo de infra solo necesita qué configurar y dónde

---

## Variantes frecuentes (además de variables de entorno)

Títulos con etiquetas entre corchetes: `[CLIENTE][AMBIENTE][EQUIPO] Solicitud de …`.
Secciones con H2 en verde (ver `SKILL.md` → "Publicar en Jira").

| Variante | Equipo | Secciones | Ejemplo de título |
|---|---|---|---|
| **Apoyo para diagnosticar un incidente** | BD | Contexto → Hallazgos (de tickets previos) → ¿En qué nos gustaría su apoyo? | `[MIO][UAT][DB] Solicitud de apoyo: validar evento en la BD el <fecha> (<error>)` |
| **Recursos vigentes de producción** (código de packages, `.ctl`, `.sh`) para preparar un pase | BD | Contexto (pase a PRD, no homologación) → ¿En qué…? (lista de objetos y rutas) → Datos del ambiente → Entrega (Keeper, no adjuntos) | `[MIO][PRD][DB] Solicitud de recursos de producción: <PACKAGE> (spec y body), <archivos>` |
| **Logs de un proceso agendado** | Infra / BD | Contexto → ¿En qué…? (log del agendado por paso, salida del script) → Datos del ambiente (agendado, script, ruta del log, fecha de corrida) → Entrega | `[MIO][UAT] Solicitud de logs del agendado <proceso> - Corrida <fecha>` |
| **Cambio de objeto de BD** (directorio Oracle, grants) | BD | Contexto (por qué) → ¿En qué…? (desde → hacia) → Datos del ambiente → Resultado esperado + query de validación | `[MIO][UAT][DB] Solicitud de apoyo: homologar el directorio <NOMBRE> con Producción` |
| **Redirección NGINX / ruteo** | Cloud-DevOps | 📌 Descripción → 🎯 Objetivo (ruta origen → destino) → 🔎 Ejemplo funcional (`curl` con `Bearer <token>`) → 🧪 Resultado esperado | `[ZINLI][TEST][GOLANG][NGINX] Configuración NGINX para redirigir <endpoint> JAVA a Golang` |

### Reglas para estas variantes

- **Imitar el ticket de referencia** que indique el usuario (mismo orden de secciones, emojis, nivel de detalle).
- **Pedir, no prescribir**: no incluir bloques `location`, regex, comandos `CREATE DIRECTORY`, etc. Se indica qué se necesita y el resultado esperado. Las dudas técnicas se comentan al usuario en el chat, no en el ticket.
- **Datos del ambiente** en tabla: cliente, ambiente, esquema, servidor/rol (sin credenciales), rutas.
- **Entrega de archivos sensibles** (código de producción, logs con datos): vía Keeper, nunca adjuntos al ticket; esperar VoBo.
- **Nombres exactos**: agendado (`uat_<cliente>_<proceso>.json`), script, rutas de log. Si no se conocen, buscarlos en tickets CDSI anteriores con JQL (`text ~ "<proceso>"`) antes de dejar *(por definir)*.
- **Incluir la query de validación** cuando el cambio sea verificable con SQL (ej. `SELECT directory_name, directory_path FROM dba_directories WHERE directory_name = '<NOMBRE>';`).
