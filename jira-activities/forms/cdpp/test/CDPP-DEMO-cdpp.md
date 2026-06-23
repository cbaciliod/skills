# [PRD][DEMO][US][STANDARD] - Corrección de NullPointerException en procesamiento de pagos recurrentes con externalReference nulo

**Tickets relacionados:** [CEB-9999](https://jira4novo.atlassian.net/browse/CEB-9999)

---

## Situación Inicial

El microservicio `api-tbs-demo-payment-microservice` presentó un error en el procesamiento de pagos recurrentes cuando el campo `externalReference` llega con valor nulo desde el cliente. Al recibir el request, el handler intentaba acceder al valor del campo sin validación previa, generando un `NullPointerException` no controlado. Como consecuencia, la transacción quedaba persistida en estado `PENDING` de forma indefinida, sin avanzar al procesamiento ni notificar el error al cliente. El problema no generaba alerta visible en los dashboards de monitoreo porque la excepción era absorbida por el handler global, retornando HTTP 500 sin registro en el sistema de alertas.

Adicionalmente, la versión actual del pool de conexiones (`hikari-cp 5.0.1`) presentaba un comportamiento conocido de pérdida de conexiones inactivas bajo carga baja sostenida, documentado en el changelog de la librería.

---

## Situación Final

Tras el despliegue de la versión `v1.4.2` del microservicio `api-tbs-demo-payment-microservice`, el servicio operará con las siguientes mejoras:

- **Validación de `externalReference`:** El request handler valida el campo antes de persistir la transacción. Si el valor es nulo o vacío, retorna HTTP 400 con mensaje de error descriptivo y registra el evento en los logs de auditoría. La transacción no se persiste en estado inválido.
- **Actualización de hikari-cp a 5.1.0:** Incorpora el fix para pérdida de conexiones inactivas bajo carga baja sostenida, mejorando la estabilidad del pool de conexiones a base de datos.
- **Nuevos parámetros de reintento externalizados:** Los valores de `maxRetry` y `retryDelayMs` se resuelven desde variables de entorno (`ENV_PAYMENT_MAX_RETRY` y `ENV_PAYMENT_RETRY_DELAY_MS`), permitiendo ajuste por ambiente sin necesidad de redespliegue.

Se garantiza que el cambio es acotado al microservicio `api-tbs-demo-payment-microservice` y no afecta otras funcionalidades ni servicios existentes del cliente DEMO.

---

## Plan de Certificación

Se realizó la certificación en ambiente TEST. Se verificó:

- Que al enviar un request con `externalReference` nulo, el servicio retorna HTTP 400 con mensaje de error descriptivo y no persiste la transacción.
- Que al enviar un request válido con `externalReference` presente, el flujo completo de pago recurrente opera correctamente.
- Que la actualización de hikari-cp 5.1.0 no introduce cambios de comportamiento en la gestión del pool de conexiones bajo carga normal.
- Que los parámetros `ENV_PAYMENT_MAX_RETRY` y `ENV_PAYMENT_RETRY_DELAY_MS` se leen correctamente desde variables de entorno con los valores configurados.
- Que no se introducen regresiones en otros flujos del microservicio (pagos únicos, consultas de estado).

Ticket de certificación: [CEB-9999](https://jira4novo.atlassian.net/browse/CEB-9999)

---

## Afectación

En caso de que el pase no sea exitoso:

- El microservicio `api-tbs-demo-payment-microservice` podría quedar en estado degradado si la nueva versión presenta algún problema de compatibilidad con el ambiente de producción.
- El alcance del impacto está acotado exclusivamente al procesamiento de pagos recurrentes del cliente DEMO.
- No se afectan otras funcionalidades del cliente DEMO ni otros microservicios del ecosistema.
- El rollback restaura la versión `v1.4.1` del microservicio y el ConfigMap previo, devolviendo el servicio al estado operativo anterior al pase sin indisponibilidad perceptible para el usuario final.

---

## Plan de Rollback

**Consideraciones:**

- El cambio afecta exclusivamente al microservicio `api-tbs-demo-payment-microservice`.
- El despliegue no genera indisponibilidad, dado que Kubernetes gestiona el rolling update de los pods.
- El rollback de la imagen debe acompañarse del rollback del ConfigMap al estado previo, ya que se añaden 2 variables nuevas (`ENV_PAYMENT_MAX_RETRY` y `ENV_PAYMENT_RETRY_DELAY_MS`). Sin revertir el ConfigMap, la versión anterior podría iniciar con variables no reconocidas.
- No se realizan cambios de esquema en base de datos ni modificaciones en infraestructura compartida.

**Acciones de rollback:**

1. Identificar la versión anterior `v1.4.1` del artefacto `api-tbs-demo-payment-microservice` desplegada en producción.
2. Restaurar el ConfigMap al estado previo al pase (sin las 2 variables nuevas).
3. Ejecutar el rollback del deployment en Kubernetes hacia la versión `v1.4.1` de la imagen.
4. Verificar que los pods levantan correctamente en estado `Running` con health checks verdes.
5. Validar que el servicio procesa pagos recurrentes correctamente ejecutando una transacción de prueba.
6. Notificar al equipo de soporte y al Líder Técnico el rollback ejecutado.

**Alcance del rollback:**

- Se revierte: la imagen del microservicio `api-tbs-demo-payment-microservice` y el ConfigMap de variables de entorno.
- No se ve afectado: los manifiestos de Kubernetes ni otros microservicios del ecosistema DEMO.

---

## Revisión Postproducción

- Verificar que los pods de `api-tbs-demo-payment-microservice` levantan correctamente en estado `Running`.
- Ejecutar una transacción de pago recurrente con `externalReference` válido y verificar respuesta correcta.
- Ejecutar una transacción con `externalReference` nulo y verificar que retorna HTTP 400 con mensaje descriptivo.
- Confirmar que las transacciones no quedan en estado `PENDING` indefinido en la base de datos.
- Verificar que `ENV_PAYMENT_MAX_RETRY` y `ENV_PAYMENT_RETRY_DELAY_MS` están configuradas en el ConfigMap de producción.
- Monitorear el consumo de CPU y memoria durante los primeros 15 minutos post-despliegue.
- Verificar que el pool de conexiones hikari-cp opera correctamente y no registra pérdidas de conexión en los logs.

---

## Equipo de Soporte

- Gustavo Lopez — Líder Técnico Backend
- Christian Bacilio De la Cruz — Analista de Desarrollo

---

## Documentación

- Enlace SharePoint: *(por definir)*
