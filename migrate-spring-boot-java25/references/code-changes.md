# Referencia: Cambios en Código Fuente

## 1. javax.validation → jakarta.validation

Spring Boot 3 usa Jakarta EE 9. Todas las importaciones de validación deben migrar.

```bash
# Buscar archivos afectados
grep -rl "javax.validation" src/
```

```java
// ANTES
import javax.validation.constraints.NotNull;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;

// DESPUÉS
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
```

Aplica también en contratos (`IAccountTransactionController.java`, etc.), no solo en DTOs.

---

## 2. Eliminar @JsonbProperty de DTOs

Spring Boot 3 usa Jackson por defecto. `@JsonbProperty` es de JSON-B (eliminado).

```bash
grep -rl "@JsonbProperty" src/
```

```java
// ANTES
@JsonbProperty("response_code")
@JsonProperty("response_code")
@SerializedName("response_code")
private String responseCode;

// DESPUÉS
@JsonProperty("response_code")
@SerializedName("response_code")
private String responseCode;
```

Eliminar también el import:
```java
// ELIMINAR
import jakarta.json.bind.annotation.JsonbProperty;
```

---

## 3. Gson con TypeAdapter para LocalDateTime

Java 17+ restringe la reflexión sobre clases del JDK (`java.time.*`). Crear un bean centralizado:

**`BeanConfiguration.java`** (nuevo archivo):
```java
package com.novo.microservices.components.configurations;

import com.google.gson.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import java.time.LocalDateTime;

@Configuration
public class BeanConfiguration {
    @Bean
    public Gson gson() {
        return new GsonBuilder()
            .registerTypeAdapter(LocalDateTime.class,
                (JsonSerializer<LocalDateTime>) (src, type, ctx) ->
                    new JsonPrimitive(src.toString()))
            .registerTypeAdapter(LocalDateTime.class,
                (JsonDeserializer<LocalDateTime>) (json, type, ctx) ->
                    LocalDateTime.parse(json.getAsString()))
            .create();
    }
}
```

**Si una clase tiene `Gson` como campo estático** (ej: `TransactionLogHelper`):
```java
private static final Gson gson = new GsonBuilder()
    .registerTypeAdapter(LocalDateTime.class,
        (JsonSerializer<LocalDateTime>) (src, type, ctx) -> new JsonPrimitive(src.toString()))
    .registerTypeAdapter(LocalDateTime.class,
        (JsonDeserializer<LocalDateTime>) (json, type, ctx) -> LocalDateTime.parse(json.getAsString()))
    .create();
```

**Si una clase inyecta `Gson` como bean** (ej: `TransactionOrchestratorProducer`):
```java
// Reemplazar campo estático o new Gson() por inyección
@Autowired
private Gson gson;
```

---

## 4. Suprimir advertencias de Sonar en clases con reflexión (java:S3011)

Clases que usan `setAccessible(true)` recibirán `java:S3011` de Sonar.

Ejemplo real — `TransactionLogHelper.java`:
```java
@Log4j2
@UtilityClass
@SuppressWarnings("java:S3011")
public class TransactionLogHelper {
    // ...
    public static void writeTransactionLog(...) {
        // ...
        currentField.setAccessible(true);
    }
}
```

---

## 5. Suprimir advertencia java:S6830 en @Component con nombre

Sonar `java:S6830` señala que el nombre del bean debería ir en `@Bean` en lugar de `@Component`.
Si cambiar el patrón no es viable en este ciclo de migración:

```java
@SuppressWarnings("java:S6830")
@Component(NOMBRE_CONSTANTE)
public class MiTransaccion extends BaseClass<Request, Response> { ... }
```

Aplica a todas las clases de transacción que extienden de una clase base con nombre de bean.

---

## 6. Reemplazar @SuppressFBWarnings por @SuppressWarnings de Sonar

```bash
grep -rl "@SuppressFBWarnings" src/
grep -rl "edu.umd.cs.findbugs" src/
```

```java
// ANTES
import edu.umd.cs.findbugs.annotations.SuppressFBWarnings;

@SuppressFBWarnings(value = {"DP_DO_INSIDE_DO_PRIVILEGED", "REC_CATCH_EXCEPTION"})
@SuppressWarnings(value = {"DP_DO_INSIDE_DO_PRIVILEGED", "REC_CATCH_EXCEPTION"})
public class MiClase { ... }

// DESPUÉS (sin import de findbugs)
@SuppressWarnings("java:S3011")
public class MiClase { ... }
```

---

## 7. Conflictos de beans al arrancar

Spring Boot 3 no permite beans con el mismo nombre por defecto.

**Síntoma:** `The bean '...' could not be registered. A bean with that name has already been defined`

**Solución temporal** en `application.yml`:
```yaml
spring:
  main:
    allow-bean-definition-overriding: true
```

**Causa real en `api-tbs-zinli-orchestrator-microservice`:**
El bean `commonApplicationInfo` estaba definido tanto en el código local como en `novo-microservices-utils-configurations-loader`. La solución fue actualizar a `5.0.0-SNAPSHOT` que resolvió la duplicación en la raíz.

**Investigar con:**
```bash
grep -rl "@Bean\|@Component\|@Service\|@Repository" src/ | xargs grep -l "NOMBRE_DEL_BEAN"
```

---

## 8. @ComponentScan — limpiar excludeFilters obsoletos

Si la clase principal tiene `excludeFilters` que apuntan a clases eliminadas en las nuevas versiones de librerías, Spring no puede encontrarlas y falla.

**Ejemplo en `MicroservicesApplication.java`:**
```java
// ANTES (clases que ya no existen en novo-microservices-utils 4.1.0)
@ComponentScan(
    excludeFilters = {
        @ComponentScan.Filter(type = FilterType.ASSIGNABLE_TYPE, classes = DeleteCacheCommonController.class),
        @ComponentScan.Filter(type = FilterType.ASSIGNABLE_TYPE, classes = PodInfoCommonController.class)
    }
)

// DESPUÉS (remover los filtros de clases que ya no existen)
@ComponentScan(
    basePackages = {
        "com.novo.util.microservices.configurations.loader",
        "com.novo.microservices",
        "com.novo.microservices.utils",
        "com.novo.utils.messaging"
    }
)
```

---

## 9. Comentar preferred-json-mapper en application.yml

```yaml
spring:
  main:
    # mvc:
    #   converters:
    #     preferred-json-mapper: jsonb  # JSON-B eliminado en Spring Boot 3
```

---

## 10. Patrón catch con variable unnamed (Java 21+)

Java 21 introdujo unnamed variables en catch. Aplicar cuando `e` no se usa en el bloque:

```java
// ANTES
} catch (Exception e) {
    log.error("the field {} is no present in class {}", fieldName, currentClass.getCanonicalName());
}

// DESPUÉS (Java 21+)
} catch (Exception _) {
    log.error("the field {} is no present in class {}", fieldName, currentClass.getCanonicalName());
}
```

Ejemplo real de `TransactionLogHelper.java` (línea 76):
```java
} catch (Exception _) {
    log.error("the field {} is no present in class {}", fieldName, currentClass.getCanonicalName());
}
```

> Solo aplicar si `e` realmente no se usa. Si se necesita el mensaje de la excepción, mantener `e`.

---

## 11. Eliminar doble punto y coma (;;)

Lombok y refactorings rápidos a veces dejan `;;`:

```bash
grep -rn ";;" src/
```

Corregir: eliminar el `;` redundante.

---

## 12. OpenTelemetry — log4j2.xml (CEB-5914)

Agregar el appender `<OpenTelemetry>` y referenciarlo en el Root logger.
El nombre del servicio en `LOG_PATTERN_CONSOLE` debe coincidir con `${spring.application.name}`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN" monitorInterval="30">

    <Properties>
        <!-- Formato: fecha|requestId|tenantId|{thread}|nivel|nombre-servicio|method|trace_id|span_id|clase#línea: mensaje -->
        <Property name="LOG_PATTERN_CONSOLE">%d|%X{requestId}|%X{tenantId}|{%t}|%p|NOMBRE-DEL-SERVICIO|%X{method}|%X{trace_id}|%X{span_id}|%c{1} #%L: %m%n</Property>
    </Properties>

    <Appenders>
        <Console name="console" target="SYSTEM_OUT">
            <PatternLayout pattern="${LOG_PATTERN_CONSOLE}"/>
        </Console>

        <!-- Appender OpenTelemetry: correlaciona logs con trazas (trace_id, span_id) -->
        <OpenTelemetry name="OpenTelemetryAppender"/>
    </Appenders>

    <Loggers>
        <Root level="INFO">
            <AppenderRef ref="console"/>
            <AppenderRef ref="OpenTelemetryAppender"/>
        </Root>
    </Loggers>
</Configuration>
```

> Reemplazar `NOMBRE-DEL-SERVICIO` con el `artifactId` del microservicio
> (ej: `api-tbs-zinli-orchestrator-microservice`).
>
> El `<OpenTelemetry>` appender es provisto por la dependencia `opentelemetry-log4j-appender-2.17`
> con scope `runtime`. Sin esta dependencia, el XML falla al parsear con error
> `"OpenTelemetry" appender is not recognized`.

---

## 13. `@Generated` en el método `main` (exclusión JaCoCo)

JaCoCo reporta cobertura 0% en el `main` de Spring Boot. Agregar `@Generated` para excluirlo:

```java
import lombok.Generated;

@SpringBootApplication
public class MicroservicesApplication extends MicroservicesBaseApplication {

    public MicroservicesApplication(@NotNull MicroServicesProperties microServicesProperties) {
        super(microServicesProperties);
    }

    @Generated   // ← excluye este método del reporte de cobertura JaCoCo
    public static void main(String[] args) {
        SpringApplication.run(MicroservicesApplication.class);
    }
}
```

> `@lombok.Generated` es reconocido por JaCoCo automáticamente para excluir el método
> del reporte de cobertura sin necesidad de configuración adicional.

---

## 14. Migrar SpringFox → SpringDoc (CEB-5882)

### Anotaciones en Controllers

```java
// ANTES (Swagger 2 / SpringFox)
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;

@Api(value = "Account Transactions", tags = {"Transactions"})
public interface IAccountTransactionController {

    @ApiOperation(value = "Execute Balance Transaction")
    @ApiResponses({
        @ApiResponse(code = 200, message = "OK"),
        @ApiResponse(code = 400, message = "Bad Request")
    })
    Mono<ResponseEntity<BaseBusinessResponseDto>> executeBalanceTransaction(
        @ApiParam(required = true) @RequestBody BalanceTransactionRequest request);
}

// DESPUÉS (OpenAPI 3 / SpringDoc)
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;

@Tag(name = "Transactions", description = "Account Transactions")
public interface IAccountTransactionController {

    @Operation(summary = "Execute Balance Transaction")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "OK"),
        @ApiResponse(responseCode = "400", description = "Bad Request")
    })
    Mono<ResponseEntity<BaseBusinessResponseDto>> executeBalanceTransaction(
        @Parameter(required = true) @RequestBody BalanceTransactionRequest request);
}
```

### Anotaciones en DTOs

```java
// ANTES (Swagger 2)
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

@ApiModel(description = "Balance Transaction Request")
public class BalanceTransactionRequest {
    @ApiModelProperty(value = "Account number", required = true)
    private String accountNumber;
}

// DESPUÉS (OpenAPI 3)
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Balance Transaction Request")
public class BalanceTransactionRequest {
    @Schema(description = "Account number", required = true)
    private String accountNumber;
}
```

### Clase de configuración OpenAPI

```java
package com.novo.microservices.components.configurations;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfiguration {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Microservice API")
                .version("1.0")
                .description("API Documentation"));
    }
}
```

### Test de la configuración OpenAPI

```java
import org.junit.jupiter.api.Test;
import org.springframework.test.context.junit.jupiter.SpringJUnitConfig;

@SpringJUnitConfig(OpenApiConfiguration.class)
class OpenApiConfigurationTest {

    @Autowired
    private OpenAPI openAPI;

    @Test
    void openApiBeanShouldNotBeNull() {
        assertNotNull(openAPI);
    }

    @Test
    void openApiInfoShouldNotBeNull() {
        assertNotNull(openAPI.getInfo());
    }
}
```
