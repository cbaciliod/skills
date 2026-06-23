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
