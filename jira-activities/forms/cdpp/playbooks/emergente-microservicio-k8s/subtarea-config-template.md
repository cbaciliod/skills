# PASO 1: [Infra Middleware] Kubernetes - Rolling Update - <componente> — Despliegue <vX.X.X> <descripción breve>

> Plantilla basada en CDPP-35124 (validado — 2026-06-19)
> Este paso lo crea el desarrollador/analista. Lo ejecuta Infra Middleware.

---

## ¿Qué se va a cambiar?

Se desplegará la versión `<vX.X.X>` del microservicio `<componente>` en el
entorno productivo mediante rolling update en Kubernetes. Los cambios incluyen:

- <Mejora/fix 1 — descripción técnica concreta>
- <Mejora/fix 2>
- <Actualización de variables de entorno del ConfigMap (ver sección Variables)>

## ¿Por qué se hace?

<Descripción del incidente o problema que origina el pase. Referenciar el ticket
CEB si existe. Incluir fecha, síntoma observable e impacto.>

## ¿Qué impacto tiene?

El cambio afecta exclusivamente al microservicio `<componente>`. El despliegue
se realiza mediante rolling update en Kubernetes — no genera indisponibilidad
del servicio.

---

## Datos del Componente

| Campo | Valor |
|---|---|
| Nombre del componente | `<componente>` |
| Versión actual en PRD | *(por definir)* |
| Versión a desplegar | `<vX.X.X>` |
| Namespace / Cluster | `<namespace>` |
| Tipo de despliegue | Kubernetes Rolling Update |

---

## Variables de Entorno

### Variables nuevas (requieren configuración en ConfigMap/Secret antes del despliegue)

| Variable | Valor | Descripción |
|---|---|---|
| `<VAR_NUEVA_1>` | `<valor>` | <descripción> |
| `<VAR_NUEVA_2>` | `<valor>` | <descripción> |

### Variables existentes ahora validadas en startup

> El `StartupConfigurationValidator` verifica estas variables al arranque.
> Si alguna está vacía o ausente, el pod entra en `CrashLoopBackOff`.

| Variable | Valor | Descripción |
|---|---|---|
| `<VAR_EXISTENTE_1>` | `<valor>` | <descripción> |
| `<VAR_EXISTENTE_2>` | `*(sensible — Secret K8s)*` | <descripción> |

### ConfigMap completo (YAML — listo para aplicar)

```yaml
- name: <VAR_1>
  value: "<valor>"

- name: <VAR_2>
  value: "<valor>"

# Credenciales — referenciar desde Secret
- name: <VAR_SENSIBLE>
  valueFrom:
    secretKeyRef:
      name: <nombre-secret>
      key: <clave>
```

> **Nota:** Las variables sensibles (contraseñas, tokens) se validan en startup
> pero nunca se imprimen en logs.

---

## Orden de Ejecución

1. Confirmar que las variables nuevas están configuradas en el ConfigMap del
   namespace `<namespace>`.
2. Actualizar los valores de las variables existentes que cambian
   (ej: `<VAR_HOST>`, `<VAR_SSL>`).
3. Ejecutar el despliegue de la imagen `<componente>:<vX.X.X>`.
4. Verificar que los pods levantan en estado `Running` con health checks verdes.
5. Ejecutar validaciones post-ejecución.

En caso de fallo en cualquier paso, detener y ejecutar el plan de rollback.

---

## Validaciones Post-Ejecución

- Verificar en los logs de arranque el bloque de confirmación de variables
  resueltas (las credenciales no deben aparecer en el log).
- Ejecutar una transacción / petición de prueba de extremo a extremo y
  verificar resultado correcto.
- Monitorear CPU y memoria durante los primeros 15 minutos post-despliegue.
- <Validación específica del fix principal>.
- <Validación de la integración migrada si aplica (ej: broker, BD)>.

---

## Plan de Rollback

| Componente | Acción de rollback |
|---|---|
| `<componente>` | Rollback del deployment en Kubernetes a la versión anterior |
| ConfigMap | Restaurar estado previo al pase (sin las variables nuevas, con valores originales de las modificadas) |

Tiempo estimado de rollback: < 5 minutos.

Verificación post-rollback:
- Confirmar pods en estado `Running`.
- Ejecutar una transacción de prueba y verificar respuesta correcta.

---

## Estimación de Impacto y Ventana

| Campo | Valor |
|---|---|
| Tiempo estimado de ejecución | ~5-10 minutos (rolling update + validaciones) |
| Tiempo estimado de rollback | < 5 minutos |
| Requiere ventana de mantenimiento | No — rolling update sin downtime |
| Afecta disponibilidad del servicio | No |
| Variables de entorno nuevas | <N> variables nuevas + <M> existentes validadas en startup |

---

## Dependencias y Coordinación

- Coordinar con Infra la configuración de las variables nuevas en el ConfigMap
  y los Secrets **antes** del despliegue (PASO 1 debe completarse antes del PASO 2).
- El responsable técnico (<nombre>) debe estar disponible durante la ventana de
  ejecución para validar el resultado y autorizar rollback si fuera necesario.
