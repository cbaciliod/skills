# Estándar de Redacción — Historia de Usuario

## ¿Cuándo usar este tipo?

Una Historia de Usuario (User Story) representa un requerimiento funcional desde la perspectiva del usuario final o del negocio. Es el tipo de ticket más común para nuevas funcionalidades o mejoras.

---

## Flujo de creación

### Paso 0 — Identificar el contexto

Preguntar al usuario:
- ¿Cuál es el requerimiento o funcionalidad?
- ¿Quién es el usuario/actor beneficiado?
- ¿A qué épica o proyecto pertenece?
- ¿Hay criterios de aceptación ya definidos?

### Paso 1 — Solicitar datos

```
Épica/Proyecto       : (ej. NOVA-100 / nombre del proyecto)
Actor/Usuario        : (quién hace la acción — usuario, sistema, cliente)
Funcionalidad        : (qué quiere hacer)
Objetivo/Beneficio   : (para qué lo necesita)
Sprint/Versión       : (opcional)
Responsable técnico  : 
Estimación           : (story points / horas)
Criterios de aceptación:
  - CA1: 
  - CA2:
  - CA3:
Notas técnicas       : (restricciones, dependencias, consideraciones)
```

### Paso 2 — Generar la historia

Usar el template en `historia/templates/template.md` como base.

---

## Reglas de redacción

**Título:**
- Corto, descriptivo, orientado a la funcionalidad
- Ejemplos:
  - `Validar externalReference antes de persistir transacción`
  - `Notificar al cliente cuando el pago recurrente falla`
  - `Exportar reporte de conciliación en formato Excel`

**Historia (cuerpo):**
- Formato obligatorio: **Como** [actor], **quiero** [funcionalidad], **para** [beneficio/objetivo]
- Ejemplo: *Como sistema de pagos, quiero validar que `externalReference` no sea nulo, para evitar transacciones en estado PENDING indefinido.*

**Criterios de aceptación:**
- Formato: **Dado** [contexto], **cuando** [acción], **entonces** [resultado esperado]
- Usar ✅ o `[ ]` para marcar cada criterio
- Mínimo 2 criterios, máximo lo necesario para cubrir todos los escenarios

**Descripción técnica (opcional):**
- Agregar solo si hay restricciones técnicas, decisiones de arquitectura, o dependencias externas relevantes
- Nunca inventar datos — usar `*(por definir)*`
