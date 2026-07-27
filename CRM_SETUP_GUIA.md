# 🔗 CENERH RECRUIT OS - Integración CRM

Guía completa para sincronizar candidatos con HubSpot o Pipedrive automáticamente.

---

## ⚙️ CONFIGURACIÓN INICIAL

### OPCIÓN 1: HubSpot (Recomendado)

HubSpot es la opción más popular para CRM. Cuenta gratuita con funcionalidades completas.

#### Paso 1: Crear cuenta en HubSpot

1. Ir a https://www.hubspot.com
2. Sign up (crear cuenta gratuita)
3. Completar setup inicial

#### Paso 2: Obtener API Key

1. Ir a Settings (esquina superior derecha)
2. Account defaults → Private app access
3. Click en "Create app"
4. Nombre: "CENERH Recruit OS"
5. Scopes necesarios:
   - `crm.objects.contacts.read`
   - `crm.objects.contacts.write`
   - `crm.objects.deals.read`
   - `crm.objects.deals.write`
   - `crm.objects.tasks.write`
6. Click "Create"
7. Copiar el token (API key)

#### Paso 3: Configurar en CENERH

En archivo `.env.production`:

```
HUBSPOT_API_KEY=pat-na1-xxxxxxxxxxxxx
```

En Railway dashboard (Variables):

```
HUBSPOT_API_KEY = tu-clave-aqui
```

---

### OPCIÓN 2: Pipedrive

Alternativa si prefieres Pipedrive. También gratuito con limitaciones.

#### Paso 1: Crear cuenta en Pipedrive

1. Ir a https://www.pipedrive.com
2. Sign up (cuenta gratuita)
3. Completar onboarding

#### Paso 2: Obtener API Token

1. Ir a Settings (rueda dentada)
2. Personal preferences
3. API (en el menú izquierdo)
4. Copiar el "API token"

#### Paso 3: Configurar en CENERH

En `.env.production`:

```
PIPEDRIVE_API_TOKEN=tu_token_aqui
```

---

## 🔄 CÓMO FUNCIONA LA SINCRONIZACIÓN

### Flujo Automático (Webhooks)

```
Candidato se registra
        ↓
CENERH crea candidato
        ↓
🔔 WEBHOOK: Candidato creado
        ↓
✅ Se sincroniza automáticamente a HubSpot
   - Crea Contacto
   - Agrega propiedades custom
        ↓
Candidato completa tests
        ↓
🔔 WEBHOOK: Evaluación completada
        ↓
✅ Se crea Deal (oportunidad) automáticamente
✅ Se envía email automático
✅ Se crea tarea de seguimiento
        ↓
Candidato es PRIORITARIO
        ↓
🔔 WEBHOOK: Candidato prioritario
        ↓
✅ Se actualiza estado en HubSpot
✅ Se agrega nota con evaluación
```

### Flujo Manual (si lo necesitas)

```bash
# Sincronizar un candidato específico
curl -X POST https://tu-api.com/api/crm/sync/candidato/cand_001

# Sincronizar todos (bulk)
curl -X POST https://tu-api.com/api/crm/sync/todos

# Crear deal para candidato
curl -X POST https://tu-api.com/api/crm/deal/cand_001

# Ver estado de CRM
curl https://tu-api.com/api/crm/status
```

---

## 📊 EVENTOS Y ACCIONES

### Eventos Disponibles

```
CANDIDATO_CREADO
   → Sincronizar a HubSpot/Pipedrive

CANDIDATO_EVALUACION_COMPLETADA
   → Crear Deal
   → Enviar Email
   → Crear Tarea
   → Log de Auditoría

CANDIDATO_PRIORITARIO
   → Actualizar estado en CRM
   → Agregar nota con evaluación
   → Crear tarea de seguimiento

CANDIDATO_VIABLE
   → Actualizar estado

CANDIDATO_NO_RECOMENDADO
   → Marcar como "disqualified"
```

### Agregar Eventos Custom

En `webhooks.py`:

```python
# 1. Crear evento
class EventoCandidato(str, Enum):
    MI_EVENTO_CUSTOM = "candidato.mi_evento"

# 2. Crear handler
async def mi_handler(datos):
    print(f"Mi evento: {datos}")

# 3. Registrar
webhook_manager.registrar(
    EventoCandidato.MI_EVENTO_CUSTOM,
    mi_handler
)

# 4. Disparar (desde código)
await webhook_manager.disparar(
    EventoCandidato.MI_EVENTO_CUSTOM,
    {"candidato_id": "123", "data": "value"}
)
```

---

## 🎯 MAPEO DE DATOS

### Candidato CENERH → Contacto HubSpot

```
CENERH              HubSpot
├─ nombre      →    firstname + lastname
├─ email       →    email
├─ telefono    →    phone
├─ candidato_id →   [custom field]
├─ vacante_id  →    [custom field]
└─ fecha       →    hs_lead_status = OPEN
```

### Evaluación CENERH → Deal HubSpot

```
CENERH              HubSpot
├─ candidato_id →   deal.asociado a contacto
├─ nombre       →    dealname
├─ vacante_id   →    dealstage
├─ score_final  →    amount
└─ fecha        →    closedate (30 días después)
```

---

## 📱 USANDO LA API

### Ejemplo 1: Sincronizar candidato

```bash
# Request
POST /api/crm/sync/candidato/cand_001?plataforma=hubspot

# Response
{
  "status": "success",
  "mensaje": "Candidato sincronizado a HubSpot",
  "hubspot_id": "7891234567"
}
```

### Ejemplo 2: Crear deal

```bash
# Request
POST /api/crm/deal/cand_001?plataforma=hubspot

# Response
{
  "status": "success",
  "deal_id": "9876543210"
}
```

### Ejemplo 3: Verificar estado

```bash
# Request
GET /api/crm/status

# Response
{
  "hubspot": {
    "configurado": true,
    "estado": "✅ Conectado"
  },
  "pipedrive": {
    "configurado": false,
    "estado": "❌ No configurado"
  }
}
```

### Ejemplo 4: Sincronizar todos

```bash
# Request (toma varios minutos para muchos candidatos)
POST /api/crm/sync/todos?plataforma=hubspot

# Response
{
  "status": "success",
  "total_candidatos": 150,
  "sincronizados": 145,
  "errores": 5,
  "detalles_errores": [...]
}
```

---

## 🚨 TROUBLESHOOTING

### "HUBSPOT_API_KEY no configurada"

**Solución:**
```bash
# Verificar que existe en variables de entorno
echo $HUBSPOT_API_KEY

# Si no existe, agregarla
export HUBSPOT_API_KEY=pat-na1-xxxxx

# O en Railway: Dashboard → Project → Variables → Add
```

### "Error sincronizando a HubSpot"

**Causas posibles:**
1. API key inválida o expirada
2. Sin permisos suficientes
3. Rate limit de HubSpot

**Solución:**
1. Verificar API key en HubSpot
2. Regenerar si es necesario
3. Esperar 1 hora si es rate limit

### "Contacto no encontrado en HubSpot"

**Causa:** El candidato no se sincronizó primero

**Solución:**
```bash
# Sincronizar el candidato primero
POST /api/crm/sync/candidato/cand_001

# Luego crear deal
POST /api/crm/deal/cand_001
```

### "Email no se envía automáticamente"

**Verificar:**
1. SMTP está configurado
2. Evento `CANDIDATO_EVALUACION_COMPLETADA` se dispara
3. Revisar logs en server

```python
# En logs deberías ver:
🔔 EVENTO: candidato.evaluacion_completada
   Datos: {...}
📧 Enviando email automático a: email@example.com
```

---

## 📈 MONITOREO

### Ver histórico de sincronización

```bash
GET /api/crm/candidatos/hubspot

# Response
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

### Logs de auditoría

Los eventos se registran en tabla `AuditLog`:

```sql
SELECT * FROM auditlog 
WHERE evento = 'candidato_evaluado'
ORDER BY fecha DESC;
```

---

## 🔐 SEGURIDAD

### Proteger API Keys

✅ **Hacer:**
```bash
# Guardar en variables de entorno (no en código)
export HUBSPOT_API_KEY=xxx
```

❌ **No hacer:**
```python
# Nunca hardcodear
api_key = "pat-na1-xxx"  # ❌ INSEGURO
```

### Permisos Mínimos

En HubSpot, dar solo permisos necesarios:
- ✅ `contacts.read` + `contacts.write` (crear/actualizar)
- ✅ `deals.read` + `deals.write` (crear deals)
- ✅ `tasks.write` (crear tareas)
- ❌ No necesita: `delete` permisos

### Rate Limiting

HubSpot tiene límites:
- 10 requests/segundo (tier gratuito)
- 100 requests/segundo (tier pagado)

Si excedes:
- Automático: espera 1 segundo entre requests
- Manual: implementar retry con backoff

---

## 🔄 WEBHOOK EVENTS (Servidor a Servidor)

Si quieres que HubSpot NOTIFIQUE a CENERH cuando algo cambia:

### Setup en HubSpot

1. Settings → Integrations → Webhooks
2. Click "Create webhook"
3. URL: `https://tu-api.com/webhooks/hubspot`
4. Eventos:
   - `contact.creation`
   - `contact.deletion`
   - `deal.creation`
5. Test → Save

### Handler en CENERH

```python
# api.py
@app.post("/webhooks/hubspot")
async def webhook_hubspot(request: Request):
    payload = await request.json()
    
    # Procesar evento
    if payload['event'] == 'contact.creation':
        print(f"Nuevo contacto en HubSpot: {payload}")
    
    return {"status": "ok"}
```

---

## 📋 CHECKLIST PARA PRODUCCIÓN

- [ ] Crear cuenta HubSpot/Pipedrive
- [ ] Obtener API key
- [ ] Configurar en variables de entorno
- [ ] Test: GET /api/crm/status
- [ ] Test: POST /api/crm/sync/candidato/{id}
- [ ] Revisar logs de sincronización
- [ ] Habilitar webhooks
- [ ] Documentar en equipo
- [ ] Setup alertas si sincronización falla

---

## 🎯 PRÓXIMOS PASOS

### Fase 1: Básica (Ya hecho)
- ✅ Sincronizar candidatos a CRM
- ✅ Crear deals automáticamente
- ✅ Enviar emails automáticos

### Fase 2: Avanzada (Opcional)
- Integrar scoring automático
- Asignar candidatos a vendedores
- Crear reportes en CRM
- Integrar con calendar (agendar entrevistas)

### Fase 3: Enterprise (Futuro)
- Integrar con Salesforce
- Integrar con SAP
- Custom workflows por cliente
- BI + Analytics

---

## 📞 SOPORTE

**Error con HubSpot?**
- Docs: https://developers.hubspot.com/docs/api/overview
- Community: https://community.hubspot.com

**Error con Pipedrive?**
- Docs: https://developers.pipedrive.com/docs/basics
- Support: support@pipedrive.com

**Error con CENERH?**
- Revisar logs en Railway
- Verificar variables de entorno
- Ejecutar test: GET /api/crm/test-conexion/hubspot

---

## 🚀 ¡LISTO!

Tu sistema de CRM está completamente integrado. Ahora:

1. ✅ Candidatos se sincronizan automáticamente
2. ✅ Se crean deals sin intervención manual
3. ✅ Se envían emails automáticamente
4. ✅ CENERH tiene pipeline en CRM

**Próximo:** Deploy en producción y empezar a recibir candidatos.
