"""
reclutador_router.py - Portal Reclutador

Crear vacantes seleccionando tests/assessments del banco, ver candidatos
postulados y sus fichas. Protegido con JWT (rol owner o reclutador).
"""

import os
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

import compatibilidad_service
from auth_users import hash_password, require_membresia_activa, require_role
from database import get_db
from models import (
    AssessmentCenter,
    AssessmentPregunta,
    AssessmentRespuesta,
    AssessmentScore,
    Candidato,
    CandidatoPerfil,
    Empresa,
    Referencia,
    ScoreCandidata,
    TestPsicometrico,
    Usuario,
    Vacante,
    VacanteAssessment,
    VacanteTest,
)

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_CV_DIR = BASE_DIR / "uploads" / "cv"

# Todo el panel de reclutador exige membresía paga vigente (ningún plan es
# gratuito -- ver require_membresia_activa en auth_users.py). El owner queda
# exento.
router = APIRouter(
    prefix="/api/reclutador",
    tags=["Portal Reclutador"],
    dependencies=[Depends(require_membresia_activa)],
)


# ============================================================================
# BANCO DE TESTS / ASSESSMENTS (para el selector al crear una vacante)
# ============================================================================
@router.get("/banco/tests")
def listar_banco_tests(db: Session = Depends(get_db)):
    """Lista todos los tests del banco, agrupados por categoria_banco"""
    tests = db.query(TestPsicometrico).order_by(TestPsicometrico.categoria_banco, TestPsicometrico.nombre).all()

    agrupado: Dict[str, list] = {}
    for t in tests:
        categoria = t.categoria_banco or "Sin categoría"
        agrupado.setdefault(categoria, []).append({
            "id": t.id,
            "nombre": t.nombre,
            "descripcion": t.descripcion,
            "num_preguntas": t.num_preguntas,
            "tiempo_estimado": t.tiempo_estimado,
        })

    return {"categorias": agrupado}


@router.get("/banco/assessments")
def listar_banco_assessments(db: Session = Depends(get_db)):
    """Lista los assessment centers disponibles"""
    assessments = db.query(AssessmentCenter).filter_by(activo=True).all()
    return {
        "assessments": [
            {"id": a.id, "nombre": a.nombre, "descripcion": a.descripcion, "categoria": a.categoria}
            for a in assessments
        ]
    }


# ============================================================================
# EMPRESAS CLIENTE
#
# La empresa NO se autorregistra: el reclutador levanta su ficha (incluye
# datos de facturación) y le crea la cuenta de acceso al Portal Empresa en
# el mismo paso. Esto es distinto del autorregistro de reclutador.
# ============================================================================
class EmpresaCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    contacto_email: EmailStr
    password: str = Field(..., min_length=8)
    razon_social: Optional[str] = None
    tiene_rnc: bool = False
    rnc: Optional[str] = Field(default=None, max_length=30)


@router.post("/empresas")
def crear_empresa(
    payload: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    if payload.tiene_rnc and not (payload.rnc and payload.rnc.strip()):
        raise HTTPException(status_code=400, detail="Ingresa el RNC / comprobante fiscal")
    if db.query(Usuario).filter_by(email=payload.contacto_email).first():
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con este email")

    empresa = Empresa(
        nombre=payload.nombre,
        contacto_email=payload.contacto_email,
        razon_social=payload.razon_social,
        tiene_rnc=payload.tiene_rnc,
        rnc=payload.rnc if payload.tiene_rnc else None,
    )
    db.add(empresa)
    db.flush()

    usuario_empresa = Usuario(
        email=payload.contacto_email,
        password_hash=hash_password(payload.password),
        nombre=payload.nombre,
        rol="empresa",
        empresa_id=empresa.id,
    )
    db.add(usuario_empresa)
    db.commit()

    return {"status": "success", "empresa_id": empresa.id, "nombre": empresa.nombre, "usuario_email": usuario_empresa.email}


@router.get("/empresas")
def listar_empresas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    """Todas las empresas cliente activas, para elegir al crear una vacante."""
    empresas = db.query(Empresa).filter_by(activo=True).order_by(Empresa.nombre).all()
    return {
        "empresas": [
            {"id": e.id, "nombre": e.nombre, "tiene_rnc": e.tiene_rnc, "rnc": e.rnc}
            for e in empresas
        ]
    }


# ============================================================================
# VACANTES
# ============================================================================
class VacanteCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    cliente: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    requisitos: Optional[str] = None
    test_ids: List[str] = Field(default_factory=list)
    assessment_ids: List[int] = Field(default_factory=list)
    empresa_id: Optional[int] = None


@router.post("/vacantes")
def crear_vacante(
    payload: VacanteCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    if not payload.test_ids:
        raise HTTPException(status_code=400, detail="Selecciona al menos un test para la vacante")

    tests_validos = db.query(TestPsicometrico).filter(TestPsicometrico.id.in_(payload.test_ids)).all()
    if len(tests_validos) != len(set(payload.test_ids)):
        raise HTTPException(status_code=400, detail="Uno o más test_ids no existen en el banco")

    vacante = Vacante(
        id=f"vac_{uuid.uuid4().hex[:12]}",
        nombre=payload.nombre,
        cliente=payload.cliente,
        descripcion=payload.descripcion,
        requisitos=payload.requisitos,
        tests_a_aplicar=payload.test_ids,  # se mantiene por compatibilidad con el flujo de candidato actual
        pesos_scoring={"competencias": 0.35, "psicometricos": 0.35, "cognitivos": 0.30},
        empresa_id=payload.empresa_id,
        creado_por_usuario_id=usuario.id,
        estado="borrador",  # el proceso se abre en un paso aparte, cuando ya está lista
    )
    db.add(vacante)
    db.flush()

    for orden, test_id in enumerate(payload.test_ids):
        db.add(VacanteTest(vacante_id=vacante.id, test_id=test_id, orden=orden, obligatorio=True))

    for assessment_id in payload.assessment_ids:
        db.add(VacanteAssessment(vacante_id=vacante.id, assessment_id=assessment_id, obligatorio=True))

    db.commit()

    return {"status": "success", "vacante_id": vacante.id, "nombre": vacante.nombre}


ESTADOS_VACANTE_VALIDOS = ("borrador", "activa", "inactiva")


@router.post("/vacantes/{vacante_id}/estado")
def cambiar_estado_vacante(
    vacante_id: str,
    nuevo_estado: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    """Abre ("activa") o finaliza ("inactiva") el proceso de búsqueda de una
    vacante. Solo "activa" aparece en el listado público y acepta
    aplicaciones por el link directo."""
    if nuevo_estado not in ESTADOS_VACANTE_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Usa uno de: {', '.join(ESTADOS_VACANTE_VALIDOS)}")

    vacante = db.query(Vacante).filter_by(id=vacante_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    if usuario.rol != "owner" and vacante.creado_por_usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="No autorizado para modificar esta vacante")

    vacante.estado = nuevo_estado
    db.commit()

    return {"status": "success", "vacante_id": vacante.id, "estado": vacante.estado}


@router.get("/vacantes/{vacante_id}/sugerencias-bolsa")
def sugerencias_bolsa_talento_vacante(
    vacante_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    """Compara los candidatos de la Bolsa de Talento contra esta vacante y
    sugiere a quién invitar. No es una aplicación formal — es apoyo para que
    el reclutador decida a quién contactar."""
    if not compatibilidad_service.ANTHROPIC_API_KEY:
        raise HTTPException(status_code=503, detail="El análisis de compatibilidad con IA no está configurado todavía")

    vacante = db.query(Vacante).filter_by(id=vacante_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    if usuario.rol != "owner" and vacante.creado_por_usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="No autorizado para esta vacante")

    sugerencias = compatibilidad_service.sugerir_candidatos_bolsa(db, vacante)
    return {"sugerencias": sugerencias}


@router.get("/vacantes")
def listar_vacantes(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    query = db.query(Vacante)
    if usuario.rol != "owner":
        query = query.filter_by(creado_por_usuario_id=usuario.id)

    vacantes = query.order_by(Vacante.creado_en.desc()).all()
    return {
        "vacantes": [
            {
                "id": v.id,
                "nombre": v.nombre,
                "cliente": v.cliente,
                "total_tests": len(v.vacante_tests),
                "total_candidatos": len(v.candidatos),
                "estado": v.estado,
                "creado_en": v.creado_en.isoformat(),
            }
            for v in vacantes
        ]
    }


@router.get("/vacantes/{vacante_id}")
def detalle_vacante(
    vacante_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    vacante = db.query(Vacante).filter_by(id=vacante_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    if usuario.rol != "owner" and vacante.creado_por_usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="No autorizado para ver esta vacante")

    return {
        "id": vacante.id,
        "nombre": vacante.nombre,
        "cliente": vacante.cliente,
        "descripcion": vacante.descripcion,
        "requisitos": vacante.requisitos,
        "estado": vacante.estado,
        "tests": [
            {"id": vt.test.id, "nombre": vt.test.nombre, "orden": vt.orden}
            for vt in sorted(vacante.vacante_tests, key=lambda vt: (vt.orden if vt.orden is not None else 0))
        ],
        "assessments": [
            {"id": va.assessment.id, "nombre": va.assessment.nombre}
            for va in vacante.vacante_assessments
        ],
    }


@router.get("/vacantes/{vacante_id}/candidatos")
def listar_candidatos_vacante(
    vacante_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    vacante = db.query(Vacante).filter_by(id=vacante_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    if usuario.rol != "owner" and vacante.creado_por_usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="No autorizado para ver esta vacante")

    candidatos = db.query(Candidato).filter_by(vacante_id=vacante_id).order_by(Candidato.fecha_inicio.desc()).all()

    return {
        "candidatos": [
            {
                "id": c.id,
                "nombre": c.nombre,
                "email": c.email,
                "estado": c.estado,
                "score_final": c.score_final,
                "clasificacion": c.clasificacion,
                "fecha_inicio": c.fecha_inicio.isoformat() if c.fecha_inicio else None,
                "tiene_cv": bool(c.perfil and c.perfil.cv_storage_path),
                "status_reclutamiento": c.status_reclutamiento,
            }
            for c in candidatos
        ]
    }


# Etapas del proceso, en orden. El reclutador las asigna a mano; el candidato
# las ve en su página de resultados (ver /api/candidatos/{id}/resultados).
STATUS_RECLUTAMIENTO_VALIDOS = [
    "Aplicación recibida",
    "En evaluación",
    "Preseleccionado",
    "Entrevista",
    "Decisión final",
    "Contratado",
    "Rechazado",
]


@router.get("/metricas")
def metricas_reclutador(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    """Embudo de reclutamiento: cuántos candidatos hay en cada etapa, tasa de
    conversión a contratado, y tiempo promedio en completar la evaluación.
    El owner ve todas las vacantes; el reclutador solo las suyas."""
    query_vacantes = db.query(Vacante.id)
    if usuario.rol != "owner":
        query_vacantes = query_vacantes.filter(Vacante.creado_por_usuario_id == usuario.id)
    vacante_ids = [v.id for v in query_vacantes.all()]

    candidatos = (
        db.query(Candidato).filter(Candidato.vacante_id.in_(vacante_ids)).all()
        if vacante_ids else []
    )

    por_status = {etapa: 0 for etapa in STATUS_RECLUTAMIENTO_VALIDOS}
    for c in candidatos:
        if c.status_reclutamiento in por_status:
            por_status[c.status_reclutamiento] += 1

    total = len(candidatos)
    contratados = por_status.get("Contratado", 0)
    rechazados = por_status.get("Rechazado", 0)

    dias_evaluacion = [
        (c.fecha_completitud - c.fecha_inicio).total_seconds() / 86400
        for c in candidatos if c.fecha_completitud and c.fecha_inicio
    ]
    promedio_dias_evaluacion = round(sum(dias_evaluacion) / len(dias_evaluacion), 1) if dias_evaluacion else None

    return {
        "total_vacantes": len(vacante_ids),
        "total_candidatos": total,
        "por_status": por_status,
        "tasa_conversion_contratado": round(contratados / total * 100, 1) if total else 0.0,
        "tasa_rechazo": round(rechazados / total * 100, 1) if total else 0.0,
        "promedio_dias_evaluacion": promedio_dias_evaluacion,
    }


class StatusReclutamientoPayload(BaseModel):
    status: str


@router.post("/candidatos/{candidato_id}/status")
def cambiar_status_reclutamiento(
    candidato_id: str,
    payload: StatusReclutamientoPayload,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    if payload.status not in STATUS_RECLUTAMIENTO_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Status inválido. Usa uno de: {', '.join(STATUS_RECLUTAMIENTO_VALIDOS)}")

    candidato = _validar_propietario_candidato(db, candidato_id, usuario)
    candidato.status_reclutamiento = payload.status
    db.commit()

    if candidato.telefono:
        import whatsapp_service

        nombre_vacante = candidato.vacante.nombre if candidato.vacante else "tu proceso con nosotros"
        whatsapp_service.notificar_cambio_status(candidato.telefono, candidato.nombre, payload.status, nombre_vacante)

    return {"status": "success", "candidato_id": candidato.id, "status_reclutamiento": candidato.status_reclutamiento}


@router.get("/candidatos/bolsa-talento")
def listar_bolsa_talento(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    """Candidatos que completaron su perfil sin aplicar a una vacante todavía.
    No pertenecen a ningún reclutador en particular, así que cualquier
    reclutador con sesión puede verlos (no hay vacante que filtre por dueño)."""
    candidatos = (
        db.query(Candidato)
        .filter(Candidato.vacante_id.is_(None))
        .order_by(Candidato.fecha_inicio.desc())
        .all()
    )
    return {
        "candidatos": [
            {
                "id": c.id,
                "nombre": c.nombre,
                "email": c.email,
                "telefono": c.telefono,
                "fecha_inicio": c.fecha_inicio.isoformat() if c.fecha_inicio else None,
                "tiene_cv": bool(c.perfil and c.perfil.cv_storage_path),
                "ciudad_provincia": c.perfil.ciudad_provincia if c.perfil else None,
                "ultimo_cargo": c.perfil.ultimo_cargo if c.perfil else None,
            }
            for c in candidatos
        ]
    }


# ============================================================================
# Acceso a datos de un candidato específico (ficha, CV, assessment centers).
# El reclutador solo puede ver candidatos de vacantes que él mismo creó; el
# owner ve todo. La membresía activa ya se exige a nivel de todo el router
# (ver require_membresia_activa arriba), así que aquí solo queda validar
# la propiedad del candidato.
# ============================================================================
def _validar_propietario_candidato(db: Session, candidato_id: str, usuario: Usuario) -> Candidato:
    candidato = db.query(Candidato).filter_by(id=candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    # Bolsa de talento (sin vacante): no pertenece a ningún reclutador en
    # particular, cualquiera con sesión puede verlo.
    if candidato.vacante_id is None:
        return candidato

    vacante = db.query(Vacante).filter_by(id=candidato.vacante_id).first()
    if usuario.rol != "owner" and (not vacante or vacante.creado_por_usuario_id != usuario.id):
        raise HTTPException(status_code=403, detail="No autorizado para ver este candidato")

    return candidato


@router.get("/candidatos/{candidato_id}/cv")
def descargar_cv_candidato(
    candidato_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    """Descarga el CV original (PDF/DOC/DOCX) que subió el candidato."""
    _validar_propietario_candidato(db, candidato_id, usuario)

    perfil = db.query(CandidatoPerfil).filter_by(candidato_id=candidato_id).first()
    if not perfil or not perfil.cv_storage_path:
        raise HTTPException(status_code=404, detail="Este candidato no ha subido un CV")

    ruta_absoluta = (BASE_DIR / perfil.cv_storage_path).resolve()
    if UPLOADS_CV_DIR.resolve() not in ruta_absoluta.parents or not ruta_absoluta.is_file():
        raise HTTPException(status_code=404, detail="El archivo del CV ya no existe en el servidor")

    return FileResponse(path=str(ruta_absoluta), filename=perfil.cv_filename or ruta_absoluta.name)


# ============================================================================
# ASSESSMENT CENTERS: revisión humana de las respuestas puntuadas por IA
#
# El score de IA no debe usarse ciego para contratar (ver AssessmentScore en
# models.py), así que el reclutador dueño de la vacante puede leer la
# respuesta del candidato y el análisis de la IA antes de decidir.
# ============================================================================


@router.get("/candidatos/{candidato_id}/assessments")
def listar_assessments_candidato_reclutador(
    candidato_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    candidato = _validar_propietario_candidato(db, candidato_id, usuario)

    respuestas = db.query(AssessmentRespuesta).filter_by(candidato_id=candidato_id).all()
    preguntas_por_id = {
        p.id: p
        for p in db.query(AssessmentPregunta)
        .filter(AssessmentPregunta.id.in_([r.assessment_pregunta_id for r in respuestas]))
        .all()
    }
    scores_por_assessment = {
        s.assessment_id: s
        for s in db.query(AssessmentScore).filter_by(candidato_id=candidato_id).all()
    }

    resultado = []
    for r in respuestas:
        pregunta = preguntas_por_id.get(r.assessment_pregunta_id)
        if not pregunta:
            continue
        score = scores_por_assessment.get(pregunta.assessment_id)
        resultado.append({
            "assessment_id": pregunta.assessment_id,
            "nombre": pregunta.assessment.nombre,
            "categoria": pregunta.assessment.categoria,
            "escenario": pregunta.escenario,
            "respuesta_texto": r.respuesta_texto,
            "respondido_en": r.respondido_en.isoformat() if r.respondido_en else None,
            "score_ia": score.score_normalizado if score else None,
            "feedback_ia": score.feedback_llm if score else None,
            "criterios_detalle": score.criterios_detalle if score else None,
            "revisado_por_humano": score.revisado_por_humano if score else False,
        })

    compat = compatibilidad_service.obtener_o_calcular_compatibilidad(db, candidato_id)
    compatibilidad = None
    if compat:
        compatibilidad = {
            "score": compat.score_compatibilidad,
            "resumen": compat.resumen,
            "fortalezas": compat.fortalezas,
            "brechas": compat.brechas,
            "calculado_en": compat.calculado_en.isoformat() if compat.calculado_en else None,
        }

    return {"candidato_id": candidato.id, "assessments": resultado, "compatibilidad": compatibilidad}


@router.post("/candidatos/{candidato_id}/assessments/{assessment_id}/marcar-revisado")
def marcar_assessment_revisado(
    candidato_id: str,
    assessment_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    _validar_propietario_candidato(db, candidato_id, usuario)

    score = db.query(AssessmentScore).filter_by(candidato_id=candidato_id, assessment_id=assessment_id).first()
    if not score:
        raise HTTPException(status_code=404, detail="Este assessment aún no ha sido puntuado por la IA")

    score.revisado_por_humano = True
    db.commit()

    return {"status": "success", "candidato_id": candidato_id, "assessment_id": assessment_id, "revisado_por_humano": True}


# ============================================================================
# VERIFICACIÓN DE REFERENCIAS
#
# El candidato carga sus referencias al completar el perfil (ver
# candidato_router.py). Aquí el reclutador dispara el correo con el link al
# formulario público (token-based, ver /api/referencias/{token} en api.py) y
# revisa las respuestas ya recibidas.
# ============================================================================
@router.get("/candidatos/{candidato_id}/referencias")
def listar_referencias_reclutador(
    candidato_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    _validar_propietario_candidato(db, candidato_id, usuario)

    referencias = db.query(Referencia).filter_by(candidato_id=candidato_id).order_by(Referencia.id).all()
    return {
        "referencias": [
            {
                "id": r.id,
                "nombre": r.nombre,
                "telefono": r.telefono,
                "email": r.email,
                "relacion": r.relacion,
                "enviado_en": r.enviado_en.isoformat() if r.enviado_en else None,
                "respondido_en": r.respondido_en.isoformat() if r.respondido_en else None,
                "calificacion_general": r.calificacion_general,
                "recontrataria": r.recontrataria,
                "comentarios": r.comentarios,
            }
            for r in referencias
        ]
    }


@router.post("/candidatos/{candidato_id}/referencias/{referencia_id}/enviar")
def enviar_solicitud_referencia(
    candidato_id: str,
    referencia_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    candidato = _validar_propietario_candidato(db, candidato_id, usuario)

    referencia = db.query(Referencia).filter_by(id=referencia_id, candidato_id=candidato_id).first()
    if not referencia:
        raise HTTPException(status_code=404, detail="Referencia no encontrada")
    if not referencia.email:
        raise HTTPException(status_code=400, detail="Esta referencia no tiene email registrado")

    from datetime import datetime as _datetime

    from email_sender import EnviadorEmail

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    link_formulario = f"{frontend_url}/referencia/{referencia.token}"

    resultado = EnviadorEmail.enviar_solicitud_referencia(
        email_destinatario=referencia.email,
        nombre_referencia=referencia.nombre,
        nombre_candidato=candidato.nombre,
        link_formulario=link_formulario,
    )
    if resultado["status"] != "success":
        raise HTTPException(status_code=500, detail=resultado["mensaje"])

    referencia.enviado_en = _datetime.utcnow()
    db.commit()

    return {"status": "success", "referencia_id": referencia_id, "modo_envio": resultado.get("modo")}
