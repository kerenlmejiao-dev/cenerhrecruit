# 🚀 CENERH RECRUIT OS

**Platform de Reclutamiento y Evaluación Psicométrica**

---

## 📊 ¿QUÉ ES?

CENERH RECRUIT OS es una plataforma automatizada que:

- ✅ Administra **300 preguntas** distribuidas en **9 tests psicométricos**
- ✅ Calcula **scores automáticos** con sistema de pesos ponderados (A + B)
- ✅ Genera **PDFs de resultados** con perfil psicológico
- ✅ Envía **emails automáticos** a candidatos
- ✅ Permite **configuración manual** de tests por vacante

---

## 🏗️ ESTRUCTURA

```
/cenerh-recruit-os/
├── models.py          # SQLAlchemy models (8 tablas)
├── api.py             # FastAPI endpoints (4 iniciales)
├── scoring.py         # Sistema de scoring ponderado
├── seed.py            # Cargar datos en BD
├── requirements.txt   # Dependencias Python
├── README.md          # Este archivo
├── .env.example       # Variables de entorno (ejemplo)
└── tests/
    └── test_api.py    # Tests unitarios
```

---

## 📋 BASES DE DATOS

### Tablas (8)

```
1. tests_psicometricos     → 9 tests disponibles
2. preguntas_tests         → 300 preguntas
3. vacantes                → Vacantes a llenar
4. candidatos              → Candidatos evaluados
5. respuestas_candidatas   → Respuestas de candidatos
6. scores_candidatas       → Scores por test
7. pesos_vacantes          → Configuración de pesos
8. audit_logs              → Registro de acciones
```

### Conexión (Local)

- **Tipo:** SQLite (desarrollo)
- **Archivo:** `cenerh_recruit.db`
- **Sin credenciales:** Funciona localmente sin configuración

---

## 🚀 INICIO RÁPIDO

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Crear BD y cargar datos

```bash
python seed.py
```

**Output esperado:**
```
📊 Cargando 9 tests...
  ✓ Razonamiento Verbal (20 preg)
  ✓ Razonamiento Numérico (40 preg)
  ✓ Big Five (20 preg)
  ...
✅ Tests cargados

❓ Cargando preguntas...
  ✓ Verbal: 1 preg cargada
  ✓ Atención: 1 preg cargada
  ...
✅ 300 preguntas cargadas

✅ SEED COMPLETADO
```

### 3. Iniciar API

```bash
python api.py
```

**Output esperado:**
```
🚀 Iniciando CENERH RECRUIT OS API
   URL: http://localhost:8000
   Docs: http://localhost:8000/docs
```

### 4. Acceder a la API

- **API:** http://localhost:8000
- **Docs interactivos:** http://localhost:8000/docs
- **Health check:** http://localhost:8000/health

---

## 🔌 ENDPOINTS (FASE 1)

### Lectura (4 endpoints)

#### 1️⃣ GET /api/tests/disponibles
```bash
curl http://localhost:8000/api/tests/disponibles
```

**Response:**
```json
{
  "status": "success",
  "total_tests": 9,
  "total_preguntas": 300,
  "tests": [
    {
      "id": "verbal",
      "nombre": "Razonamiento Verbal",
      "num_preguntas": 20,
      "tipo": "cognitivo",
      "calidad": 94.0
    },
    ...
  ]
}
```

#### 2️⃣ GET /api/tests/{test_id}/info
```bash
curl http://localhost:8000/api/tests/verbal/info
```

#### 3️⃣ GET /api/vacantes/{vacante_id}/config
```bash
curl http://localhost:8000/api/vacantes/contador_paraiso/config
```

#### 4️⃣ GET /api/tests/{test_id}/{candidato_id}
```bash
curl http://localhost:8000/api/tests/verbal/cand_001
```

Retorna lista de 20 preguntas del test verbal listas para responder.

---

## 🎯 TESTS DISPONIBLES (9)

| ID | Nombre | Preguntas | Tipo | Calidad |
|----|--------|-----------|------|---------|
| `verbal` | Razonamiento Verbal | 20 | cognitivo | 94/100 |
| `numerico` | Razonamiento Numérico | 40 | cognitivo | 95/100 |
| `big_five` | Big Five - Personalidad | 20 | psicometrico | 96/100 |
| `ie` | Inteligencia Emocional | 20 | psicometrico | 95/100 |
| `motivacion` | Motivación Laboral | 20 | psicometrico | 98/100 |
| `valores` | Valores Organizacionales | 20 | psicometrico | 94/100 |
| `liderazgo` | Potencial de Liderazgo | 20 | psicometrico | 96/100 |
| `competencias` | Competencias Laborales | 90 | competencias | 99/100 |
| `atencion` | Atención y Concentración | 40 | atencion | 94/100 |

**TOTAL: 300 preguntas**

---

## 📊 SISTEMA DE SCORING

### Opción A: Default (Ponderado)

```
Score Final = (Competencias × 35%) + (Psicométricos × 35%) + (Cognitivos × 30%)
```

**Clasificación:**
- 81-100: **PRIORITARIO** ⭐⭐⭐
- 61-80: **VIABLE** ⭐⭐
- 41-60: **CONSIDERAR** ⭐
- 0-40: **NO RECOMENDADO**

### Opción B: Custom (Por vacante)

Reclutador puede ajustar pesos al crear vacante:
```json
{
  "competencias": 0.40,
  "psicometricos": 0.30,
  "cognitivos": 0.30
}
```

---

## 🔐 CONFIGURACIÓN

### Variables de entorno (.env)

```bash
# Database (desarrollo: SQLite local)
DATABASE_URL=sqlite:///./cenerh_recruit.db

# API
API_HOST=0.0.0.0
API_PORT=8000

# Email (para producción)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=tu-email@gmail.com
EMAIL_PASSWORD=tu-contraseña

# App
ENV=development  # development, production
DEBUG=True
```

---

## 🧪 TESTING

```bash
python -m pytest tests/
```

---

## 📈 PRÓXIMAS FASES

### FASE 2: Endpoints de Escritura
- POST /api/tests/{test_id}/{candidato_id}/respuestas
- Calcular scores automáticamente
- Validar respuestas

### FASE 3: Resultados + PDF
- GET /api/candidatos/{id}/resultados
- GET /api/candidatos/{id}/ficha.pdf
- POST /api/candidatos/{id}/email

### FASE 4: Production
- Cambiar a PostgreSQL
- Email real (SMTP)
- Deploy a Railway/Heroku

---

## 🛠️ PROBLEMAS COMUNES

### "SQLite: database is locked"
```bash
# Reiniciar API
python api.py
```

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### "Port 8000 already in use"
```bash
python api.py --port 8001
```

---

## 📧 CONTACTO

- **Email:** servicios@cenerhconsulting.com
- **WhatsApp:** 829-557-9632
- **Web:** cenerhconsulting.com

---

## 📝 NOTAS

- 🚀 **Desarrollo:** SQLite local (rápido, sin credenciales)
- 🔐 **Producción:** PostgreSQL + SMTP real
- 📊 **Validez:** 95.1/100 promedio en todos los tests
- ⏱️ **Tiempo estimado:** 30-40 minutos por candidato (300 preguntas)

---

**Última actualización:** Domingo 27 de julio de 2026  
**Versión:** 1.0.0 (MVP)  
**Status:** ✅ Desarrollo activo
