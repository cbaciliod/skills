# Playbook — Microservicio Emergente (Kubernetes Rolling Update)

**Tipo de pase:** EMERGENTE  
**Equipo ejecutor:** Infra Middleware  
**Genera indisponibilidad:** No  
**Ticket modelo:** [CDPP-35117](https://jira4novo.atlassian.net/browse/CDPP-35117) ✅ validado  

---

## Cuándo usar este playbook

- Despliegue de un microservicio Java / Spring Boot en Kubernetes.
- El cambio atiende uno o más incidentes críticos en producción.
- Puede incluir: migración de Java version, migración de broker o integraciones,
  variables de entorno nuevas, actualización de librerías críticas.
- No requiere ventana de mantenimiento (K8s rolling update).

---

## Estructura de subtareas

```
CDPP-XXXXX (padre — Requirement Pass)
├── PASO 1: [Infra Middleware] Kubernetes - Rolling Update - <componente>
│   Config de variables + preparación pre-despliegue
│   → cdpp-template.md + subtarea-config-template.md
│   Asignado: desarrollador / analista
│
└── PASO 2: Desplegar microservicio
    Ejecución real del despliegue (GitHub Actions)
    → subtarea-deploy-template.md
    Asignado: Infra Middleware (Guillermo Infante Martinez)
```

---

## Archivos de este playbook

| Archivo | Descripción |
|---|---|
| `cdpp-template.md` | Plantilla del ticket CDPP principal |
| `subtarea-config-template.md` | Plantilla PASO 1 — configuración, variables, preparación |
| `subtarea-deploy-template.md` | Plantilla PASO 2 — ejecución del despliegue (formato simple) |

---

## Datos a solicitar al usuario

```
- Nombre del componente (ej: api-tbs-zinli-orchestrator-microservice):
- Versión a desplegar (ej: v2.3.3):
- Versión actual en PRD:
- Namespace / Cluster en PRD:
- Ticket de certificación CEB:
- Cliente:
- País:
- Descripción del incidente o problema que origina el pase:
- Mejoras incluidas en la versión (lista):
- Variables de entorno nuevas (nombre | valor PRD | descripción):
- Variables existentes que ahora se validan en startup:
- ¿Migración de Java, runtime o dependencias críticas? (SI → cuáles):
- ¿Migración de broker, BD u otras integraciones? (SI → cuáles):
- ¿Link de GitHub Actions del despliegue? (para PASO 2):
- Equipo de soporte (Líder Técnico + Analista):
```

---

## Lecciones aprendidas de CDPP-35117

- Nombrar cada incidente con fecha concreta en Situación Inicial.
- Separar variables en dos grupos en PASO 1: nuevas vs existentes validadas.
- Incluir el bloque YAML completo del ConfigMap listo para aplicar.
- El rollback de imagen siempre va acompañado del rollback del ConfigMap si hay variables nuevas.
- `ENV_RABBIT_PASSWORD` y credenciales similares → `*(sensible — Secret K8s)*` en tablas.
- PASO 2 lo ejecuta Infra (no el desarrollador) — asignarlo a Guillermo Infante Martinez o quien corresponda.
- Confirmar el namespace con el usuario — no asumir `prd-api-backend`.
