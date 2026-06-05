# Referencia: Librerías internas Novopayment

Catálogo de librerías `com.novo.microservices.utils` disponibles en GitHub Packages
(`https://maven.pkg.github.com/novopayment/central-repository`).

Fuente: POMs del caché local `~/.m2/repository/com/novo/microservices/utils/`.
Actualizado: junio 2026.

---

## Catálogo de librerías

### novo-microservices-tbs-transactions-utils

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 1.7.0 | 2.7.x | 11 | Versión anterior a la migración |
| 1.9.0 | 2.7.x | 11 | — |
| 3.0.0 | 3.5.8 | 25 | **Versión actual** — usa `findbugs:annotations` transitivo |

**Usada en:** microservicios TBS (orquestadores de transacciones).
**Incluye:** mapstruct 1.6.3, guava 33.4.0-jre, gson, modelmapper, httpclient.

> ⚠️ `3.0.0` aún depende de `findbugs:annotations:3.0.1u2` como `compile`. No agregar
> `@SuppressFBWarnings` en el microservicio propio, pero la librería lo trae transitivamente
> — no hay que excluirlo, SpotBugs lo ignorará con el `spotbugs-exclude.xml`.

---

### novo-microservices-utils-messaging-broker

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 3.1.0 | 2.7.x | 11 | Versión anterior a la migración |
| 3.2.0 | 2.7.x | 11 | — |
| 4.0.1 | 3.5.x | 25 | **Versión usada en zinli** |
| 5.0.0 | 3.5.13 | 25 | Versión más reciente — usa `--enable-preview` |

> ⚠️ **Si se actualiza a `5.0.0`**, la librería compila con `--enable-preview`. El microservicio
> consumidor también necesitará ese flag en `maven-compiler-plugin` y `maven-surefire-plugin`:
>
> ```xml
> <compilerArgs>
>     <arg>--enable-preview</arg>
> </compilerArgs>
> ```
>
> ```xml
> <!-- surefire -->
> <argLine>@{jacocoArgLine} --enable-preview -XX:+EnableDynamicAgentLoading</argLine>
> ```
>
> Para evitar esta complejidad, mantener `4.0.1` hasta que sea necesario subir.

---

### novo-microservices-utils-configurations-loader

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 3.0.0 | 2.x | 11 | Versión antigua |
| 4.4.0 | 2.7.x | 11 | Versión anterior a la migración |
| 5.0.0-SNAPSHOT | 3.5.x | 25 | **Versión actual** — resuelve colisión de bean `commonApplicationInfo` |

> La actualización de `4.4.0` → `5.0.0-SNAPSHOT` fue la solución definitiva al error
> `duplicate bean: commonApplicationInfo` en Spring Boot 3. La versión 4.x definía un bean
> que colisionaba con el bean definido por `novo-microservices-utils:4.1.0`.

---

### novo-microservices-utils

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 3.5.2 | 2.7.x | 11 | Versión anterior a la migración |
| 3.5.9 | 2.7.x | 11 | — |
| 3.6.1 | 2.7.x | 11 | — |
| 4.1.0 | 3.5.9 | 25 | **Versión actual** |

**Incluye transitivamente:** `springdoc-openapi-starter-common:2.8.15`, `yasson:3.0.4` (Jakarta EE 3),
`modelmapper`, `spotbugs-annotations:4.7.3`.

> ⚠️ Esta librería incluye `spring-boot-starter-web`. En proyectos **WebFlux** siempre excluirlo:
> ```xml
> <exclusions>
>     <exclusion>
>         <groupId>org.springframework.boot</groupId>
>         <artifactId>spring-boot-starter-web</artifactId>
>     </exclusion>
> </exclusions>
> ```

---

### novo-microservices-common-utils

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 2.1.0 | 2.7.x | 11 | Versión anterior |
| 4.0.0 | 3.5.x | 25 | **Versión actual** |

**Usada en:** microservicios que necesitan utilidades comunes (no reactivos).

---

### novo-microservices-common-reactive-utils

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 1.3.1 | 2.7.x | 11 | Versión anterior a la migración |
| 1.4.1 | 3.5.x | 25 | **Versión actual** |

**Usada en:** microservicios WebFlux con utilidades reactivas comunes.

---

### novo-microservices-common-general-reactive-utils

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 2.0.0 | 3.5.0 | 21 | Java 21, no Java 25 todavía |

> ℹ️ Esta librería aún está en Java 21 y usa `novo-microservices-utils:4.0.0-SNAPSHOT`.
> Si el microservicio ya migró a Java 25, puede haber incompatibilidad de bytecode.
> Verificar antes de usar.

---

### novo-microservices-utils-multi-tenant-repository

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 3.1.0 | 2.7.x | 11 | Versión anterior |
| 4.0.0 | 3.5.9 | 25 | **Versión estable** |

**Usada en:** microservicios con acceso a base de datos multi-tenant (Oracle JDBC).
**Incluye:** `spring-boot-starter-data-jdbc`, `spotbugs-annotations:4.9.8`.

> Si el microservicio usa Oracle multi-tenant, agregar también:
> ```xml
> <dependency>
>     <groupId>com.oracle.database.jdbc</groupId>
>     <artifactId>ojdbc17</artifactId>
> </dependency>
> <dependency>
>     <groupId>org.springframework</groupId>
>     <artifactId>spring-jdbc</artifactId>
> </dependency>
> ```

---

### novo-microservices-utils-security-encryption

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 4.2.0 | — | — | — |
| 4.4.0 | — | — | **Versión más reciente disponible** |

**Usada en:** microservicios que manejan encriptación JWE/JWA.

---

### novo-microservices-utils-security-jwa

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 4.1.0 | — | — | **Versión disponible** |

**Usada en:** microservicios con autenticación JWT/JWA.

---

### novo-microservices-common-repository-utils

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 5.0.0 | **2.4.0** | **8** | OBSOLETA — no compatible con SB 3 ni Java 25 |

> ❌ **No usar en la migración.** A pesar del número de versión alto (5.0.0), esta librería
> fue compilada con Spring Boot 2.4.0 y Java 8. Usa Hazelcast client 3.12.x y depende de
> `novo-microservices-utils-configurations-loader:4.4.0` (versión SB 2.x).
> Si algún microservicio la usa, necesita un reemplazo o actualización de esta librería primero.

---

### lib-mcr-common-utils

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 1.0.0 | 3.5.x | 25 | — |
| 1.0.1 | 3.5.9 | 25 | **Versión actual** — desarrollada por cbacilio |

**groupId:** `com.novo.microservices.utils`

**Usada en:** microservicios Core Credit reactivos (nuevo patrón de plantilla).
**Incluye:** WebFlux, AMQP, JPA, mapstruct 1.6.3, novo-microservices-utils 4.1.0, messaging-broker 4.0.1.

> Esta librería es una **plantilla base moderna** para nuevos microservicios reactivos.
> Excluye variantes de `log4j-slf4j*` que causan conflicto con log4j2 standalone.

---

### banking-utils

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 1.0.1 | **2.7.1** | **11** | No migrada — SB 2.x / Java 11 |

**groupId:** `com.novo.banking.utils` *(groupId distinto)*

> ⚠️ **No compatible con SB 3 sin migración previa.** Usa `javax.validation` (no jakarta),
> `ojdbc11:21.7.0.0`, `guava:12.0` (muy antigua). Si un microservicio la depende, es un
> **bloqueante** para la migración — hay que migrar esta librería antes o reemplazarla.

---

### lib-microservices-utils

| Versión | Spring Boot | Java | Notas |
|---------|-------------|------|-------|
| 1.0.8 | 2.7.18 | — | OBSOLETA — naming scheme antiguo |

**groupId:** `com.novo.microservices.utils`

> ❌ **No usar.** Librería de naming scheme antiguo (`lib-*`). Incluye `javax.json.bind:1.0`,
> `yasson:1.0`, `springdoc-openapi-ui:1.6.15` — todos obsoletos en SB 3.
> Su reemplazo funcional es `novo-microservices-utils:4.1.0`.

---

## Tabla de equivalencias: versión anterior → versión nueva

| Librería | groupId | Versión SB 2.x | Versión SB 3.5.x | Estado |
|----------|---------|----------------|------------------|--------|
| `novo-microservices-tbs-transactions-utils` | `com.novo.microservices.utils` | 1.7.0 | **3.0.0** | ✅ Migrada |
| `novo-microservices-utils-messaging-broker` | `com.novo.microservices.utils` | 3.1.0 | **4.0.1** *(o 5.0.0)* | ✅ Migrada |
| `novo-microservices-utils-configurations-loader` | `com.novo.microservices.utils` | 4.4.0 | **5.0.0-SNAPSHOT** | ✅ Migrada |
| `novo-microservices-utils` | `com.novo.microservices.utils` | 3.5.2 | **4.1.0** | ✅ Migrada |
| `novo-microservices-common-utils` | `com.novo.microservices.utils` | 2.1.0 | **4.0.0** | ✅ Migrada |
| `novo-microservices-common-reactive-utils` | `com.novo.microservices.utils` | 1.3.1 | **1.4.1** | ✅ Migrada |
| `novo-microservices-utils-multi-tenant-repository` | `com.novo.microservices.utils` | 3.1.0 | **4.0.0** | ✅ Migrada |
| `novo-microservices-common-general-reactive-utils` | `com.novo.microservices.utils` | — | 2.0.0 (Java 21) | ⚠️ Parcial |
| `lib-mcr-common-utils` | `com.novo.microservices.utils` | — | **1.0.1** | ✅ Nueva SB 3 |
| `novo-microservices-utils-security-encryption` | `com.novo.microservices.utils` | 4.2.0 | **4.4.0** | ❓ Sin confirmar SB 3 |
| `novo-microservices-utils-security-jwa` | `com.novo.microservices.utils` | — | **4.1.0** | ❓ Sin confirmar SB 3 |
| `novo-microservices-common-repository-utils` | `com.novo.microservices.utils` | 5.0.0 | ❌ No disponible | 🚫 Obsoleta (Java 8) |
| `banking-utils` | `com.novo.banking.utils` | 1.0.1 | ❌ No disponible | 🚫 Sin migrar (Java 11) |
| `lib-microservices-utils` | `com.novo.microservices.utils` | 1.0.8 | ❌ No disponible | 🚫 Obsoleta |

---

## Notas sobre findbugs transitivo

Las librerías `novo-microservices-tbs-transactions-utils:3.0.0` y
`novo-microservices-utils-messaging-broker:5.0.0` aún incluyen `findbugs:annotations` como
dependencia `compile`. Esto es una decisión de las librerías, no del microservicio.

**Comportamiento:** el JAR de findbugs estará en el classpath del microservicio aunque lo
hayamos eliminado del `pom.xml` propio. Esto es inofensivo: SpotBugs 4.9.x en Java 25 lo
ignora correctamente gracias a `US_USELESS_SUPPRESSION_ON_CLASS` en el `spotbugs-exclude.xml`.

**No hay que agregar exclusiones** en cada dependencia para quitar findbugs transitivo — no
aporta nada y complica el `pom.xml`.

---

## Cómo verificar versiones disponibles en GitHub Packages

```bash
# Listar versiones disponibles de una librería (requiere gh login)
gh api "orgs/novopayment/packages/maven/com.novo.microservices.utils:ARTIFACT_ID/versions" \
  --jq '.[] | "\(.name) — creado: \(.created_at)"'

# Alternativa: ver versiones en el caché local de Maven
dir "$env:USERPROFILE\.m2\repository\com\novo\microservices\utils\ARTIFACT_ID"
```

> El token de `gh` necesita el scope `read:packages` para acceder a la API de packages.
> Si da `403`, las versiones disponibles se pueden ver directamente en
> https://github.com/orgs/novopayment/packages con sesión activa en GitHub.
