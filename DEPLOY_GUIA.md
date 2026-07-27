# 🚀 GUÍA DE DEPLOY - CENERH RECRUIT OS

**Objetivo:** Poner tu API en producción en internet  
**Tiempo:** 45 minutos  
**Costo:** $7-35/mes (depende de la plataforma)

---

## 🎯 OPCIÓN 1: RAILWAY (RECOMENDADO) ⭐

Railway es la más fácil y moderna. Pasos:

### Paso 1: Crear cuenta en Railway

1. Ir a https://railway.app
2. Sign up con GitHub (es lo más fácil)
3. Autorizar Railway en tu cuenta GitHub

### Paso 2: Conectar repositorio Git

```bash
# 1. En tu proyecto, crear repo git
cd /home/claude
git init
git add .
git commit -m "Initial commit - CENERH RECRUIT OS"

# 2. Crear repo en GitHub
# (ir a github.com, crear nuevo repo "cenerh-recruit-os")

# 3. Conectar local con GitHub
git remote add origin https://github.com/TU_USUARIO/cenerh-recruit-os.git
git branch -M main
git push -u origin main
```

### Paso 3: Crear proyecto en Railway

1. Ir a https://railway.app/dashboard
2. Click en "New Project"
3. Seleccionar "Deploy from GitHub"
4. Seleccionar tu repo "cenerh-recruit-os"
5. Click "Deploy"

Railway detectará automáticamente que es un proyecto Python.

### Paso 4: Configurar variables de entorno

En la dashboard de Railway:

1. Click en "Variables"
2. Agregar las siguientes variables:

```
DATABASE_URL = postgresql://...
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
SMTP_USER = tu-email@cenerh.com
SMTP_PASSWORD = tu-app-password
API_ENV = production
API_DEBUG = false
```

### Paso 5: Agregar base de datos PostgreSQL

En Railway dashboard:

1. Click en "New Service"
2. Seleccionar "PostgreSQL"
3. Click "Create"
4. Railway agregará automáticamente DATABASE_URL

### Paso 6: Deploy automático

¡Listo! Cada vez que hagas `git push`, Railway despliega automáticamente.

```bash
# Para actualizar en producción:
git add .
git commit -m "Update features"
git push
```

### Paso 7: Obtener URL pública

En Railway dashboard:
- Tu API está en: `https://tu-proyecto-railway.up.railway.app`
- API Docs: `https://tu-proyecto-railway.up.railway.app/docs`

---

## 🎯 OPCIÓN 2: HEROKU

### Paso 1: Instalar Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Descargar desde https://devcenter.heroku.com/articles/heroku-cli
```

### Paso 2: Login en Heroku

```bash
heroku login
# Se abrirá navegador para autenticar
```

### Paso 3: Crear app

```bash
cd /home/claude
heroku create cenerh-recruit-os
```

### Paso 4: Agregar PostgreSQL

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### Paso 4: Configurar variables

```bash
heroku config:set DATABASE_URL=postgresql://...
heroku config:set SMTP_SERVER=smtp.gmail.com
heroku config:set SMTP_USER=tu-email@cenerh.com
heroku config:set SMTP_PASSWORD=tu-password
```

### Paso 5: Deploy

```bash
git push heroku main
```

### Paso 6: Ver URL

```bash
heroku open
# Tu API está en: https://cenerh-recruit-os.herokuapp.com
```

---

## 🎯 OPCIÓN 3: RENDER

### Paso 1: Ir a https://render.com

1. Sign up
2. Connect GitHub
3. New Web Service
4. Select tu repo

### Paso 2: Configurar

- Name: `cenerh-recruit-os`
- Runtime: `Python 3.11`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

### Paso 3: Agregar PostgreSQL

- New PostgreSQL
- Conectar a tu app

### Paso 4: Deploy

Render hace deploy automático. Tu API está en: `https://cenerh-recruit-os.onrender.com`

---

## ✅ DESPUÉS DEL DEPLOY

Una vez que tu API está en producción:

### 1. Verificar que funciona

```bash
# Reemplazar URL con tu dominio
curl https://tu-api.com/health

# Response esperado:
# {"status": "ok"}
```

### 2. Ver documentación

Ir a: `https://tu-api.com/docs`

Verás todos los endpoints listos para usar.

### 3. Configurar dominio personalizado

Si usas Railway/Heroku/Render, puedes agregar tu dominio:

- Ir a configuración del servicio
- Custom Domain
- Agregar: `api.cenerhconsulting.com`
- Configurar DNS (CNAME o A record)

### 4. Habilitar SSL/HTTPS

Automático en todas las plataformas (Let's Encrypt)

### 5. Monitoreo

Configurar alertas en caso de caídas:
- Email cuando API no responde
- Logs centralizados
- Métricas de uso

---

## 📊 COMPARATIVA PLATAFORMAS

| Aspecto | Railway | Heroku | Render |
|---------|---------|--------|--------|
| Facilidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Precio | $7-50/mes | $7-50/mes | $7-50/mes |
| PostgreSQL | Incluido | Extra | Incluido |
| SSL | ✅ Gratis | ✅ Gratis | ✅ Gratis |
| Deploy | Git push | Git push | Git push |
| Escalabilidad | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Recomendación:** Railway (mejor UX, más rápido, más barato)

---

## 🔐 SEGURIDAD EN PRODUCCIÓN

### 1. Cambiar credenciales

```bash
# Generar SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Agregar a variables de entorno
heroku config:set SECRET_KEY=tu-nueva-key
```

### 2. Habilitar HTTPS

Automático en todas las plataformas.

### 3. Rate limiting

```python
# En api.py (agregar después de importes)
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### 4. Logging y auditoría

Los logs están en:
- Railway: Dashboard → Logs
- Heroku: `heroku logs --tail`
- Render: Dashboard → Logs

### 5. Monitoreo con Sentry (opcional)

```bash
# Crear cuenta en https://sentry.io
# Agregar DSN:
heroku config:set SENTRY_DSN=https://...
```

---

## 🚨 TROUBLESHOOTING

### "Application error"

```bash
# Ver logs
heroku logs --tail

# Reiniciar
heroku restart
```

### "Database connection error"

```bash
# Verificar DATABASE_URL
heroku config:get DATABASE_URL

# Reconectar BD
heroku addons:destroy heroku-postgresql
heroku addons:create heroku-postgresql:hobby-dev
```

### "Port already in use"

El puerto debe ser 8000 (desarrollo) o $PORT (producción).

```python
# En api.py
import os
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## ✅ CHECKLIST FINAL

- [ ] Crear repo en GitHub
- [ ] Elegir plataforma (Railway recomendado)
- [ ] Conectar repo
- [ ] Agregar PostgreSQL
- [ ] Configurar variables de entorno
- [ ] Hacer deploy
- [ ] Verificar que API responde
- [ ] Ver documentación en /docs
- [ ] Configurar dominio personalizado (opcional)
- [ ] Habilitar SSL (automático)
- [ ] Configurar logging
- [ ] Configurar backups de BD

---

## 📞 URLS DESPUÉS DE DEPLOY

**Railway:**
```
API: https://tu-proyecto.up.railway.app
Docs: https://tu-proyecto.up.railway.app/docs
```

**Heroku:**
```
API: https://tu-app.herokuapp.com
Docs: https://tu-app.herokuapp.com/docs
```

**Render:**
```
API: https://tu-app.onrender.com
Docs: https://tu-app.onrender.com/docs
```

---

## 🎉 ¡LISTO!

Tu API está viva en internet. Ahora puedes:

1. ✅ Compartir la URL con clientes
2. ✅ Integrar con frontend
3. ✅ Recibir solicitudes de candidatos
4. ✅ Generar reportes automáticos

**Próximo paso:** Crear Frontend (PASO 2)

