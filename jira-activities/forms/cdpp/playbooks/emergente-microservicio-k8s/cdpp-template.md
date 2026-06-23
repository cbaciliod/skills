# [PRD][<CLIENTE>] - <Descripción concisa del cambio>

> Plantilla basada en CDPP-35117 (validado por Líder Técnico — 2026-06-19)
> Reemplazar todo lo que está entre < > con los datos reales.

**Tickets relacionados:** [<CEB-XXXX>](https://jira4novo.atlassian.net/browse/<CEB-XXXX>)

---

## Situación Inicial

El microservicio `<componente>` presentó <N> incidente(s) crítico(s) en producción:

**Incidente <FECHA> — <Nombre corto del incidente>:**
<Descripción técnica concreta del incidente: qué ocurrió, qué síntoma fue visible,
cuál fue el impacto (% de transacciones, pérdida financiera, CPU spike, etc.),
por qué no era detectable desde el dashboard de Kubernetes si aplica.>

> Si hay más de un incidente, repetir el bloque anterior para cada uno.

Adicionalmente, se identificaron los siguientes problemas de configuración:

- <Problema 1 identificado — no necesariamente un incidente, puede ser un riesgo latente>
- <Problema 2>
- <Problema N>

---

## Situación Final

Tras el despliegue de la versión `<vX.X.X>` del microservicio `<componente>`,
el servicio operará con las siguientes mejoras:

- **<Mejora 1 — nombre técnico>:** <descripción de qué hace y qué resuelve>.
- **<Mejora 2>:** <descripción>.
- **<Mejora N>:** <descripción>.

Se garantiza que el cambio es acotado al microservicio `<componente>` y no
afecta otras funcionalidades ni servicios existentes del cliente <CLIENTE>.

---

## Plan de Certificación

Se realizó la certificación en ambiente TEST. Se verificó:

- Que <verificación 1 — comportamiento correcto tras el fix principal>.
- Que <verificación 2>.
- Que <verificación N>.

> Si alguna subtarea de certificación está Blocked, indicarlo:
> **Nota:** La subtarea <CEB-XXXX> (<descripción>) se encuentra en estado Blocked
> por <motivo>. Se deberá confirmar el estado antes del pase a producción.

Ticket de certificación: [<CEB-XXXX>](https://jira4novo.atlassian.net/browse/<CEB-XXXX>)

---

## Afectación

En caso de que el pase no sea exitoso:

- El microservicio `<componente>` podría quedar en estado degradado si la nueva
  versión presenta algún problema de compatibilidad <con Java X / con el broker / etc.>.
- El alcance del impacto está acotado exclusivamente al procesamiento de
  <descripción del flujo afectado>.
- No se afectan otras funcionalidades del cliente <CLIENTE> ni otros
  microservicios del ecosistema.
- El rollback restaura la versión anterior del microservicio y el ConfigMap
  previo, devolviendo el servicio al estado operativo previo al pase sin
  indisponibilidad perceptible para el usuario final.

---

## Plan de Rollback

**Consideraciones:**

- El cambio afecta exclusivamente al microservicio `<componente>`.
- El despliegue no genera indisponibilidad, dado que Kubernetes gestiona el
  rolling update de los pods.
- <Si hay variables nuevas en ConfigMap> El rollback de la imagen debe
  acompañarse del rollback del ConfigMap al estado previo, ya que se añaden
  <N> variables nuevas/modificadas. Sin revertir el ConfigMap, la versión
  anterior podría no conectar correctamente a <la integración afectada>.
- No se realizan cambios de esquema en base de datos ni modificaciones en
  infraestructura compartida.

**Acciones de rollback:**

1. Identificar la versión anterior del artefacto `<componente>` desplegada en producción.
2. Restaurar el ConfigMap al estado previo al pase <(con los valores originales de <VAR> y sin las <N> variables nuevas)>.
3. Ejecutar el rollback del deployment en Kubernetes hacia la versión anterior de la imagen.
4. Verificar que los pods levantan correctamente en estado `Running` con health checks verdes.
5. Validar que el servicio procesa transacciones correctamente ejecutando una transacción de prueba de extremo a extremo.
6. Notificar al equipo de soporte y al Líder Técnico el rollback ejecutado.

**Alcance del rollback:**

- Se revierte: la imagen del microservicio `<componente>` y el ConfigMap de variables de entorno.
- No se ve afectado: los manifiestos de Kubernetes ni otros microservicios del ecosistema <CLIENTE>.

---

## Revisión Postproducción

- Verificar que los pods de `<componente>` levantan correctamente en estado `Running`.
- <Verificación específica del fix principal, ej: revisar log de startup, ejecutar transacción con dato inválido, etc.>
- Ejecutar una transacción de extremo a extremo y verificar que el flujo opera correctamente.
- Monitorear el consumo de CPU y memoria durante los primeros 15 minutos post-despliegue.
- <Verificación adicional relacionada con las mejoras del release>.
- Confirmar que las <N> variables del ConfigMap están configuradas correctamente
  en el ambiente de producción (ver subtarea [<CDPP-XXXXX>](https://jira4novo.atlassian.net/browse/<CDPP-XXXXX>)).

---

## Equipo de Soporte

- <Nombre> — Líder Técnico Backend
- <Nombre> — Analista de Desarrollo

---

## Documentación

- Enlace SharePoint: *(por definir)*
