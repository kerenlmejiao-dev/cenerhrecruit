# 🚀 CENERH RECRUIT OS - DEPLOY EN PRODUCCIÓN

Guía paso a paso para poner tu sistema completo en vivo.

---

## ✅ CHECKLIST PRE-PRODUCCIÓN

### Backend API (FastAPI)

- [ ] `api.py` actualizado con imports de CRM
- [ ] `crm_service.py` copiado a proyecto
- [ ] `webhooks.py` copiado a proyecto
- [ ] `api_crm_endpoints.py` copiado a proyecto
- [ ] `requirements.txt` incluye `httpx==0.25.2`
- [ ] `.env.production` configurado con todas las variables
- [ ] Base de datos PostgreSQL creada en Railway
- [ ] `Procfile` en raíz del proyecto
- [ ] `api.py` se inicia con `uvicorn` correctamente
- [ ] Todos los endpoints responden localmente

### Frontend React

- [ ] `npm install` ejecutado
- [ ] `.env.local` configurado con `VITE_API_URL`
- [ ] `npm run build` genera `dist/` sin errores
- [ ] `npm run preview` muestra el app correctamente
- [ ] Formulario de registro funciona
- [ ] Tests se cargan y responden
- [ ] Resultados se muestran correctamente
- [ ] Admin dashboard carga datos

### CRM Integration

- [ ] Cuenta HubSpot creada (gratuita)
- [ ] API key generada en HubSpot
- [ ] Pipedrive setup (opcional)
- [ ] Variables de entorno documentadas
- [ ] Webhooks configurados localmente

### Emails

- [ ] Gmail con 2-factor activado
- [ ] App password generado
- [ ] SMTP variables configuradas

### Dominio (Opcional)

- [ ] Dominio registrado (tudominio.com)
- [ ] DNS apuntando a hosting (opcional)

---

## 🎯 PASO 4.2: Deploy Backend en Railway

### Paso 1: Preparar repositorio Git

```bash
cd /home/claude
git init
git add .
git commit -m "CENERH RECRUIT OS - Initial commit"
git remote add origin https://github.com/TU_USUARIO/cenerh-recruit-os.git
git branch -M main
git push -u origin main
```

### Paso 2: Crear proyecto en Railway

1. Ir a https://railway.app
2. Sign up con GitHub
3. Autorizar Railway en tu cuenta GitHub
4. Click en "Dashboard"
5. Click en "+ New Project"
6. Seleccionar "Deploy from GitHub"
7. Seleccionar tu repo `cenerh-recruit-os`
8. Railway detectará Python automáticamente

### Paso 3: Agregar PostgreSQL

1. En Railway dashboard, click "+ Add Service"
2. Seleccionar "PostgreSQL"
3. Click "Add"
4. Railway crea base de datos automáticamente
5. Agrega `DATABASE_URL` automáticamente a variables

### Paso 4: Configurar variables de entorno

En Railway, Project → Variables → Add:

```
DATABASE_URL=postgresql://...  (automatico)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
SMTP_FROM_EMAIL=reportes@cenerhconsulting.com
SMTP_FROM_NAME=CENERH Consulting
HUBSPOT_API_KEY=pat-na1-xxxxxxxxxxxxx
API_ENV=production
API_DEBUG=false
CORS_ORIGINS=["https://tuapp.com", "http://localhost:5173"]
FRONTEND_URL=https://tuapp.com
```

### Paso 5: Deploy automático

```bash
# Hacer cambios locales
git add .
git commit -m "Update features"
git push

# Railway automáticamente redeploy en 2-3 minutos
```

### Paso 6: Obtener URL de API

En Railway:
- Project → Deployments → Opening URL
- Tu API está en: `https://tu-proyecto.up.railway.app`

```bash
# Test
curl https://tu-proyecto.up.railway.app/health
# Response: {"status": "ok"}

# Ver estado de CRM
curl https://tu-proyecto.up.railway.app/api/crm/status
```

---

## 🎨 PASO 4.3: Deploy Frontend en Vercel

### Opción A: Vercel (Recomendado - 5 minutos)

#### Paso 1: Instalar Vercel CLI

```bash
npm install -g vercel
```

#### Paso 2: Login en Vercel

```bash
vercel login
# Se abrirá navegador para autenticar con GitHub
```

#### Paso 3: Deploy

```bash
cd frontend
vercel --prod
```

Se abre navegador:
- Project name: `cenerh-recruit-os-frontend`
- Framework: React
- Build settings: npm run build, dist

#### Paso 4: Configurar variables

En Vercel dashboard:
- Project → Settings → Environment Variables
- Agregar: `VITE_API_URL=https://tu-api.up.railway.app`

#### Paso 5: Redeploy

```bash
vercel --prod
```

Tu frontend está en: `https://cenerh-recruit-os-frontend.vercel.app`

---

### Opción B: Netlify (Alternativa)

```bash
npm install -g netlify-cli
cd frontend
netlify deploy --prod --dir=dist
```

Tu frontend está en: `https://cenerh-recruit-os.netlify.app`

---

### Opción C: AWS S3 + CloudFront

```bash
# Crear bucket S3
aws s3 mb s3://cenerh-recruit-os

# Build
npm run build

# Upload
aws s3 cp dist/ s3://cenerh-recruit-os --recursive --acl public-read

# Crear CloudFront distribution (opcional)
# Resultado: https://cdn.amazonaws.com/...
```

---

## 🌐 PASO 4.4: Configurar dominios personalizados

### Para Backend (API)

Si tienes dominio: `api.cenerhconsulting.com`

**En Railway:**
1. Project → Settings → Domains
2. Click "+ Add Domain"
3. Ingresar: `api.cenerhconsulting.com`
4. Copiar el CNAME que Railway proporciona
5. En tu registrador de dominios (GoDaddy, Namecheap, etc):
   - DNS → Agregar CNAME record
   - Name: `api`
   - Value: lo que Railway proporciona

**Esperar 15-30 minutos para que DNS se propague**

```bash
# Verificar que funciona
curl https://api.cenerhconsulting.com/health
```

### Para Frontend (Portal)

Si tienes dominio: `app.cenerhconsulting.com`

**En Vercel:**
1. Project → Settings → Domains
2. Click "Add Domain"
3. Ingresar: `app.cenerhconsulting.com`
4. Vercel proporciona CNAME
5. Configurar en registrador igual que arriba

```bash
# Verificar
curl https://app.cenerhconsulting.com
```

---

## 🔐 PASO 4.5: Obtener API Keys Necesarias

### HubSpot API Key

1. Ir a https://app.hubspot.com
2. Settings (rueda dentada, esquina superior derecha)
3. Account defaults → Private app access
4. Click "Create app"
5. Nombre: "CENERH Recruit OS"
6. Scopes necesarios:
   - `crm.objects.contacts.read`
   - `crm.objects.contacts.write`
   - `crm.objects.deals.read`
   - `crm.objects.deals.write`
   - `crm.objects.tasks.write`
7. Click "Create"
8. Copiar token: `pat-na1-xxxxxxxxxxxxx`
9. Agregar en Railway variables: `HUBSPOT_API_KEY`

### Gmail App Password

1. Ir a https://myaccount.google.com
2. Security (izquierda)
3. 2-Step Verification (activar si no lo está)
4. App passwords
5. Seleccionar: Mail + Windows
6. Copiar contraseña generada
7. Agregar en Railway: `SMTP_PASSWORD`

---

## 🧪 PASO 4.6: Tests en Producción

### Test 1: Backend funcionando

```bash
# Health check
curl https://tu-api.up.railway.app/health
# Response: {"status": "ok"}

# Ver documentación
curl https://tu-api.up.railway.app/docs
# (Abre Swagger UI en navegador)

# Estado de CRM
curl https://tu-api.up.railway.app/api/crm/status
```

### Test 2: Frontend carga

```bash
# Abrir en navegador
https://tu-frontend.vercel.app

# Verificar que:
# ✅ Página de registro carga
# ✅ Formulario es funcional
# ✅ Botón "Comenzar" funciona
```

### Test 3: Flujo completo de candidato

1. Abrir frontend: `https://tu-frontend.vercel.app`
2. Completar registro:
   - Nombre: "Test Candidato"
   - Email: "test@example.com"
   - Teléfono: "809-000-0000"
   - Vacante: "Contador General"
3. Click "Comenzar Evaluación"
4. Verificar:
   - ✅ Tests cargan
   - ✅ Preguntas aparecen
   - ✅ Barra de progreso funciona
5. Responder 2-3 preguntas, click "Siguiente"
6. Debe redirigir a resultados
7. Ver:
   - ✅ Score aparece
   - ✅ Gráficos se muestran
   - ✅ Botones funcionan

### Test 4: Verificar sincronización a CRM

1. Abrir HubSpot: https://app.hubspot.com
2. Ir a Contactos
3. Buscar "Test Candidato"
4. Verificar:
   - ✅ Contacto existe
   - ✅ Email es correcto
   - ✅ Teléfono guardado
   - ✅ Estado: "Abierto"
5. Click en contacto
6. Ver Deals asociados
7. Verificar:
   - ✅ Deal existe
   - ✅ Nombre correcto
   - ✅ Estado: "En Evaluación"

### Test 5: Verificar email automático

1. Revisar bandeja de entrada de test@example.com
2. Buscar email de CENERH
3. Verificar:
   - ✅ Email recibido
   - ✅ Asunto correcto
   - ✅ PDF adjunto
   - ✅ Contenido personalizado

---

## 📊 PASO 4.7: Monitoreo en Producción

### Logs en Railway

```bash
# Ver logs en tiempo real
railway logs -f

# Buscar errores
railway logs | grep ERROR

# Ver logs de última hora
railway logs --since 1h
```

Desde dashboard Railway:
1. Project → Logs
2. Ver eventos en tiempo real
3. Buscar por palabra clave (ej: "EVENTO", "ERROR")

### Métricas

En Railway dashboard:
1. Project → Metrics
2. Ver:
   - CPU usage
   - Memory usage
   - Disk usage
   - Request count
   - Response time

### Alertas

Configurar notificaciones:
1. Project → Settings → Alerts
2. Add Alert
3. Configurar: API down, Error rate alto, etc

### Monitoreo de Base de Datos

```sql
-- Ver candidatos creados hoy
SELECT COUNT(*) FROM candidato 
WHERE DATE(fecha_registro) = CURRENT_DATE;

-- Ver evaluaciones completadas
SELECT COUNT(*) FROM score_candidata 
WHERE DATE(fecha_calculo) = CURRENT_DATE;

-- Ver sincronizaciones a CRM
SELECT COUNT(*) FROM auditlog 
WHERE evento = 'candidato.creado' 
AND DATE(fecha) = CURRENT_DATE;
```

---

## 🔧 PASO 4.8: Troubleshooting en Producción

### Error: "502 Bad Gateway"

**Causa:** Backend está caído o no responde

**Solución:**
```bash
# Ver logs
railway logs -f

# Buscar ERROR
railway logs | grep ERROR

# Si hay error de conexión a BD:
# → Railway → PostgreSQL → Verificar estado

# Reiniciar
railway restart
```

### Error: "CORS error" en Frontend

**Causa:** Backend no tiene CORS configurado

**Solución:**
```python
# En api.py, verificar:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-frontend.vercel.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Luego:
```bash
git push  # Railway redeploy automático
```

### Error: "HUBSPOT_API_KEY no configurada"

**Solución:**
```bash
# Railway Dashboard → Variables
# Verificar que HUBSPOT_API_KEY existe
# Si no, agregar:
HUBSPOT_API_KEY = pat-na1-xxxxxxxxxxxxx

# Redeploy
railway restart
```

### Error: "Email no se envía"

**Verificar:**
```bash
# Logs
railway logs | grep "Enviando email"

# Si sale error de autenticación:
# → SMTP_PASSWORD es incorrecto
# → Regenerar en Gmail

# Si sale "timeout":
# → Puerto SMTP incorrecto
# → Debe ser 587 (TLS)
```

### Error: "Candidato no se sincroniza a HubSpot"

**Verificar:**
```bash
# Logs
railway logs | grep "Sincronizando"

# Si sale error 401:
# → API key inválida o expirada
# → Regenerar en HubSpot

# Si sale error 429:
# → Rate limit de HubSpot
# → Esperar 1 hora
```

---

## 📈 PASO 4.9: Métricas y KPIs

### Dashboard de Monitoreo

Crear en Google Sheets o Looker Studio:

```
Candidatos por día:
├─ Día 1: 5 candidatos
├─ Día 2: 8 candidatos
├─ Día 3: 12 candidatos
└─ Total: 25 candidatos

Evaluaciones completadas:
├─ Totales: 22 (88%)
├─ Prioritarios: 8 (32%)
├─ Viables: 10 (40%)
└─ Otros: 4 (16%)

Sincronizaciones a CRM:
├─ Exitosas: 25 (100%)
├─ Fallidas: 0
└─ Pendientes: 0

Emails enviados:
├─ Exitosos: 22 (100%)
├─ Fallidos: 0
└─ Rebote: 0

Tiempo promedio respuesta API:
└─ 250ms (bien < 1000ms)
```

### Comandos útiles

```bash
# Ver candidatos en BD
psql $DATABASE_URL -c "SELECT COUNT(*) FROM candidato;"

# Ver evaluaciones
psql $DATABASE_URL -c "SELECT COUNT(*) FROM score_candidata;"

# Ver errores
railway logs | grep -i error | tail -20

# Ver eventos de CRM
railway logs | grep "EVENTO"
```

---

## ✅ PASO 4.10: Checklist Final

- [ ] Backend deployado en Railway
- [ ] Frontend deployado en Vercel/Netlify
- [ ] Database PostgreSQL conectada
- [ ] HubSpot API key configurada
- [ ] Gmail app password configurado
- [ ] CORS configurado correctamente
- [ ] Test 1: Health check pasa
- [ ] Test 2: Frontend carga
- [ ] Test 3: Flujo de candidato completo funciona
- [ ] Test 4: Candidato aparece en HubSpot
- [ ] Test 5: Email se recibe correctamente
- [ ] Logs sin errores
- [ ] Métricas se muestran normales
- [ ] Dominios configurados (opcional)
- [ ] Alertas configuradas
- [ ] Documentación actualizada
- [ ] Equipo notificado
- [ ] Listo para recibir candidatos reales

---

## 🎯 URLS FINALES DE PRODUCCIÓN

```
Frontend:
├─ Vercel: https://cenerh-recruit-os-frontend.vercel.app
├─ Personalizado: https://app.cenerhconsulting.com (si tienes dominio)
└─ Acceso: Candidatos se registran aquí

Backend API:
├─ Railway: https://tu-proyecto.up.railway.app
├─ Personalizado: https://api.cenerhconsulting.com (si tienes dominio)
├─ Health: https://tu-api.up.railway.app/health
├─ Docs: https://tu-api.up.railway.app/docs
└─ CRM Status: https://tu-api.up.railway.app/api/crm/status

Base de Datos:
├─ PostgreSQL en Railway
├─ Automáticamente escalada
└─ Backups automáticos

Monitoreo:
├─ Railway Dashboard
├─ Logs en tiempo real
├─ Métricas de CPU/Memory
└─ Error tracking
```

---

## 🚨 RESPONSABILIDADES POST-DEPLOYMENT

### Diarias

- [ ] Revisar logs de errores
- [ ] Verificar métricas de CPU/Memory
- [ ] Contar nuevos candidatos

### Semanales

- [ ] Generar reporte de candidatos
- [ ] Revisar sincronizaciones a CRM
- [ ] Validar emails enviados

### Mensuales

- [ ] Optimizar base de datos
- [ ] Revisar usage de Railway
- [ ] Actualizar documentación
- [ ] Backup manual de datos críticos

---

## 🎉 ¡SISTEMA EN VIVO!

Después del deploy:

✅ Candidatos pueden registrarse  
✅ Completar evaluaciones  
✅ Recibir PDF con resultados  
✅ Aparecer automáticamente en HubSpot  
✅ CENERH cierra candidatos desde CRM  

**Tu sistema está 100% operacional y listo para escalar.**

---

## 📞 LINKS ÚTILES

Railway: https://railway.app  
Vercel: https://vercel.com  
HubSpot: https://www.hubspot.com  
GitHub: https://github.com  
PostgreSQL: https://www.postgresql.org  
FastAPI: https://fastapi.tiangolo.com  
React: https://react.dev  

---

## 🏆 PROYECTO COMPLETADO

**CENERH RECRUIT OS v1.0**

Sistema de evaluación psicométrica y selección de candidatos con:

✅ Backend API profesional (FastAPI)  
✅ Frontend moderno (React)  
✅ Base de datos escalable (PostgreSQL)  
✅ Integración CRM (HubSpot)  
✅ Email automation  
✅ PDF generation  
✅ Webhooks automáticos  
✅ Auditoría completa  
✅ Monitoreo en vivo  
✅ Escalabilidad ilimitada  

**Tiempo total: ~6 horas**  
**Resultado: Sistema completamente operacional**  
**Costo: Gratuito (excepto dominios personalizados)**

---

## 🚀 PROXIMOS PASOS (FASE 2)

### Mejoras a corto plazo (1-3 meses)

- Integración con Google Calendar (agendar entrevistas)
- Dashboard de análisis más avanzado
- Sistema de reportería
- Integración con Slack
- API pública para partners

### Mejoras a mediano plazo (3-6 meses)

- Módulo de capacitación (training)
- Assessment 360 grados
- Análisis de competencias por industria
- Integración con ATS (Applicant Tracking System)
- Mobile app nativa

### Visión a largo plazo (6+ meses)

- Producto SaaS "CENERH Recruit OS" para headhunters independientes
- Marketplace de evaluaciones
- IA predictiva de rotación
- Integración con Salesforce
- Certificación internacional

---

## 💡 TIPS PARA MANTENER SISTEMA ACTIVO

1. **Revisar logs regularmente** - Evita sorpresas
2. **Hacer backups manuales** - Seguridad de datos
3. **Actualizar dependencias** - Security patches
4. **Monitorear costos** - Railway tiene tier gratuito generoso
5. **Validar integraciones** - HubSpot sync está funcionando
6. **Documentar cambios** - Facilita el mantenimiento
7. **Entrenar al equipo** - Asegurar uso correcto
8. **Recolectar feedback** - De candidatos y CENERH

---

## ✨ ¡FELICIDADES!

Has completado el proyecto **CENERH RECRUIT OS** de principio a fin.

Tu sistema está:
- ✅ Deployado en producción
- ✅ Conectado a HubSpot
- ✅ Enviando emails automáticamente
- ✅ Listo para candidatos reales
- ✅ Monitorizado en vivo
- ✅ Escalable sin límites

**Ahora es momento de:**

1. 📢 Promocionar tu plataforma
2. 📧 Invitar a clientes a probarla
3. 📊 Recopilar feedback
4. 🚀 Iterar y mejorar
5. 💰 Convertir en ingresos

**¡Tu plataforma está lista para transformar la forma en que CENERH selecciona talento!**
