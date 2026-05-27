# Estándar de Commits

## Formato

`<tipo>(<scope>): <descripción en español, imperativo, max 72 chars>`
[cuerpo opcional: explica el QUÉ y el POR QUÉ]
Refs: #CEB-XXXX

## Tipos

|Tipo|Cuándo usarlo|
|------|---------------|
|`feat`|Nueva funcionalidad|
|`fix`|Corrección de bug|
|`hotfix`|Corrección urgente en producción|
|`refactor`|Cambio sin nueva funcionalidad ni bug|
|`test`|Agregar o corregir tests|
|`docs`|Cambios de documentación|

## Reglas

- Descripción en minúsculas (excepto nombres propios o acrónimos)
- Usar espacios, no guiones bajos
- Verbos en infinitivo: "agregar", "corregir", "implementar", "refactorizar"
- Máximo 72 caracteres en la primera línea
- El ID del ticket va en el footer como `Refs: #CEB-XXXX`

## Ejemplos correctos

feat(auth): agregar mecanismo de reintento automático
Se implementó retry con backoff exponencial para el servicio de autenticación.
Refs: #CEB-3233

refactor(repository): extraer lógica de consulta a métodos privados

test(services): agregar pruebas unitarias para RetryService

fix(orders): corregir timeout en consulta con más de 1000 items
Refs: #CEB-3250

## Ejemplos incorrectos

ID en el título
feat: CEB-123 nuevo onboarding

Guiones bajos
fix: corregir_validacion_de_email

Demasiado genérico
feat: cambios en la base de datos

Sin tipo
actualizar código de usuarios

## CHANGELOG

Al cerrar una versión, agrupar commits así:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- feat: descripción

### Fixed
- fix: descripción

### Changed
- refactor: descripción

```

Si tu PR supera estos límites → ver `pr-guidelines.md` para dividirlo.
