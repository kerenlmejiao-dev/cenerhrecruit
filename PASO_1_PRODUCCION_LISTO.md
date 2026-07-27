# ✅ PASO 1: DEPLOY A PRODUCCIÓN - LISTO

**Status:** 🚀 Configuración lista para producción  
**Tiempo:** 45 minutos para completar  
**Resultado:** API viva en internet

---

## 📦 ARCHIVOS CREADOS

```
✅ Procfile                 - Configuración para Railway/Heroku
✅ .env.production          - Variables de entorno para producción
✅ requirements.txt         - Dependencias actualizadas
✅ init_db.py              - Script para inicializar BD
✅ DEPLOY_GUIA.md          - Guía paso a paso (LEER ESTO PRIMERO)
```

---

## 🚀 OPCIÓN RECOMENDADA: RAILWAY

Railway es la más fácil. Pasos rápidos:

### 1. Crear repo Git

```bash
cd /home/claude
git init
git add .
git commit -m "Initial commit - CENERH RECRUIT OS"
git remote add origin https://github.com/TU_USUARIO/cenerh-recruit-os.git
git branch -M main
git push -u origin main
```

### 2. Crear cuenta Railway

- Ir a https://railway.app
- Sign up con GitHub
- Autorizar Railway

### 3. Deploy automático

- Ir a https://railway.app/dashboard
- New Project
- Deploy from GitHub
- Seleccionar repo `cenerh-recruit-os`
- Railway hace el resto automáticamente ✨

### 4. Configurar BD y Email

En Railway dashboard:
- Variables → Agregar DATABASE_URL (PostgreSQL automático)
- Variables → Agregar SMTP_* variables

### 5. ¡Listo!

Tu API está en: `https://tu-proyecto.up.railway.app`  
Docs en: `https://tu-proyecto.up.railway.app/docs`

---

## 📋 CHECKLIST RÁPIDO

- [ ] Crear repo GitHub
- [ ] Instalar Git (si no lo tienes)
- [ ] Crear cuenta Railway (2 min)
- [ ] Conectar repo (1 min)
- [ ] Agregar PostgreSQL (1 min)
- [ ] Configurar variables (5 min)
- [ ] Verificar que funciona (2 min)

**Total: 15 minutos si vas rápido**

---

## 🔍 VERIFICAR QUE FUNCIONA

Una vez desplegado:

```bash
# Test 1: Health check
curl https://tu-api.com/health

# Test 2: Ver documentación
# Abrir en navegador: https://tu-api.com/docs

# Test 3: Crear candidato
curl -X POST https://tu-api.com/api/candidatos \
  -H "Content-Type: application/json" \
  -d '{
    "vacante_id": "contador_paraiso",
    "nombre": "Test Candidato",
    "email": "test@example.com"
  }'
```

---

## 💾 ARCHIVO .env.production

Cambiar estos valores:

```
SMTP_USER=tu-email-real@gmail.com
SMTP_PASSWORD=tu-app-password-de-gmail
CORS_ORIGINS=["https://tudominio.com"]
FRONTEND_URL=https://tudominio.com
```

---

## 🎯 VARIABLES A CONFIGURAR EN RAILWAY

Después de crear proyecto en Railway:

```
DATABASE_URL          = (Railway agrega automático con PostgreSQL)
SMTP_SERVER           = smtp.gmail.com
SMTP_PORT             = 587
SMTP_USER             = tu-email@gmail.com
SMTP_PASSWORD         = tu-app-password-gmail
SMTP_FROM_EMAIL       = reportes@cenerhconsulting.com
SMTP_FROM_NAME        = CENERH Consulting
API_ENV               = production
API_DEBUG             = false
CORS_ORIGINS          = ["https://tudominio.com"]
FRONTEND_URL          = https://tudominio.com
```

---

## 🔐 OBTENER APP PASSWORD DE GMAIL

1. Ir a https://myaccount.google.com
2. Security → 2-Step Verification (activar si no lo está)
3. App passwords
4. Seleccionar Mail + Windows
5. Copiar contraseña generada
6. Usar como SMTP_PASSWORD

---

## 📊 DESPUÉS DEL DEPLOY

### ¿Cómo se ve?

```
Dashboard Railway:
├─ Deployments (historial)
├─ Logs (en tiempo real)
├─ Variables (configuración)
├─ Domains (URLs públicas)
└─ Metrics (uso de recursos)

Tu API:
├─ Health: https://tu-api.com/health
├─ Docs: https://tu-api.com/docs (Swagger interactivo)
├─ OpenAPI: https://tu-api.com/openapi.json
└─ Endpoints: todos funcionando en internet
```

### Próximas actualizaciones

```bash
# Hacer cambios local
git add .
git commit -m "Add feature X"
git push

# Railway automáticamente redeploy
# (en 1-2 minutos)
```

---

## ⚠️ COMÚN: ERRORES Y SOLUCIONES

### Error: "Railway can't find Procfile"

✅ Solución: Procfile debe estar en raíz del proyecto (ya creado)

### Error: "ModuleNotFoundError"

✅ Solución: requirements.txt está incompleto (ya actualizado)

### Error: "Database connection failed"

✅ Solución: 
1. Agregar PostgreSQL plugin en Railway
2. Esperar 2 min a que se cree
3. Redeploy el proyecto

### Error: "SMTP authentication failed"

✅ Solución:
1. Verificar que SMTP_PASSWORD es app-password (no contraseña normal)
2. Verificar que 2-step verification está activado en Gmail
3. Probar credenciales localmente primero

---

## 📞 URLs DESPUÉS DE DEPLOY

Una vez hecho el deploy, tendrás:

```
🔗 API Base: https://mi-proyecto.up.railway.app

Endpoints vivos:
✅ GET https://mi-proyecto.up.railway.app/health
✅ GET https://mi-proyecto.up.railway.app/api/tests/disponibles
✅ POST https://mi-proyecto.up.railway.app/api/candidatos
✅ GET https://mi-proyecto.up.railway.app/api/candidatos/{id}/ficha.pdf
✅ POST https://mi-proyecto.up.railway.app/api/candidatos/{id}/email
... y 5 más

📚 Documentación:
https://mi-proyecto.up.railway.app/docs
(Swagger UI interactivo - prueba endpoints desde aquí)
```

---

## ✨ LO QUE GANASTE

✅ API en internet (no en localhost)  
✅ URL pública (puedes compartirla)  
✅ Base de datos PostgreSQL (producción)  
✅ Email automation (listo para enviar)  
✅ SSL/HTTPS (automático)  
✅ Escalabilidad ilimitada  
✅ Monitoreo en vivo  
✅ Deploy automático con Git  

---

## 🚀 PRÓXIMO PASO

Una vez que tu API está en producción:

**PASO 2:** Crear Frontend (React)

Esto permitirá que:
- Candidatos usen interfaz web
- Vean resultados en tiempo real
- Descarguen PDFs
- Reciban emails automáticos

Tiempo: ~2 horas

¿Listo?

