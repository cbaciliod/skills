# Referencia: Cambios en pom.xml

## 1. Versiones base

```xml
<properties>
    <java.version>25</java.version>
    <!-- NO agregar maven.compiler.source/target; spring-boot-starter-parent ya los toma de java.version -->
</properties>
```

Parent de Spring Boot:
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.5.14</version>
    <relativePath/>
</parent>
```

---

## 2. Librerías internas de Novo Microservices

Catálogo completo de versiones. Aplicar solo las que el microservicio ya tenga en su `pom.xml`.
Ver `novo-libraries.md` para contexto completo de cada librería.

### groupId: `com.novo.microservices.utils`

| Artifact ID | Versión SB 2.x → SB 3.5.x | Notas |
|-------------|---------------------------|-------|
| `novo-microservices-tbs-transactions-utils` | 1.7.0 → **3.0.0** | Para microservicios TBS orquestadores |
| `novo-microservices-utils-messaging-broker` | 3.1.0 → **4.0.1** | ⚠️ 5.0.0 disponible pero requiere `--enable-preview` |
| `novo-microservices-utils-configurations-loader` | 4.4.0 → **5.0.0-SNAPSHOT** | Resuelve colisión de bean `commonApplicationInfo` |
| `novo-microservices-utils` | 3.5.2 → **4.1.0** | Incluye `spring-boot-starter-web` — excluir en WebFlux |
| `novo-microservices-common-utils` | 2.1.0 → **4.0.0** | |
| `novo-microservices-common-reactive-utils` | 1.3.1 → **1.4.1** | Para microservicios WebFlux |
| `novo-microservices-utils-multi-tenant-repository` | 3.1.0 → **4.0.0** | Solo si el microservicio usa multi-tenant DB |
| `novo-microservices-utils-security-encryption` | 4.2.0 → **4.4.0** | Solo si el microservicio maneja encriptación |
| `novo-microservices-utils-security-jwa` | — → **4.1.0** | Solo si el microservicio usa JWT/JWA |
| `lib-mcr-common-utils` | — → **1.0.1** | Plantilla base nueva para microservicios reactivos |

### groupId: `com.novo.banking.utils`

| Artifact ID | Versión actual | Estado |
|-------------|---------------|--------|
| `banking-utils` | 1.0.1 | 🚫 **Bloqueante** — Spring Boot 2.7 / Java 11, sin versión SB 3 disponible |

> Si el microservicio usa `banking-utils`, **detener la migración** y abrir ticket para migrar esa librería primero.

---

### Versiones SNAPSHOT

Las versiones `*-SNAPSHOT` requieren el repositorio GitHub Packages con snapshots habilitados:

```xml
<repositories>
    <repository>
        <id>github</id>
        <name>GitHub Packages - novopayment</name>
        <url>https://maven.pkg.github.com/novopayment/central-repository</url>
        <snapshots>
            <enabled>true</enabled>
        </snapshots>
    </repository>
</repositories>
```

---

### Exclusiones obligatorias en proyectos WebFlux

Todas las librerías que traigan `spring-boot-starter-web` deben excluirlo:

```xml
<exclusions>
    <exclusion>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </exclusion>
</exclusions>
```

Librerías que traen `spring-boot-starter-web` transitivamente: `novo-microservices-utils`, `novo-microservices-utils-messaging-broker`, `novo-microservices-utils-configurations-loader`.

---

## 3. JAXB: reemplazar CDDL por EDL

**Eliminar** (licencia CDDL-1.0 incompatible):
```xml
<dependency>
    <groupId>com.sun.xml.bind</groupId>
    <artifactId>jaxb-impl</artifactId>
</dependency>
<dependency>
    <groupId>com.sun.xml.bind</groupId>
    <artifactId>jaxb-core</artifactId>
</dependency>
```

**Agregar** (licencia EDL-1.0 compatible):
```xml
<dependency>
    <groupId>org.glassfish.jaxb</groupId>
    <artifactId>jaxb-runtime</artifactId>
    <version>2.3.9</version>
    <scope>runtime</scope>
</dependency>
```

> Si el SDK de Postilion u otro SDK de terceros requiere `javax.xml.bind`, mantener:
> ```xml
> <dependency>
>     <groupId>javax.xml.bind</groupId>
>     <artifactId>jaxb-api</artifactId>
>     <version>2.3.1</version>
> </dependency>
> ```
> En `api-tbs-zinli-orchestrator-microservice` Postilion requiere esta dependencia — se mantiene.

---

## 4. Dependencias a ELIMINAR

```xml
<!-- JSON-B (reemplazado por Jackson en Spring Boot 3) -->
<dependency>
    <groupId>jakarta.json.bind</groupId>
    <artifactId>jakarta.json.bind-api</artifactId>
</dependency>
<dependency>
    <groupId>org.eclipse</groupId>
    <artifactId>yasson</artifactId>
</dependency>

<!-- FindBugs (reemplazado por SpotBugs; las anotaciones ya no compilan con Java 25) -->
<dependency>
    <groupId>com.google.code.findbugs</groupId>
    <artifactId>annotations</artifactId>
</dependency>
<dependency>
    <groupId>com.google.code.findbugs</groupId>
    <artifactId>jsr305</artifactId>
</dependency>

<!-- Guava (si no se usa directamente en código propio) -->
<dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
</dependency>
```

---

## 5. SpringDoc OpenAPI (CEB-5882 — reemplaza SpringFox)

**Eliminar** SpringFox:
```xml
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-boot-starter</artifactId>
</dependency>
```

**Agregar** SpringDoc (elegir según tipo de proyecto):
```xml
<!-- Para proyectos WebFlux (reactivos) -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webflux-ui</artifactId>
    <version>2.8.15</version>
</dependency>

<!-- Para proyectos WebMVC (tradicionales) -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.8.15</version>
</dependency>
```

Configuración en `application.yml`:
```yaml
springdoc:
  api-docs:
    path: /v3/api-docs
  swagger-ui:
    path: /swagger-ui.html
    disable-swagger-default-url: true
    operations-sorter: alpha
  show-actuator: true
  packages-to-scan: com.novo.microservices.controllers.contracts
```

---

## 6. OpenTelemetry (CEB-5914)

Agregar en `<properties>`:
```xml
<opentelemetry-instrumentation.version>2.22.0-alpha</opentelemetry-instrumentation.version>
```

Agregar en `<dependencyManagement>`:
```xml
<dependency>
    <groupId>io.opentelemetry.instrumentation</groupId>
    <artifactId>opentelemetry-instrumentation-bom-alpha</artifactId>
    <version>${opentelemetry-instrumentation.version}</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

Agregar dependencias:
```xml
<!-- Instrumentación automática Spring Boot -->
<dependency>
    <groupId>io.opentelemetry.instrumentation</groupId>
    <artifactId>opentelemetry-spring-boot-starter</artifactId>
</dependency>

<!-- Appender Log4j2 para correlación de trazas en logs -->
<dependency>
    <groupId>io.opentelemetry.instrumentation</groupId>
    <artifactId>opentelemetry-log4j-appender-2.17</artifactId>
    <scope>runtime</scope>
</dependency>

<!-- Exportar métricas Micrometer vía OTLP -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-otlp</artifactId>
</dependency>
```

Configuración en `application.yml`:
```yaml
otel:
  sdk:
    disabled: ${ENV_OTEL_DISABLED:false}
  service:
    name: ${spring.application.name}
  exporter:
    otlp:
      endpoint: ${ENV_OTEL_EXPORTER_OTLP_ENDPOINT:http://newrelic-otel-collector-opentelemetry-collector.newrelic.svc.cluster.local:4317}
      protocol: ${ENV_OTEL_EXPORTER_OTLP_PROTOCOL:grpc}
      metrics:
        temporality:
          preference: delta
  instrumentation:
    micrometer:
      enabled: true
  traces:
    exporter: otlp
  metrics:
    exporter: otlp
  logs:
    exporter: otlp
  resource:
    attributes:
      service.version: ${spring.application.version}
```

---

## 7. Plugins Maven

### maven-compiler-plugin — procesadores de anotaciones
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <source>${java.version}</source>
        <target>${java.version}</target>
        <annotationProcessorPaths>
            <path>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok</artifactId>
                <version>${lombok.version}</version>
            </path>
            <path>
                <groupId>org.mapstruct</groupId>
                <artifactId>mapstruct-processor</artifactId>
                <version>${dependency-mapstruct-version}</version>
            </path>
        </annotationProcessorPaths>
    </configuration>
</plugin>
```

> Si el proyecto no usa MapStruct, omitir ese `<path>`. `${lombok.version}` viene del parent de Spring Boot.

### sonar-maven-plugin
```xml
<plugin>
    <groupId>org.sonarsource.scanner.maven</groupId>
    <artifactId>sonar-maven-plugin</artifactId>
    <version>5.0.0.4389</version>
</plugin>
```

### jacoco-maven-plugin
```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.14</version>
    <executions>
        <execution>
            <id>pre-test</id>
            <goals><goal>prepare-agent</goal></goals>
            <configuration>
                <propertyName>jacocoArgLine</propertyName>
                <destFile>${project.test.result.directory}/jacoco/jacoco.exec</destFile>
            </configuration>
        </execution>
        <execution>
            <id>post-test</id>
            <phase>test</phase>
            <goals><goal>report</goal></goals>
            <configuration>
                <dataFile>${project.test.result.directory}/jacoco/jacoco.exec</dataFile>
                <outputDirectory>${project.test.result.directory}/jacoco</outputDirectory>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### maven-surefire-plugin — debe referenciar jacocoArgLine
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <argLine>${jacocoArgLine}</argLine>
        <reportsDirectory>${project.test.result.directory}/surefire</reportsDirectory>
    </configuration>
</plugin>
```

> **Si los tests fallan con `InaccessibleObjectException` o `IllegalAccessError` en Java 25**,
> agregar flags de apertura del módulo al `argLine`. Patrón tomado de
> `novo-microservices-utils-messaging-broker:5.0.0`:
>
> ```xml
> <argLine>
>     @{jacocoArgLine}
>     --add-opens java.base/java.time=ALL-UNNAMED
>     --add-opens java.base/java.lang=ALL-UNNAMED
>     --add-opens java.base/java.util=ALL-UNNAMED
>     -XX:+EnableDynamicAgentLoading
> </argLine>
> ```
>
> Nota: usar `@{jacocoArgLine}` (con `@`) cuando JaCoCo se configura con
> `prepare-agent` como goal propio; usar `${jacocoArgLine}` cuando se pasa
> via `<propertyName>` en la ejecución `pre-test`. En zinli se usa `${jacocoArgLine}`.

### spotbugs-maven-plugin
```xml
<plugin>
    <groupId>com.github.spotbugs</groupId>
    <artifactId>spotbugs-maven-plugin</artifactId>
    <version>4.9.8.1</version>
    <configuration>
        <effort>Max</effort>
        <threshold>Medium</threshold>
        <xmlOutput>true</xmlOutput>
        <htmlOutput>true</htmlOutput>
        <outputDirectory>${project.build.directory}</outputDirectory>
        <excludeFilterFile>config/spotbugs/spotbugs-exclude.xml</excludeFilterFile>
    </configuration>
</plugin>
```

### maven-checkstyle-plugin (nuevo en la migración)
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-checkstyle-plugin</artifactId>
    <version>3.6.0</version>
    <dependencies>
        <dependency>
            <groupId>com.puppycrawl.tools</groupId>
            <artifactId>checkstyle</artifactId>
            <version>12.3.1</version>
        </dependency>
    </dependencies>
    <configuration>
        <configLocation>config/checkstyle/google_checks_custom.xml</configLocation>
        <consoleOutput>true</consoleOutput>
        <failsOnError>false</failsOnError>
        <violationSeverity>warning</violationSeverity>
        <maxAllowedViolations>150</maxAllowedViolations>
    </configuration>
    <executions>
        <execution>
            <id>validate</id>
            <phase>validate</phase>
            <goals><goal>check</goal></goals>
        </execution>
    </executions>
</plugin>
```

> `failsOnError: false` y `maxAllowedViolations: 150` en la primera migración para no bloquear el build.
> Reducir gradualmente en iteraciones siguientes.

---

## 8. Dependencias de test

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-logging</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>

<!-- Solo si el proyecto es WebFlux -->
<dependency>
    <groupId>io.projectreactor</groupId>
    <artifactId>reactor-test</artifactId>
    <scope>test</scope>
</dependency>
```

---

## 9. Verificación

```bash
# Compilar sin tests
mvn clean compile -q

# Verificar árbol de dependencias (buscar conflictos)
mvn dependency:tree | findstr /i "WARN conflict omitted"

# Compilar incluyendo tests
mvn test-compile -q
```
