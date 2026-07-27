# 🔧 INTEGRACIÓN CRM EN API EXISTENTE

Pasos para integrar los módulos de CRM en tu `api.py` existente.

---

## PASO 1: Agregar imports en api.py

Al inicio de tu archivo `api.py`, agregar:

```python
# Importar módulos de CRM
from crm_service import hubspot_service
from webhooks import webhook_manager, EventoCandidato, registrar_todos_los_webhooks
from api_crm_endpoints import router as crm_router

# Importar para eventos
from fastapi import BackgroundTasks
```

---

## PASO 2: Registrar router de CRM

Después de crear la app de FastAPI:

```python
app = FastAPI(
    title="CENERH RECRUIT OS",
    description="Sistema de evaluación psicométrica",
    version="1.0.0"
)

# Registrar router de CRM
app.include_router(crm_router)

# Registrar todos los webhooks al inicio
registrar_todos_los_webhooks()

# Evento de startup
@app.on_event("startup")
async def startup_event():
    print("""
    ╔════════════════════════════════════════╗
    ║   CENERH RECRUIT OS - API INICIADA    ║
    ╠════════════════════════════════════════╣
    ║   ✅ Base de datos conectada          ║
    ║   ✅ CRM sincronizado                 ║
    ║   ✅ Webhooks registrados             ║
    ║   ✅ API lista para candidatos        ║
    ╚════════════════════════════════════════╝
    """)
```

---

## PASO 3: Modificar endpoint de crear candidato

Actualizar el endpoint POST `/api/candidatos`:

```python
from datetime import datetime

@app.post("/api/candidatos")
async def crear_candidato(
    request: CandidatoRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Crear nuevo candidato"""
    
    # Validar que vacante existe
    vacante = db.query(Vacante).filter(Vacante.id == request.vacante_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")

    # Crear candidato
    candidato = Candidato(
        nombre=request.nombre,
        email=request.email,
        telefono=request.telefono,
        vacante_id=request.vacante_id,
        fecha_registro=datetime.now()
    )
    db.add(candidato)
    db.commit()
    db.refresh(candidato)

    # 🔔 DISPARAR WEBHOOK: Nuevo candidato
    background_tasks.add_task(
        webhook_manager.disparar,
        EventoCandidato.CANDIDATO_CREADO,
        {
            "candidato_id": candidato.id,
            "nombre": candidato.nombre,
            "email": candidato.email,
            "telefono": candidato.telefono,
            "vacante_id": candidato.vacante_id,
        }
    )

    return {
        "candidato_id": candidato.id,
        "nombre": candidato.nombre,
        "email": candidato.email,
        "mensaje": "Candidato registrado. Sincronizando con CRM..."
    }
```

---

## PASO 4: Modificar endpoint de guardar respuestas

Actualizar el endpoint POST `/api/tests/{test_id}/{candidato_id}/respuestas`:

```python
@app.post("/api/tests/{test_id}/{candidato_id}/respuestas")
async def guardar_respuestas_test(
    test_id: str,
    candidato_id: str,
    request: RespuestasRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Guardar respuestas y calcular score"""
    
    # ... código existente para guardar respuestas ...
    
    # Obtener candidato y vacante
    candidato = db.query(Candidato).filter(Candidato.id == candidato_id).first()
    
    # Calcular scores
    scores = calcular_scores_candidato(db, candidato_id)
    
    # Guardar scores
    score_candidato = ScoreCandidato(
        candidato_id=candidato_id,
        score_competencias=scores.get("competencias", 0),
        score_psicometricos=scores.get("psicometricos", 0),
        score_cognitivos=scores.get("cognitivos", 0),
        score_final=scores.get("total", 0),
        fecha_calculo=datetime.now()
    )
    db.add(score_candidato)
    db.commit()

    # 🔔 DISPARAR WEBHOOK: Evaluación completada
    background_tasks.add_task(
        webhook_manager.disparar,
        EventoCandidato.CANDIDATO_EVALUACION_COMPLETADA,
        {
            "candidato_id": candidato_id,
            "nombre": candidato.nombre,
            "email": candidato.email,
            "vacante_id": candidato.vacante_id,
            "score_final": scores.get("total", 0),
        }
    )

    # Disparar webhook adicional según clasificación
    clasificacion = clasificar_candidato(scores.get("total", 0))
    
    if clasificacion == "PRIORITARIO":
        background_tasks.add_task(
            webhook_manager.disparar,
            EventoCandidato.CANDIDATO_PRIORITARIO,
            {
                "candidato_id": candidato_id,
                "nombre": candidato.nombre,
                "email": candidato.email,
                "score_final": scores.get("total", 0),
            }
        )
    
    return {"score_final": scores.get("total", 0), "clasificacion": clasificacion}
```

---

## PASO 5: Variables de entorno

Agregar en `.env.production`:

```
# ============================================================================
# CRM INTEGRATION
# ============================================================================

# HubSpot
HUBSPOT_API_KEY=pat-na1-xxxxxxxxxxxxx

# Pipedrive (alternativa)
PIPEDRIVE_API_TOKEN=xxxxxxxxxxxxx

# Email (para envíos automáticos)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@cenerhconsulting.com
SMTP_PASSWORD=tu-app-password
```

---

## PASO 6: Dependencias Python

Agregar a `requirements.txt`:

```
# CRM Integration
httpx==0.25.2  # Cliente HTTP async para HubSpot/Pipedrive
```

Instalar:
```bash
pip install --break-system-packages httpx==0.25.2
```

---

## PASO 7: Verificar que funciona

### Test 1: Health Check
```bash
curl http://localhost:8000/health
# Response: {"status": "ok"}
```

### Test 2: Estado de CRM
```bash
curl http://localhost:8000/api/crm/status
# Response: {"hubspot": {"configurado": true, "estado": "✅ Conectado"}, ...}
```

### Test 3: Crear candidato (con webhook)
```bash
curl -X POST http://localhost:8000/api/candidatos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test User",
    "email": "test@example.com",
    "telefono": "809-000-0000",
    "vacante_id": "contador_paraiso"
  }'

# En logs deberías ver:
# 🔔 EVENTO: candidato.creado
# 📤 Sincronizando candidato a CRM: Test User
# ✅ Candidato creado en HubSpot: {...}
```

### Test 4: Completar tests (con webhook)
```bash
curl -X POST http://localhost:8000/api/tests/verbal/cand_001/respuestas \
  -H "Content-Type: application/json" \
  -d '{"respuestas": {"q1": "A", "q2": "B", ...}}'

# En logs:
# 🔔 EVENTO: candidato.evaluacion_completada
# 🤝 Creando oportunidad en CRM para: Test User
# 📧 Enviando email automático a: test@example.com
# ✅ PDF generado y email enviado
```

---

## PASO 8: Logs esperados

Cuando todo está bien integrado:

```
✅ WEBHOOKS REGISTRADOS:
   • Nuevo candidato → Sincronizar a HubSpot
   • Evaluación completada → Crear deal + Email + Auditoría
   • Candidato prioritario → Actualizar estado + Tarea

🔔 EVENTO: candidato.creado
   Datos: {
     "candidato_id": "cand_001",
     "nombre": "Juan García",
     "email": "juan@example.com",
     ...
   }

📤 Sincronizando candidato a CRM: Juan García
✅ Candidato creado en HubSpot: {"hubspot_id": "7891234567"}

🔔 EVENTO: candidato.evaluacion_completada
📧 Enviando email automático a: juan@example.com
✅ Email enviado
✅ Evento registrado en auditoría
```

---

## PASO 9: Troubleshooting

### Error: "ModuleNotFoundError: No module named 'crm_service'"

**Solución:**
```bash
# Verificar que crm_service.py está en el mismo directorio que api.py
ls -la crm_service.py
ls -la api.py

# Si no está, copiar archivo
cp /home/claude/crm_service.py /path/to/project/
```

### Error: "HUBSPOT_API_KEY no configurada"

**Solución:**
```python
# En api.py, esto es normal en desarrollo
# Para producción, agregar clave en variables de entorno
# En Railway: Dashboard → Variables → Add HUBSPOT_API_KEY
```

### Error: "Webhook no se dispara"

Verificar:
1. `registrar_todos_los_webhooks()` se ejecuta en startup
2. `background_tasks.add_task()` se usa en endpoints
3. Revisar logs de la API

---

## PASO 10: Estructura final

```
proyecto/
├── api.py                        (API principal + imports CRM)
├── models.py                     (Modelos existentes)
├── database.py                   (Conexión BD existente)
├── crm_service.py               (🆕 Servicio CRM)
├── webhooks.py                  (🆕 Sistema de webhooks)
├── api_crm_endpoints.py         (🆕 Endpoints de CRM)
├── email_sender.py              (Existente)
├── pdf_generator.py             (Existente)
├── requirements.txt             (Actualizado con httpx)
└── .env.production              (Con variables de CRM)
```

---

## ✅ CHECKLIST DE INTEGRACIÓN

- [ ] Copiar `crm_service.py` a proyecto
- [ ] Copiar `webhooks.py` a proyecto
- [ ] Copiar `api_crm_endpoints.py` a proyecto
- [ ] Actualizar imports en `api.py`
- [ ] Registrar router de CRM
- [ ] Registrar webhooks en startup
- [ ] Actualizar endpoint de crear candidato
- [ ] Actualizar endpoint de guardar respuestas
- [ ] Agregar variables de entorno
- [ ] Instalar `httpx`
- [ ] Test local: crear candidato
- [ ] Test local: completar tests
- [ ] Revisar logs
- [ ] Deploy en producción

---

## 🚀 PRÓXIMO PASO

Después de integrar CRM:

1. Desplegar en producción
2. Configurar API keys en Railway
3. Probar flujo completo
4. Monitorear sincronización

¡Listo! Tu sistema está completamente integrado.
