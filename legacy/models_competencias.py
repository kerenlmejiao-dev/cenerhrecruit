# models_competencias.py
# SQLAlchemy Models para Tests de Competencias (90 preguntas Likert)
# Estructura lista para insertar en PostgreSQL

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# ============================================================================
# TABLA: COMPETENCIAS (18 competencias maestras)
# ============================================================================
class Competencia(Base):
    __tablename__ = "competencias"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)  # Ej: "Orientación a Resultados"
    descripcion = Column(String(500))
    numero_preguntas = Column(Integer, default=5)  # Cada competencia tiene 5 preguntas
    
    def __repr__(self):
        return f"<Competencia {self.nombre}>"


# ============================================================================
# TABLA: PREGUNTAS_COMPETENCIAS (90 preguntas)
# ============================================================================
class PreguntaCompetencia(Base):
    __tablename__ = "preguntas_competencias"
    
    id = Column(Integer, primary_key=True)
    competencia_id = Column(Integer, ForeignKey('competencias.id'), nullable=False)
    numero_pregunta = Column(Integer)  # 1-5 por competencia
    pregunta = Column(String(500), nullable=False)
    escala_minima = Column(Integer, default=1)
    escala_maxima = Column(Integer, default=5)
    escala_valores = Column(String(100), default="1=Nunca, 2=Rara vez, 3=Algunas veces, 4=Frecuentemente, 5=Siempre")
    
    def __repr__(self):
        return f"<PreguntaCompetencia ID:{self.id} Comp:{self.competencia_id} Preg:{self.numero_pregunta}>"


# ============================================================================
# TABLA: RESPUESTAS_TEST_COMPETENCIAS (Respuestas del candidato)
# ============================================================================
class RespuestaTestCompetencia(Base):
    __tablename__ = "respuestas_test_competencias"
    
    id = Column(Integer, primary_key=True)
    candidato_id = Column(Integer, ForeignKey('candidatos.id'), nullable=False)
    pregunta_competencia_id = Column(Integer, ForeignKey('preguntas_competencias.id'), nullable=False)
    respuesta = Column(Integer, nullable=False)  # 1-5
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<RespuestaCompetencia Candidato:{self.candidato_id} Pregunta:{self.pregunta_competencia_id} Respuesta:{self.respuesta}>"


# ============================================================================
# TABLA: SCORES_COMPETENCIAS (Scores calculados por competencia)
# ============================================================================
class ScoreCompetencia(Base):
    __tablename__ = "scores_competencias"
    
    id = Column(Integer, primary_key=True)
    candidato_id = Column(Integer, ForeignKey('candidatos.id'), nullable=False)
    competencia_id = Column(Integer, ForeignKey('competencias.id'), nullable=False)
    score_raw = Column(Float)  # Suma bruta (1-25)
    score_normalizado = Column(Float)  # (score_raw/25) × 100 = 0-100
    nivel = Column(String(20))  # "Muy Alto", "Alto", "Medio", "Bajo", "Muy Bajo"
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ScoreCompetencia Candidato:{self.candidato_id} Comp:{self.competencia_id} Score:{self.score_normalizado}>"


# ============================================================================
# TABLA: PERFIL_CANDIDATO (Perfil integral: competencias + psicometría)
# ============================================================================
class PerfilCandidato(Base):
    __tablename__ = "perfil_candidato"
    
    id = Column(Integer, primary_key=True)
    candidato_id = Column(Integer, ForeignKey('candidatos.id'), nullable=False, unique=True)
    
    # Scores globales
    score_competencias_promedio = Column(Float)  # Promedio de 18 competencias
    score_psicometrico_promedio = Column(Float)  # Promedio de tests psico
    score_razonamiento_numerico = Column(Float)  # Test numérico (0-100)
    
    # Clasificación final
    clasificacion = Column(String(20))  # PRIORITARIO | VIABLE | CONSIDERAR | NO RECOMENDADO
    score_final = Column(Float)  # Puntaje agregado (0-100)
    
    # Perfil psicológico resumido
    perfil_fortalezas = Column(String(500))  # Top 3-5 competencias
    perfil_areas_desarrollo = Column(String(500))  # Bottom 3-5 competencias
    recomendacion_cenerh = Column(String(1000))  # Nota de consultor
    
    test_completado = Column(Integer, default=0)  # 0=No, 1=Sí
    timestamp_creacion = Column(DateTime, default=datetime.utcnow)
    timestamp_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<PerfilCandidato Candidato:{self.candidato_id} Clasificacion:{self.clasificacion}>"


# ============================================================================
# SCRIPT DE INICIALIZACIÓN (Insertar 18 competencias + 90 preguntas)
# ============================================================================
"""
USAR ASÍ:

from models_competencias import Base, Competencia, PreguntaCompetencia
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import seed_competencias  # ver archivo seed_competencias.py

engine = create_engine("postgresql://user:pass@localhost/cenerh_recruit_os")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Insertar datos
seed_competencias.cargar_competencias(session)
print("✅ 18 Competencias + 90 Preguntas cargadas en BD")
"""

