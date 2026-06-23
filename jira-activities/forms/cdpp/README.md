# cdpp

Skill para redactar y crear en Jira los documentos de pase a producción de
NovoPayment: CDPP, Anexo 1 y Anexo 4.

## ¿Qué hace?

| Documento | Descripción |
|-----------|-------------|
| **CDPP** | Control de Pases a Producción — ticket principal en Jira con situación inicial/final, plan de rollback, subtareas por equipo y revisión postproducción |
| **Anexo 1** | Plan de Pase a Producción — documento Word con plan de implementación, análisis de riesgo/impacto y plan de retorno |
| **Anexo 4** | Plan de Pruebas Funcionales Postproducción — documento Word con tabla de pruebas y criterios de aceptación |

## Activación

El skill se activa cuando el mensaje contiene (sin distinguir mayúsculas):
`cdpp`, `pase a producción`, `plan de pase`, `anexo 1`, `anexo 4`,
`plan de implementación`, `plan de rollback`, `plan de certificación`,
`plan de retorno`, `plan de pruebas postproducción`.

## Uso

Proporciona los datos del caso al invocar el skill:

```
- Cliente:
- País:
- Tipo de pase (NORMAL | STANDARD | EMERGENTE):
- Genera indisponibilidad (SI | NO):
- Equipos ejecutores:
- Ticket de certificación (CEB-XXXX):
- Contexto del cambio:
- Evidencias / VoBo del cliente:
- Aspectos especiales:
```

El skill generará primero el CDPP completo, luego lo usará como base para el
Anexo 1 y el Anexo 4. Si la conexión a Jira (MCP Atlassian) está disponible,
también puede crear el ticket y sus subtareas directamente.

## Referencias

| Archivo | Propósito |
|---------|-----------|
| `references/prompt-cdpp.md` | Plantilla y estándar para redactar el CDPP |
| `references/prompt-anexo1.md` | Plantilla y estándar para redactar el Anexo 1 |
| `references/prompt-anexo4.md` | Plantilla y estándar para redactar el Anexo 4 |

## Equipo de Soporte por defecto

- Gustavo Lopez — Líder Técnico Backend
- Alonzo Cumpa — Analista de Desarrollo
