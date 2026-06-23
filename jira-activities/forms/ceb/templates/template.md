# Ticket técnico — [descripción del cambio]

**Repo objetivo:** `<nombre-del-repo>`
**Repo de referencia:** `<repo-con-cambios-validados>` — si aplica
**Fecha:** `<YYYY-MM-DD>`
**Tickets origen:** `<CEB-XXXX>`, `<CEB-YYYY>` — si aplica
**Canal de seguimiento:** link hilo Teams/Slack si aplica

---

## 1. Contexto

Explicar por qué existe este ticket. Qué problema concreto se manifestó en producción o qué deuda técnica se está atacando. Si vienen cambios de otro repo hermano, explicar la relación entre ambos.

Problemas concretos que este ticket resuelve:

* problema 1
* problema 2
* problema N

---

## 2. Alcance

### Dentro de alcance

* qué se va a hacer

### Fuera de alcance

* qué explícitamente NO entra en este ticket y por qué

---

## 3. Fases / entregables

Cada fase = un PR independiente para minimizar blast radius.

### Fase 1 — [Nombre de la fase] (un PR)

Descripción breve de la fase y nivel de riesgo/impacto.

#### 1.1 [Sub-tarea]

* **Archivo a modificar:** `ruta/al/archivo.java`
* **Referencia:** `ruta/en/repo-referencia.java:línea` — si aplica
* **Cambio:** qué exactamente se modifica
* **Síntoma que resuelve:** qué falla observable desaparece
* **Origen:** commit `<hash>` — `<mensaje del commit>` — si aplica

#### 1.2 [Sub-tarea]

* **Archivo nuevo:** `ruta/al/archivo.java`
* **Referencia:** si aplica
* **Cambio:** descripción del archivo nuevo y su propósito
* **Síntoma que resuelve:** qué falla observable desaparece

#### Criterios de aceptación Fase 1

* \[ \] criterio verificable 1
* \[ \] criterio verificable 2

---

### Fase 2 — [Nombre de la fase] (un PR)

Descripción breve.

#### 2.1 [Sub-tarea]

* **Archivo a modificar:** `ruta/al/archivo.java`
* **Referencia:** si aplica
* **Cambio:** qué se modifica
* **Síntoma que resuelve:** qué falla desaparece

#### Criterios de aceptación Fase 2

* \[ \] criterio verificable 1
* \[ \] criterio verificable 2

---

## 4. Inventario de diferencias estructurales

Tabla comparativa entre repos o sistemas involucrados. Omitir si no aplica.

| Tema | Estado actual | Estado destino | Comentario |
| --- | --- | --- | --- |
| elemento | cómo está hoy | cómo debe quedar | notas |

> Nota aclaratoria sobre elementos que deben permanecer sin cambios.

---

## 5. Riesgos y mitigaciones

| Riesgo | Mitigación |
| --- | --- |
| riesgo 1 | cómo se mitiga |
| riesgo 2 | cómo se mitiga |

---

## 6. Plan de rollout

1. Fase 1 → dev → qa → prod — tiempo de soak en qa si aplica.
2. Fase 2 → dev → qa → prod.
3. Fase N → dev → qa → prod.

Cada fase = PR independiente con su propio QA-OK.

---

## 7. Backlog (no parte de este ticket)

* mejora pendiente 1 — registrar como ticket separado
* mejora pendiente 2

---

## 8. Referencias

* Repo de referencia: `<URL del repo>`
* Commits clave:
  * `<hash>` — descripción del commit
  * `<hash>` — descripción del commit

---

## 9. Definición de "Done"

* \[ \] Fase 1 mergeada y validada en prod.
* \[ \] Fase 2 mergeada y validada en prod.
* \[ \] README del repo actualizado si aplica.
* \[ \] Backlog (§7) registrado como tickets separados en Jira.
