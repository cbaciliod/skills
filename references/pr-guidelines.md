# Pull Requests: Pautas y mejores prácticas

> **Autor:** Gabriel Rosales
> **Lectura estimada:** 11 min

---

## 1. Por qué PRs pequeños

Los Pull Requests grandes son difíciles de revisar, propensos a errores y retrasan el feedback. Un PR pequeño:

- Se revisa en minutos, no horas
- Reduce errores por fatiga del revisor
- Permite feedback más rápido y específico
- Facilita identificar la causa de bugs
- Disminuye conflictos de merge

> 💡 **Regla de oro:** Si dudas si tu PR es muy grande, probablemente lo es.

---

## 2. Límites prácticos

Usa estos límites como guía, no como reglas absolutas:

|Métrica|Ideal|Máximo aceptable|
|---------|-------|-----------------|
|Líneas de código modificadas|< 200|< 400|
|Archivos modificados|< 5|< 10|
|Tiempo de revisión estimado|< 15 min|< 30 min|

**Excepciones válidas:**

- Refactoring automático (renombrado masivo)
- Migración de dependencias
- Cambios generados automáticamente
- Documentación extensa

### ⚠️ Si superas el límite debes justificarlo

Si tu PR supera los límites, **es obligatorio** agregar una sección
de justificación en la descripción del PR:

```markdown
## Justificación de sobre límite:
- **Motivo:** [por qué no se pudo dividir]
- **Condición técnica:** [qué lo produce, ej: migración atómica, cambio de contrato]
- **Técnicas evaluadas:** [qué técnica se consideró y por qué no aplicó]
```

**Ejemplos válidos de justificación:**

- Refactoring automático por renombrado masivo de paquete
- Migración de dependencia que afecta múltiples capas de forma atómica
- Cambio de contrato de API que requiere actualizar todos los consumers a la vez
- Cambios generados automáticamente (mocks, protobuf, etc.)

**Ejemplos NO válidos:**

- "Se me fue de las manos"
- "Era urgente"
- "No tuve tiempo de dividirlo"

---

## 3. Técnicas de división de trabajo

### 3.1 Branch by Abstraction

Permite cambiar implementaciones sin romper el código existente, dividiendo el trabajo en múltiples PRs pequeños.

**Pasos:**

- **PR 1** — Crear abstracción: Introduce una interfaz o abstracción sobre el código existente
- **PR 2** — Migrar llamadas: Actualiza el código para usar la abstracción (sin cambiar comportamiento)
- **PR 3** — Nueva implementación: Agrega la nueva implementación detrás de la abstracción
- **PR 4** — Cambiar a nueva implementación: Cambia la configuración para usar la nueva implementación
- **PR 5** — Limpieza: Elimina código obsoleto una vez validada la nueva implementación

#### Ejemplo Java — Cambiar servicio de email

```java
// PR 1: Crear abstracción
public interface EmailService {
    void send(String to, String subject, String body);
}
public class LegacyEmailService implements EmailService {
    // Wrapper del código existente
    public void send(String to, String subject, String body) {
        legacyMailer.sendMail(to, subject, body);
    }
}

// PR 2: Migrar llamadas existentes
// Antes
legacyMailer.sendMail(user.getEmail(), "Welcome", "Hello!");
// Después
emailService.send(user.getEmail(), "Welcome", "Hello!");

// PR 3: Nueva implementación
public class SendGridEmailService implements EmailService {
    public void send(String to, String subject, String body) {
        sendGridClient.send(buildEmail(to, subject, body));
    }
}

// PR 4: Cambiar implementación (configuración)
@Bean
public EmailService emailService() {
    // return new LegacyEmailService(); // Viejo
    return new SendGridEmailService(); // Nuevo
}

// PR 5: Eliminar código legacy
// Eliminar LegacyEmailService y legacyMailer
```

#### Ejemplo Go — Cambiar servicio de email

```go
// PR 1: Crear abstracción
type EmailService interface {
    Send(to, subject, body string) error
}
type LegacyEmailService struct {
    legacyMailer *LegacyMailer
}
func (s *LegacyEmailService) Send(to, subject, body string) error {
    return s.legacyMailer.SendMail(to, subject, body)
}

// PR 2: Migrar llamadas existentes
// Antes
legacyMailer.SendMail(user.Email, "Welcome", "Hello!")
// Después
emailService.Send(user.Email, "Welcome", "Hello!")

// PR 3: Nueva implementación
type SendGridEmailService struct {
    client *sendgrid.Client
}
func (s *SendGridEmailService) Send(to, subject, body string) error {
    email := s.buildEmail(to, subject, body)
    return s.client.Send(email)
}

// PR 4: Cambiar implementación (configuración)
func NewEmailService() EmailService {
    // return &LegacyEmailService{...} // Viejo
    return &SendGridEmailService{...} // Nuevo
}

// PR 5: Eliminar código legacy
// Eliminar LegacyEmailService y legacyMailer
```

---

### 3.2 Strangler Fig Pattern

Similar a Branch by Abstraction, pero específico para reemplazar sistemas o módulos completos gradualmente.

**Pasos:**

- **PR 1** — Router/Facade: Crea un punto de entrada que puede dirigir a sistema viejo o nuevo
- **PR 2-N** — Migrar funcionalidad: Migra una funcionalidad a la vez al nuevo sistema
- **PR Final** — Eliminar sistema viejo: Remueve el sistema antiguo completamente

#### Ejemplo Java — Migrar procesamiento de pagos

```java
// PR 1: Router que decide qué sistema usar
public class PaymentRouter {
    private final LegacyPaymentService legacyService;
    private final NewPaymentService newService;
    private final FeatureToggleService featureToggle;

    public PaymentResponse processPayment(PaymentRequest request) {
        if (featureToggle.isEnabled("NEW_PAYMENT_SYSTEM", request.getUserId())) {
            return newService.process(request);
        }
        return legacyService.process(request);
    }
}

// PR 2: Implementar primera funcionalidad en nuevo sistema
public class NewPaymentService {
    public PaymentResponse process(PaymentRequest request) {
        validateRequest(request);
        return processWithNewProvider(request);
    }
}

// PR 3-N: Migrar más funcionalidades progresivamente
// PR Final: Eliminar LegacyPaymentService cuando todo esté migrado
```

#### Ejemplo Go — Migrar procesamiento de pagos

```go
// PR 1: Router que decide qué sistema usar
type PaymentRouter struct {
    legacyService *LegacyPaymentService
    newService    *NewPaymentService
    featureToggle *FeatureToggle
}
func (r *PaymentRouter) ProcessPayment(ctx context.Context, req PaymentRequest) (*PaymentResponse, error) {
    if r.featureToggle.IsEnabled("NEW_PAYMENT_SYSTEM", req.UserID) {
        return r.newService.Process(ctx, req)
    }
    return r.legacyService.Process(ctx, req)
}

// PR 2: Implementar primera funcionalidad en nuevo sistema
type NewPaymentService struct {
    provider PaymentProvider
}
func (s *NewPaymentService) Process(ctx context.Context, req PaymentRequest) (*PaymentResponse, error) {
    if err := s.validateRequest(req); err != nil {
        return nil, err
    }
    return s.processWithNewProvider(ctx, req)
}

// PR 3-N: Migrar más funcionalidades progresivamente
// PR Final: Eliminar LegacyPaymentService cuando todo esté migrado
```

---

### 3.3 Parallel Change (Expand-Contract)

Técnica para cambios que requieren modificar contratos o interfaces.

**Fases:**

- **Expand (PR 1):** Agregar nueva funcionalidad SIN remover la vieja
- **Migrate (PR 2-N):** Migrar consumidores gradualmente
- **Contract (PR Final):** Eliminar funcionalidad antigua

#### Ejemplo Java — Cambiar formato de respuesta API

```java
// PR 1 (Expand): Agregar nuevo campo sin romper existente
public class UserResponse {
    @Deprecated
    @JsonProperty("user_id")
    private Long userId;           // Viejo formato (deprecated)

    @JsonProperty("userId")
    private Long id;               // Nuevo formato

    @Deprecated
    @JsonProperty("full_name")
    private String fullName;       // Viejo formato (deprecated)

    @JsonProperty("fullName")
    private String name;           // Nuevo formato

    // Constructor que llena ambos campos
    public UserResponse(Long id, String name) {
        this.userId = id;   // Backward compatibility
        this.id = id;
        this.fullName = name; // Backward compatibility
        this.name = name;
    }
}

// PR 2-N (Migrate): Actualizar consumidores uno por uno
// Cliente móvil: PR 2 | Cliente web: PR 3 | Servicios internos: PR 4-N

// PR Final (Contract): Remover campos deprecated
public class UserResponse {
    @JsonProperty("userId")
    private Long id;

    @JsonProperty("fullName")
    private String name;

    public UserResponse(Long id, String name) {
        this.id = id;
        this.name = name;
    }
}
```

#### Ejemplo Go — Cambiar formato de respuesta API

```go
// PR 1 (Expand): Agregar nuevo campo sin romper existente
type UserResponse struct {
    // Deprecated: Usar UserId en su lugar
    UserIdOld   int64  `json:"user_id"`    // Viejo formato
    UserId      int64  `json:"userId"`     // Nuevo formato
    // Deprecated: Usar FullName en su lugar
    FullNameOld string `json:"full_name"`  // Viejo formato
    FullName    string `json:"fullName"`   // Nuevo formato
}
func NewUserResponse(id int64, name string) UserResponse {
    return UserResponse{
        UserIdOld:   id,   // Backward compatibility
        UserId:      id,
        FullNameOld: name, // Backward compatibility
        FullName:    name,
    }
}

// PR Final (Contract): Remover campos deprecated
type UserResponse struct {
    UserId   int64  `json:"userId"`
    FullName string `json:"fullName"`
}
func NewUserResponse(id int64, name string) UserResponse {
    return UserResponse{UserId: id, FullName: name}
}
```

---

### 3.4 Descomposición por capas

Divide el trabajo siguiendo las capas de tu arquitectura.

**Orden sugerido:**

- **PR 1** — Capa de datos: Modelos, entidades, schemas de BD
- **PR 2** — Capa de persistencia: Repositorios, DAOs, queries
- **PR 3** — Capa de negocio: Servicios, lógica de dominio
- **PR 4** — Capa de API: Controllers, endpoints, DTOs
- **PR 5** — Tests: Tests end-to-end y de integración

#### Ejemplo Java — Nueva funcionalidad de búsqueda

```java
// PR 1: Modelo de datos
// CREATE TABLE search_history (id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, ...)

@Entity
@Table(name = "search_history")
public class SearchHistory {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(name = "user_id", nullable = false)
    private Long userId;
    @Column(name = "search_term")
    private String searchTerm;
    @Column(name = "created_at")
    private LocalDateTime createdAt;
}

// PR 2: Repositorio
public interface SearchHistoryRepository extends JpaRepository<SearchHistory, Long> {
    List<SearchHistory> findByUserIdOrderByCreatedAtDesc(Long userId);
}

// PR 3: Servicio
@Service
public class SearchService {
    private final SearchHistoryRepository repository;
    public List<SearchResult> search(String term, Long userId) {
        repository.save(new SearchHistory(userId, term));
        return performSearch(term);
    }
}

// PR 4: API
@RestController
@RequestMapping("/api/search")
public class SearchController {
    @GetMapping
    public ResponseEntity<List<SearchResult>> search(
        @RequestParam String term,
        @AuthenticationPrincipal User user
    ) {
        return ResponseEntity.ok(searchService.search(term, user.getId()));
    }
}
```

---

### 3.5 Refactoring incremental

Para refactorings grandes, divide en pasos pequeños y seguros.

#### A) Preparar → Cambiar → Limpiar

```java
// PR 1 (Preparar): Extraer métodos sin cambiar comportamiento
private void processOrder(Order order) {
    validateOrder(order);
    calculateTotal(order);
    saveOrder(order);
}

// PR 2 (Cambiar): Mejorar un método a la vez
private void validateOrder(Order order) {
    if (order.getItems().isEmpty())
        throw new InvalidOrderException("Order must have items");
    if (order.getTotal().compareTo(BigDecimal.ZERO) <= 0)
        throw new InvalidOrderException("Order total must be positive");
}

// PR 3 (Limpiar): Remover código duplicado y obsoleto
```

#### B) Agregar paralelo → Migrar → Eliminar viejo

```java
// PR 1: Agregar nueva clase sin usarla aún
public class OrderProcessorV2 {
    public OrderResult process(Order order) {
        validateOrder(order);
        enrichOrderData(order);
        return executePayment(order);
    }
}

// PR 2: Usar con feature toggle
public class OrderService {
    public OrderResult processOrder(Order order) {
        if (featureToggle.isEnabled("ORDER_PROCESSOR_V2", order.getUserId()))
            return orderProcessorV2.process(order);
        return orderProcessor.process(order);
    }
}

// PR 3: Expandir uso gradualmente
// PR 4: Eliminar OrderProcessor viejo
```

---

## 4. Estrategias adicionales

### 4.1 Commits atómicos

Cada commit debe ser una unidad lógica completa que compila y pasa tests.

```bash
# ✅ Bueno: Commits atómicos
git commit -m "feat: agregar validación de email en User model"
git commit -m "feat: implementar endpoint POST /users"
git commit -m "test: agregar tests unitarios para UserService"

# ❌ Malo: Un commit gigante
git commit -m "feat: implementar sistema completo de usuarios"
```

> **Ventaja:** Puedes crear múltiples PRs pequeños a partir de commits individuales.

### 4.2 Stack de PRs

Para funcionalidades que requieren múltiples PRs secuenciales:

```text
PR #1 (base: main)    → Infraestructura básica
    ↓
PR #2 (base: PR#1)    → Capa de datos
    ↓
PR #3 (base: PR#2)    → Lógica de negocio
    ↓
PR #4 (base: PR#3)    → API endpoints
```

**Flujo:**

1. Abre PR#1 contra `main`
2. Una vez aprobado PR#1, haz merge
3. Abre PR#2 contra `main` (ahora incluye cambios de PR#1)
4. Repite el proceso

**Herramientas útiles:** `gh` CLI, Graphite, Aviator

### 4.3 Separar refactoring de nueva funcionalidad

> **Regla:** NUNCA mezcles refactoring con nueva funcionalidad en el mismo PR.

```text
❌ Malo:
PR: "Refactorizar UserService y agregar funcionalidad de exportación"

✅ Bueno:
PR #1: "refactor: simplificar UserService y extraer validaciones"
PR #2: "feat: agregar exportación de usuarios a CSV"
```

**Razón:** Facilita identificar si un bug viene del refactoring o de la nueva feature.

---

## 5. Nombrando mis PRs

### Formato

```text
<tipo>: <descripción en minúsculas>
```

**Tipos válidos:**

|Tipo|Uso|
|------|-----|
|`feat:`|Nueva funcionalidad|
|`fix:`|Corrección de errores|
|`hotfix:`|Corrección urgente en producción|
|`refactor:`|Refactorización de código|
|`test:`|Agregar o modificar tests|
|`docs:`|Cambios en documentación|

**Reglas:**

- Descripción en minúsculas (excepto nombres propios o acrónimos)
- Usar espacios, NO guiones bajos
- NO incluir el ID del ticket en el título (va en el cuerpo como `Refs: #CEB-XXXX`)
- Ser específico y descriptivo
- Máximo 50-72 caracteres

### ❌ Ejemplos incorrectos

```text
feat: CEB_1234_nuevo_onboarding_en_proveedor   ← ID en título y guiones bajos
CEB-1234: agregar validación                   ← ID al principio, sin tipo
FEAT: NUEVA FUNCIONALIDAD DE REPORTES          ← Todo en mayúsculas
actualizar código de usuarios                  ← Sin tipo de commit
fix: corregir_validacion_de_email              ← Guiones bajos
feat: cambios en la base de datos              ← Demasiado genérico
```

### ✅ Ejemplos correctos

```text
feat: implementar nuevo onboarding en proveedor
fix: corregir validación de email en formulario de registro
refactor: simplificar lógica de procesamiento de pagos
hotfix: corregir vulnerabilidad de seguridad en endpoint de login
test: agregar tests unitarios para servicio de notificaciones
docs: actualizar guía de instalación con requisitos de Java 17
feat: agregar exportación de reportes a formato Excel
fix: resolver timeout en consulta de órdenes con más de 1000 items
```

### Dónde va el ID del ticket

El ID del ticket **NO va en el título**. Debe incluirse en el cuerpo:

```text
feat: implementar autenticación con OAuth

Se agrega soporte para login usando proveedores OAuth:
- Configuración de Google OAuth
- Implementación de callback de autenticación
- Validación de tokens JWT
- Tests unitarios

Refs: #CEB-1234
```

### Tips para buenos títulos

- **Responde qué hace el cambio:** No "arreglar bug" sino "corregir validación de email"
- **Sé específico:** No "actualizar base de datos" sino "agregar índice a columna user_id en tabla orders"
- **Usa verbos en infinitivo:** "implementar", "agregar", "corregir", "refactorizar"
- **Piensa en el changelog:** Tu título podría aparecer en las notas de release
- **Si dudas, sé más descriptivo:** Es mejor un título largo y claro que uno corto y confuso

---

## 6. Checklist antes de abrir PR

### Tamaño y alcance

- [ ] El PR tiene < 400 líneas de código modificadas
- [ ] Toca < 10 archivos
- [ ] Se puede revisar en < 30 minutos
- [ ] Resuelve UN solo problema o agrega UNA funcionalidad

### Calidad

- [ ] Todos los tests pasan
- [ ] Cumple umbral de cobertura (50% mínimo)
- [ ] Linters pasan sin errores
- [ ] No hay conflictos con `main`

### Descripción

- [ ] Título claro siguiendo convención de commits
- [ ] Descripción explica el QUÉ y el POR QUÉ
- [ ] Incluye referencias a tickets (`Refs: #CEB-XXXX`)
- [ ] Screenshots/videos si hay cambios visuales
- [ ] **Si supera límites:** incluye sección de justificación de sobre límite

> Si alguna respuesta es **NO** → Considera dividir el PR usando las técnicas de la sección 3.

---

## 7. Tips para revisores

Si estás revisando un PR grande:

- **Solicita división:** Pide amablemente al autor dividirlo usando estas técnicas
- **Usa el template:** *"Este PR parece grande. ¿Podrías dividirlo usando Branch by Abstraction? Por ejemplo: PR1 para la abstracción, PR2 para la migración"*
- **Aprueba PRs pequeños rápido:** Incentiva el comportamiento que quieres ver

---

## 8. Recursos adicionales

- [Martin Fowler - Branch by Abstraction](https://martinfowler.com/bliki/BranchByAbstraction.html)
- [Parallel Change Pattern](https://martinfowler.com/bliki/ParallelChange.html)
- Documento relacionado: Proceso SDLC Estándar
