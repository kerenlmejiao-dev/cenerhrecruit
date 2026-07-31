"""
admin_router.py - Endpoints administrativos protegidos por ADMIN_API_KEY.

Reutiliza los cargadores idempotentes de seed.py (cada uno hace
"if existing: continue" antes de insertar) para poder completar el
banco de tests/preguntas/assessment centers en cualquier entorno --
incluida producción -- sin necesitar acceso directo a la base de datos:
el propio servidor corre el seed usando su DATABASE_URL interno.
"""

from fastapi import APIRouter, Depends

from auth import require_admin
from database import SessionLocal
from models import (
    AssessmentCenter,
    AssessmentRespuesta,
    AssessmentScore,
    AuditLog,
    Candidato,
    CandidatoAcceso,
    CandidatoPerfil,
    CompatibilidadCandidato,
    Empresa,
    PesoVacante,
    PreguntaTest,
    RespuestaCandidata,
    ScoreCandidata,
    Suscripcion,
    TestPsicometrico,
    Transaccion,
    Usuario,
    Vacante,
    VacanteAssessment,
    VacanteTest,
)
import seed

router = APIRouter(prefix="/api/admin", tags=["Admin"], dependencies=[Depends(require_admin)])


@router.post("/seed-banco-completo")
def seed_banco_completo():
    session = SessionLocal()
    try:
        seed.cargar_tests(session)
        seed.cargar_preguntas_generales(session)
        seed.cargar_preguntas_roles_estrategicos(session)
        seed.cargar_competencias(session)
        seed.cargar_assessment_centers(session)
        seed.cargar_vacante_ejemplo(session)

        return {
            "tests": session.query(TestPsicometrico).count(),
            "preguntas": session.query(PreguntaTest).count(),
            "assessment_centers": session.query(AssessmentCenter).count(),
            "vacantes": session.query(Vacante).count(),
        }
    finally:
        session.close()


# Identificadores exactos de los datos creados durante las pruebas end-to-end
# en producción (ver conversación del 2026-07-31). Borrado acotado a solo
# estos registros -- ninguno más.
_EMAILS_CANDIDATOS_PRUEBA = [
    "prueba.candidato.deploy@example.com",
    "prueba.bolsa.deploy@example.com",
    "prueba.candidato.ventas.deploy@example.com",
]
_NOMBRES_VACANTES_PRUEBA = [
    "PRUEBA DEPLOY - Analista de Compras",
    "PRUEBA DEPLOY - Gerente de Ventas",
]
_EMAILS_USUARIOS_PRUEBA = [
    "prueba.empresa.deploy@example.com",
    "prueba.deploy.produccion@example.com",
]
_NOMBRE_EMPRESA_PRUEBA = "PRUEBA DEPLOY - Constructora Test"


@router.post("/limpiar-datos-prueba")
def limpiar_datos_prueba():
    session = SessionLocal()
    try:
        candidato_ids_sq = session.query(Candidato.id).filter(
            Candidato.email.in_(_EMAILS_CANDIDATOS_PRUEBA)
        ).scalar_subquery()
        vacante_ids_sq = session.query(Vacante.id).filter(
            Vacante.nombre.in_(_NOMBRES_VACANTES_PRUEBA)
        ).scalar_subquery()
        usuario_ids_sq = session.query(Usuario.id).filter(
            Usuario.email.in_(_EMAILS_USUARIOS_PRUEBA)
        ).scalar_subquery()
        empresa_ids_sq = session.query(Empresa.id).filter(
            Empresa.nombre == _NOMBRE_EMPRESA_PRUEBA
        ).scalar_subquery()

        borrados = {}

        # Hijas de candidatos primero (incluye transacciones.candidato_id,
        # que es FK real -- debe irse antes que la tabla candidatos).
        borrados["respuestas_candidatas"] = session.query(RespuestaCandidata).filter(
            RespuestaCandidata.candidato_id.in_(candidato_ids_sq)
        ).delete(synchronize_session=False)
        borrados["scores_candidatas"] = session.query(ScoreCandidata).filter(
            ScoreCandidata.candidato_id.in_(candidato_ids_sq)
        ).delete(synchronize_session=False)
        borrados["assessment_respuestas"] = session.query(AssessmentRespuesta).filter(
            AssessmentRespuesta.candidato_id.in_(candidato_ids_sq)
        ).delete(synchronize_session=False)
        borrados["assessment_scores"] = session.query(AssessmentScore).filter(
            AssessmentScore.candidato_id.in_(candidato_ids_sq)
        ).delete(synchronize_session=False)
        borrados["compatibilidad_candidatos"] = session.query(CompatibilidadCandidato).filter(
            CompatibilidadCandidato.candidato_id.in_(candidato_ids_sq)
        ).delete(synchronize_session=False)
        borrados["candidato_accesos"] = session.query(CandidatoAcceso).filter(
            CandidatoAcceso.candidato_id.in_(candidato_ids_sq)
            | CandidatoAcceso.empresa_id.in_(empresa_ids_sq)
        ).delete(synchronize_session=False)
        borrados["transacciones"] = session.query(Transaccion).filter(
            Transaccion.candidato_id.in_(candidato_ids_sq)
            | Transaccion.usuario_id.in_(usuario_ids_sq)
            | Transaccion.empresa_id.in_(empresa_ids_sq)
        ).delete(synchronize_session=False)
        borrados["candidato_perfil"] = session.query(CandidatoPerfil).filter(
            CandidatoPerfil.candidato_id.in_(candidato_ids_sq)
        ).delete(synchronize_session=False)
        borrados["audit_logs"] = session.query(AuditLog).filter(
            AuditLog.candidato_id.in_(candidato_ids_sq)
        ).delete(synchronize_session=False)

        borrados["candidatos"] = session.query(Candidato).filter(
            Candidato.email.in_(_EMAILS_CANDIDATOS_PRUEBA)
        ).delete(synchronize_session=False)

        # Hijas de vacantes
        borrados["vacante_tests"] = session.query(VacanteTest).filter(
            VacanteTest.vacante_id.in_(vacante_ids_sq)
        ).delete(synchronize_session=False)
        borrados["vacante_assessments"] = session.query(VacanteAssessment).filter(
            VacanteAssessment.vacante_id.in_(vacante_ids_sq)
        ).delete(synchronize_session=False)
        borrados["pesos_vacantes"] = session.query(PesoVacante).filter(
            PesoVacante.vacante_id.in_(vacante_ids_sq)
        ).delete(synchronize_session=False)

        borrados["vacantes"] = session.query(Vacante).filter(
            Vacante.nombre.in_(_NOMBRES_VACANTES_PRUEBA)
        ).delete(synchronize_session=False)

        borrados["suscripciones"] = session.query(Suscripcion).filter(
            Suscripcion.usuario_id.in_(usuario_ids_sq)
        ).delete(synchronize_session=False)

        borrados["usuarios"] = session.query(Usuario).filter(
            Usuario.email.in_(_EMAILS_USUARIOS_PRUEBA)
        ).delete(synchronize_session=False)

        borrados["empresas"] = session.query(Empresa).filter(
            Empresa.nombre == _NOMBRE_EMPRESA_PRUEBA
        ).delete(synchronize_session=False)

        session.commit()
        return borrados
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
