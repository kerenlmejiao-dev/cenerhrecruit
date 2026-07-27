"""
models.py - SQLAlchemy Models para CENERH RECRUIT OS
9 tests + 300 preguntas + Sistema de scoring
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


# ============================================================================
# TABLA: Tests Disponibles (9 tests)
# ============================================================================
class TestPsicometrico(Base):
    __tablename__ = "tests_psicometricos"
    
    id = Column(String(50), primary_key=True)  # "verbal", "numerico", "competencias", etc.
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    num_preguntas = Column(Integer, nullable=False)
    tipo = Column(String(50), nullable=False)  # "cognitivo", "psicometrico", "competencias", "atencion"
    calidad_psicometrica = Column(Float, default=90.0)  # Score 0-100
    tiempo_estimado = Column(Integer, nullable=False)  # segundos
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    preguntas = relationship("PreguntaTest", back_populates="test")
    
    def __repr__(self):
        return f"<TestPsicometrico {self.nombre} ({self.num_preguntas} preg)>"


# ============================================================================
# TABLA: Preguntas de los Tests (300 preguntas)
# ============================================================================
class PreguntaTest(Base):
    __tablename__ = "preguntas_tests"
    
    id = Column(String(100), primary_key=True)  # "verbal_1", "numerico_1", "competencias_1", etc.
    test_id = Column(String(50), ForeignKey("tests_psicometricos.id"), nullable=False)
    numero_pregunta = Column(Integer, nullable=False)  # 1-20, 1-40, 1-90, etc.
    pregunta = Column(Text, nullable=False)
    tipo_respuesta = Column(String(20), nullable=False)  # "multiple_choice", "likert", "si_no"
    opciones = Column(JSON, nullable=True)  # {"A": "opcion1", "B": "opcion2", ...}
    respuesta_correcta = Column(String(10), nullable=False)  # "A", "C", "Sí", etc.
    dificultad = Column(String(20), nullable=True)  # "facil", "media", "dificil"
    discriminacion = Column(Float, nullable=True)  # Índice de discriminación IRT
    creado_en = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    test = relationship("TestPsicometrico", back_populates="preguntas")
    respuestas = relationship("RespuestaCandidata", back_populates="pregunta")
    
    def __repr__(self):
        return f"<PreguntaTest {self.id}: {self.pregunta[:50]}...>"


# ============================================================================
# TABLA: Vacantes (Define qué tests aplica cada vacante)
# ============================================================================
class Vacante(Base):
    __tablename__ = "vacantes"
    
    id = Column(String(50), primary_key=True)  # "vacante_1", "contador_paraiso", etc.
    nombre = Column(String(100), nullable=False)
    cliente = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    tests_a_aplicar = Column(JSON, nullable=False)  # ["verbal", "numerico", "competencias", ...]
    pesos_scoring = Column(JSON, nullable=False)  # {"competencias": 0.35, "psico": 0.35, "cognitivo": 0.30}
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    candidatos = relationship("Candidato", back_populates="vacante")
    
    def __repr__(self):
        return f"<Vacante {self.nombre} ({', '.join(self.tests_a_aplicar)})>"


# ============================================================================
# TABLA: Candidatos
# ============================================================================
class Candidato(Base):
    __tablename__ = "candidatos"
    
    id = Column(String(50), primary_key=True)  # UUID
    vacante_id = Column(String(50), ForeignKey("vacantes.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    estado = Column(String(20), default="iniciado")  # "iniciado", "en_progreso", "completado", "rechazado"
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_completitud = Column(DateTime, nullable=True)
    score_final = Column(Float, nullable=True)  # 0-100
    clasificacion = Column(String(20), nullable=True)  # "PRIORITARIO", "VIABLE", "CONSIDERAR", "NO_RECOMENDADO"
    
    # Relaciones
    vacante = relationship("Vacante", back_populates="candidatos")
    respuestas = relationship("RespuestaCandidata", back_populates="candidato")
    scores = relationship("ScoreCandidata", back_populates="candidato")
    
    def __repr__(self):
        return f"<Candidato {self.nombre} - Score: {self.score_final}>"


# ============================================================================
# TABLA: Respuestas de Candidatos (Las respuestas que da cada candidato)
# ============================================================================
class RespuestaCandidata(Base):
    __tablename__ = "respuestas_candidatas"
    
    id = Column(String(100), primary_key=True)
    candidato_id = Column(String(50), ForeignKey("candidatos.id"), nullable=False)
    pregunta_id = Column(String(100), ForeignKey("preguntas_tests.id"), nullable=False)
    respuesta = Column(String(10), nullable=False)  # "A", "B", "C", "D", o valor Likert (1-5)
    es_correcta = Column(Boolean, nullable=True)  # True, False, o None (si es Likert)
    tiempo_respuesta = Column(Integer, nullable=True)  # segundos
    respondido_en = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    candidato = relationship("Candidato", back_populates="respuestas")
    pregunta = relationship("PreguntaTest", back_populates="respuestas")
    
    def __repr__(self):
        return f"<RespuestaCandidata {self.candidato_id} - {self.pregunta_id}: {self.respuesta}>"


# ============================================================================
# TABLA: Scores por Test (Resultados de cada test para cada candidato)
# ============================================================================
class ScoreCandidata(Base):
    __tablename__ = "scores_candidatas"
    
    id = Column(String(100), primary_key=True)
    candidato_id = Column(String(50), ForeignKey("candidatos.id"), nullable=False)
    test_id = Column(String(50), ForeignKey("tests_psicometricos.id"), nullable=False)
    
    # Puntuaciones
    puntuacion_directa = Column(Float, nullable=False)  # PD (0-aciertos)
    t_score = Column(Float, nullable=False)  # T-Score estandarizado (media 50, DE 10)
    percentil = Column(Float, nullable=True)  # Percentil 0-100
    score_normalizado = Column(Float, nullable=False)  # 0-100 para usar en cálculo final
    
    # Clasificación individual del test
    clasificacion_test = Column(String(20), nullable=True)  # "Alto", "Medio", "Bajo"
    
    # Metadata
    aciertos = Column(Integer, nullable=True)  # Número de aciertos (solo para tests cognitivos)
    total_preguntas = Column(Integer, nullable=False)
    calculado_en = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    candidato = relationship("Candidato", back_populates="scores")
    
    def __repr__(self):
        return f"<ScoreCandidata {self.candidato_id} - {self.test_id}: {self.score_normalizado}/100>"


# ============================================================================
# TABLA: Pesos por Vacante (Permite customizar scoring por vacante)
# ============================================================================
class PesoVacante(Base):
    __tablename__ = "pesos_vacantes"
    
    id = Column(String(100), primary_key=True)
    vacante_id = Column(String(50), ForeignKey("vacantes.id"), nullable=False)
    
    # Pesos (deben sumar 100)
    peso_competencias = Column(Float, default=35.0)
    peso_psicometricos = Column(Float, default=35.0)  # IE + Motivación + Valores + Liderazgo
    peso_cognitivos = Column(Float, default=30.0)  # Verbal + Numérico
    
    # Si hay personalización por test individual
    pesos_individual = Column(JSON, nullable=True)  # {"verbal": 10, "numerico": 20, ...}
    
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<PesoVacante {self.vacante_id}: C={self.peso_competencias}% P={self.peso_psicometricos}% Cog={self.peso_cognitivos}%>"


# ============================================================================
# TABLA: Audit Log (Registro de acciones para debugging)
# ============================================================================
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String(100), primary_key=True)
    candidato_id = Column(String(50), nullable=True)
    accion = Column(String(100), nullable=False)  # "inició_test", "respondió_pregunta", "completó_test", etc.
    detalles = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AuditLog {self.candidato_id} - {self.accion}>"


# ============================================================================
# SUMA DE MODELOS
# ============================================================================
"""
MODELOS:
1. TestPsicometrico       - 9 tests disponibles
2. PreguntaTest           - 300 preguntas
3. Vacante                - Vacantes a llenar
4. Candidato              - Candidatos evaluados
5. RespuestaCandidata     - Respuestas de candidatos (300 respuestas por candidato)
6. ScoreCandidata         - Scores por test (9 scores por candidato)
7. PesoVacante            - Pesos personalizables por vacante
8. AuditLog               - Registro de acciones

RELACIONES:
TestPsicometrico → PreguntaTest (1:N)
PreguntaTest → RespuestaCandidata (1:N)
Vacante → Candidato (1:N)
Candidato → RespuestaCandidata (1:N)
Candidato → ScoreCandidata (1:N)
Vacante → PesoVacante (1:1)
"""
