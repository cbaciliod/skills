# Template de Pull Request

## Título

Seguir la misma convención de commits:

`<tipo>: <descripción en minúsculas>`

**Reglas:**

- Sin ID de ticket en el título
- Máximo 50-72 caracteres
- Específico y descriptivo

## Cuerpo del PR

```markdown
## Description:
- [cambio lógico 1]
- [cambio lógico 2]
- [cambio lógico 3]

## Issue ticket number and link:
[CEB-XXXX](https://jira4novo.atlassian.net/browse/CEB-XXXX)

## Checklist before requesting a review:
- [ ] I have performed a self-review of my code
- [ ] If it is a core feature, I have added thorough tests.
```

## Cómo completar el Description

- Un bullet por cambio **lógico**, no por archivo
- Si hay muchos cambios, agrupar por categoría

```markdown
## Description:
**Nuevas funcionalidades:**
- Implementar mecanismo de reintento automático

**Refactor:**
- Extraer métodos de validación al servicio base

**Tests:**
- Agregar pruebas unitarias para RetryService

**Configuración:**
- Agregar variable de entorno RETRY_MAX_ATTEMPTS
```

## Límites recomendados

|Métrica|Ideal|Máximo|
|---------|-------|--------|
|Líneas modificadas|< 200|< 400|
|Archivos modificados|< 5|< 10|
|Tiempo de revisión|< 15 min|< 30 min|
