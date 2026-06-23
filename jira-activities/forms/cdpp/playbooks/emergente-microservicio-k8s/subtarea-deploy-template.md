# Paso 2: Desplegar microservicio

> Plantilla basada en CDPP-35132 (validado — 2026-06-19)
> Este paso lo ejecuta Infra Middleware. Formato simple — solo la tabla de
> despliegue con el link del GitHub Actions run.

---

Saludos team

Por favor se requiere ejecutar el despliegue de acuerdo al siguiente tablero:

| **Aplicación** | **POD** | **APPSERVER** | **NOMBRE WAR** | **job** | **Link Github Action** |
|---|---|---|---|---|---|
| microservicio | `<componente>` | MS | N/A | N/A | [<link del run>](<link del run>) |

---

> **Notas para completar esta subtarea:**
> - **POD:** nombre exacto del componente en Kubernetes.
> - **APPSERVER:** `MS` para microservicios (no aplica servidor de apps).
> - **NOMBRE WAR:** `N/A` para microservicios (no es un WAR).
> - **job:** `N/A` para microservicios (el despliegue lo gestiona GitHub Actions).
> - **Link Github Action:** URL del workflow run de GitHub Actions que ejecuta
>   el despliegue. Ejemplo:
>   `https://github.com/novopayment/<repo>/actions/runs/<run-id>`
>
> Esta subtarea se asigna al equipo de **Infra Middleware**.
> El PASO 1 (configuración de variables y ConfigMap) debe estar completado
> antes de ejecutar este paso.
