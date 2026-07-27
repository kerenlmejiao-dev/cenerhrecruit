# ✅ PASO 3: INTEGRAR CRM - LISTO

**Status:** 🚀 Integración CRM completamente desarrollada  
**Tiempo:** 2 horas (implementación) + 30 min (setup producción)  
**Resultado:** Sincronización automática de candidatos con HubSpot/Pipedrive

---

## 📦 ARCHIVOS CREADOS (4 archivos)

```
✅ crm_service.py
   ├─ HubSpotService (crear contactos, deals, tareas)
   └─ PipedrivService (alternativa)

✅ webhooks.py
   ├─ Sistema de eventos
   ├─ 9 handlers automáticos
   └─ Integración con CRM, Email, Auditoría

✅ api_crm_endpoints.py
   ├─ POST /api/crm/sync/candidato/{id}
   ├─ POST /api/crm/sync/todos (bulk)
   ├─ POST /api/crm/deal/{id}
   ├─ GET /api/crm/status
   └─ GET /api/crm/test-conexion/{plataforma}

✅ CRM_SETUP_GUIA.md
   ├─ Setup HubSpot
   ├─ Setup Pipedrive
   ├─ Troubleshooting
   └─ Monitoreo

✅ INTEGRACION_CRM_EN_API.md
   ├─ Pasos para integrar en API existente
   ├─ Modificaciones necesarias
   └─ Tests de validación
```

---

## 🎯 FUNCIONALIDADES IMPLEMENTADAS

### ✅ Sincronización de Candidatos
```
Candidato se registra en CENERH
        ↓
Se crea en HubSpot automáticamente
   • Nombre, email, teléfono
   • Propiedades custom (candidato_id, vacante_id)
   • Estado: ABIERTO (Lead)
```

### ✅ Gestión de Oportunidades (Deals)
```
Candidato completa evaluación
        ↓
Se crea Deal en HubSpot
   • Nombre: "Juan García - Contador"
   • Monto: Fee de CENERH
   • Estado: "En Evaluación"
   • Fecha cierre: 30 días
```

### ✅ Webhooks Automáticos (9 eventos)
```
1. CANDIDATO_CREADO
   → Sincronizar a HubSpot

2. CANDIDATO_EVALUACION_COMPLETADA
   → Crear deal
   → Enviar email automático
   → Crear tarea de seguimiento
   → Registrar en auditoría

3. CANDIDATO_PRIORITARIO
   → Actualizar estado en CRM
   → Agregar nota con scores
   → Crear tarea urgente

4. CANDIDATO_VIABLE
   → Actualizar estado

5. CANDIDATO_NO_RECOMENDADO
   → Marcar como "disqualified"

+ 4 eventos más customizables
```

### ✅ API REST para CRM

```
POST   /api/crm/sync/candidato/{id}     → Sincronizar uno
POST   /api/crm/sync/todos              → Sincronizar todos (bulk)
POST   /api/crm/deal/{id}               → Crear deal
PATCH  /api/crm/deal/{id}/estado        → Actualizar estado
GET    /api/crm/status                  → Ver conexión
GET    /api/crm/candidatos/hubspot      → Listar sincronizados
POST   /api/crm/test-conexion/{plataforma} → Test de conexión
```

### ✅ Manejo de Errores y Reintentos

```
Si HubSpot no responde:
   → Registrar error en log
   → Reintentar en siguiente ciclo
   → No bloquear usuario

Si email falla:
   → Registrar error
   → Reintentar en 5 minutos
   → Notificar a admin
```

### ✅ Auditoría Completa

```
AuditLog registra:
   • Cada candidato creado
   • Cada evaluación completada
   • Cada sincronización a CRM
   • Errores y excepciones
   • Timestamps exactos
```

---

## 🏗️ ARQUITECTURA

```
┌────────────────────────────────────┐
│      Frontend (React)              │
│  Candidato se registra             │
└──────────────┬─────────────────────┘
               │
        POST /api/candidatos
               │
┌──────────────▼─────────────────────┐
│       Backend API (FastAPI)        │
│                                    │
│  1. Guardar en BD                  │
│  2. 🔔 Disparar webhook            │
│     CANDIDATO_CREADO               │
└──────────────┬─────────────────────┘
               │
    Async Background Task
               │
┌──────────────▼─────────────────────┐
│   Webhook Manager                  │
│  (webhooks.py)                     │
│                                    │
│  ├─ Ejecutar handlers              │
│  ├─ sync_a_crm_nuevo_candidato     │
│  ├─ crear_deal_en_crm              │
│  ├─ enviar_email_automatico        │
│  └─ registrar_en_log_auditoria     │
└──────────────┬──────────────────────┘
               │
      ┌────────┴───────┬────────────────┐
      │                │                │
 HubSpot          Gmail SMTP       PostgreSQL
  Create          Send Email        Audit Log
  Contact         (PDF)             Update
```

---

## 📋 INSTALACIÓN PASO A PASO

### Paso 1: Copiar archivos
```bash
# Copiar a proyecto
cp crm_service.py /home/claude/
cp webhooks.py /home/claude/
cp api_crm_endpoints.py /home/claude/
```

### Paso 2: Instalar dependencias
```bash
pip install --break-system-packages httpx==0.25.2
```

### Paso 3: Actualizar API
```python
# En api.py agregar:
from crm_service import hubspot_service
from webhooks import webhook_manager, EventoCandidato, registrar_todos_los_webhooks
from api_crm_endpoints import router as crm_router

# Registrar router
app.include_router(crm_router)

# Registrar webhooks
registrar_todos_los_webhooks()
```

### Paso 4: Configurar HubSpot

**En HubSpot (gratuito):**
1. Crear cuenta: https://www.hubspot.com
2. Settings → Private app access
3. Crear app "CENERH Recruit OS"
4. Copiar API key

**En .env.production:**
```
HUBSPOT_API_KEY=pat-na1-xxxxxxxxxxxxx
```

**En Railway variables:**
```
HUBSPOT_API_KEY = tu-clave-aqui
```

### Paso 5: Test
```bash
# Health check
curl http://localhost:8000/health

# Ver estado de CRM
curl http://localhost:8000/api/crm/status
# Response: {"hubspot": {"configurado": true, "estado": "✅ Conectado"}}

# Crear candidato (triggers webhook)
curl -X POST http://localhost:8000/api/candidatos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test User",
    "email": "test@example.com",
    "telefono": "809-000-0000",
    "vacante_id": "contador_paraiso"
  }'

# Ver en logs:
# 🔔 EVENTO: candidato.creado
# 📤 Sincronizando candidato a CRM: Test User
# ✅ Candidato creado en HubSpot
```

---

## 🎯 FLUJO COMPLETO

### Para Candidatos

```
1. Se registra en CENERH
   ├─ Ingresa nombre, email, teléfono
   └─ 🔔 Se sincroniza a HubSpot (automático)

2. Completa tests (300 preguntas)
   └─ 🔔 Se crea deal en HubSpot (automático)

3. Ve resultados
   └─ 📧 Se envía email con PDF (automático)

4. Si es PRIORITARIO
   ├─ Se actualiza estado en CRM
   ├─ Se agrega nota con evaluación
   └─ Se crea tarea de seguimiento
```

### Para CENERH

```
1. Dashboard Admin
   ├─ Ve candidatos sincronizados
   └─ Filtros por estado

2. HubSpot CRM
   ├─ Contacto de candidato
   ├─ Deal con oportunidad
   ├─ Tareas de seguimiento
   └─ Emails y comunicación

3. API CENERH
   ├─ POST /api/crm/sync/candidato/{id}
   ├─ POST /api/crm/deal/{id}
   ├─ GET /api/crm/status
   └─ Sincronización manual si es necesario
```

---

## 📊 EJEMPLO DE DATOS EN HUBSPOT

### Contacto
```
Nombre:        Juan García
Email:         juan@example.com
Teléfono:      809-123-4567
Estado:        ABIERTO (Open)
Fuente:        CENERH Recruit OS
candidato_id:  cand_001
vacante_id:    contador_paraiso
```

### Deal (Oportunidad)
```
Nombre:        Juan García - Contador
Monto:         $100 (Fee de CENERH)
Etapa:         En Evaluación
Fecha Cierre:  2026-08-27 (30 días)
Asociado a:    Juan García (contacto)
Score:         85/100
```

### Tarea
```
Título:        Seguimiento: Evaluación de candidato
Descripción:   Hacer seguimiento con Juan García
Vencimiento:   2026-07-30 (3 días)
Asociado a:    Juan García (contacto)
```

---

## 🔄 OPERACIONES MANUALES (Si lo necesitas)

### Sincronizar candidato específico
```bash
curl -X POST http://localhost:8000/api/crm/sync/candidato/cand_001?plataforma=hubspot
```

### Sincronizar todos
```bash
curl -X POST http://localhost:8000/api/crm/sync/todos?plataforma=hubspot
```

### Crear deal
```bash
curl -X POST http://localhost:8000/api/crm/deal/cand_001?plataforma=hubspot
```

### Ver estado
```bash
curl http://localhost:8000/api/crm/status
```

---

## 📈 MÉTRICAS Y MONITOREO

### Verificar sincronización
```bash
GET /api/crm/candidatos/hubspot

Response:
{
  "total_candidatos": 50,
  "en_hubspot": [
    {
      "id": "cand_001",
      "nombre": "Juan García",
      "email": "juan@example.com",
      "vacante": "Contador",
      "score": 85
    },
    ...
  ]
}
```

### Ver logs en Railway
```
Dashboard → Logs → Filtrar por "EVENTO"

Verás:
🔔 EVENTO: candidato.creado
📤 Sincronizando candidato a CRM: Juan García
✅ Candidato creado en HubSpot
```

---

## 🔐 SEGURIDAD

✅ **Hacer:**
- Guardar API keys en variables de entorno
- No commitear .env en Git
- Usar tokens con permisos limitados

❌ **No hacer:**
- Hardcodear API keys en código
- Compartir tokens por email
- Usar misma key en dev/prod

---

## ⚙️ CONFIGURACIÓN PLATAFORMAS

### HubSpot (Recomendado)
- ✅ Gratuito con funciones completas
- ✅ Fácil de setup
- ✅ Buena documentación
- ✅ Integración activa

### Pipedrive
- ✅ Alternativa si prefieres
- ⚠️ Más enfocado en ventas
- ⚠️ Interfaz diferente

---

## 🚀 PRÓXIMAS FASES

### Fase 1: Básica ✅ (Ya hecho)
- Sincronizar candidatos
- Crear deals
- Enviar emails
- Crear tareas

### Fase 2: Avanzada (Próximo)
- Asignar a vendedores
- Scoring automático
- Reportes avanzados
- Integración con calendario

### Fase 3: Enterprise (Futuro)
- Salesforce integration
- SAP integration
- Custom workflows
- BI y analytics

---

## ✅ CHECKLIST FINAL

**Desarrollo Local:**
- [ ] Archivos copiados a proyecto
- [ ] `httpx` instalado
- [ ] Imports agregados en api.py
- [ ] Router de CRM registrado
- [ ] Webhooks registrados
- [ ] Tests locales pasan
- [ ] API responde en /api/crm/status

**Producción:**
- [ ] Cuenta HubSpot creada
- [ ] API key generada
- [ ] HUBSPOT_API_KEY en Railway variables
- [ ] Deploy en Railway actualizado
- [ ] Test: GET /api/crm/status
- [ ] Test: Crear candidato
- [ ] Verificar sincronización
- [ ] Monitorear logs

---

## 📞 SOPORTE

### Error: "HUBSPOT_API_KEY no configurada"
```bash
# Ir a Railway Dashboard
# Project → Variables → Add Variable
# HUBSPOT_API_KEY = tu-clave-aqui
# Deploy
```

### Error: "Module not found"
```bash
# Verificar que archivos están en proyecto
ls -la crm_service.py
ls -la webhooks.py
ls -la api_crm_endpoints.py
```

### Webhook no se dispara
```bash
# Verificar en logs
# Railway Dashboard → Logs
# Buscar "EVENTO"
# Si no aparece, revisar código de integración
```

---

## 🎉 ¡SISTEMA COMPLETO!

**Tienes:**
✅ Backend API (FastAPI)  
✅ Frontend React  
✅ Base de datos PostgreSQL  
✅ Integración CRM (HubSpot/Pipedrive)  
✅ Email automation  
✅ PDF generation  
✅ Webhooks automáticos  
✅ Auditoría completa  

**Falta:**
- Deploy en producción ← **SIGUIENTE**
- Configurar dominio personalizado

---

## 🚀 PRÓXIMO PASO

**PASO 4: DEPLOY EN PRODUCCIÓN**

Tiempo: 1 hora

Resultado: Sistema vivo, recibiendo candidatos reales

¿Continuamos?
