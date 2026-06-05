# Changelog

Todos los cambios notables de este repositorio se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.0.0/) y el versionado usa [Semantic Versioning](https://semver.org/lang/es/).

---

## [1.0.1] - 2026-06-05

- style(readme): compactar formato de tablas en README principal
- docs(migrate): corregir MD036 reemplazando `**bold**` por `####` headings en fases
- chore(git-workflow): eliminar CHANGELOG redundante, historial consolidado en raíz
- docs(changelog): agregar entrada de migrate-spring-boot-java25 e incorporar historial de git-workflow

---

## [1.0.0] - 2026-06-05

- docs: agregar README con resumen de skills disponibles
- chore: limpiar archivos duplicados en raíz, skills organizadas en subcarpetas
- chore: merge historial remoto de git-workflow al nuevo repo skills
- chore: initial commit — agregar skills git-workflow y migrate-spring-boot-java25

---

## [migrate-spring-boot-java25 1.0.0] - 2026-06-05

- feat: skill `migrate-spring-boot-java25` para migrar microservicios de Spring Boot 2.7.x / Java 11 a Spring Boot 3.5.14 / Java 25
- docs: agregar `references/pom-changes.md` con cambios de dependencias, plugins y versiones de librerías Novo
- docs: agregar `references/code-changes.md` con migración de `javax` → `jakarta`, Gson TypeAdapter, SpringDoc y OpenTelemetry
- docs: agregar `references/test-changes.md` con actualizaciones de tests para Spring Boot 3
- docs: agregar `references/quality-config.md` con configuración de SpotBugs, Checkstyle y Sonar
- docs: agregar `references/novo-libraries.md` con catálogo de librerías Novo y versiones compatibles con SB 3
- docs: agregar `skill.md` con flujo de migración en 3 fases (upgrade, SpringDoc, OpenTelemetry) y preguntas de diagnóstico

---

## [git-workflow 1.0.0] - 2026-05-22

- feat: skill `git-workflow` para generar commits, Pull Requests y CHANGELOG siguiendo Conventional Commits
- docs: agregar `references/commit-standard.md` con estándar de commits, tipos permitidos y reglas de formato
- docs: agregar `references/pr-guidelines.md` con guía de PRs pequeños, límites prácticos y técnicas de división
- docs: agregar `references/pr-template.md` con el template de título y cuerpo de PR
- docs: agregar `SKILL.md` con definición del skill, flujo recomendado y reglas prioritarias
