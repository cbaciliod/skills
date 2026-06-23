# PASO 1: [Infra Middleware] Kubernetes - Rolling Update - api-tbs-demo-payment-microservice — Despliegue v1.4.2 corrección NullPointerException pagos recurrentes

## ¿Qué se va a cambiar?

Se desplegará la versión `v1.4.2` del microservicio `api-tbs-demo-payment-microservice`
en el entorno productivo mediante rolling update en Kubernetes. Los cambios incluyen:

- **Validación de `externalReference`:** el request handler valida el campo antes de
  persistir la transacción. Valor nulo o vacío → HTTP 400 con mensaje descriptivo y
  registro en auditoría.
- **Actualización de hikari-cp 5.0.1 → 5.1.0:** fix de pérdida de conexiones inactivas
  bajo carga baja sostenida.
- **Parámetros de reintento externalizados:** `ENV_PAYMENT_MAX_RETRY` y
  `ENV_PAYMENT_RETRY_DELAY_MS` se resuelven desde variables de entorno.

## ¿Por qué se hace?

El campo `externalReference` llegaba nulo desde el cliente en flujos de pagos
recurrentes, generando un `NullPointerException` no controlado. La transacción
quedaba persistida en estado `PENDING` indefinido sin alertas visibles en monitoreo.

## ¿Qué impacto tiene?

El cambio afecta exclusivamente al microservicio `api-tbs-demo-payment-microservice`.
El despliegue se realiza mediante rolling update en Kubernetes — no genera
indisponibilidad del servicio.

---

## Datos del Componente

| Campo | Valor |
|---|---|
| Nombre del componente | `api-tbs-demo-payment-microservice` |
| Versión actual en PRD | `v1.4.1` |
| Versión a desplegar | `v1.4.2` |
| Namespace / Cluster | `prd-api-backend` |
| Tipo de despliegue | Kubernetes Rolling Update |

## Variables de Entorno Nuevas/Modificadas

> Verificar que las variables estén configuradas en el ConfigMap de producción
> antes del despliegue.

| Variable | Descripción | Valor PRD |
|---|---|---|
| `ENV_PAYMENT_MAX_RETRY` | Número máximo de reintentos ante fallo transitorio | `3` |
| `ENV_PAYMENT_RETRY_DELAY_MS` | Delay entre reintentos en milisegundos | `2000` |

## Orden de Ejecución

1. Confirmar que `ENV_PAYMENT_MAX_RETRY` y `ENV_PAYMENT_RETRY_DELAY_MS` están
   configuradas en el ConfigMap del namespace `prd-api-backend`.
2. Ejecutar el despliegue de la imagen `api-tbs-demo-payment-microservice:v1.4.2`.
3. Verificar que los pods levantan en estado `Running` con `RESTARTS = 0`.
4. Ejecutar validaciones post-ejecución.

En caso de fallo, detener y ejecutar el plan de rollback.

## Validaciones Post-Ejecución

- Verificar estado del pod:
  `kubectl get pods -n prd-api-backend -l app=api-tbs-demo-payment-microservice`
  Resultado esperado: STATUS = Running, RESTARTS = 0.
- Enviar request con `externalReference` nulo → resultado esperado: HTTP 400 con
  mensaje de error descriptivo.
- Enviar request con `externalReference` válido → resultado esperado: transacción
  procesada correctamente, sin estado PENDING indefinido.
- Verificar en la base de datos que no hay transacciones nuevas en estado `PENDING`
  tras la prueba con campo nulo.
- Monitorear CPU y memoria los primeros 15 minutos post-despliegue.

## Plan de Rollback

| Componente | Acción de rollback |
|---|---|
| `api-tbs-demo-payment-microservice` | Rollback del deployment a la versión `v1.4.1` |
| ConfigMap de variables de entorno | Restaurar estado previo (sin `ENV_PAYMENT_MAX_RETRY` y `ENV_PAYMENT_RETRY_DELAY_MS`) |

Tiempo estimado de rollback: < 10 minutos.

Verificación post-rollback:
- Confirmar pods en estado Running.
- Ejecutar una transacción de pago recurrente válida y verificar respuesta correcta.

## Estimación de Impacto y Ventana

| Campo | Valor |
|---|---|
| Tiempo estimado de ejecución | ~10-15 minutos (rolling update + validaciones) |
| Tiempo estimado de rollback | < 10 minutos |
| Requiere ventana de mantenimiento | No — rolling update sin downtime |
| Afecta disponibilidad del servicio | No |

## Dependencias y Coordinación

- Certificación en TEST confirmada bajo ticket CEB-9999 antes del pase.
- Responsable técnico: Gustavo Lopez (líder técnico) y Christian Bacilio De la Cruz
  (analista de desarrollo), disponibles durante la ventana de ejecución.
