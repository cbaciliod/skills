# Jira Activities

Skill para crear y redactar actividades en Jira siguiendo los estándares del equipo de NovoPayment.

## Tipos soportados

| Tipo | Descripción | Directorio |
|------|-------------|------------|
| **CDPP** | Control de Pase a Producción — ticket principal + subtareas + Anexo 1 + Anexo 4 | `forms/cdpp/` |
| **Sub-tarea** | Subtarea estándar de un ticket padre (historia, CDPP, CDSI, GPBD) | `forms/sub-tarea/` |
| **CEB** | Ticket de comité/evaluación de cambio | `forms/ceb/` |
| **Historia** | Historia de usuario / requerimiento funcional | `forms/historia/` |
| **CDSI** | Control de Solicitudes de Infraestructura | `forms/cdsi/` |
| **GPBD** | Gestión de Proyectos de Base de Datos | `forms/gpbd/` |

## Cómo usar

Ejecuta el skill mencionando el tipo que necesitas:

- *"Quiero crear un CDPP para el microservicio X"*
- *"Necesito redactar una historia para el requerimiento Y"*
- *"Crea un ticket CDSI para la solicitud de servidor"*
- *"Genera una sub-tarea para el ticket NOVA-1234"*

Si no especificas el tipo, el skill te preguntará con un menú numerado.

## Estructura

```
jira-activities/
├── SKILL.md              ← orquestación y menú principal
├── README.md             ← este archivo
└── forms/                ← formularios por tipo de actividad
    ├── cdpp/             ← tipo CDPP (más complejo, incluye playbooks)
    ├── sub-tarea/        ← subtareas genéricas
    ├── ceb/              ← tickets CEB
    ├── historia/         ← historias de usuario
    ├── cdsi/             ← solicitudes de infraestructura
    └── gpbd/             ← proyectos de base de datos
```

## Migración

Este skill unifica y expande el anterior skill `cdpp`. Todo el contenido de CDPP se mantiene en `forms/cdpp/` sin cambios.
