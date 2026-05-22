# git-workflow skill

Skill para Claude Code que automatiza el flujo de trabajo con Git siguiendo el estándar [Conventional Commits](https://www.conventionalcommits.org/). Genera mensajes de commit, crea Pull Requests y actualiza el CHANGELOG con un formato consistente.

---

## Qué hace

- **Commits atómicos** — genera mensajes siguiendo `<tipo>(<scope>): <descripción>` con el ID del ticket en el footer
- **Pull Requests** — crea título y cuerpo del PR listos para abrir en GitHub
- **División de PRs grandes** — propone técnicas (Branch by Abstraction, Strangler Fig, Parallel Change, descomposición por capas) cuando un PR supera los límites recomendados
- **CHANGELOG** — agrupa los commits por categoría (`Added`, `Fixed`, `Changed`, `Chore`) al cerrar una versión
- **Checklist de PR** — valida tamaño, calidad y descripción antes de abrir revisión

---

## Cómo se usa

El skill se activa automáticamente cuando el mensaje contiene alguna de estas palabras (sin distinguir mayúsculas):

> `commit`, `pull request`, `PR`, `documentar cambios`, `CHANGELOG`, `git diff`, `revisar cambios`

### Ejemplos de uso

```text
Genera el commit para estos cambios
```

```text
Crea el PR para la feature CEB-1234
```

```text
Actualiza el CHANGELOG con los commits del sprint
```

```text
Mi PR tiene 800 líneas, ¿cómo lo divido?
```

### Flujo completo

Si no sabes por dónde empezar, escribe algo como "no sé qué hacer primero" y el skill te guiará por estos pasos:

1. Evaluar si el PR supera los límites (> 400 líneas o > 10 archivos) y proponer división
2. Generar commits atómicos por cada unidad lógica de cambio
3. Completar el título y cuerpo del PR
4. Verificar el checklist antes de abrir revisión
5. Actualizar el CHANGELOG tras el merge

---

## Requisitos

|Requisito|Versión mínima|
|-----------|----------------|
|[Claude Code](https://docs.anthropic.com/en/docs/claude-code)|cualquier versión con soporte de skills|
|Git|2.x|
|Repositorio en GitHub|—|

El skill no instala dependencias externas ni ejecuta comandos en la terminal. Toda la salida es texto que puedes copiar directamente.

---

## Instalación

### 1. Clonar o copiar el skill

```bash
git clone <url-de-este-repo> ~/.claude/skills/git-workflow
```

O copia manualmente la carpeta `git-workflow/` dentro de tu directorio de skills de Claude Code.

### 2. Registrar el skill en Claude Code

Abre o crea el archivo de configuración de skills (habitualmente `~/.claude/settings.json`) y agrega la ruta:

```json
{
  "skills": [
    "~/.claude/skills/git-workflow"
  ]
}
```

### 3. Verificar

Reinicia Claude Code y escribe:

```text
commit
```

El skill debe activarse y guiarte para generar el mensaje de commit.

---

## Estructura del proyecto

```text
git-workflow/
├── SKILL.md                     # Definición del skill y reglas de activación
├── references/
│   ├── commit-standard.md       # Estándar de commits y formato de CHANGELOG
│   ├── pr-guidelines.md         # Guía de PRs pequeños y técnicas de división
│   └── pr-template.md           # Template de título y cuerpo de PR
├── README.md
└── CHANGELOG.md
```

---

## Convenciones que aplica el skill

|Elemento|Regla|
|----------|-------|
|Tipo y scope del commit|en inglés (`feat`, `fix`, `chore`…)|
|Título del commit / PR|en español, imperativo, máx. 72 chars|
|ID de ticket|en el footer del commit y en el cuerpo del PR, nunca en el título|
|Breaking changes|`tipo!: descripción` + footer `BREAKING CHANGE: <detalle>`|
|Tamaño de PR recomendado|< 200 líneas, < 5 archivos|
|Tamaño de PR máximo|< 400 líneas, < 10 archivos|
