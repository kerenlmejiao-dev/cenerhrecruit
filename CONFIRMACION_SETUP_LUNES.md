# ✅ CONFIRMO SETUP API - LUNES EMPIEZO

Keren, tengo lo que necesito. Acá va lo que hago:

---

## 📋 SETUP FINAL CONFIRMADO

### **1. Tests a integrar LUNES: TODOS 8 + COMPETENCIAS**

```
✅ Razonamiento Verbal (20 preg) - 94/100
✅ Razonamiento Numérico (20 preg) - 82/100 (v1)
✅ Big Five Personalidad (20 preg) - 96/100
✅ Inteligencia Emocional (20 preg) - 95/100
✅ Motivación Laboral (20 preg) - 98/100
✅ Valores Organizacionales (20 preg) - 94/100
✅ Potencial de Liderazgo (20 preg) - 96/100
✅ Competencias Likert (90 preg) - En progreso
= 250 PREGUNTAS LISTAS

FASE 2 (Septiembre):
├─ Atención & Concentración (Reconstruida)
└─ Razonamiento Numérico v2 (Mejorado nivel empresa)
```

---

### **2. CONFIGURACIÓN MANUAL POR VACANTE**

**El reclutador decide qué tests aplica:**

```
Cuando crea vacante en plataforma:

PASO 1: Datos de vacante
├─ Nombre: "Diseñador Estructural Junior"
├─ Rol: [dropdown]
├─ Salario: [input]
└─ Descripción: [textarea]

PASO 2: Seleccionar tests (CHECKBOX)
├─ ☑️ Competencias Likert (90 preg)
├─ ☑️ Razonamiento Verbal (20 preg)
├─ ☑️ Razonamiento Numérico (20 preg)
├─ ☑️ Big Five (20 preg)
├─ ☐ Inteligencia Emocional (20 preg)
├─ ☐ Motivación Laboral (20 preg)
├─ ☐ Valores Organizacionales (20 preg)
├─ ☐ Potencial de Liderazgo (20 preg)
└─ ☐ Atención & Concentración (cuando esté ready)

PASO 3: Definir PESOS (si quiere personalizar)
├─ Competencias: [slider] 35%
├─ Tests Psico: [slider] 35%
├─ Tests Cognitivos: [slider] 30%
└─ O usar "Pesos sugeridos" por rol

PASO 4: Crear vacante
└─ API crea registro + candidatos hacen tests en ese orden
```

---

### **3. SCORING FINAL: PONDERADO**

🔴 **NECESITO CONFIRMAR LOS PESOS:**

**Opción A (Propuesta): Estándar**
```
- Competencias: 35%
- Tests Psicométricos (IE+Motivación+Valores+Liderazgo): 35%
- Tests Cognitivos (Verbal+Numérico): 30%

Score Final = (Comp × 0.35) + (Psico_Avg × 0.35) + (Cognitivo_Avg × 0.30)
Rango: 0-100

Clasificación:
├─ 81-100: PRIORITARIO ⭐⭐⭐
├─ 61-80: VIABLE ⭐⭐
├─ 41-60: CONSIDERAR ⭐
└─ 0-40: NO RECOMENDADO
```

**Opción B (Alternativa): Solo reclutador decide**
```
Reclutador elige pesos al crear vacante:
├─ Competencias: [slider] XX%
├─ Razonamiento Verbal: [slider] XX%
├─ Razonamiento Numérico: [slider] XX%
├─ Big Five: [slider] XX%
├─ IE: [slider] XX%
├─ Motivación: [slider] XX%
├─ Valores: [slider] XX%
└─ Liderazgo: [slider] XX%
(Total debe = 100%)

API calcula: Sum(Test_Score × Weight%)
```

**¿Cuál prefieres?**

---

### **4. ATENCIÓN & CONCENTRACIÓN**

```
⏳ Esperando tu mejora

Cuando me pases el test reconstruido:
├─ Lo integro a BD
├─ Lo agrego a menú de tests disponibles
└─ Reclutador puede seleccionarlo en vacantes

Timeline: Cuando lo tengas listo (ASAP)
```

---

## 🔧 CHECKLIST LUNES 29 JUL

```
MAÑANA A LAS 8AM EMPIEZO:

[ ] 08:00 - 09:00
    ├─ Copiar models_competencias.py a src/models/
    ├─ Copiar seed_competencias.py a src/database/
    └─ Crear models para 8 tests (TestPsicometrico, RespuestaTest, ScoreTest)

[ ] 09:00 - 10:00
    ├─ Crear tablas en PostgreSQL
    ├─ Ejecutar seed de competencias (18 comp + 90 preg)
    └─ Ejecutar seed de tests psicométricos (8 tests + 160 preg)

[ ] 10:00 - 12:00
    ├─ Endpoint: GET /api/vacantes/{id}/tests (obtener tests disponibles)
    ├─ Endpoint: GET /api/tests/{test_id}/{candidato_id} (obtener preguntas)
    └─ Endpoint: POST /api/tests/{test_id}/{candidato_id}/respuestas (guardar)

[ ] 12:00 - 14:00
    ├─ Función: calcular_scores_por_test() (normaliza 0-100)
    ├─ Función: calcular_score_final() (ponderado)
    └─ Endpoint: GET /api/candidatos/{id}/resultados

[ ] 14:00 - 15:00
    ├─ PDF generación (ficha candidato con perfil)
    └─ Email automático al candidato

[ ] 15:00 - 16:00
    ├─ Testing LIVE con datos dummy
    └─ Debugging

[ ] 16:00 - 17:00
    ├─ Documentación Swagger
    ├─ README.md actualizado
    └─ Push a GitHub
```

**Resultado LUNES 5PM:**
```
✅ API con 250 preguntas listas
✅ Sistema de scoring ponderado
✅ Menú de selección manual por vacante
✅ PDFs generados automáticamente
✅ 100% en GitHub
```

---

## 📊 ESTADO FINAL (Lunes antes de dormir)

| Componente | Status |
|------------|--------|
| Competencias (90 preg) | ✅ Ready |
| Tests Psico (160 preg) | ✅ Ready |
| Razonamiento Verbal (20) | ✅ Ready |
| Razonamiento Numérico v1 (20) | ✅ Ready |
| Scoring automático | ✅ Ready |
| Score ponderado | ✅ Ready |
| Menú manual por vacante | ✅ Ready |
| PDF generación | ✅ Ready |
| API endpoints | ✅ Ready (10 endpoints) |
| Testing | ✅ Ready |
| GitHub | ✅ Ready |

---

## 🎯 LO QUE NECESITO DE TI HOY

**1. Confirmar pesos de scoring:**
```
¿Opción A (estándar) u Opción B (manual por reclutador)?

Si A:
├─ Competencias: 35%? (o diferente)
├─ Psico: 35%? (o diferente)
└─ Cognitivo: 30%? (o diferente)
```

**2. El test de Atención & Concentración mejorado**
```
Cuándo me lo pases (ASAP, sin presión):
├─ Lo estructuro
├─ Lo subo a BD
└─ Reclutador puede usarlo en vacantes
```

**3. Confirmar que puedo empezar**
```
"Dale, ¡adelante!"
```

---

## 🚀 MIENTRAS TANTO

**Tú:** RAAS + Pádel (dinero)
**Yo:** API (plataforma)

**Viernes:** Testeamos con primer candidato REAL

---

¿Confirmás los pesos + "adelante"?

Así empiezo LUNES sin dudas.

