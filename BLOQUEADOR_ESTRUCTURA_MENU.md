# 🔥 BATERÍA PSICOMÉTRICA VALIDADA

**Keren acaba de entregar validación técnica profesional de 8 TESTS**

Esto cambia **TODO** lo que teníamos planeado.

---

## 📊 TESTS DISPONIBLES (CON VALIDACIÓN)

| Test | Calidad | Status | Para API |
|------|---------|--------|----------|
| 1. Razonamiento Verbal | 94/100 ✅ | LISTO | ✅ 20 preguntas |
| 2. Razonamiento Numérico | 82/100 ⚠️ | Corregir + mejorar | ✅ 20 preguntas (v1) |
| 3. Atención & Concentración | 55/100 ❌ | RECONSTRUIR COMPLETO | ❌ 9/20 preguntas válidas |
| 4. Big Five (Personalidad) | 96/100 ✅ | LISTO | ✅ 20 preguntas |
| 5. Inteligencia Emocional | 95/100 ✅ | LISTO | ✅ 20 preguntas |
| 6. Motivación Laboral | 98/100 ✅ | LISTO | ✅ 20 preguntas |
| 7. Valores Organizacionales | 94/100 ✅ | LISTO (sin invertidas) | ✅ 20 preguntas |
| 8. Potencial de Liderazgo | 96/100 ✅ | LISTO | ✅ 20 preguntas |
| **BONUS**: 90 preguntas Competencias | (en progreso) | ESTRUCTURADAS | ✅ 18 competencias |
| **BONUS**: 7 Assessments SJT | (en progreso) | DISEÑADOS | ✅ Casos prácticos |

---

## 🔴 DECISIONES CRÍTICAS PARA API

### Decisión 1: Tests a integrar AHORA vs. después

**OPCIÓN A: Lanzar TODO listo**
```
LUNES empiezo con:
- Competencias Likert (90 preg) ✅
- Razonamiento Verbal (20 preg) ✅
- Razonamiento Numérico v1 (20 preg, con correcciones)
- Big Five (20 preg) ✅
- Inteligencia Emocional (20 preg) ✅
- Motivación Laboral (20 preg) ✅
- Valores Organizacionales (20 preg) ✅
- Potencial de Liderazgo (20 preg) ✅
= 210 PREGUNTAS LISTAS

FASE 2 (Septiembre):
- Atención & Concentración (RECONSTRUIDO)
- Razonamiento Numérico (MEJORADO - nivel empresa)
- Assessments SJT (7 casos)
```

**OPCIÓN B: Solo lo imprescindible LUNES**
```
Integrar SOLO:
- Competencias Likert (90 preg)
- Razonamiento Numérico v1

Fase 2: Todo lo demás
```

---

### Decisión 2: ¿ESTRUCTURA DEL MENÚ?

🔴 **PREGUNTA PENDIENTE: ¿Cómo selecciona cada vacante qué tests aplicar?**

**Posibilidad 1: Por tipo de vacante**
```
VACANTE: Diseñador Estructural Junior
├─ Tests automáticos para este rol:
│  ├─ Razonamiento Verbal (lógica)
│  ├─ Razonamiento Numérico v1 (matemática)
│  ├─ Big Five (personalidad)
│  └─ Competencias (18 áreas)
└─ Tests opcionales:
   ├─ Atención & Concentración
   └─ Motivación Laboral

Candidato hace TODO automáticamente.
Score final = promedio ponderado.
```

**Posibilidad 2: Por nivel de puesto**
```
NIVEL OPERATIVO:
├─ Competencias (sí)
├─ Razonamiento Numérico (sí)
├─ Big Five (sí)
└─ Inteligencia Emocional (sí)

NIVEL SUPERVISOR:
├─ Competencias (sí)
├─ Razonamiento Verbal (sí)
├─ Potencial de Liderazgo (sí)
├─ Inteligencia Emocional (sí)
├─ Motivación Laboral (sí)
└─ Big Five (sí)

NIVEL GERENCIAL:
├─ Todo lo anterior +
├─ Valores Organizacionales
├─ Assessments SJT
└─ Razonamiento Numérico (v2 - mejorado)
```

**Posibilidad 3: Configuración manual por vacante**
```
Al crear vacante en CENERH RECRUIT OS:
├─ Nombre vacante
├─ Rol/Nivel
├─ Tests a aplicar: ☑️ Competencias ☑️ Liderazgo ☐ Atención
└─ Pesos: Competencias 40% | Liderazgo 30% | Tests psico 30%

API calcula score final con pesos personalizados.
```

---

## 🗄️ ESTRUCTURA BD NECESARIA

```sql
-- Maestro de Tests disponibles
CREATE TABLE tests (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion VARCHAR(500),
    numero_preguntas INTEGER,
    tiempo_minutos INTEGER,
    calidad_psicometrica FLOAT,  -- 55-98
    estado VARCHAR(20),  -- LISTO, RECONSTRUIR, MEJORA
    tipo VARCHAR(20)  -- PSICOMETRICO, COGNITIVO, COMPETENCIAS, SJT
);

-- Relación: Vacante → Tests
CREATE TABLE vacante_tests (
    id INTEGER PRIMARY KEY,
    vacante_id INTEGER FOREIGN KEY,
    test_id INTEGER FOREIGN KEY,
    obligatorio BOOLEAN,  -- true = obligatorio, false = opcional
    peso_en_score FLOAT,  -- 0.1 - 1.0
    orden_aplicacion INTEGER
);

-- Respuestas del candidato
CREATE TABLE respuestas_candidato (
    id INTEGER PRIMARY KEY,
    candidato_id INTEGER FOREIGN KEY,
    vacante_id INTEGER FOREIGN KEY,
    test_id INTEGER FOREIGN KEY,
    pregunta_id INTEGER FOREIGN KEY,
    respuesta VARIANT,  -- Puede ser INTEGER (1-5) o VARCHAR (A,B,C,D)
    timestamp DATETIME
);

-- Scores por test
CREATE TABLE scores_test (
    id INTEGER PRIMARY KEY,
    candidato_id INTEGER FOREIGN KEY,
    vacante_id INTEGER FOREIGN KEY,
    test_id INTEGER FOREIGN KEY,
    score_raw FLOAT,
    score_normalizado FLOAT,  -- 0-100
    timestamp DATETIME
);

-- Score final integrado
CREATE TABLE score_candidato_final (
    id INTEGER PRIMARY KEY,
    candidato_id INTEGER FOREIGN KEY,
    vacante_id INTEGER FOREIGN KEY,
    score_competencias FLOAT,
    score_psicometrico FLOAT,
    score_cognitivo FLOAT,
    score_final FLOAT,
    clasificacion VARCHAR(20),  -- PRIORITARIO, VIABLE, CONSIDERAR, NO RECOMENDADO
    perfil_resumido TEXT
);
```

---

## 📱 FLUJO COMPLETO CANDIDATO

```
1. CANDIDATO VE MENÚ
   GET /api/vacantes/{id}/tests
   → "Diseñador Estructural - Tests"
   → 4 tests disponibles (90-120 min total)

2. CANDIDATO COMIENZA TEST 1
   GET /api/tests/competencias/{candidato_id}
   → 90 preguntas, 15 min estimado

3. RESPONDE Y PASA A TEST 2
   POST /api/tests/competencias/{candidato_id}/respuestas
   → Score de competencias calculado
   GET /api/tests/razonamiento-verbal/{candidato_id}
   → 20 preguntas, 10 min

4. CONTINÚA HASTA TERMINAR TODOS

5. SISTEMA CALCULA SCORE FINAL
   POST /api/candidatos/{id}/calcular-score-final
   
   Formula:
   Score = (Comp×0.35) + (PsicoAvg×0.35) + (CogAvg×0.30)
   
   Clasificación:
   ├─ 81-100: PRIORITARIO
   ├─ 61-80: VIABLE
   ├─ 41-60: CONSIDERAR
   └─ 0-40: NO RECOMENDADO

6. CENERH DESCARGA FICHA + PERFIL
   GET /api/candidatos/{id}/ficha-completa.pdf
   
   Incluye:
   ├─ Datos básicos
   ├─ Score final
   ├─ Fortalezas por competencia
   ├─ Perfil psicológico
   ├─ Recomendación CENERH
   └─ Gráficos comparativos
```

---

## 🎯 TIMELINE CORRECTO LUNES

**Si respondes HOY la estructura del menú:**

**LUNES**
```
[ ] 08:00 - 10:00  Copiar models + seed de competencias
[ ] 10:00 - 11:00  Crear modelos para 8 tests psicométricos
[ ] 11:00 - 13:00  Endpoints GET tests / POST respuestas
[ ] 13:00 - 14:00  Función scoring automática (8 tests)
[ ] 14:00 - 15:00  Score final ponderado
[ ] 15:00 - 16:00  Testing + documentación
[ ] 16:00 - 17:00  Push GitHub
```

**Resultado: API con 290 preguntas listas**

---

## 🔴 BLOQUEO

**NO PUEDO EMPEZAR A PROGRAMAR LUNES SIN SABER:**

1. **¿Qué tests integro LUNES?** (todos 8 o solo 2-3?)
2. **¿Cómo selecciona cada vacante sus tests?**
   - ¿Por rol automático?
   - ¿Configuración manual?
   - ¿Menú fijo?
3. **¿Score final cómo se calcula?**
   - ¿Promedio simple?
   - ¿Ponderado? ¿Con qué pesos?
4. **¿Atención & Concentración va?**
   - Keren dice que está al 55% de calidad
   - ¿Reconstruimos primero o la dejamos fuera?

---

**Responde esas 4 cosas y empiezo LUNES.**

Sin eso, programo algo que no funciona con el negocio.

¿Dale?

