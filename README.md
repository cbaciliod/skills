# Claude Code Skills

Colección de skills para Claude Code usadas en proyectos de Novopayment.

## Skills disponibles

### [`git-workflow`](./git-workflow/)

Genera commits, pull requests y CHANGELOG siguiendo [Conventional Commits](https://www.conventionalcommits.org/).

**Cuándo se activa:** cuando el mensaje contiene `commit`, `pull request`, `PR`, `CHANGELOG`, `git diff`, `revisar cambios`.

|Capacidad|Descripción|
|-----------|-------------|
|Commits atómicos|Tipo e scope en inglés (`feat`, `fix`, `refactor`…), descripción en español|
|Pull requests|Título, descripción y checklist usando plantilla del equipo|
|División de PRs|Estrategias para PRs que superan 400 líneas o 10 archivos|
|CHANGELOG|Generación automática a partir del historial de commits|

---

### [`migrate-spring-boot-java25`](./migrate-spring-boot-java25/)

Guía y ejecuta la migración de microservicios Java de Novopayment desde **Spring Boot 2.7.x / Java 11** hacia **Spring Boot 3.5.14 / Java 25**.

Basado en el patrón probado en `api-tbs-zinli-orchestrator-microservice` (PRs #34, #40, #41).

|Fase|Tickets|Qué cubre|
|------|---------|-----------|
|Fase 1|`TICKET-UPGRADE`|Actualizar `pom.xml`, migrar `javax` → `jakarta`, tests, calidad (SpotBugs, Checkstyle)|
|Fase 2|`TICKET-OPENAPI`|Migrar SpringFox 3.0.0 → SpringDoc OpenAPI 2.8.15|
|Fase 3|`TICKET-OTL`|Implementar OpenTelemetry con exportación OTLP a New Relic|

**Prerequisito:** cada migración requiere identificar los tickets Jira asignados al microservicio antes de iniciar.

## Instalación

```bash
# Clonar en el directorio de skills de Claude Code
git clone git@github.com:cbaciliod/skills.git ~/.claude/skills
```

O agregar la ruta local en la configuración de Claude Code.
