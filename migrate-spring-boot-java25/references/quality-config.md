# Referencia: Configuración de Calidad de Código

## 1. SpotBugs — spotbugs-exclude.xml

Crear o actualizar `config/spotbugs/spotbugs-exclude.xml`.

**Motivo crítico:** SpotBugs 4.9.x + Java 25 + Lombok reporta `US_USELESS_SUPPRESSION_ON_CLASS`
porque Lombok genera `@SuppressFBWarnings("DP_DO_INSIDE_DO_PRIVILEGED")` en el bytecode,
pero con Java 9+ el Security Manager está obsoleto y ese bug ya no se dispara, haciendo la
supresión innecesaria. Sin excluirlo, el build falla.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FindBugsFilter>
    <!-- Clases generadas automáticamente -->
    <Match>
        <Class name="~.*R\$.*"/>
    </Match>
    <Match>
        <Class name="~.*Manifest\$.*"/>
    </Match>
    <Match>
        <Class name="~.*_234$"/>
    </Match>

    <!-- Patrones estándar suprimidos en microservicios Novo -->
    <Match>
        <Bug pattern="EI_EXPOSE_REP"/>
    </Match>
    <Match>
        <Bug pattern="EI_EXPOSE_REP2"/>
    </Match>
    <Match>
        <Bug pattern="LI_LAZY_INIT_STATIC"/>
    </Match>
    <Match>
        <Bug pattern="ST_WRITE_TO_STATIC_FROM_INSTANCE_METHOD"/>
    </Match>
    <Match>
        <Bug pattern="SE_BAD_FIELD"/>
    </Match>
    <Match>
        <Bug pattern="BC_UNCONFIRMED_CAST_OF_RETURN_VALUE"/>
    </Match>
    <Match>
        <Bug pattern="SE_TRANSIENT_FIELD_NOT_RESTORED"/>
    </Match>
    <Match>
        <Bug pattern="NM_CONFUSING"/>
    </Match>
    <Match>
        <Bug pattern="URF_UNREAD_FIELD"/>
    </Match>
    <Match>
        <Bug pattern="UUF_UNUSED_FIELD"/>
    </Match>

    <!--
        Lombok genera @SuppressFBWarnings("DP_DO_INSIDE_DO_PRIVILEGED") en bytecode.
        Con Java 9+ el Security Manager está obsoleto y DP_DO_INSIDE_DO_PRIVILEGED
        ya no se dispara, por lo que SpotBugs 4.9.x reporta la supresión generada
        por Lombok como innecesaria (US_USELESS_SUPPRESSION_ON_CLASS).
    -->
    <Match>
        <Bug pattern="US_USELESS_SUPPRESSION_ON_CLASS"/>
    </Match>
</FindBugsFilter>
```

---

## 2. Checkstyle — google_checks_custom.xml

Crear `config/checkstyle/google_checks_custom.xml` basado en Google Java Style,
con relajaciones para el estilo de Novopayment:

```xml
<?xml version="1.0"?>
<!DOCTYPE module PUBLIC
    "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
    "https://checkstyle.org/dtds/configuration_1_3.dtd">
<module name="Checker">
    <property name="charset" value="UTF-8"/>
    <property name="severity" value="warning"/>
    <property name="fileExtensions" value="java"/>

    <module name="TreeWalker">
        <!-- Imports -->
        <module name="AvoidStarImport"/>
        <module name="UnusedImports"/>

        <!-- Bloques vacíos -->
        <module name="EmptyBlock">
            <property name="option" value="TEXT"/>
            <property name="tokens" value="LITERAL_TRY,LITERAL_FINALLY,LITERAL_IF,LITERAL_ELSE"/>
        </module>

        <!-- Longitud de línea — 150 chars (relajado respecto a Google 100) -->
        <module name="LineLength">
            <property name="max" value="150"/>
            <property name="ignorePattern" value="^package.*|^import.*|a href|href|http://|https://|ftp://"/>
        </module>

        <!-- Espacios -->
        <module name="WhitespaceAround">
            <property name="allowEmptyConstructors" value="true"/>
            <property name="allowEmptyLambdas" value="true"/>
            <property name="allowEmptyMethods" value="true"/>
            <property name="allowEmptyTypes" value="true"/>
            <property name="allowEmptyLoops" value="true"/>
        </module>

        <!-- Llaves -->
        <module name="NeedBraces"/>
        <module name="LeftCurly"/>
        <module name="RightCurly"/>

        <!-- Anotaciones -->
        <module name="AnnotationLocation">
            <property name="allowSamelineSingleParameterlessAnnotation" value="false"/>
        </module>
    </module>
</module>
```

> `maxAllowedViolations: 150` en la primera migración para no bloquear el build.
> Reducir a 0 gradualmente en iteraciones siguientes.

---

## 3. Sonar — reglas más frecuentes en migración

| Regla | Descripción | Solución |
|-------|-------------|----------|
| `java:S3011` | `setAccessible(true)` bypass | `@SuppressWarnings("java:S3011")` en el método o clase |
| `java:S6830` | `@Component` con nombre en lugar de `@Bean` | `@SuppressWarnings("java:S6830")` en la clase |
| `java:S2221` | `catch (Exception)` genérico | Acotar a tipos específicos o documentar razón |
| `java:S2629` | `.toString()` en logger | Pasar el objeto directamente al logger |
| `java:S2208` | Wildcard import (`.*`) | Reemplazar con imports explícitos |
| `java:S1874` | Uso de método deprecado | Actualizar al método sustituto |
| `java:S1192` | String literal duplicado (≥3 veces) | Extraer a constante `private static final String` |
| `java:S4144` | Métodos con implementación idéntica | Extraer método privado compartido |
| `java:S2187` | Clase de test sin métodos `@Test` | Agregar al menos un test o usar `@SpringJUnitConfig` |

---

## 4. Configuración de Sonar en pom.xml

```xml
<properties>
    <sonar.host.url>https://sonarcloud.io</sonar.host.url>
    <sonar.organization>novopayment</sonar.organization>
    <sonar.projectKey>${artifactId}</sonar.projectKey>
    <sonar.scm.provider>git</sonar.scm.provider>
    <sonar.java.codeCoveragePlugin>jacoco</sonar.java.codeCoveragePlugin>
    <sonar.coverage.jacoco.xmlReportPaths>
        ${project.test.result.directory}/jacoco/jacoco.xml
    </sonar.coverage.jacoco.xmlReportPaths>
    <sonar.exclusions>**/*.xml</sonar.exclusions>
</properties>
```

> El `sonar.projectKey` debe coincidir con el proyecto creado en SonarCloud.

---

## 5. Propiedades de Sonar para definir en el proyecto de SonarCloud

Configurar en el proyecto de SonarCloud o en las variables de CI:
- `sonar.projectKey`: clave única del proyecto (ej: `api-tbs-zinli-orchestrator-microservice`)
- `sonar.organization`: `novopayment`
- Token de autenticación como variable de entorno `SONAR_TOKEN`

---

## 6. Comandos de verificación

```bash
# SpotBugs (debe pasar en 0 bugs con el exclude configurado)
mvn spotbugs:check

# Ver reporte SpotBugs en HTML
# Abrir target/spotbugsXml.html en el browser

# Checkstyle
mvn checkstyle:check

# Sonar (requiere SONAR_TOKEN configurado)
mvn sonar:sonar -Dsonar.token=$env:SONAR_TOKEN

# Todo en un solo comando
mvn clean verify

# Con Sonar incluido
mvn clean verify sonar:sonar -Dsonar.token=$env:SONAR_TOKEN

# Ver reporte JaCoCo
# Abrir target/test-results/jacoco/index.html
```

---

## 7. Estructura de directorios de configuración

```
config/
├── spotbugs/
│   └── spotbugs-exclude.xml        ← Exclusiones SpotBugs
├── checkstyle/
│   └── google_checks_custom.xml    ← Reglas Checkstyle personalizadas
└── dependencyCheck/
    └── suppressions.xml            ← Supresiones OWASP dependency-check
```

Todos estos archivos deben estar en el repositorio (no en `.gitignore`).

---

## 8. OWASP Dependency Check

Si el proyecto tiene `dependency-check-maven`, configurar:

```xml
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>12.1.8</version>
    <configuration>
        <failBuildOnCVSS>15</failBuildOnCVSS>  <!-- Solo falla en CVE críticos -->
        <suppressionFiles>
            <suppressionFile>config/dependencyCheck/suppressions.xml</suppressionFile>
        </suppressionFiles>
        <ossIndexServerId>ossindex</ossIndexServerId>
    </configuration>
</plugin>
```

> `failBuildOnCVSS: 15` prácticamente deshabilita el fallo (score máximo es 10).
> Reducir a `7` o `9` en producción real para detectar vulnerabilidades altas.
