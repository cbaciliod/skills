# .claude — Agentes y Skills del Proyecto

Este directorio contiene skills (agentes especializados) para tareas recurrentes del proyecto.

## Skills disponibles

| Skill | Comando | Descripción |
|-------|---------|-------------|
| `migrate-spring-boot-java25` | `/migrate-spring-boot-java25` | Migra un microservicio de Spring Boot 2.7.x / Java 11 a Spring Boot 3.5.14 / Java 25 |

---

## migrate-spring-boot-java25

Basado en la migración real de `api-tbs-zinli-orchestrator-microservice` (Mayo 2026).
Cubre 3 fases de trabajo entregadas en PRs separados.

### Cómo usarlo

En Claude Code, escribe:
```
/migrate-spring-boot-java25
```

O describe qué quieres migrar:
```
migra el componente api-tbs-[nombre] siguiendo el mismo patrón de upgrade
```

### Qué hace

| Fase | Tarea | Jira | PR de referencia |
|------|-------|------|-----------------|
| 1 | Upgrade Spring Boot 3.5.14 + Java 25 | CEB-5855 | #34 |
| 2 | Migrar SpringFox → SpringDoc OpenAPI 2.8.15 | CEB-5882 | #40 |
| 3 | Implementar OpenTelemetry | CEB-5914 | #41 |

Detalle por fase:

**Fase 1 — Spring Boot + Java (CEB-5855)**
- Actualiza `pom.xml`: parent, `java.version`, librerías `novo-microservices-*`
- Reemplaza JAXB CDDL por EDL (mantiene `javax.xml.bind` para Postilion SDK)
- Elimina JSON-B, FindBugs, dependencias obsoletas
- Migra `javax.validation` → `jakarta.validation`
- Crea `BeanConfiguration` con TypeAdapter Gson para `LocalDateTime`
- Limpia `@ComponentScan` de clases eliminadas en nuevas librerías
- Configura SpotBugs, Checkstyle, JaCoCo
- Actualiza tests: `@MockBean` para producer/consumer, timeouts

**Fase 2 — SpringDoc OpenAPI (CEB-5882)**
- Reemplaza anotaciones Swagger 2 → OpenAPI 3
- Agrega `springdoc-openapi-starter-webflux-ui`
- Crea/migra `OpenApiConfiguration.java`
- Agrega `OpenApiConfigurationTest.java`

**Fase 3 — OpenTelemetry (CEB-5914)**
- Agrega BOM `opentelemetry-instrumentation-bom-alpha`
- Configura trazas, métricas y logs exportados vía OTLP a New Relic
- Integra `OpenTelemetryAppender` en `log4j2.xml`

### Referencias internas

```
.claude/skills/migrate-spring-boot-java25/
├── skill.md                        ← Lógica principal y flujo paso a paso
└── references/
    ├── pom-changes.md              ← Cambios de dependencias y plugins
    ├── code-changes.md             ← Cambios en código fuente
    ├── test-changes.md             ← Cambios en tests
    ├── quality-config.md           ← SpotBugs, Checkstyle, Sonar
    └── novo-libraries.md           ← Catálogo de librerías Novo con versiones y compatibilidad
```

### Componente de referencia

`api-tbs-zinli-orchestrator-microservice` — PRs #34, #40, #41 (Mayo 2026)

| Antes | Después |
|-------|---------|
| Spring Boot 2.7.1 | Spring Boot 3.5.14 |
| Java 11 | Java 25 |
| SpringFox 3.0.0 | SpringDoc OpenAPI 2.8.15 |
| Sin telemetría | OpenTelemetry 2.22.0-alpha → New Relic |
| Versión 1.6.1 | Versión 2.2.0 |

### Precondiciones para aplicar el skill a otro microservicio

1. El microservicio usa el mismo stack base: Spring Boot 2.7.x, Java 11, librerías `novo-microservices-*`
2. Tiene acceso al repositorio `novopayment/central-repository` en GitHub Packages
3. Existe el proyecto en SonarCloud bajo la organización `novopayment`
4. El equipo tiene JDK 25 instalado localmente (o CI tiene Java 25)
