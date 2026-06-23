# Catálogo de Tipos de Pase a Producción — NovoPayment

## Cómo usar este archivo

Cuando el usuario solicite crear un CDPP o una subtarea, **primero** pregunta:

> "¿Qué tipo de pase es? Elige una opción:
>
> 1. Microservicio (Kubernetes Rolling Update)
> 2. Base de Datos (DDL / DML — Oracle / PostgreSQL)
> 3. WAR / JAR (servidor de aplicaciones Tomcat / JBoss / WildFly)
> 4. Configuración pura (solo ConfigMap / variables / properties, sin nuevo artefacto)
> 5. Proceso Agendado / Batch (scheduler, cron job, K8s CronJob)
> 6. Infraestructura (certificados SSL, balanceadores, DNS, red)"

El tipo seleccionado determina:
- El formulario de datos a solicitar al usuario
- El equipo ejecutor por defecto (Category en Jira)
- Si el cambio genera indisponibilidad
- El template de subtarea a usar

---

## Resumen rápido

| # | Tipo | Equipo Ejecutor | Downtime | Rollback | Ejemplo validado |
|---|------|----------------|----------|----------|-----------------|
| 1 | Microservicio K8s | Infra Middleware | No | Imagen + ConfigMap | CDPP-35117 ✅ |
| 2 | Base de Datos DDL/DML | Infra BD | No* | Backup + script | CDPP-34680 ✅ |
| 3 | WAR / JAR | Infra Middleware | Depende | Artefacto anterior | *(pendiente)* |
| 4 | Configuración pura | Infra Middleware / Backend | Depende | ConfigMap/properties anterior | *(pendiente)* |
| 5 | Proceso Agendado / Batch | Backend / Infra Middleware | No | Desactivar job | *(pendiente)* |
| 6 | Infraestructura | DevOps / Infra | Depende | Config previa | *(pendiente)* |

*Oracle DDL (CREATE OR REPLACE PACKAGE) no bloquea DML concurrente.

---

## Tipo 1 — Microservicio (Kubernetes Rolling Update)

**Equipo ejecutor:** Infra Middleware  
**Genera indisponibilidad:** No (K8s gestiona el rolling update)  
**Rollback:** Rollback de imagen Docker + rollback del ConfigMap si hay variables nuevas  
**Ejemplo validado:** [CDPP-35117](https://jira4novo.atlassian.net/browse/CDPP-35117) — subtarea: [CDPP-35124](https://jira4novo.atlassian.net/browse/CDPP-35124)

### Formulario de datos — mostrar al usuario

```
- Nombre del componente (ej: api-tbs-zinli-orchestrator-microservice):
- Versión a desplegar (ej: v2.3.3):
- Versión actual en PRD (si se conoce):
- Namespace / Cluster en PRD:
- Ticket de certificación CEB:
- Cliente:
- País:
- Tipo de pase (NORMAL | STANDARD | EMERGENTE):
- Descripción del cambio (incidente que origina, qué mejoras incluye la versión):
- Variables de entorno nuevas o modificadas:
  (nombre | valor de PRD | descripción corta)
- ¿La imagen cambia Java, runtime base u otras dependencias críticas? (SI/NO → cuáles):
- ¿Hay cambios en la configuración de RabbitMQ, BD u otras integraciones? (SI/NO → cuáles):
```

### Qué aplica en el CDPP

- **Situación Inicial:** Describir el incidente o problema observado en producción. Si hubo más de un incidente, nombrar cada uno con fecha y síntoma concreto (ej: CPU spike, pod Running con transacciones fallidas, pérdida de mensajes).
- **Situación Final:** Un bullet por cada mejora o fix del release. Incluir la versión (`v2.3.3`). Terminar con frase de alcance acotado.
- **Plan de Rollback — Consideraciones:** Si hay variables nuevas en el ConfigMap, indicar que el rollback de la imagen debe acompañarse del rollback del ConfigMap. Sin revertir el ConfigMap la versión anterior puede no conectar correctamente a las integraciones.
- **Revisión Postproducción:** Verificar: estado del pod (Running), logs de startup, transacción E2E, CPU/memoria primeros 15 minutos, ACKs en RabbitMQ (si aplica), variables del ConfigMap configuradas.

### Qué aplica en la subtarea

- **Título:** `PASO N: [Infra Middleware] Kubernetes - Rolling Update - <componente> — Despliegue v<X.X.X> <descripción>`
- **Sección Datos del Componente:** tabla con nombre, versión actual en PRD, versión a desplegar, namespace/cluster, tipo de despliegue.
- **Sección Variables de Entorno:** tabla con TODAS las variables del ConfigMap (nombre, descripción, valor de PRD) + bloque YAML listo para aplicar.
- **Orden de ejecución:** (1) confirmar variables en PRD, (2) desplegar imagen, (3) verificar pods Running, (4) validaciones post-ejecución.
- **Rollback:** rollback del deployment (imagen) + restauración del ConfigMap.

---

## Tipo 2 — Base de Datos (DDL / DML — Oracle / PostgreSQL)

**Equipo ejecutor:** Infra BD  
**Genera indisponibilidad:** No (compilación DDL en Oracle no bloquea DML concurrente)  
**Rollback:** Restaurar desde backup o ejecutar script de rollback preparado  
**Ejemplo validado:** CDPP-34680

### Formulario de datos — mostrar al usuario

```
- Nombre del esquema (ej: ORION214001):
- Base de datos / SID (ej: novo):
- Servidor / Ruta (ej: p-db-mw-1.novopayment.net):
- Puerto:
- Objetos afectados (nombre, tipo: PACKAGE / TABLE / INDEX / SP / VIEW / TRIGGER):
- Tipo de operación:
    DDL → CREATE OR REPLACE / ALTER / DROP
    DML → INSERT / UPDATE / DELETE (con volumen estimado de registros)
- Archivos SQL a ejecutar (nombres en orden):
- ¿Hay script de rollback preparado? (SI/NO):
- Ticket de certificación CEB:
- Cliente:
- País:
- Tipo de pase (NORMAL | STANDARD | EMERGENTE):
- Descripción del cambio (qué reporta mal y qué corrige):
```

### Qué aplica en el CDPP

- **Situación Inicial:** El comportamiento incorrecto observable por el usuario o el sistema (ej: reporte muestra ID interno en lugar del número de documento real).
- **Situación Final:** El comportamiento correcto tras el cambio. Aclarar qué objetos no se modifican.
- **Plan de Rollback:** Restauración desde backup del equipo de BD + query de verificación post-rollback (STATUS = 'VALID'). Si hay script de rollback, listarlo.

### Qué aplica en la subtarea

- **Título:** `PASO N: [Infra BD] Oracle - DDL - <ESQUEMA>.<OBJETO> — <descripción>`
- **Sección Datos del Esquema Destino:** tabla con esquema, SID, servidor, puerto.
- **Sección Objetos Afectados:** tabla con esquema / objeto / tipo / acción.
- **Validaciones Post-Ejecución:** query que verifica STATUS = 'VALID' y query de errores de compilación (0 filas esperadas).

---

## Tipo 3 — WAR / JAR (Servidor de Aplicaciones)

**Equipo ejecutor:** Infra Middleware  
**Genera indisponibilidad:** Depende — hot-deploy = no; reinicio del servidor = sí (indicar ventana)  
**Rollback:** Restaurar el WAR/JAR anterior en la ruta de deploy  
**Ejemplo validado:** *(pendiente — agregar cuando se tenga un CDPP validado)*

### Formulario de datos — mostrar al usuario

```
- Nombre del componente / aplicación:
- Versión a desplegar:
- Versión actual en PRD:
- Servidor de aplicaciones (Tomcat / JBoss / WildFly):
- Ruta de deploy en el servidor:
- Nombre del archivo a desplegar (ej: api-tbs-zinli-auth.war):
- ¿Requiere detener y reiniciar el servidor? (SI/NO):
- ¿Genera ventana de mantenimiento? (SI/NO → duración estimada):
- ¿Hay cambios en properties o variables de entorno del servidor? (SI/NO → cuáles):
- Ticket de certificación CEB:
- Cliente:
- País:
- Tipo de pase (NORMAL | STANDARD | EMERGENTE):
- Descripción del cambio:
```

### Qué aplica en el CDPP

- **Plan de Rollback — Consideraciones:** Si requiere reinicio del servidor → el pase genera indisponibilidad. Indicar duración estimada y ventana acordada.
- **Revisión Postproducción:** Verificar que el contexto de la aplicación levanta sin errores en el log del servidor de aplicaciones + endpoint de health si existe.

### Qué aplica en la subtarea

- **Título:** `PASO N: [Infra Middleware] <Servidor> - Deploy - <componente> — Despliegue v<X.X.X>`
- **Sección Datos del Componente:** nombre, versión actual, versión nueva, servidor, ruta, tipo de despliegue (Hot-deploy / Reinicio).
- Si hay cambios en properties, incluir tabla antes/después de cada parámetro.

---

## Tipo 4 — Configuración pura (ConfigMap / Properties / Variables)

**Equipo ejecutor:** Infra Middleware o Backend  
**Genera indisponibilidad:** Depende — K8s ConfigMap sin reinicio = no; con reinicio del pod = breve  
**Rollback:** Revertir el ConfigMap / archivo de propiedades a la versión anterior  
**Ejemplo validado:** *(pendiente)*

### Formulario de datos — mostrar al usuario

```
- Componente / microservicio afectado:
- ¿Dónde vive la configuración? (ConfigMap K8s / application.properties / Secret / variable en servidor):
- Variables o propiedades que cambian:
  (nombre | valor anterior | valor nuevo | motivo)
- ¿El cambio requiere reinicio del pod/servicio? (SI/NO):
- ¿Hay otros servicios que consuman esta configuración y se vean afectados? (SI/NO → cuáles):
- Ticket de certificación CEB:
- Cliente:
- País:
- Tipo de pase (NORMAL | STANDARD | EMERGENTE):
- Motivo del cambio:
```

### Qué aplica en el CDPP

- **Situación Inicial:** El comportamiento actual con la configuración vigente.
- **Situación Final:** El comportamiento esperado con los nuevos valores. Aclarar que no se despliega nuevo artefacto.
- **Afectación:** Si no requiere reinicio → no genera indisponibilidad. Si sí requiere reinicio → indicar que habrá un breve período de pod en Terminating.

### Qué aplica en la subtarea

- No incluye sección de imagen/versión de artefacto.
- **Sección Variables:** tabla nombre / valor anterior / valor nuevo. Si es ConfigMap K8s, incluir el bloque YAML completo.
- **Validación:** comando `kubectl describe configmap <nombre>` o equivalente para confirmar los nuevos valores aplicados.

---

## Tipo 5 — Proceso Agendado / Batch

**Equipo ejecutor:** Backend o Infra Middleware  
**Genera indisponibilidad:** No (generalmente)  
**Rollback:** Desactivar el job / restaurar versión anterior del componente que lo contiene  
**Ejemplo validado:** *(pendiente)*

### Formulario de datos — mostrar al usuario

```
- Nombre del proceso / job:
- Tipo de scheduler (Spring Batch / Quartz / cron OS / K8s CronJob / otro):
- Expresión cron actual (si existe):
- Expresión cron nueva (si cambia):
- ¿Qué hace el job? (descripción funcional):
- ¿Modifica datos en base de datos? (SI/NO → tablas y volumen estimado):
- ¿Se puede ejecutar manualmente para prueba? (SI/NO):
- ¿El job está embebido en un microservicio existente? (SI → ¿cuál?):
- Ticket de certificación CEB:
- Cliente:
- País:
- Tipo de pase (NORMAL | STANDARD | EMERGENTE):
- Descripción del cambio:
```

### Qué aplica en el CDPP

- **Situación Inicial:** El comportamiento del job actual (o la ausencia del job si es nuevo).
- **Plan de Rollback:** Si el job solo lee datos → desactivarlo es suficiente. Si modifica datos → se necesita script DML de reversión; aplicar también el Tipo 2.

### Qué aplica en la subtarea

- Incluir la expresión cron (anterior y nueva) si aplica.
- **Validación Post-Ejecución:** log de primera ejecución del job + resultado esperado (registros procesados, sin errores).

---

## Tipo 6 — Infraestructura (Certificados / LB / DNS / Red)

**Equipo ejecutor:** DevOps / Infra  
**Genera indisponibilidad:** Depende del cambio (renovación de cert puede causar flap breve)  
**Rollback:** Revertir a la configuración previa  
**Ejemplo validado:** *(pendiente)*

### Formulario de datos — mostrar al usuario

```
- Tipo de cambio (certificado SSL / balanceador / DNS / regla de firewall / red):
- Componente / endpoint / dominio afectado:
- ¿Genera ventana de mantenimiento? (SI/NO → duración estimada):
- ¿Hay impacto en clientes o usuarios finales durante el cambio? (SI/NO → cuánto tiempo):
- Ticket de certificación CEB:
- Cliente:
- País:
- Tipo de pase (NORMAL | STANDARD | EMERGENTE):
- Descripción del cambio:
```

---

## Combinaciones frecuentes (pases compuestos)

Algunos pases incluyen más de un tipo. En ese caso, crear una subtarea por cada tipo:

| Combinación | Subtareas |
|-------------|-----------|
| Microservicio + variables nuevas | PASO 1: Infra Middleware (Config pura) → PASO 2: Infra Middleware (K8s deploy) |
| Microservicio + scripts BD | PASO 1: Infra BD (DDL/DML) → PASO 2: Infra Middleware (K8s deploy) |
| WAR + properties | PASO 1: Infra Middleware (Config) → PASO 2: Infra Middleware (WAR deploy) |
| Batch nuevo embebido en micro | PASO 1: Infra Middleware (K8s deploy del micro que lo contiene) |
