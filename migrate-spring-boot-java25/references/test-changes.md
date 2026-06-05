# Referencia: Cambios en Tests

## 1. Reemplazar @Import de producers/consumers por @MockBean

Spring Boot 3 es más estricto con el contexto de tests. Los producers y consumers de mensajería
deben mockearse con `@MockBean` en lugar de importarse o inicializarse.

```bash
grep -rl "@Import" src/test/
```

**Antes:**
```java
@SpringBootTest
@Import({TransactionOrchestratorProducer.class})
class MiControllerTest {
    @Autowired
    private ITransactionOrchestratorProducer producer;
}
```

**Después:**
```java
@SpringBootTest  // o @WebFluxTest
class MiControllerTest {
    @MockBean
    private ITransactionOrchestratorProducer transactionOrchestratorProducer;

    @MockBean
    private ITransactionOrchestratorConsumer transactionOrchestratorConsumer;
}
```

> Agregar `@MockBean` tanto para el **producer** como para el **consumer**. Spring Boot 3 intenta
> inicializar ambos durante la carga del contexto y falla si el broker no está disponible.

---

## 2. Patrón completo de test WebFlux con @MockBean

Ejemplo real de `CardTransactionControllerTest.java`:

```java
@WebFluxTest(controllers = AccountTransactionController.class)
@Import({
    DocumentationMicroservice.class,
    BusinessResponse.class,
    ContextInformationService.class,
    // ... resto de beans necesarios
    ActivationTransaction.class
})
@TestPropertySource(properties = {
    "spring.config.location=classpath:application.yml",
    "ENV_ORCHESTRATOR_CONFIG_TIMEOUT=1000"   // ← timeout reducido para tests
})
@AutoConfigureWebTestClient(timeout = "20000")
public class CardTransactionControllerTest {

    @MockBean
    private ITransactionOrchestratorProducer transactionOrchestratorProducer;

    @MockBean
    private ITransactionOrchestratorConsumer transactionOrchestratorConsumer;

    @Autowired
    private WebTestClient webClient;

    @BeforeEach
    void setUp() {
        Mockito.when(transactionOrchestratorProducer.doOnProcessTransaction(Mockito.any()))
            .thenAnswer(invocation -> {
                TransactionMessage<StandardTransaction> msg = invocation.getArgument(0);
                Event<TransactionMessage<StandardTransaction>> event = new Event<>();
                event.setData(msg);
                return event;
            });
    }
}
```

Puntos clave:
- `@TestPropertySource` con `ENV_ORCHESTRATOR_CONFIG_TIMEOUT=1000` para evitar timeouts lentos
- `@AutoConfigureWebTestClient(timeout = "20000")` para el cliente HTTP en tests
- El mock del producer devuelve el mensaje recibido como respuesta (sin broker real)

---

## 3. application-test.yml: deshabilitar JSON-B

```bash
grep -r "preferred-json-mapper" src/test/
```

```yaml
# ANTES
spring:
  mvc:
    converters:
      preferred-json-mapper: jsonb

# DESPUÉS
spring:
  mvc:
    converters:
      # preferred-json-mapper: jsonb  # JSON-B eliminado en Spring Boot 3
```

---

## 4. Ajustar timeouts en tests de integración

Spring Boot 3 + Java 25 puede tardar más en inicializar. Timeouts muy bajos causan tests intermitentes.

```bash
grep -rn "TIMEOUT\|timeout" src/test/
```

```java
// ANTES (demasiado restrictivo)
private static final int TIMEOUT = 9000;

// DESPUÉS (suficiente con mocks en Spring Boot 3)
private static final int TIMEOUT = 1000;
```

En `@TestPropertySource`:
```java
@TestPropertySource(properties = {
    "ENV_ORCHESTRATOR_CONFIG_TIMEOUT=1000"
})
```

> Para tests de integración real contra servicios externos, mantener `>= 5000ms`.

---

## 5. src/test/resources/application.yml (archivo nuevo recomendado)

Si el proyecto no tiene este archivo, crearlo. Proporciona un contexto limpio para tests con H2 y sin broker real:

```yaml
server:
  port: 8000
  compression:
    enabled: true
  error:
    include-stacktrace: never
  netty:
    connection-timeout: 5000
    idle-timeout: 60000

spring:
  application:
    name: microservice-test
    version: 1.0.0
  messages:
    encoding: UTF-8
  main:
    banner-mode: log
    lazy-initialization: false
    allow-bean-definition-overriding: true   # Necesario en tests con contexto completo
  #mvc:
    #converters:
      #preferred-json-mapper: jsonb

logging:
  level:
    root: INFO

management:
  info:
    git:
      enabled: false
  health:
    db:
      enabled: false

# Pod Configuration (valores de test)
entityUuid: bc607fa5-01d2-4da2-803d-ce0721c50d89
configurationDomainPath: http://localhost:8000
hazelcastYmlPath: /hazelcast.yml
configMap.message: Test configuration
coreTenantConnectTimeout: 1000
coreTenantReadTimeout: 1000
novo-microservices-index-control: "00"

# Rabbit (no se conecta en tests porque el consumer está mockeado)
rabbit:
  host: localhost
  port: 5672
  username: guest
  password: guest
  virtualhost: /
  ssl-enabled: false
  publisher-returns: false
  publisher-confirm-type: SIMPLE
  queue-properties:
    x-expires: 600000
    x-message-ttl: 30000
    x-queue-type: quorum

broker-configuration:
  common-configuration:
    queue-uuid: test-queue
    routing-key-origin: MD-test-queue
    broker-declare-exchange: postilion
    broker-declare-exchange-type: TOPIC
  response-consumer:
    queue: QU-TEST-RESPONSE
    command: RESPONSE
    routing-key: SERVICE.POSTILION.MD-test-queue.TRANSACTION.RESPONSE
    routing-domain: TRANSACTION
    routing-key-origin: POSTILION
    routing-key-destiny: MD-test-queue
  request-producer:
    command: REQUEST
    routing-key: SERVICE.MD-test-queue.POSTILION.TRANSACTION.REQUEST
    routing-domain: TRANSACTION
    routing-key-origin: MD-test-queue
    routing-key-destiny: POSTILION

orchestrator-transactions:
  common-configuration:
    routing-key-destiny-parameter: routingKeyDestiny
    transaction-tenant-id-default: pa-zinli
    transaction-time-out: ${ENV_ORCHESTRATOR_CONFIG_TIMEOUT:1000}
    transaction-waiting-purge: 10

# OpenTelemetry deshabilitado en tests
otel:
  sdk:
    disabled: true

# SpringDoc
springdoc:
  api-docs:
    path: /v3/api-docs
  swagger-ui:
    path: /swagger-ui.html
    disable-swagger-default-url: true
  packages-to-scan: com.novo.microservices.controllers.contracts
```

---

## 6. Verificar imports de validación en tests

```bash
grep -rn "javax.validation" src/test/
```

Reemplazar igual que en código fuente (ver `code-changes.md` sección 1).

---

## 7. Test de OpenApiConfiguration (SpringDoc)

Después de migrar SpringFox → SpringDoc, agregar este test para evitar `java:S2187`:

```java
package com.novo.microservices;

import com.novo.microservices.components.configurations.OpenApiConfiguration;
import io.swagger.v3.oas.models.OpenAPI;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.junit.jupiter.SpringJUnitConfig;

import static org.junit.jupiter.api.Assertions.assertNotNull;

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

> `@SpringJUnitConfig` es más ligero que `@SpringBootTest` — carga solo la clase de configuración indicada.

---

## 8. Comandos de verificación de tests

```bash
# Solo compilar tests (rápido, detecta errores de import)
mvn test-compile -q

# Ejecutar todos los tests
mvn test -q

# Ejecutar un test específico
mvn test -Dtest=CardTransactionControllerTest -q

# Ejecutar un método específico
mvn test "-Dtest=CardTransactionControllerTest#balanceTransactionOk" -q

# Ver reporte de coverage
mvn jacoco:report
# Abrir target/test-results/jacoco/index.html
```

---

## 9. Errores comunes en tests con Spring Boot 3

| Error | Causa | Solución |
|-------|-------|----------|
| `UnsatisfiedDependencyException: TransactionOrchestratorProducer` | Producer no mockeado | Agregar `@MockBean ITransactionOrchestratorProducer` |
| `UnsatisfiedDependencyException: TransactionOrchestratorConsumer` | Consumer no mockeado | Agregar `@MockBean ITransactionOrchestratorConsumer` |
| `NoSuchBeanDefinitionException: jsonbHttpMessageConverter` | JSON-B eliminado | Comentar `preferred-json-mapper: jsonb` |
| `IllegalStateException: duplicate bean` | Allow overriding false | Agregar `allow-bean-definition-overriding: true` en test yml |
| `TimeoutException` en tests | Timeout muy bajo | Agregar `ENV_ORCHESTRATOR_CONFIG_TIMEOUT=1000` en `@TestPropertySource` |
| `InaccessibleObjectException` en Gson | Java 17+ reflexión restringida | Agregar TypeAdapter para `LocalDateTime` (ver `code-changes.md`) |
| `AmqpConnectException: Connection refused` | Rabbit no disponible | Asegurarse que producer/consumer están mockeados con `@MockBean` |
| `NoSuchBeanDefinitionException: openAPI` | SpringFox no eliminado o SpringDoc no configurado | Verificar dependencias y clase `OpenApiConfiguration` |
