# Jira Activities

Skill para crear y redactar actividades en Jira siguiendo los estándares del equipo de NovoPayment.

## Tipos soportados

| Tipo | Descripción | Directorio |
|------|-------------|------------|
| **CEB** | Story de desarrollo del equipo POD 1 - Legión de Zeus | `forms/ceb/` |
| **Sub-tarea** | Subtarea técnica de un CEB — mapea 1:1 con una rama de código | `forms/sub-tarea/` |
| **CDSI** | Solicitud de configuración al equipo Cloud - DevOps | `forms/cdsi/` |

## Cómo usar

Ejecuta el skill mencionando el tipo que necesitas:

- *"Quiero crear un CEB para mejorar el orquestador"*
- *"Crea una sub-tarea para el CEB-6222"*
- *"Necesito un CDSI para configurar variables de entorno en TEST"*

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
