# Estándar de Redacción — CDSI (Control de Solicitudes de Infraestructura)

## ¿Cuándo usar este tipo?

Un CDSI se crea para solicitudes formales al equipo de Infraestructura que requieren aprovisionamiento, configuración o modificación de recursos de infraestructura:
- Nuevos servidores, VMs, contenedores o namespaces
- Configuración de balanceadores, firewalls, certificados SSL
- Gestión de secrets, variables de entorno o ConfigMaps en K8s
- Accesos, permisos o roles en sistemas de infraestructura
- Cambios en pipelines CI/CD o repositorios

---

## Flujo de creación

### Paso 0 — Identificar el tipo de solicitud

Preguntar al usuario:
- ¿Qué tipo de recurso o configuración se solicita?
- ¿En qué ambiente aplica? (PRD / STG / DEV)
- ¿Es urgente o puede planificarse en el sprint?
- ¿Hay ticket relacionado (historia, CDPP, etc.)?

### Paso 1 — Solicitar datos

```
Tipo de solicitud    : (servidor / namespace / secret / acceso / pipeline / otro)
Componente/Sistema   : 
Ambiente             : (PRD / STG / DEV / todos)
Urgencia             : (normal / urgente / bloqueante)
Solicitante          : (nombre + equipo)
Fecha límite         : 
Ticket relacionado   : (ej. NOVA-XXXX / CDPP-XXXX)
Descripción técnica  : (qué se necesita y para qué)
Criterio de aceptación: (cómo se valida que la solicitud fue atendida)
Justificación        : (por qué se necesita)
```

### Paso 2 — Generar el ticket CDSI

Usar el template en `cdsi/templates/template.md` como base.

---

## Reglas de redacción

**Título:**
- Formato: `[CDSI][AMBIENTE] Tipo de solicitud — componente o sistema`
- Ejemplos:
  - `[CDSI][PRD] Crear namespace Kubernetes — api-tbs-new-service`
  - `[CDSI][STG] Configurar Secret K8s — credenciales RabbitMQ`
  - `[CDSI][PRD] Otorgar acceso SSH — equipo Backend api-payments`

**Descripción:**
- Ser específico sobre el recurso solicitado (nombre, tipo, configuración esperada)
- Incluir el contexto: qué lo genera (ticket, sprint, incidente)
- Definir claramente cuándo la solicitud se considera atendida
- Nunca inventar datos técnicos — usar `*(por definir)*`

**Secciones obligatorias:**
1. Descripción de la solicitud
2. Especificaciones técnicas
3. Justificación
4. Criterio de aceptación
5. Dependencias / Ticket relacionado
