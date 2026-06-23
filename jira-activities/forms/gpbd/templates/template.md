# [GPBD][MOTOR][AMBIENTE] Tipo — esquema.objeto

**Solicitante:** `<Nombre> — <Equipo>`
**Responsable DBA:** `<Nombre>`
**Fecha planificada:** `<DD/MM/YYYY>`
**Urgencia:** `<normal / urgente>`
**Ticket relacionado:** `<NOVA-XXXX / CDPP-XXXX>` *(si aplica)*

---

## Descripción del cambio

*(Qué se ejecuta en la base de datos, por qué es necesario, y cuál es el resultado esperado.)*

## Objetos afectados

| Esquema | Objeto | Tipo | Tipo de cambio | Registros estimados |
|---------|--------|------|----------------|---------------------|
| *(schema)* | *(tabla/paquete/índice)* | *(TABLE / PACKAGE / INDEX / JOB)* | *(DDL / DML)* | *(N registros / N/A)* |

## Script(s) de ejecución

```sql
-- Script DDL/DML
-- Agregar script aquí o indicar que está en adjunto

*(por definir)*
```

## Orden de ejecución

1. *(Paso 1 — ej. Tomar backup de tabla objetivo)*
2. *(Paso 2 — ej. Ejecutar script DDL)*
3. *(Paso 3 — ej. Recompilar paquetes dependientes)*
4. *(Paso N — ej. Actualizar estadísticas)*

## Validaciones post-ejecución

- [ ] *(Validación 1 — ej. Contar registros: SELECT COUNT(*) FROM tabla)*
- [ ] *(Validación 2 — ej. Verificar estructura: DESCRIBE tabla)*
- [ ] *(Validación 3 — ej. Ejecutar consulta de prueba funcional)*

## Plan de rollback

```sql
-- Script de rollback
-- Cómo revertir el cambio si algo falla

*(por definir)*
```

**Tiempo estimado de rollback:** *(X minutos)*

## Estimación de ventana

| Campo | Valor |
|-------|-------|
| Tiempo de ejecución | *(X minutos)* |
| Requiere downtime | *(sí / no)* |
| Horario recomendado | *(fuera de horario pico / ventana mantenimiento)* |
| Impacto en servicio | *(ninguno / degradación parcial / servicio detenido)* |
