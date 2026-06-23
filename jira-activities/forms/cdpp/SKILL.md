---
name: cdpp
description: >
  Redacta y crea en Jira los documentos de pase a producción de NovoPayment:
  CDPP (Control de Pases a Producción), Anexo 1 (Plan de Pase a Producción) y
  Anexo 4 (Plan de Pruebas Funcionales Postproducción). Activa este skill cuando
  el mensaje contenga (sin distinguir mayúsculas) cualquiera de estas palabras:
  cdpp, "pase a producción", "pase a produccion", "plan de pase", anexo 1, anexo 4,
  "plan de implementación", "plan de rollback", "plan de certificación",
  "plan de retorno", "plan de pruebas postproducción".
---

# Redactor de CDPP y Documentos de Pase a Producción

## Archivos de referencia

Antes de generar cada documento, lee el archivo indicado como fuente primaria.
Si no puedes acceder, responde: "No puedo acceder a references/[nombre], por favor
pega su contenido o indícame si procedo sin él."

| Tarea | Leer |
|-------|------|
| Ver tipos validados y lecciones aprendidas | `APRENDIZAJES.md` |
| Determinar tipo de pase | `references/tipos-cdpp.md` |
| Usar plantilla validada (si existe playbook) | `playbooks/<tipo>/` |
| Generar CDPP (sin playbook) | `references/prompt-cdpp.md` |
| Generar subtareas (Pasos) | `references/tarea-cdpp.md` |
| Generar Anexo 1 — Plan de Pase a Producción | `references/prompt-anexo1.md` |
| Generar Anexo 4 — Plan de Pruebas Postproducción | `references/prompt-anexo4.md` |

**Prioridad de fuentes:** Si existe un playbook validado para el tipo de pase
solicitado, usar sus plantillas en lugar del prompt genérico. Los playbooks
contienen patrones extraídos de tickets reales aprobados por el Líder Técnico.

---

## Flujo recomendado

Usa este flujo solo si el usuario pide un plan o expresa incertidumbre. En
cualquier otro caso, responde directamente a la tarea solicitada.

0. **Seleccionar tipo de pase**
   Lee `references/tipos-cdpp.md` y pregunta al usuario:
   > "¿Qué tipo de pase es? 1. Microservicio K8s  2. Base de Datos  3. WAR/JAR
   > 4. Configuración pura  5. Proceso Agendado/Batch  6. Infraestructura"
   El tipo determina: formulario de datos, equipo ejecutor, si genera downtime,
   template de subtarea y ejemplo de referencia a aplicar.

1. **¿Tiene los datos del caso? — Condicional de entrada**
   Pregunta al usuario:
   > "¿Tienes un ticket de Jira con la información del cambio (CEB, historia,
   > incidente)? Si es así, comparte el link y lo leo directamente.
   > Si no, completa el formulario a continuación."

   - **Con link Jira** → leer el ticket con el MCP de Atlassian, extraer:
     componente, versión, descripción del cambio, variables, equipo, ticket CEB.
     Confirmar los datos extraídos al usuario antes de continuar.
   - **Sin link** → presentar el formulario específico del tipo seleccionado
     (ver `references/tipos-cdpp.md`, sección "Formulario de datos") y esperar
     respuesta antes de continuar.

2. **¿El usuario quiere generar el CDPP?**
   - Sí → Lee `references/prompt-cdpp.md` y genera el CDPP completo.
     Presenta el resultado y confirma antes de crear el ticket en Jira.
   - No → Saltar a paso 4 si ya tiene un CDPP redactado.

3. **¿Crear el ticket CDPP en Jira?**
   - Sí → Autenticar con MCP de Atlassian y crear el ticket (ver sección
     "Integración Jira").
   - No → Entregar el contenido en Markdown para copiar manualmente.

3b. **¿Crear las subtareas (Pasos)?**
   - Siempre crear o preguntar. Si el usuario no indicó los pasos de ejecución,
     preguntar: "¿Cuáles son los pasos del pase? Ej: PASO 1 Infra Middleware,
     PASO 2 Infra BD…"
   - Sí → Leer `references/tarea-cdpp.md`, generar el contenido de cada subtarea
     y crearlas en Jira como Sub-task hijas del ticket CDPP principal.
   - No → Entregar el contenido Markdown de cada PASO para copiar manualmente.

4. **¿El usuario quiere el Anexo 1?**
   - Sí → Lee `references/prompt-anexo1.md` y genera el Anexo 1 usando el
     CDPP ya redactado como entrada.

5. **¿El usuario quiere el Anexo 4?**
   - Sí → Lee `references/prompt-anexo4.md` y genera el Anexo 4 usando el
     CDPP ya redactado como entrada.

---

## Formulario de entrada

Si faltan datos, presenta este formulario y espera que el usuario lo complete:

```
- **Cliente:**
- **País:**
- **Tipo de pase (NORMAL | STANDARD | EMERGENTE):**
- **Genera indisponibilidad (SI | NO):**
- **Equipos ejecutores:**
- **Ticket de certificación (CEB-XXXX):**
- **Contexto del cambio (descripción libre del cambio, componentes, rutas, etc.):**
- **Evidencias / VoBo del cliente (si aplica):**
- **Aspectos especiales (riesgos conocidos, dependencias, reprocesos, etc.):**
```

---

## Integración Jira

Para crear o consultar tickets en Jira, usa el MCP de Atlassian:

1. **Autenticar:** llama a `mcp__claude_ai_Atlassian__authenticate` si la sesión
   no está activa. Completa el flujo con `mcp__claude_ai_Atlassian__complete_authentication`.
2. **Crear el ticket CDPP:** usa la herramienta de creación de issues de Jira con:
   - Tipo: el tipo de ticket CDPP configurado en el proyecto (consultar con el
     usuario si es necesario).
   - Resumen: el título generado en el CDPP (formato `[PRD][CLIENTE][PAÍS][TIPO]`).
   - Descripción: el cuerpo completo del CDPP en formato Jira Markdown.
3. **Crear subtareas:** una subtarea por cada `PASO N: EQUIPO - acción` del CDPP.
4. **Confirmar:** devolver al usuario la URL del ticket creado.

Si el usuario no tiene la autenticación configurada o prefiere no crear el ticket
automáticamente, entrega el contenido en Markdown para copiar al ticket de Jira
manualmente.

---

## Estas reglas son prioritarias

- Nunca inventar datos técnicos no provistos (rutas, versiones, esquemas,
  credenciales). Usar placeholder explícito `*(por definir)*`.
- El ticket de certificación CEB va en el cuerpo del CDPP, nunca en el título.
- Equipo de Soporte por defecto: **Gustavo Lopez — Líder Técnico Backend** y
  **Alonzo Cumpa — Analista de Desarrollo**. Si el usuario indica otro equipo,
  usar ese.
- Si "no genera indisponibilidad", reforzarlo en: Afectación, Consideraciones del
  Rollback, Análisis de Impacto del Anexo 1 y Plan de Retorno del Anexo 1.
- Mantener coherencia total entre CDPP, Anexo 1 y Anexo 4: mismo cliente,
  componente, situación y alcance.
- Si el usuario pide solo uno de los documentos, generar únicamente ese sin
  forzar el flujo completo.
- Si no hay ticket CEB disponible, usar `CEB-XXXX` como placeholder; no inventar
  ni suponer un ID.
- Siempre terminar cada documento con una lista corta de preguntas de cierre
  sobre datos faltantes.
- Formato de salida por defecto: Markdown limpio con tablas, listo para copiar al
  documento Word o al ticket de Jira.
