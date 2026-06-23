---
name: git-workflow
description: >
  Genera commits, pull requests y CHANGELOG siguiendo Conventional Commits (tipos en inglés: feat, fix…; título corto y descripción en español) para Github. Activa este skill cuando el mensaje del usuario contenga (sin distinguir mayúsculas) cualquiera de estas palabras o sus variantes: commit, "pull request", PR, documentar cambios, CHANGELOG, git diff, revisar cambios. Si la intención no es clara, pregunta ¿quieres ayuda con commits/PR/CHANGELOG?
---

# Git Workflow

## Archivos de referencia

Antes de responder, lee el contenido completo del archivo de referencia indicado y úsalo como fuente primaria. Si no puedes acceder al archivo, responde: "No puedo acceder a references/[nombre], por favor pega su contenido o indícame si procedo sin él."

|Tarea|Leer|
|-------|------|
|Generar mensaje de commit|`references/commit-standard.md`|
|Crear o titular un PR|`references/pr-template.md` + `references/commit-standard.md`|
|Dividir un PR grande|`references/pr-guidelines.md`|
|Revisar checklist antes de abrir PR|`references/pr-guidelines.md`|
|Generar CHANGELOG|`references/commit-standard.md`|

---

## Flujo recomendado

Usa este flujo solo si el usuario pide un plan o expresa incertidumbre ("no sé por dónde empezar", "¿qué hago primero?"). En cualquier otro caso, responde directamente a la tarea solicitada.

1. **¿El PR supera 400 líneas o 10 archivos?**
   - Sí → Lee `pr-guidelines.md` y propón técnicas de división. No continúes al paso 2 hasta que el alcance esté acotado.
   - No → Continuar al paso 2.
2. **¿Hay cambios pendientes de commitear?** → Genera commits atómicos (uno por unidad lógica) con `commit-standard.md`. Continúa al paso 3 cuando los commits estén listos.
3. **¿Falta título o descripción del PR?** → Completa ambos con `pr-template.md`. Continúa al paso 4.
4. **¿El PR está listo para abrir?** → Pasa el checklist de `pr-guidelines.md`. Si algún ítem falla, resuélvelo antes de continuar.
5. **¿Se completó el merge?** → Actualiza CHANGELOG, README y versión con `commit-standard.md`.

---

## Estas reglas son prioritarias

- Nunca mezclar refactoring con nueva funcionalidad en el mismo PR
- El ID del ticket (CEB-XXXX) va en el cuerpo del PR, nunca en el título
- Prefijo y scope del commit en inglés (feat, fix...); título corto del commit y descripción del PR en español
- Si el usuario indica preferencia de idioma, respétala en todo el output; si es ambigua, pregunta: "¿prefieres español o inglés para el título y descripción?"
- Un PR debe abordar exactamente un ticket identificable (bug o feature) o una única funcionalidad autocontenida. Para múltiples pequeños cambios no relacionados, crea PRs separados; para cambios estrechamente relacionados, agrúpalos bajo un único ticket.
- Si el usuario pide generar commits o PR sin proporcionar diff ni lista de cambios, pregunta: "Por favor pega el `git diff` o la lista de archivos cambiados y un resumen de los cambios."
- Para breaking changes usa `tipo!: descripción` y agrega footer `BREAKING CHANGE: <qué cambia o rompe>`.
- Si no hay ticket CEB disponible, omite la línea `Refs:` del commit y del cuerpo del PR; no inventes ni supongas un ID.

## Validación de CHANGELOG, README y versión

Aplica **siempre** al generar un PR o al hacer commit de tipo `feat`, `fix`, `hotfix` o `feat!`:

### 1. CHANGELOG

- Verifica si existe `CHANGELOG.md` en la raíz del repositorio.
- Si el PR incluye commits `feat`, `fix`, `hotfix` o `feat!`, el CHANGELOG **debe** tener una entrada nueva bajo la versión correspondiente.
- Si no existe la entrada, genera el bloque y avisa al usuario que debe incluirlo en el PR.

### 2. README

- Si el PR agrega una nueva funcionalidad visible (`feat`), verifica que el `README.md` refleje el cambio.
- Si hay una sección de "Features", "Capacidades" o tabla de funcionalidades, comprueba que el ítem nuevo esté listado.
- Si el README no está actualizado, indícalo al usuario como ítem pendiente antes de abrir el PR.

### 3. Versionado semántico

Determina el tipo de bump según los commits del PR:

| Commits presentes | Bump |
|-------------------|------|
| `feat!` / `BREAKING CHANGE` | **MAJOR** — x.0.0 |
| Al menos un `feat` | **MINOR** — 0.x.0 |
| Solo `fix` / `hotfix` / `docs` / `refactor` / `test` | **PATCH** — 0.0.x |

- Si no hay un archivo de versión (`pom.xml`, `package.json`, `version.txt`, etc.) y el repo usa solo CHANGELOG, incluye el número de versión en el encabezado del CHANGELOG.
- Si el usuario no especificó versión, propón el bump calculado y pide confirmación antes de incluirlo.