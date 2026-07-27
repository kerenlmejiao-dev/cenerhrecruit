# INTEGRACIÓN: 90 PREGUNTAS DE COMPETENCIAS AL API

## 📋 RESUMEN

Las 90 preguntas de competencias Likert diseñadas por Keren están **listos para integrar** al backend de CENERH RECRUIT OS.

**Qué tienes:**
- ✅ 18 competencias maestras
- ✅ 90 preguntas (5 por competencia)
- ✅ Escala Likert 1-5 standardizada
- ✅ SQLAlchemy models listos
- ✅ Seed script para cargar BD
- ✅ Excel profesional para referencia

---

## 🔧 PASO 1: ESTRUCTURA DE BASE DE DATOS

### Tablas necesarias:

```sql
-- TABLA 1: Competencias (18 registros)
CREATE TABLE competencias (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion VARCHAR(500),
    numero_preguntas INTEGER DEFAULT 5
);

-- TABLA 2: Preguntas de Competencias (90 registros)
CREATE TABLE preguntas_competencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competencia_id INTEGER NOT NULL FOREIGN KEY REFERENCES competencias(id),
    numero_pregunta INTEGER,  -- 1-5
    pregunta VARCHAR(500) NOT NULL,
    escala_minima INTEGER DEFAULT 1,
    escala_maxima INTEGER DEFAULT 5
);

-- TABLA 3: Respuestas (Candidato responde)
CREATE TABLE respuestas_test_competencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidato_id INTEGER NOT NULL FOREIGN KEY REFERENCES candidatos(id),
    pregunta_competencia_id INTEGER NOT NULL FOREIGN KEY REFERENCES preguntas_competencias(id),
    respuesta INTEGER NOT NULL,  -- 1-5
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TABLA 4: Scores por Competencia
CREATE TABLE scores_competencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidato_id INTEGER NOT NULL FOREIGN KEY REFERENCES candidatos(id),
    competencia_id INTEGER NOT NULL FOREIGN KEY REFERENCES competencias(id),
    score_raw FLOAT,  -- Suma (1-25)
    score_normalizado FLOAT,  -- (score_raw/25) × 100 = 0-100
    nivel VARCHAR(20),  -- "Muy Alto", "Alto", etc
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📦 PASO 2: CARGAR DATOS EN BD

### Opción A: Usar seed_competencias.py (RECOMENDADO)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_competencias import Base
from seed_competencias import cargar_competencias, verificar_carga

# 1. Crear engine y tablas
engine = create_engine("postgresql://user:pass@localhost/cenerh_recruit_os")
Base.metadata.create_all(engine)

# 2. Crear sesión
Session = sessionmaker(bind=engine)
session = Session()

# 3. Cargar datos
cargar_competencias(session)

# 4. Verificar
verificar_carga(session)
```

**Resultado esperado:**
```
✅ COMPETENCIAS CARGADAS EN BD
   └─ 18 competencias
   └─ 90 preguntas (Likert 1-5)
   └─ Listo para API
```

### Opción B: Cargar manualmente desde CSV

Si prefieres usar herramientas SQL:

```bash
# Exportar CSV de Excel
# competencias_90_preguntas.csv (creado anteriormente)

# Importar a PostgreSQL
psql -U user -d cenerh_recruit_os -c "\COPY competencias FROM 'competencias.csv' WITH (FORMAT csv, HEADER true)"
```

---

## 🔌 PASO 3: ENDPOINTS API

### Endpoint 1: Obtener preguntas del test

```python
# routes/tests.py

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from models_competencias import PreguntaCompetencia

router = APIRouter(prefix="/api/tests", tags=["Tests"])

@router.get("/competencias/{candidato_id}")
async def obtener_test_competencias(candidato_id: int, db: Session):
    """
    Obtiene las 90 preguntas de competencias para un candidato.
    Devuelve las preguntas en orden randomizado.
    """
    preguntas = db.query(PreguntaCompetencia).order_by(PreguntaCompetencia.competencia_id).all()
    
    if not preguntas:
        raise HTTPException(status_code=404, detail="No se encontraron preguntas")
    
    return {
        "candidato_id": candidato_id,
        "test_tipo": "Competencias",
        "total_preguntas": len(preguntas),
        "tiempo_estimado": "15-20 minutos",
        "escala": "1=Nunca, 2=Rara vez, 3=Algunas veces, 4=Frecuentemente, 5=Siempre",
        "preguntas": [
            {
                "id": p.id,
                "competencia_id": p.competencia_id,
                "competencia": db.query(Competencia).filter_by(id=p.competencia_id).first().nombre,
                "numero_pregunta": p.numero_pregunta,
                "pregunta": p.pregunta,
                "escala_minima": p.escala_minima,
                "escala_maxima": p.escala_maxima
            }
            for p in preguntas
        ]
    }
```

### Endpoint 2: Guardar respuestas

```python
# routes/tests.py

from pydantic import BaseModel
from typing import List
from models_competencias import RespuestaTestCompetencia, ScoreCompetencia

class RespuestaCompetenciaIn(BaseModel):
    pregunta_id: int
    respuesta: int  # 1-5

@router.post("/competencias/{candidato_id}/respuestas")
async def guardar_respuestas_competencias(
    candidato_id: int,
    respuestas: List[RespuestaCompetenciaIn],
    db: Session
):
    """
    Recibe respuestas del candidato y calcula scores por competencia.
    """
    try:
        # Guardar respuestas
        for resp in respuestas:
            respuesta_obj = RespuestaTestCompetencia(
                candidato_id=candidato_id,
                pregunta_competencia_id=resp.pregunta_id,
                respuesta=resp.respuesta
            )
            db.add(respuesta_obj)
        
        db.commit()
        
        # Calcular scores
        calcular_scores_competencias(candidato_id, db)
        
        return {
            "status": "success",
            "mensaje": "Respuestas guardadas y scores calculados",
            "candidato_id": candidato_id
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
```

### Endpoint 3: Obtener resultados

```python
@router.get("/competencias/{candidato_id}/resultados")
async def obtener_resultados_competencias(candidato_id: int, db: Session):
    """
    Devuelve scores y perfil por competencia del candidato.
    """
    scores = db.query(ScoreCompetencia).filter_by(candidato_id=candidato_id).all()
    
    if not scores:
        raise HTTPException(status_code=404, detail="No se encontraron resultados")
    
    perfil = {
        "candidato_id": candidato_id,
        "competencias": [
            {
                "competencia": score.competencia_id,
                "score_raw": score.score_raw,
                "score_normalizado": round(score.score_normalizado, 2),
                "nivel": score.nivel
            }
            for score in scores
        ],
        "score_promedio": round(sum([s.score_normalizado for s in scores]) / len(scores), 2),
        "fortalezas": [s for s in scores if s.nivel == "Muy Alto"],
        "areas_desarrollo": [s for s in scores if s.nivel == "Bajo"]
    }
    
    return perfil
```

---

## 📊 PASO 4: SCORING

### Función de cálculo de scores

```python
# services/scoring.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from models_competencias import (
    RespuestaTestCompetencia,
    ScoreCompetencia,
    Competencia,
    PreguntaCompetencia
)

def calcular_scores_competencias(candidato_id: int, db: Session):
    """
    Calcula score por competencia para un candidato.
    
    Fórmula:
    - Suma de 5 respuestas (rango: 5-25)
    - Score normalizado = (Suma / 25) × 100 (rango: 0-100)
    - Nivel: Muy Alto (80-100), Alto (60-79), Medio (40-59), Bajo (20-39), Muy Bajo (0-19)
    """
    
    competencias = db.query(Competencia).all()
    
    for competencia in competencias:
        # Obtener respuestas del candidato para esta competencia
        preguntas_competencia = db.query(PreguntaCompetencia).filter_by(
            competencia_id=competencia.id
        ).all()
        
        pregunta_ids = [p.id for p in preguntas_competencia]
        
        respuestas = db.query(RespuestaTestCompetencia).filter(
            RespuestaTestCompetencia.candidato_id == candidato_id,
            RespuestaTestCompetencia.pregunta_competencia_id.in_(pregunta_ids)
        ).all()
        
        if len(respuestas) == 5:  # Si respondió todas las preguntas
            # Calcular suma
            suma = sum([r.respuesta for r in respuestas])
            
            # Normalizar
            score_normalizado = (suma / 25) * 100
            
            # Clasificar nivel
            if score_normalizado >= 80:
                nivel = "Muy Alto"
            elif score_normalizado >= 60:
                nivel = "Alto"
            elif score_normalizado >= 40:
                nivel = "Medio"
            elif score_normalizado >= 20:
                nivel = "Bajo"
            else:
                nivel = "Muy Bajo"
            
            # Guardar score
            score = ScoreCompetencia(
                candidato_id=candidato_id,
                competencia_id=competencia.id,
                score_raw=suma,
                score_normalizado=score_normalizado,
                nivel=nivel
            )
            db.add(score)
    
    db.commit()
    print(f"✅ Scores calculados para candidato {candidato_id}")


def generar_perfil_psicologico(candidato_id: int, db: Session) -> dict:
    """
    Genera perfil psicológico resumido del candidato basado en 
    las 18 competencias.
    """
    
    scores = db.query(ScoreCompetencia).filter_by(candidato_id=candidato_id).all()
    
    fortalezas = sorted([s for s in scores], key=lambda x: x.score_normalizado, reverse=True)[:3]
    debilidades = sorted([s for s in scores], key=lambda x: x.score_normalizado)[:3]
    
    promedio = sum([s.score_normalizado for s in scores]) / len(scores)
    
    return {
        "score_promedio": round(promedio, 2),
        "fortalezas": [
            {
                "competencia": s.competencia.nombre,
                "score": round(s.score_normalizado, 2)
            }
            for s in fortalezas
        ],
        "areas_desarrollo": [
            {
                "competencia": s.competencia.nombre,
                "score": round(s.score_normalizado, 2)
            }
            for s in debilidades
        ],
        "perfil_resumido": generar_narrativa_perfil(fortalezas, debilidades)
    }


def generar_narrativa_perfil(fortalezas: list, debilidades: list) -> str:
    """Genera texto narrativo del perfil psicológico del candidato."""
    
    texto_fortalezas = ", ".join([f.competencia.nombre for f in fortalezas])
    texto_debilidades = ", ".join([f.competencia.nombre for f in debilidades])
    
    return f"""
    El candidato demuestra fortalezas significativas en: {texto_fortalezas}.
    Esto indica capacidad para {generar_insight_fortalezas(fortalezas)}.
    
    Áreas de desarrollo: {texto_debilidades}.
    Se recomienda acompañamiento en estas competencias a través de 
    mentoría o capacitación específica.
    """
```

---

## ✅ PASO 5: CHECKLIST DE INTEGRACIÓN

```
[ ] Base de datos creada y tablas configuradas
[ ] 18 competencias + 90 preguntas cargadas
[ ] Models SQLAlchemy importados en main.py
[ ] Endpoints API /tests/competencias/* creados
[ ] Función de scoring implementada
[ ] Endpoints devuelven JSON correctamente
[ ] Tests unitarios para scoring
[ ] Documentación Swagger actualizada
[ ] Repositorio GitHub pusheado

FINAL: ✅ API lista para recibir tests de competencias
```

---

## 📱 EJEMPLO: FLUJO COMPLETO

### 1. Candidato inicia test

```bash
GET /api/tests/competencias/123
```

**Respuesta:**
```json
{
  "candidato_id": 123,
  "test_tipo": "Competencias",
  "total_preguntas": 90,
  "tiempo_estimado": "15-20 minutos",
  "escala": "1=Nunca, 2=Rara vez...",
  "preguntas": [
    {
      "id": 1,
      "competencia": "Orientación a Resultados",
      "pregunta": "Establezco objetivos claros antes de iniciar un trabajo.",
      "escala_minima": 1,
      "escala_maxima": 5
    },
    ...
  ]
}
```

### 2. Candidato envía respuestas

```bash
POST /api/tests/competencias/123/respuestas
```

**Payload:**
```json
{
  "respuestas": [
    {"pregunta_id": 1, "respuesta": 5},
    {"pregunta_id": 2, "respuesta": 4},
    {"pregunta_id": 3, "respuesta": 5},
    ...
    {"pregunta_id": 90, "respuesta": 4}
  ]
}
```

### 3. Obtener resultados

```bash
GET /api/tests/competencias/123/resultados
```

**Respuesta:**
```json
{
  "candidato_id": 123,
  "competencias": [
    {
      "competencia": "Orientación a Resultados",
      "score_raw": 23,
      "score_normalizado": 92.0,
      "nivel": "Muy Alto"
    },
    {
      "competencia": "Trabajo en Equipo",
      "score_raw": 20,
      "score_normalizado": 80.0,
      "nivel": "Alto"
    },
    ...
  ],
  "score_promedio": 82.5,
  "fortalezas": [...],
  "areas_desarrollo": [...]
}
```

---

## 🚀 PRÓXIMO PASO

**LUNES 29 JUL:**
- Crear models_competencias.py en repo
- Ejecutar seed_competencias.py
- Implementar endpoints
- Pushear a GitHub

¿Confirmás que empiezo LUNES?

