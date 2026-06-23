# Skill: Jira Activities

## Activación

Activa este skill cuando el mensaje contenga (sin distinguir mayúsculas/minúsculas) cualquiera de estas palabras o sus variantes:

`jira`, `actividad`, `crear tarea`, `nueva tarea`, `crear ticket`, `cdpp`, `pase a producción`, `sub-tarea`, `subtarea`, `ceb`, `historia`, `story`, `cdsi`, `solicitud infraestructura`, `gpbd`, `base de datos proyecto`, `control de solicitudes`

Si la intención no es clara, pregunta: *¿Quieres crear una actividad en Jira?*

---

## Flujo principal

### Paso 0 — Mostrar menú de tipos

Si el usuario no especificó el tipo en su mensaje, presenta este menú:

```
¿Qué tipo de actividad Jira quieres crear?

1. CDPP   — Control de Pase a Producción
2. Sub-tarea — Subtarea de un ticket padre
3. CEB    — (tipo de ticket de cambio)
4. Historia — Historia de usuario / requerimiento
5. CDSI   — Control de Solicitudes de Infraestructura
6. GPBD   — Gestión de Proyectos de Base de Datos

Responde con el número o el nombre del tipo.
```

Si el usuario ya mencionó el tipo (ej. "quiero crear un CDPP"), ir directamente al flujo correspondiente sin mostrar el menú.

### Paso 1 — Ejecutar flujo del tipo seleccionado

Según el tipo elegido, lee el archivo de referencia correspondiente y sigue su flujo:

| Tipo | Flujo | Referencias principales |
|------|-------|------------------------|
| CDPP | `forms/cdpp/SKILL.md` | `forms/cdpp/references/prompt-cdpp.md`, `forms/cdpp/references/prompt-anexo1.md`, `forms/cdpp/references/prompt-anexo4.md`, `forms/cdpp/references/tipos-cdpp.md` |
| Sub-tarea | `forms/sub-tarea/references/prompt.md` | `forms/sub-tarea/templates/template.md` |
| CEB | `forms/ceb/references/prompt.md` | `forms/ceb/templates/template.md` |
| Historia | `forms/historia/references/prompt.md` | `forms/historia/templates/template.md` |
| CDSI | `forms/cdsi/references/prompt.md` | `forms/cdsi/templates/template.md` |
| GPBD | `forms/gpbd/references/prompt.md` | `forms/gpbd/templates/template.md` |

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
