# Skill: Migración Spring Boot 3.x + Java 25

## Propósito

Guía y ejecuta la migración de microservicios Java de Novopayment desde Spring Boot 2.7.x / Java 11
hacia Spring Boot 3.5.14 / Java 25, aplicando el mismo patrón probado en `api-tbs-zinli-orchestrator-microservice`
(PRs #34, #40, #41 — Jira: CEB-5855, CEB-5882, CEB-5914).

## Archivos de referencia

Antes de ejecutar cualquier paso, lee el archivo correspondiente:

| Tarea | Leer |
|-------|------|
| Actualizar `pom.xml` | `references/pom-changes.md` |
| Migrar código fuente | `references/code-changes.md` |
| Actualizar tests | `references/test-changes.md` |
| Configurar calidad de código | `references/quality-config.md` |
| Versiones de librerías Novo | `references/novo-libraries.md` |

---

## Antes de empezar — Identificar los tickets Jira

Cada migración tiene sus propios tickets. Antes de escribir un solo commit, confirmar con el equipo qué tickets Jira están asignados para este microservicio:

| Fase | Qué cubre | Variable a usar | Ejemplo en zinli |
|------|-----------|----------------|-----------------|
| Upgrade Spring Boot + Java | Pasos 2-5 | `TICKET-UPGRADE` | CEB-5855 |
| Migrar SpringFox → SpringDoc | Paso 6 | `TICKET-OPENAPI` | CEB-5882 |
| Implementar OpenTelemetry | Paso 7 | `TICKET-OTL` | CEB-5914 |

> Si el equipo planea todo en un solo ticket, usar ese mismo ID en todos los pasos.
> Si no hay ticket para SpringDoc u OpenTelemetry, omitir el paso correspondiente.

---

## Flujo de migración

Sigue este orden estrictamente. **Cada paso debe compilar y pasar tests antes de continuar.**
Hacer commits atómicos entre pasos.

### Paso 1 — Auditoría previa

```bash
# Guardar estado base
mvn dependency:tree > dependency-tree-before.txt
mvn test 2>&1 | tail -20 > tests-before.txt
```

#### 1a. Detectar qué librerías Novo usa este microservicio

Leer el `pom.xml` y extraer todas las dependencias `com.novo.*`:

```bash
# PowerShell
$xml = [xml](Get-Content "pom.xml")
$xml.project.dependencies.dependency |
  Where-Object { $_.groupId -like "*novo*" } |
  ForEach-Object { "$($_.groupId) : $($_.artifactId) : $($_.version)" }
```

```bash
# Bash / CI
grep -A2 "<groupId>com.novo" pom.xml | grep -E "artifactId|version"
```

#### 1b. Comparar contra el catálogo de versiones target

Con las librerías detectadas, comparar contra la tabla de `references/pom-changes.md` sección 2.
Solo actualizar las que el microservicio **ya tiene** — no agregar librerías nuevas que no usaba.

Ejemplo de salida esperada del análisis:

| Librería detectada | Versión actual | Versión target | Acción |
|--------------------|---------------|---------------|--------|
| `novo-microservices-utils` | 3.5.2 | 4.1.0 | ✅ Actualizar |
| `novo-microservices-utils-messaging-broker` | 3.1.0 | 4.0.1 | ✅ Actualizar |
| `novo-microservices-utils-configurations-loader` | 4.4.0 | 5.0.0-SNAPSHOT | ✅ Actualizar |
| `novo-microservices-utils-multi-tenant-repository` | 3.1.0 | 4.0.0 | ✅ Actualizar |
| `banking-utils` | 1.0.1 | ❌ Sin versión SB 3 | 🚫 Blocker |

#### 1c. Verificar blockers

Si en la comparación aparece alguna de estas, **detener y no continuar**:

| Librería bloqueante | Problema | Acción requerida |
|--------------------|----------|-----------------|
| `banking-utils` (cualquier versión) | Spring Boot 2.7 / Java 11 sin versión SB 3 | Abrir ticket para migrar esa librería primero |
| `novo-microservices-common-repository-utils:5.0.0` | Spring Boot 2.4 / Java 8 | Reemplazar por `utils-multi-tenant-repository:4.0.0` |
| `lib-microservices-utils:1.0.8` | Spring Boot 2.7, `javax.json.bind` obsoleto | Reemplazar por `novo-microservices-utils:4.1.0` |

#### 1d. Documentar el estado inicial

- Versión actual de Spring Boot y Java en el `pom.xml`
- Lista de librerías Novo con versión actual vs. target (resultado del 1b)
- Tests en rojo antes de la migración
- Si usa SpringFox o SpringDoc
- Si usa JSON-B (`jakarta.json.bind`, `yasson`, `preferred-json-mapper: jsonb`)
- Si hay `@SuppressFBWarnings` o `edu.umd.cs.findbugs` en el código
- Si usa `javax.validation` (debe migrar a `jakarta.validation`)
- Si usa `novo-microservices-utils-multi-tenant-repository` (requiere pasos adicionales en Paso 3)

---

### Paso 2 — Actualizar `pom.xml` (`TICKET-UPGRADE`)

Lee `references/pom-changes.md` y aplica **solo los cambios que corresponden a este microservicio**
(basado en el análisis del Paso 1b). En este orden:

1. Parent Spring Boot: `2.7.x` → `3.5.14`
2. `<java.version>25</java.version>`
3. **Solo las librerías `novo-microservices-*` que el microservicio ya usa** — actualizar cada una a su versión target según la tabla del Paso 1b. No agregar librerías que no existían.
4. Reemplazar JAXB CDDL → EDL si el proyecto usa Postilion SDK u otro SDK con `javax.xml.bind`
5. Eliminar solo las que el microservicio tenga: `jakarta.json.bind-api`, `yasson`, `findbugs:annotations`, `jsr305`
6. Actualizar plugins: sonar `5.0.0.4389`, jacoco `0.8.14`, spotbugs `4.9.8.1`, checkstyle `3.6.0`
7. Agregar procesador de anotaciones de MapStruct en `maven-compiler-plugin` (solo si el proyecto usa MapStruct)

```bash
mvn clean compile -q  # Verificar antes de continuar
```

> Usar `/git-workflow` para generar el commit. Tipo: `refactor`, scope: `deps`, Refs: `#TICKET-UPGRADE`.

---

### Paso 3 — Migrar código fuente (`TICKET-UPGRADE`)

Lee `references/code-changes.md` y aplica en este orden:

1. `javax.validation.*` → `jakarta.validation.*` en todos los DTOs y contratos
2. Eliminar anotaciones `@JsonbProperty` y su import de todos los DTOs
3. Crear `BeanConfiguration.java` con bean `Gson` + TypeAdapter para `LocalDateTime`
4. Inyectar el bean `Gson` en clases que lo usen (no usar `new Gson()`)
5. Agregar `@SuppressWarnings("java:S3011")` en clases con `setAccessible`
6. Agregar `@SuppressWarnings("java:S6830")` en `@Component` con nombre de bean
7. Reemplazar `@SuppressFBWarnings` → `@SuppressWarnings` de Sonar; eliminar imports findbugs
8. Limpiar `;;` dobles
9. Revisar `@ComponentScan` en la clase principal — eliminar `excludeFilters` de clases que ya no existen
10. Si Spring arranca con `duplicate bean`: agregar `allow-bean-definition-overriding: true` en `application.yml` (temporal) e investigar la causa raíz
11. Comentar `preferred-json-mapper: jsonb` en `application.yml` de producción

```bash
mvn clean compile -q
```

> Usar `/git-workflow`. Commits atómicos con tipos `fix` o `refactor`, scope según área afectada, Refs: `#TICKET-UPGRADE`.

---

### Paso 4 — Actualizar tests (`TICKET-UPGRADE`)

Lee `references/test-changes.md` y aplica:

1. Reemplazar `@Import({TransactionOrchestratorProducer.class})` por `@MockBean ITransactionOrchestratorProducer`
2. Agregar `@MockBean ITransactionOrchestratorConsumer` (Spring Boot 3 intenta inicializar ambos)
3. Comentar `preferred-json-mapper: jsonb` en `application-test.yml`
4. Agregar `ENV_ORCHESTRATOR_CONFIG_TIMEOUT=1000` en `@TestPropertySource`
5. Crear `src/test/resources/application.yml` si no existe (ver plantilla en `test-changes.md`)
6. Verificar que no hay `javax.validation` en tests

```bash
mvn test -q
```

> Usar `/git-workflow`. Tipo: `test`, scope: área de test afectada, Refs: `#TICKET-UPGRADE`.

---

### Paso 5 — Configurar herramientas de calidad (`TICKET-UPGRADE`)

Lee `references/quality-config.md` y aplica:

1. Crear/actualizar `config/spotbugs/spotbugs-exclude.xml` — incluir `US_USELESS_SUPPRESSION_ON_CLASS` (Lombok + Java 25)
2. Crear `config/checkstyle/google_checks_custom.xml` con relajaciones Novopayment

```bash
mvn spotbugs:check -q
mvn checkstyle:check -q
```

> Usar `/git-workflow`. Tipo: `fix`, scopes: `spotbugs` / `sonar`, Refs: `#TICKET-UPGRADE`.

---

### Paso 6 — Migrar SpringFox → SpringDoc OpenAPI (`TICKET-OPENAPI`)

Lee `references/pom-changes.md` sección "SpringDoc" y `references/code-changes.md` sección "SpringDoc".

1. Eliminar dependencias SpringFox del `pom.xml`
2. Agregar `springdoc-openapi-starter-webflux-ui` (WebFlux) o `webmvc-ui` (MVC)
3. Reemplazar anotaciones Swagger 2 → OpenAPI 3 en controllers y DTOs
4. Actualizar `application.yml` con bloque `springdoc:`
5. Crear o migrar clase de configuración `OpenApiConfiguration.java`
6. Agregar test `OpenApiConfigurationTest` con `@SpringJUnitConfig`

```bash
mvn test -Dtest=OpenApiConfigurationTest -q
```

> Usar `/git-workflow`. Tipo: `feat`, scope: `openapi`, Refs: `#TICKET-OPENAPI`.

---

### Paso 7 — Implementar OpenTelemetry (`TICKET-OTL`)

Lee `references/pom-changes.md` sección "OpenTelemetry" y `references/code-changes.md` sección "OpenTelemetry — log4j2.xml".

1. Agregar `dependencyManagement` con BOM `opentelemetry-instrumentation-bom-alpha`
2. Agregar `opentelemetry-spring-boot-starter` y `opentelemetry-log4j-appender-2.17` (scope `runtime`)
3. Agregar `micrometer-registry-otlp`
4. Configurar bloque `otel:` en `application.yml`
5. Agregar appender `<OpenTelemetry name="OpenTelemetryAppender"/>` en `log4j2.xml` y referenciarlo en `<Root>`
6. Agregar `otel.sdk.disabled: true` en `src/test/resources/application.yml` para desactivar en tests

```bash
mvn clean compile -q
```

> Usar `/git-workflow`. Tipo: `feat`, scopes: `build` / `logging` / `config`, Refs: `#TICKET-OTL`.

---

### Paso 8 — Validación final

```bash
mvn clean verify -q
```

Todos los checks deben pasar: `compile → test → spotbugs → checkstyle → jacoco`.

Si se usó `allow-bean-definition-overriding: true` como temporal, investigar y resolver la colisión de beans antes de hacer el PR.

---

## Estándar de commits y PRs

> Usa el skill `/git-workflow` para generar los commits y el PR. Esta sección define los
> parámetros específicos para la migración.

### Formato de commit

```
<tipo>(<scope>): <descripción en español, imperativo, max 72 chars>

[cuerpo opcional: explica el QUÉ y el POR QUÉ]

Refs: #CEB-XXXX
```

**Tipos válidos para migración:**

| Tipo | Cuándo usarlo en la migración |
|------|-------------------------------|
| `refactor` | Actualizar versiones, migrar imports, limpiar código sin cambiar funcionalidad |
| `feat` | Agregar OpenTelemetry, SpringDoc, nueva configuración de herramientas |
| `fix` | Corregir errores de arranque, beans duplicados, serialización |
| `test` | Actualizar o agregar tests |
| `docs` | Actualizar CHANGELOG, README |

**Reglas:**
- Descripción en minúsculas, verbos en infinitivo en español ("actualizar", "corregir", "agregar")
- El ID del ticket **NUNCA** va en el título — va en el footer `Refs: #CEB-XXXX`
- Máximo 72 caracteres en la primera línea

**Commits atómicos por paso de migración** — reemplazar `TICKET-*` con el ID real de Jira:

```
# Paso 2 — pom.xml
refactor(deps): actualizar Spring Boot a 3.5.14 y Java a versión 25
Refs: #TICKET-UPGRADE

# Paso 3 — código  (uno o varios según lo que aplique al microservicio)
fix(config): corregir conflictos de beans y mappings duplicados al arrancar
Refs: #TICKET-UPGRADE

fix(messaging): corregir fallo de serialización de LocalDateTime con Gson
Refs: #TICKET-UPGRADE

# Paso 4 — tests
test(controllers): reemplazar @Import por @MockBean y ajustar timeouts
Refs: #TICKET-UPGRADE

# Paso 5 — calidad
fix(spotbugs): excluir US_USELESS_SUPPRESSION_ON_CLASS generado por Lombok en Java 25
Refs: #TICKET-UPGRADE

fix(sonar): suprimir advertencias S3011 y S6830 en clases con reflexión
Refs: #TICKET-UPGRADE

# Paso 6 — SpringDoc  (si el ticket aplica)
feat(openapi): migrar SpringFox 3.0.0 a SpringDoc OpenAPI 2.8.15
Refs: #TICKET-OPENAPI

# Paso 7 — OpenTelemetry  (si el ticket aplica)
feat(build): agregar BOM y dependencias de OpenTelemetry
Refs: #TICKET-OTL

feat(logging): integrar OpenTelemetryAppender con correlación de trazas
Refs: #TICKET-OTL
```

---

### Estructura del PR por fase

Cada fase (ticket Jira) corresponde a un PR separado. La migración por fases es una
**excepción válida al límite de 400 líneas** (cambio atómico de dependencias).

> Reemplazar `TICKET-*` y `CEB-XXXX` con los IDs reales asignados en Jira para este microservicio.
> El link de Jira sigue el patrón: `https://jira4novo.atlassian.net/browse/CEB-XXXX`

**PR Fase 1 — Spring Boot + Java (`TICKET-UPGRADE`):**

```
Título:  refactor: actualizar Spring Boot a 3.5.14 y migrar a Java 25

## Description:
**Dependencias:**
- Actualizar parent Spring Boot de 2.7.x a 3.5.14
- Actualizar Java a versión 25
- Actualizar librerías internas novo-microservices-* a versiones SB 3.x
- [ajustar según lo que aplique a este microservicio]

**Código:**
- Migrar javax.validation.* a jakarta.validation.* en DTOs y contratos
- [ajustar según hallazgos del Paso 1d]

**Tests:**
- [listar los cambios reales aplicados en este microservicio]

**Calidad:**
- Agregar config/spotbugs/spotbugs-exclude.xml con US_USELESS_SUPPRESSION_ON_CLASS
- Agregar config/checkstyle/google_checks_custom.xml

## Justificación de sobre límite:
- **Motivo:** migración atómica de dependencias — no se puede dividir sin romper el build
- **Condición técnica:** Spring Boot 3 requiere Jakarta EE 9 en todos los módulos a la vez
- **Técnicas evaluadas:** Branch by Abstraction no aplica para upgrade de framework

## Issue ticket number and link:
[CEB-XXXX](https://jira4novo.atlassian.net/browse/CEB-XXXX)

## Checklist before requesting a review:
- [ ] I have performed a self-review of my code
- [ ] If it is a core feature, I have added thorough tests.
```

**PR Fase 2 — SpringDoc (`TICKET-OPENAPI`) — solo si aplica:**

```
Título:  feat: migrar SpringFox 3.0.0 a SpringDoc OpenAPI 2.8.15

## Description:
- Reemplazar dependencia springfox-boot-starter por springdoc-openapi-starter-webflux-ui
- Migrar anotaciones Swagger 2 (@Api, @ApiOperation) a OpenAPI 3 (@Tag, @Operation)
- Crear OpenApiConfiguration.java con bean OpenAPI personalizado
- Agregar OpenApiConfigurationTest con @SpringJUnitConfig

## Issue ticket number and link:
[CEB-YYYY](https://jira4novo.atlassian.net/browse/CEB-YYYY)

## Checklist before requesting a review:
- [ ] I have performed a self-review of my code
- [ ] If it is a core feature, I have added thorough tests.
```

**PR Fase 3 — OpenTelemetry (`TICKET-OTL`) — solo si aplica:**

```
Título:  feat: implementar OpenTelemetry en Spring Boot

## Description:
- Agregar BOM opentelemetry-instrumentation-bom-alpha en dependencyManagement
- Agregar opentelemetry-spring-boot-starter y opentelemetry-log4j-appender-2.17
- Agregar micrometer-registry-otlp para exportar métricas
- Configurar bloque otel: en application.yml con exportación OTLP a New Relic
- Integrar OpenTelemetryAppender en log4j2.xml para correlación de trazas

## Issue ticket number and link:
[CEB-ZZZZ](https://jira4novo.atlassian.net/browse/CEB-ZZZZ)

## Checklist before requesting a review:
- [ ] I have performed a self-review of my code
- [ ] If it is a core feature, I have added thorough tests.
```

---

## Reglas prioritarias

- **Nunca** actualizar Spring Boot y las librerías de Novo en el mismo commit. Hacerlo en commits atómicos.
- **Nunca** dejar `allow-bean-definition-overriding: true` en producción si se puede evitar. Si la colisión viene de una librería interna actualizada, la solución es actualizar esa librería.
- Si `javax.xml.bind` es requerido por un SDK de terceros (ej: Postilion), **mantener** la dependencia `javax.xml.bind:jaxb-api:2.3.1` pero reemplazar la implementación CDDL por `org.glassfish.jaxb:jaxb-runtime` (licencia EDL).
- Los `@SuppressWarnings` de Sonar van en el método o clase más pequeña posible, no a nivel de paquete.
- Después de cada paso: commit atómico siguiendo el formato de `/git-workflow`.
- En Java 25, los `catch (Exception e)` donde `e` no se usa → reemplazar por `catch (Exception _)`.

---

## Preguntas de diagnóstico

Si el build falla, responde estas preguntas antes de intentar un fix:

1. ¿El error es de compilación o de runtime?
2. ¿El error está en código propio o en una librería?
3. ¿El error existía antes de la migración (`git stash && mvn compile`)?
4. ¿El error aparece en producción o solo en tests?
5. ¿La clase afectada usa `javax.*` que debería ser `jakarta.*`?
6. ¿Hay un bean duplicado? Buscar con: `grep -rl "@Bean\|@Component\|@Service" src/ | xargs grep -l "NOMBRE_DEL_BEAN"`
7. ¿Gson falla serializando `LocalDateTime`? → Falta el TypeAdapter.
8. ¿SpotBugs reporta `US_USELESS_SUPPRESSION_ON_CLASS`? → Agregar a `spotbugs-exclude.xml`.

---

## Referencia — Ejemplo en `api-tbs-zinli-orchestrator-microservice`

Los tickets de zinli son solo referencia. Cada microservicio tendrá sus propios IDs.

| Variable | Ticket en zinli | Descripción | PR |
|----------|----------------|-------------|-----|
| `TICKET-UPGRADE` | CEB-5855 | Upgrade Spring Boot 3.5.14 + Java 25 | #34 |
| `TICKET-OPENAPI` | CEB-5882 | Migrar SpringFox → SpringDoc OpenAPI 2.8.15 | #40 |
| `TICKET-OTL` | CEB-5914 | Implementar OpenTelemetry | #41 |
