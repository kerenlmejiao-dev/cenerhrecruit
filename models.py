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
    tipo = Column(String(50), nullable=False)  # "cognitivo", "psicometrico", "competencias", "atencion" (categoría de SCORING)
    categoria_banco = Column(String(50), nullable=True)  # "Numérico", "Cognitivo", "Atención", "Personalidad", "Roles Estratégicos" (categoría de EXHIBICIÓN en el banco)
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
    # Requisitos/competencias en texto libre, usados por la IA para el
    # análisis de compatibilidad candidato-vacante (ver assessment_service.py).
    requisitos = Column(Text, nullable=True)
    tests_a_aplicar = Column(JSON, nullable=False)  # ["verbal", "numerico", "competencias", ...] (legado, ver vacante_tests)
    pesos_scoring = Column(JSON, nullable=False)  # {"competencias": 0.35, "psico": 0.35, "cognitivo": 0.30}
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=True)
    creado_por_usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    # Ciclo de vida del proceso de búsqueda:
    #   "borrador"  -> no ha iniciado, no acepta aplicaciones, no aparece en el listado público
    #   "activa"    -> proceso abierto, acepta aplicaciones (listado público + link directo)
    #   "inactiva"  -> proceso finalizado, ya no acepta aplicaciones (se puede reabrir)
    estado = Column(String(20), default="borrador")
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    candidatos = relationship("Candidato", back_populates="vacante")
    empresa = relationship("Empresa", back_populates="vacantes")
    vacante_tests = relationship("VacanteTest", back_populates="vacante", order_by="VacanteTest.orden")
    vacante_assessments = relationship("VacanteAssessment", back_populates="vacante")

    def __repr__(self):
        return f"<Vacante {self.nombre} ({', '.join(self.tests_a_aplicar)})>"


# ============================================================================
# TABLA: Candidatos
# ============================================================================
class Candidato(Base):
    __tablename__ = "candidatos"
    
    id = Column(String(50), primary_key=True)  # UUID
    # Nulo = perfil de bolsa de talento: completó sus datos sin aplicar a una
    # vacante específica todavía.
    vacante_id = Column(String(50), ForeignKey("vacantes.id"), nullable=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    estado = Column(String(20), default="iniciado")  # técnico: "iniciado", "en_progreso", "completado", "rechazado"
    # Etapa del proceso de reclutamiento, visible para el candidato y editada a
    # mano por el reclutador (distinto de "estado", que es solo si ya completó
    # los tests). Ver STATUS_RECLUTAMIENTO_VALIDOS en reclutador_router.py.
    status_reclutamiento = Column(String(40), default="Aplicación recibida")
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_completitud = Column(DateTime, nullable=True)
    score_final = Column(Float, nullable=True)  # 0-100
    clasificacion = Column(String(20), nullable=True)  # "PRIORITARIO", "VIABLE", "CONSIDERAR", "NO_RECOMENDADO"

    # Reporte de resultados en lenguaje amigable para el candidato (sin score
    # crudo ni clasificación interna) -- se genera una sola vez con IA cuando
    # paga por verlo (ver reporte_candidato_service.py) y se cachea aquí.
    reporte_resultados = Column(JSON, nullable=True)

    # Relaciones
    vacante = relationship("Vacante", back_populates="candidatos")
    respuestas = relationship("RespuestaCandidata", back_populates="candidato")
    scores = relationship("ScoreCandidata", back_populates="candidato")
    perfil = relationship("CandidatoPerfil", back_populates="candidato", uselist=False)

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
# TABLA: Empresas (Clientes que publican vacantes)
# ============================================================================
class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    contacto_email = Column(String(150), nullable=True)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    # Datos de facturación. Los levanta el reclutador al crear la empresa
    # (no la empresa por autorregistro) porque afectan cómo se factura el
    # desbloqueo de candidatos y la suscripción.
    razon_social = Column(String(200), nullable=True)
    tiene_rnc = Column(Boolean, default=False)
    rnc = Column(String(30), nullable=True)  # Registro Nacional de Contribuyente / comprobante fiscal

    # Relaciones
    usuarios = relationship("Usuario", back_populates="empresa")
    vacantes = relationship("Vacante", back_populates="empresa")

    def __repr__(self):
        return f"<Empresa {self.nombre}>"


# ============================================================================
# TABLA: Usuarios (Cuentas de reclutador/empresa/owner - creadas solo por admin)
# ============================================================================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(150), nullable=False)
    rol = Column(String(20), nullable=False)  # "owner", "reclutador", "empresa"
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=True)  # solo para rol="empresa"
    documento = Column(String(30), nullable=True)  # cédula/RNC - requerido por dLocal para pagos con tarjeta en RD
    telefono = Column(String(30), nullable=True)  # WhatsApp, para notificarle nuevas aplicaciones
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    ultimo_login = Column(DateTime, nullable=True)

    # Relaciones
    empresa = relationship("Empresa", back_populates="usuarios")

    def __repr__(self):
        return f"<Usuario {self.email} ({self.rol})>"


# ============================================================================
# TABLA: Vacante-Tests (Relación M:N - qué tests aplica cada vacante)
# ============================================================================
class VacanteTest(Base):
    __tablename__ = "vacante_tests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vacante_id = Column(String(50), ForeignKey("vacantes.id"), nullable=False)
    test_id = Column(String(50), ForeignKey("tests_psicometricos.id"), nullable=False)
    orden = Column(Integer, nullable=True)
    obligatorio = Column(Boolean, default=True)
    peso_override = Column(Float, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    vacante = relationship("Vacante", back_populates="vacante_tests")
    test = relationship("TestPsicometrico")

    def __repr__(self):
        return f"<VacanteTest {self.vacante_id} -> {self.test_id}>"


# ============================================================================
# TABLA: Perfil extendido del Candidato (cuestionario + CV)
# ============================================================================
class CandidatoPerfil(Base):
    __tablename__ = "candidato_perfil"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidato_id = Column(String(50), ForeignKey("candidatos.id"), unique=True, nullable=False)
    cv_filename = Column(String(255), nullable=True)
    cv_storage_path = Column(String(500), nullable=True)
    cv_texto_extraido = Column(Text, nullable=True)
    pretension_salarial = Column(String(50), nullable=True)
    ubicacion = Column(String(150), nullable=True)
    tiene_vehiculo = Column(Boolean, nullable=True)
    tiene_visa = Column(Boolean, nullable=True)
    disponibilidad = Column(String(50), nullable=True)
    campos_dinamicos = Column(JSON, nullable=True)

    # Datos personales
    cedula = Column(String(20), nullable=True)
    edad = Column(Integer, nullable=True)
    estado_civil = Column(String(30), nullable=True)
    cantidad_hijos = Column(Integer, nullable=True)
    edades_hijos = Column(String(200), nullable=True)  # texto libre, ej. "5, 8, 12"

    # Domicilio (más específico que "ubicacion")
    ciudad_provincia = Column(String(100), nullable=True)
    direccion_exacta = Column(Text, nullable=True)

    # Formación académica
    nivel_academico = Column(String(50), nullable=True)
    carrera = Column(String(150), nullable=True)
    universidad = Column(String(150), nullable=True)

    # Experiencia laboral
    anos_experiencia = Column(Integer, nullable=True)
    ultimo_cargo = Column(String(150), nullable=True)
    ultimo_salario = Column(String(50), nullable=True)
    funciones_ultimo_empleo = Column(Text, nullable=True)

    # Contexto de la aplicación (útil para la base de datos de candidatos)
    fuente_reclutamiento = Column(String(100), nullable=True)  # cómo se enteró de la vacante
    posiciones_interes = Column(Text, nullable=True)  # otras posiciones que le interesan
    contacto_emergencia_nombre = Column(String(150), nullable=True)
    contacto_emergencia_telefono = Column(String(30), nullable=True)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Análisis de CV generado por IA (fortalezas/debilidades/sugerencias) --
    # se genera una sola vez cuando el candidato paga por verlo y se cachea
    # aquí (ver cv_parser_service.analizar_cv).
    analisis_cv = Column(JSON, nullable=True)

    # Relaciones
    candidato = relationship("Candidato", back_populates="perfil")

    def __repr__(self):
        return f"<CandidatoPerfil {self.candidato_id}>"


# ============================================================================
# TABLA: Assessment Centers (Bancos de escenarios de respuesta abierta)
# ============================================================================
class AssessmentCenter(Base):
    __tablename__ = "assessment_centers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(50), nullable=True)  # rol estratégico: "Supervisión", "Liderazgo", "Ventas", "Mercadeo", "Desarrollo de Negocios"
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    preguntas = relationship("AssessmentPregunta", back_populates="assessment")

    def __repr__(self):
        return f"<AssessmentCenter {self.nombre}>"


class AssessmentPregunta(Base):
    __tablename__ = "assessment_preguntas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(Integer, ForeignKey("assessment_centers.id"), nullable=False)
    numero = Column(Integer, nullable=False)
    escenario = Column(Text, nullable=False)
    rubrica_json = Column(JSON, nullable=False)  # criterios de evaluación para el prompt de la IA

    # Relaciones
    assessment = relationship("AssessmentCenter", back_populates="preguntas")

    def __repr__(self):
        return f"<AssessmentPregunta {self.assessment_id}#{self.numero}>"


class AssessmentRespuesta(Base):
    __tablename__ = "assessment_respuestas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidato_id = Column(String(50), ForeignKey("candidatos.id"), nullable=False)
    assessment_pregunta_id = Column(Integer, ForeignKey("assessment_preguntas.id"), nullable=False)
    respuesta_texto = Column(Text, nullable=False)
    respondido_en = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AssessmentRespuesta {self.candidato_id} - pregunta {self.assessment_pregunta_id}>"


class AssessmentScore(Base):
    __tablename__ = "assessment_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidato_id = Column(String(50), ForeignKey("candidatos.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessment_centers.id"), nullable=False)
    score_normalizado = Column(Float, nullable=False)  # 0-100
    feedback_llm = Column(Text, nullable=True)
    criterios_detalle = Column(JSON, nullable=True)
    modelo_usado = Column(String(100), nullable=True)
    revisado_por_humano = Column(Boolean, default=False)  # el score de IA no debe usarse ciego para contratar
    calculado_en = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AssessmentScore {self.candidato_id} - {self.assessment_id}: {self.score_normalizado}/100>"


class CompatibilidadCandidato(Base):
    """Análisis de IA que compara el perfil del candidato (residencia,
    experiencia, formación) contra los requisitos de la vacante a la que
    aplicó. Igual que AssessmentScore, es apoyo para decidir, no un
    filtro automático."""
    __tablename__ = "compatibilidad_candidatos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidato_id = Column(String(50), ForeignKey("candidatos.id"), nullable=False, unique=True)
    score_compatibilidad = Column(Float, nullable=False)  # 0-100
    resumen = Column(Text, nullable=True)
    fortalezas = Column(JSON, nullable=True)  # lista de strings
    brechas = Column(JSON, nullable=True)  # lista de strings
    modelo_usado = Column(String(100), nullable=True)
    calculado_en = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CompatibilidadCandidato {self.candidato_id}: {self.score_compatibilidad}/100>"


class VacanteAssessment(Base):
    __tablename__ = "vacante_assessments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vacante_id = Column(String(50), ForeignKey("vacantes.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessment_centers.id"), nullable=False)
    obligatorio = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    vacante = relationship("Vacante", back_populates="vacante_assessments")
    assessment = relationship("AssessmentCenter")

    def __repr__(self):
        return f"<VacanteAssessment {self.vacante_id} -> {self.assessment_id}>"


# ============================================================================
# TABLA: Suscripciones (reclutadores - planes Básico/Pro/Enterprise)
# ============================================================================
class Suscripcion(Base):
    __tablename__ = "suscripciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    plan = Column(String(20), nullable=False)  # "basico", "pro", "enterprise"
    precio_mensual = Column(Float, nullable=False)
    # "vencida" = fecha_renovacion ya pasó y no se ha pagado (ni manual ni automático).
    estado = Column(String(20), default="pendiente")  # "pendiente", "activa", "vencida", "cancelada"
    # Si es True, se intenta recobrar automáticamente al vencer (requiere que
    # dLocal soporte cobro recurrente con el método de pago guardado del
    # reclutador; el cobro real todavía no está implementado, ver pagos_router.py).
    renovacion_automatica = Column(Boolean, default=False)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_renovacion = Column(DateTime, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Suscripcion usuario={self.usuario_id} plan={self.plan} estado={self.estado}>"


# ============================================================================
# TABLA: Transacciones (log de todos los cobros - suscripción y desbloqueo)
# ============================================================================
class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(30), nullable=False)  # "suscripcion", "desbloqueo_candidato",
    # "estatus_candidato", "resultados_candidato", "analisis_cv_candidato"
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)  # reclutador (suscripción)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=True)  # empresa (desbloqueo)
    candidato_id = Column(String(50), ForeignKey("candidatos.id"), nullable=True)  # candidato dueño (compras propias) o desbloqueado (empresa)
    monto = Column(Float, nullable=False)
    moneda = Column(String(10), default="DOP")
    order_id = Column(String(150), nullable=False, unique=True)  # ID generado por nosotros, enviado a dLocal
    dlocal_payment_id = Column(String(100), nullable=True)  # ID que devuelve dLocal ("id" del payment)
    estado = Column(String(20), default="pendiente")  # "pendiente", "completada", "fallida", "reembolsada"
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Transaccion {self.tipo} monto={self.monto} estado={self.estado}>"


# ============================================================================
# TABLA: Acceso a Candidatos (qué empresa desbloqueó qué candidato)
# ============================================================================
class CandidatoAcceso(Base):
    __tablename__ = "candidato_accesos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    candidato_id = Column(String(50), ForeignKey("candidatos.id"), nullable=False)
    transaccion_id = Column(Integer, ForeignKey("transacciones.id"), nullable=True)
    desbloqueado_en = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CandidatoAcceso empresa={self.empresa_id} candidato={self.candidato_id}>"


# ============================================================================
# TABLA: Compras del candidato (estatus del proceso / resultados / análisis de CV)
#
# A diferencia de CandidatoAcceso (una empresa desbloqueando a un candidato),
# aquí el propio candidato paga por desbloquear algo sobre SÍ mismo. "tipo"
# es uno de "estatus", "resultados", "analisis_cv" (ver PRODUCTOS_CANDIDATO
# en dlocal_service.py).
# ============================================================================
class CandidatoCompra(Base):
    __tablename__ = "candidato_compras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidato_id = Column(String(50), ForeignKey("candidatos.id"), nullable=False)
    tipo = Column(String(30), nullable=False)
    transaccion_id = Column(Integer, ForeignKey("transacciones.id"), nullable=True)
    desbloqueado_en = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CandidatoCompra candidato={self.candidato_id} tipo={self.tipo}>"


# ============================================================================
# TABLA: Referencias laborales (verificación de referencias)
#
# El candidato aporta contactos de referencias (ex-jefes, colegas). El
# reclutador dispara un formulario corto por email a cada referencia -- el
# "token" es la capacidad de acceso al formulario público, igual que
# candidato_id funciona como capacidad para el flujo del candidato.
# ============================================================================
class Referencia(Base):
    __tablename__ = "referencias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidato_id = Column(String(50), ForeignKey("candidatos.id"), nullable=False)
    nombre = Column(String(150), nullable=False)
    telefono = Column(String(30), nullable=True)
    email = Column(String(150), nullable=True)
    relacion = Column(String(100), nullable=True)  # "Supervisor directo", "Compañero de trabajo", etc.
    token = Column(String(64), unique=True, nullable=False)

    enviado_en = Column(DateTime, nullable=True)
    respondido_en = Column(DateTime, nullable=True)
    calificacion_general = Column(Integer, nullable=True)  # 1-5
    recontrataria = Column(Boolean, nullable=True)
    comentarios = Column(Text, nullable=True)

    creado_en = Column(DateTime, default=datetime.utcnow)

    candidato = relationship("Candidato")

    def __repr__(self):
        return f"<Referencia {self.nombre} candidato={self.candidato_id} respondido={self.respondido_en is not None}>"


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
