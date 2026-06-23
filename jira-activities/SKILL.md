# Skill: Jira Activities

## Activación

Activa este skill cuando el mensaje contenga (sin distinguir mayúsculas/minúsculas) cualquiera de estas palabras o sus variantes:

`jira`, `actividad`, `crear tarea`, `nueva tarea`, `crear ticket`, `sub-tarea`, `subtarea`, `ceb`, `cdsi`, `solicitud infraestructura`, `control de solicitudes`

Si la intención no es clara, pregunta: *¿Quieres crear una actividad en Jira?*

---

## Flujo principal

### Paso 0 — Mostrar menú de tipos

Si el usuario no especificó el tipo en su mensaje, presenta este menú:

```
¿Qué tipo de actividad Jira quieres crear?

1. CEB       — Story de desarrollo (POD 1 - Legión de Zeus)
2. Sub-tarea — Subtarea técnica de un CEB (1 rama = 1 sub-tarea)
3. CDSI      — Solicitud de configuración a infraestructura (Cloud - DevOps)

Responde con el número o el nombre del tipo.
```

Si el usuario ya mencionó el tipo (ej. "quiero crear un CDPP"), ir directamente al flujo correspondiente sin mostrar el menú.

### Paso 1 — Ejecutar flujo del tipo seleccionado

Según el tipo elegido, lee el archivo de referencia correspondiente y sigue su flujo:

| Tipo | Referencia | Template |
|------|-----------|----------|
| CEB | `forms/ceb/references/prompt.md` | `forms/ceb/templates/template.md` |
| Sub-tarea | `forms/sub-tarea/references/prompt.md` | `forms/sub-tarea/templates/template.md` |
| CDSI | `forms/cdsi/references/prompt.md` | `forms/cdsi/templates/template.md` |

---

## Reglas generales (aplican a todos los tipos)

- **Nunca inventar datos**: usar placeholder `*(por definir)*` cuando el dato no está disponible
- **Preguntar por el ticket Jira** si el usuario no lo proporciona — extraer datos del ticket o completar formulario
- **Mantener coherencia** entre el ticket principal y sus subtareas/documentos asociados
- **Usar los templates** disponibles en el directorio del tipo seleccionado como base

## Estructura del directorio

```
jira-activities/
├── SKILL.md              ← este archivo (menú y orquestación)
├── README.md             ← documentación general
└── forms/                ← formularios y flujos por tipo de actividad
    ├── cdpp/             ← Control de Pase a Producción
    │   ├── SKILL.md      ← flujo detallado CDPP
    │   ├── references/   ← prompts y estándares CDPP
    │   ├── playbooks/    ← plantillas por tipo de pase validado
    │   └── test/         ← ejemplos de demostración
    ├── sub-tarea/
    │   ├── references/   ← estándar de redacción
    │   └── templates/    ← plantilla lista para usar
    ├── ceb/
    │   ├── references/
    │   └── templates/
    ├── historia/
    │   ├── references/
    │   └── templates/
    ├── cdsi/
    │   ├── references/
    │   └── templates/
    └── gpbd/
        ├── references/
        └── templates/
```
