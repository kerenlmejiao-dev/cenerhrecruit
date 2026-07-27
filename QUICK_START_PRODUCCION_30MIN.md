# ⚡ QUICK START: DEPLOY EN 30 MINUTOS

**Para personas impacientes que quieren ir RÁPIDO a producción**

---

## 🎯 OBJETIVO

Poner CENERH RECRUIT OS en producción completo en 30 minutos.

**Requisitos previos:**
- Cuenta GitHub (gratuita)
- Cuenta HubSpot (gratuita)
- Email Gmail
- 30 minutos

---

## ⏱️ CRONOGRAMA

```
Minutos 0-5:    Preparar repositorio
Minutos 5-10:   Deploy backend en Railway
Minutos 10-15:  Deploy frontend en Vercel
Minutos 15-25:  Configurar variables
Minutos 25-30:  Tests rápidos
```

---

## 🚀 PASO 1: GITHUB (5 minutos)

### 1.1 Crear repositorio

```bash
cd /home/claude

# Inicializar Git
git init
git add .
git commit -m "CENERH RECRUIT OS - Initial commit"
```

### 1.2 Crear repo en GitHub

1. Ir a https://github.com/new
2. Nombre: `cenerh-recruit-os`
3. Descripción: "Sistema de evaluación psicométrica"
4. Public
5. Click "Create repository"

### 1.3 Subir código

```bash
git remote add origin https://github.com/TU_USUARIO/cenerh-recruit-os.git
git branch -M main
git push -u origin main
```

✅ **Código en GitHub en 5 minutos**

---

## 🚀 PASO 2: RAILWAY BACKEND (5 minutos)

### 2.1 Crear proyecto

1. Ir a https://railway.app/login
2. Sign up con GitHub (autorizar)
3. Dashboard → "+ New Project"
4. "Deploy from GitHub" → Seleccionar repo
5. Railway automáticamente:
   - Detecta Python
   - Instala dependencias
   - Crea Procfile
   - Deploy automático

### 2.2 Agregar PostgreSQL

1. Railway Dashboard
2. "+ Add Service"
3. Seleccionar "PostgreSQL"
4. Click "Add"
5. Railway agrega `DATABASE_URL` automático

### 2.3 Configurar variables (30 segundos cada una)

Ir a: Project → Variables → Raw Editor

Pegar (cambiar valores según tu caso):

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
SMTP_FROM_EMAIL=reportes@cenerhconsulting.com
HUBSPOT_API_KEY=pat-na1-xxxxxxxxxxxxx
API_ENV=production
API_DEBUG=false
CORS_ORIGINS=["https://tuapp.vercel.app", "http://localhost:5173"]
```

✅ **Backend en Railway en 5 minutos**

---

## 🎨 PASO 3: VERCEL FRONTEND (5 minutos)

### 3.1 Deploy automático

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login
# Se abre navegador para autorizar con GitHub
```

### 3.2 Crear proyecto en Vercel

```bash
cd frontend
vercel --prod
```

Preguntas (deja defaults):
- Project name: `cenerh-recruit-os-frontend`
- Framework: React
- Build: `npm run build`
- Output: `dist`

### 3.3 Obtener URL

```bash
# Después del deploy:
# Tu app está en: https://cenerh-recruit-os-frontend.vercel.app
```

✅ **Frontend en Vercel en 5 minutos**

---

## ⚙️ PASO 4: VARIABLES FINAL (10 minutos)

### 4.1 Conseguir API key HubSpot (3 minutos)

1. Ir a https://app.hubspot.com
2. Settings (arriba derecha) → Account defaults
3. Private app access → Create app
4. Nombre: "CENERH Recruit OS"
5. Scopes: Activar todos los `contacts` y `deals`
6. Create → Copiar token
7. Agregar en Railway: `HUBSPOT_API_KEY=pat-na1-xxx`

### 4.2 Gmail App Password (3 minutos)

1. Gmail: https://myaccount.google.com/security
2. 2-Step Verification (activar si no está)
3. App passwords
4. Mail + Windows → Generar
5. Copiar contraseña
6. Railway: `SMTP_PASSWORD=xxxxxxxx`

### 4.3 VITE_API_URL en Vercel (2 minutos)

1. Vercel Dashboard → Project
2. Settings → Environment Variables
3. Agregar:
   - Key: `VITE_API_URL`
   - Value: `https://tu-proyecto.up.railway.app`
4. Click "Save"

### 4.4 Redeploy (2 minutos)

```bash
# Railway redeploy automático después de cambiar variables
# Vercel redeploy manual:
vercel --prod
```

✅ **Variables configuradas en 10 minutos**

---

## ✅ PASO 5: TESTS RÁPIDOS (5 minutos)

### 5.1 Backend funciona

```bash
# Test 1: Health check
curl https://tu-proyecto.up.railway.app/health
# Response: {"status": "ok"}

# Test 2: CRM conectado
curl https://tu-proyecto.up.railway.app/api/crm/status
# Response: {"hubspot": {"configurado": true}}
```

### 5.2 Frontend funciona

```bash
# Abre en navegador
https://cenerh-recruit-os-frontend.vercel.app

# Verificar:
✅ Página de registro carga
✅ Formulario funciona
✅ Botón "Comenzar" clickeable
```

### 5.3 Flujo completo (2 minutos)

1. Abrir frontend
2. Completar registro con datos de prueba
3. Responder 2-3 preguntas
4. Ver resultados
5. Verificar en HubSpot que apareció el contacto

✅ **Tests listos en 5 minutos**

---

## 🎉 LISTO!

**Tiempo total: 30 minutos**

Tu sistema está en producción con:

✅ Backend API en Railway  
✅ Frontend en Vercel  
✅ Database PostgreSQL  
✅ HubSpot sincronizado  
✅ Emails configurados  
✅ Monitoreo activo  

---

## 📍 URLS FINALES

```
Frontend:  https://cenerh-recruit-os-frontend.vercel.app
Backend:   https://tu-proyecto.up.railway.app
API Docs:  https://tu-proyecto.up.railway.app/docs
Status:    https://tu-proyecto.up.railway.app/health
```

---

## 🔧 SI ALGO NO FUNCIONA

### Error: "Módulos no encontrados"

```bash
# En Railway, revisar logs:
# Dashboard → Logs → Buscar "ERROR"

# Solución: Asegurar que requirements.txt incluye httpx
echo "httpx==0.25.2" >> requirements.txt
git push  # Railway redeploy automático
```

### Error: "CORS error"

```bash
# Vercel: Settings → Environment Variables
# Agregar VITE_API_URL correctamente
vercel env pull  # Descargar variables
vercel --prod    # Redeploy
```

### Error: "Candidato no aparece en HubSpot"

```bash
# Railway Logs → Buscar "Sincronizando"
# Si ve error 401: API key incorrecta, regenerar en HubSpot
# Si ve error 429: Rate limit, esperar 1 hora
```

---

## 📞 SOPORTE RÁPIDO

**Railway:** https://railway.app (chat en vivo)  
**Vercel:** https://vercel.com/support  
**HubSpot:** https://app.hubspot.com/help  
**GitHub:** https://github.com/support  

---

## 📊 VERIFICAR QUE TODO FUNCIONA

```bash
# Terminal: Comprobar sincronización
curl https://tu-proyecto.up.railway.app/api/crm/status

# Response esperado:
{
  "hubspot": {
    "configurado": true,
    "estado": "✅ Conectado"
  }
}
```

```bash
# Ver candidatos en sistema
curl https://tu-proyecto.up.railway.app/api/crm/candidatos/hubspot

# Response esperado:
{
  "total_candidatos": 1,
  "en_hubspot": [
    {
      "id": "cand_001",
      "nombre": "Tu Test",
      "email": "test@example.com",
      "score": 85
    }
  ]
}
```

---

## 🚀 PRÓXIMOS PASOS

Después de estos 30 minutos:

1. ✅ Sistema en vivo
2. 📢 Invitar a testers
3. 🐛 Recolectar feedback
4. 🔧 Hacer ajustes
5. 📈 Escalar a producción real

---

## 💡 TIPS DE PRO

1. **Revisar logs regularmente**
   ```bash
   railway logs -f  # Tiempo real
   ```

2. **Hacer git push para actualizar**
   ```bash
   git add .
   git commit -m "Fix: ..."
   git push  # Railway redeploy automático
   ```

3. **Monitorear performance**
   - Railway Dashboard → Metrics
   - Ver CPU, Memory, Requests

4. **Backup de datos**
   ```bash
   # Railway PostgreSQL → Export backup
   ```

---

## ✨ FELICIDADES!

En 30 minutos tienes un sistema profesional, escalable y completamente operacional.

**Tu CENERH RECRUIT OS está VIVO.**

---

**¿Preguntas?**

- Revisar `PASO_4_DEPLOY_PRODUCCION.md` para detalles
- Revisar `CRM_SETUP_GUIA.md` para troubleshooting
- Chat de Railway: https://railway.app

---

**¡A CONQUISTAR EL MERCADO! 🚀**

