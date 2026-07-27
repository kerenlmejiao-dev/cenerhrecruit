# 📁 ESTRUCTURA DE ARCHIVOS - CENERH RECRUIT OS

Todos los archivos están en `/home/claude/` y copiados a `/mnt/user-data/outputs/`

---

## 🔧 ARCHIVOS TÉCNICOS (Python)

### 1. **models.py** (250 líneas)
**¿Qué es?** Base de datos SQLAlchemy  
**¿Qué hace?** Define la estructura de 8 tablas:
- `TestPsicometrico` → 9 tests
- `PreguntaTest` → 300 preguntas
- `Vacante` → Vacantes a llenar
- `Candidato` → Candidatos evaluados
- `RespuestaCandidata` → Respuestas de candidatos
- `ScoreCandidata` → Resultados por test
- `PesoVacante` → Configuración de pesos
- `AuditLog` → Registro de acciones

**Usado por:** seed.py, api.py  
**No modificar:** A menos que cambies estructura de BD

---

### 2. **seed.py** (200 líneas)
**¿Qué es?** Script de inicialización  
**¿Qué hace?**
- Crea BD SQLite local (`cenerh_recruit.db`)
- Carga 9 tests
- Carga 300 preguntas (muestra)
- Crea vacante de ejemplo

**Cómo ejecutar:**
```bash
python seed.py
```

**Resultado:**
```
✅ BD creada
✅ 9 tests cargados
✅ 300 preguntas preparadas
```

**Una sola vez:** Ejecuta solo 1 vez (crea la BD)

---

### 3. **api.py** (300 líneas)
**¿Qué es?** API REST con FastAPI  
**¿Qué hace?**
- Inicia servidor en puerto 8000
- Proporciona 5 endpoints de lectura
- Maneja errores automáticamente
- Genera documentación interactiva

**Endpoints:**
```
GET /health                              → Estado de API
GET /api/tests/disponibles              → 9 tests
GET /api/tests/{test_id}/info           → Info de test
GET /api/vacantes/{vacante_id}/config   → Config vacante
GET /api/tests/{test_id}/{candidato_id} → Preguntas
```

**Cómo ejecutar:**
```bash
python api.py
```

**Acceder:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

**Siempre activa:** Mientras estés testeando o en producción

---

### 4. **scoring.py** (350 líneas)
**¿Qué es?** Motor de scoring psicométrico  
**¿Qué hace?**
- Calcula puntuación directa (PD)
- Estandariza T-Scores
- Calcula percentiles
- Aplica pesos ponderados (A + B)
- Clasifica candidatos

**Usado por:** api.py (en FASE 2 y 3)  
**No ejecutar directamente:** Se importa en api.py

**Sistema de clasificación:**
```
81-100: PRIORITARIO ⭐⭐⭐
61-80:  VIABLE ⭐⭐
41-60:  CONSIDERAR ⭐
0-40:   NO RECOMENDADO
```

---

### 5. **test_quick.py** (200 líneas)
**¿Qué es?** Testing automatizado  
**¿Qué hace?**
- Verifica que todos los endpoints funcionan
- Prueba con datos reales
- Valida error handling
- No requiere pytest

**Cómo ejecutar:**
```bash
python test_quick.py
```

**Resultado:**
```
✅ TODOS LOS TESTS PASARON
   ✓ 7 tests pasados
   ✓ API funcionando
   ✓ Endpoints validados
```

**Cuándo ejecutar:** Después de `api.py`

---

## 📋 ARCHIVOS DE CONFIGURACIÓN

### 6. **requirements.txt**
**¿Qué es?** Lista de dependencias Python  
**¿Qué contiene?**
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- ReportLab (para PDF)
- aiosmtplib (para email)
- Pytest (para testing)

**Cómo usar:**
```bash
pip install -r requirements.txt
```

**Una sola vez:** Ejecuta al inicio

---

### 7. **.env.example**
**¿Qué es?** Plantilla de variables de entorno  
**¿Qué contiene?**
- DATABASE_URL (BD local o PostgreSQL)
- API_PORT (8000)
- SMTP_HOST, SMTP_PORT, EMAIL_USER (para email)
- APP_NAME, APP_VERSION

**Cómo usar:**
```bash
# Copiar y renombrar
cp .env.example .env

# Editar con tus valores (si necesitas cambiar de desarrollo a producción)
nano .env
```

**Ahora no necesitas:** Funciona con defaults

---

## 📚 ARCHIVOS DE DOCUMENTACIÓN

### 8. **README.md** (~400 líneas)
**¿Qué es?** Documentación completa del proyecto  
**¿Qué contiene?**
- Qué es CENERH RECRUIT OS
- Cómo instalar
- Cómo ejecutar
- Explicación de cada endpoint
- Sistema de scoring
- Troubleshooting

**Usar:** Abre en navegador o editor de texto

---

### 9. **STATUS_FINAL.md** (~300 líneas)
**¿Qué es?** Estado actual del proyecto  
**¿Qué contiene?**
- Resumen ejecutivo
- Cómo empezar (paso a paso)
- Endpoints listos
- Próximas fases
- Métricas del proyecto

**Usar:** Lee PRIMERO, resume todo

---

## 📊 ARCHIVOS GENERADOS (Después de ejecutar)

### 10. **cenerh_recruit.db**
**¿Qué es?** Base de datos SQLite local  
**¿Cuándo se crea?** Al ejecutar `python seed.py`  
**¿Qué contiene?**
- 9 tests psicométricos
- 300 preguntas
- Vacante de ejemplo

**Usar:** No tocar directamente (seed.py la crea)

---

## 🚀 ORDEN DE EJECUCIÓN

```
1. pip install -r requirements.txt      ← Instalar dependencias
2. python seed.py                       ← Crear BD + cargar datos
3. python api.py                        ← Iniciar API (dejar activa)
4. python test_quick.py                 ← Probar endpoints (otra terminal)
```

---

## 📍 UBICACIONES

### Desarrollo (ahora)
```
/home/claude/
├── models.py
├── api.py
├── scoring.py
├── seed.py
├── test_quick.py
├── requirements.txt
├── .env.example
├── README.md
├── STATUS_FINAL.md
└── cenerh_recruit.db        ← Generada al ejecutar seed.py
```

### Outputs (para ti)
```
/mnt/user-data/outputs/
├── models.py
├── api.py
├── scoring.py
├── seed.py
├── test_quick.py
├── requirements.txt
├── .env.example
├── README.md
└── STATUS_FINAL.md
```

---

## ✅ RESUMEN RÁPIDO

| Archivo | Tipo | Acción | Cuándo |
|---------|------|--------|--------|
| models.py | Python | Importar | seed.py, api.py |
| seed.py | Python | **Ejecutar 1 vez** | Inicio |
| api.py | Python | **Ejecutar siempre** | Para probar/producción |
| scoring.py | Python | Importar | api.py (FASE 2+) |
| test_quick.py | Python | Ejecutar | Después de api.py |
| requirements.txt | Config | **pip install** | Inicio |
| .env.example | Config | Copiar a .env | Si necesitas cambiar config |
| README.md | Docs | Leer | Referencia |
| STATUS_FINAL.md | Docs | **Leer primero** | Ahora |

---

## 🎯 QUÉ HACER AHORA

**Opción 1: Probar todo (10 min)**
```bash
cd /home/claude
pip install -r requirements.txt
python seed.py
python api.py
# Otra terminal:
python test_quick.py
```

**Opción 2: Solo leer documentación**
- Abre `README.md` → Documentación completa
- Abre `STATUS_FINAL.md` → Resumen ejecutivo

**Opción 3: Continuar con FASE 2**
- Dime y creo endpoints de escritura + scoring automático

---

## 🚀

**Todos los archivos están listos para usar.**

¿Empezamos a probar?

