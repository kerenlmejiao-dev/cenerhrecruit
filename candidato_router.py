"""
candidato_router.py - Flujo extendido de candidato: cuestionario dinámico,
subida de CV, y assessment centers (respuesta abierta evaluada por IA).

Sigue el mismo patrón de acceso que el resto del flujo de candidato: sin
login, candidato_id como token de capacidad (ver api.py).
"""

import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import (
    AssessmentPregunta,
    AssessmentRespuesta,
    Candidato,
    CandidatoPerfil,
    Vacante,
    VacanteAssessment,
)

router = APIRouter(prefix="/api/candidatos", tags=["Candidato - Perfil y Assessments"])

UPLOADS_DIR = Path(__file__).resolve().parent / "uploads" / "cv"
TIPOS_CV_PERMITIDOS = {".pdf", ".doc", ".docx"}
MAX_CV_BYTES = 5 * 1024 * 1024  # 5 MB


class CuestionarioPayload(BaseModel):
    pretension_salarial: Optional[str] = None
    ubicacion: Optional[str] = None
    tiene_vehiculo: Optional[bool] = None
    tiene_visa: Optional[bool] = None
    disponibilidad: Optional[str] = None

    # Datos personales
    cedula: Optional[str] = None
    edad: Optional[int] = None
    estado_civil: Optional[str] = None
    cantidad_hijos: Optional[int] = None
    edades_hijos: Optional[str] = None

    # Domicilio
    ciudad_provincia: Optional[str] = None
    direccion_exacta: Optional[str] = None

    # Formación académica
    nivel_academico: Optional[str] = None
    carrera: Optional[str] = None
    universidad: Optional[str] = None

    # Experiencia laboral
    anos_experiencia: Optional[int] = None
    ultimo_cargo: Optional[str] = None
    ultimo_salario: Optional[str] = None
    funciones_ultimo_empleo: Optional[str] = None

    # Contexto de la aplicación
    fuente_reclutamiento: Optional[str] = None
    posiciones_interes: Optional[str] = None
    contacto_emergencia_nombre: Optional[str] = None
    contacto_emergencia_telefono: Optional[str] = None


def _get_or_crear_perfil(db: Session, candidato_id: str) -> CandidatoPerfil:
    perfil = db.query(CandidatoPerfil).filter_by(candidato_id=candidato_id).first()
    if not perfil:
        perfil = CandidatoPerfil(candidato_id=candidato_id)
        db.add(perfil)
    return perfil


@router.get("/{candidato_id}/cuestionario")
def obtener_cuestionario(candidato_id: str, db: Session = Depends(get_db)):
    """Devuelve el perfil ya guardado de este candidato (si existe), para
    precargar el formulario: útil cuando reaplica a otra vacante (el perfil
    se copia automáticamente al crear el candidato, ver api.py) o cuando
    quiere corregir/actualizar sus propios datos."""
    candidato = db.query(Candidato).filter_by(id=candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail=f"Candidato '{candidato_id}' no encontrado")

    perfil = db.query(CandidatoPerfil).filter_by(candidato_id=candidato_id).first()
    if not perfil:
        return {"perfil": None}

    campos = list(CuestionarioPayload.model_fields.keys())
    return {
        "perfil": {campo: getattr(perfil, campo) for campo in campos},
        "cv_filename": perfil.cv_filename,
    }


@router.post("/{candidato_id}/cuestionario")
def guardar_cuestionario(
    candidato_id: str,
    payload: CuestionarioPayload,
    db: Session = Depends(get_db),
):
    candidato = db.query(Candidato).filter_by(id=candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail=f"Candidato '{candidato_id}' no encontrado")

    perfil = _get_or_crear_perfil(db, candidato_id)
    # exclude_unset: solo pisa los campos que realmente vengan en el body.
    # Si se usara model_dump() a secas, cualquier campo omitido (Optional=None
    # por default) borraría el valor ya guardado del candidato.
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(perfil, campo, valor)

    db.commit()
    return {"status": "success", "candidato_id": candidato_id}


@router.post("/{candidato_id}/cv")
async def subir_cv(
    candidato_id: str,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    candidato = db.query(Candidato).filter_by(id=candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail=f"Candidato '{candidato_id}' no encontrado")

    extension = Path(archivo.filename or "").suffix.lower()
    if extension not in TIPOS_CV_PERMITIDOS:
        raise HTTPException(status_code=400, detail="Formato no permitido. Usa PDF, DOC o DOCX")

    contenido = await archivo.read()
    if len(contenido) > MAX_CV_BYTES:
        raise HTTPException(status_code=400, detail="El archivo excede el tamaño máximo (5 MB)")

    carpeta_candidato = UPLOADS_DIR / candidato_id
    carpeta_candidato.mkdir(parents=True, exist_ok=True)

    nombre_guardado = f"{uuid.uuid4().hex[:8]}{extension}"
    ruta_destino = carpeta_candidato / nombre_guardado
    ruta_destino.write_bytes(contenido)

    perfil = _get_or_crear_perfil(db, candidato_id)
    perfil.cv_filename = archivo.filename
    perfil.cv_storage_path = str(ruta_destino.relative_to(Path(__file__).resolve().parent))

    db.commit()
    return {"status": "success", "candidato_id": candidato_id, "cv_filename": archivo.filename}


@router.get("/{candidato_id}/assessments")
def listar_assessments_candidato(candidato_id: str, db: Session = Depends(get_db)):
    """Lista los assessment centers (con su escenario) asignados a la vacante del candidato"""
    candidato = db.query(Candidato).filter_by(id=candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail=f"Candidato '{candidato_id}' no encontrado")

    vacante_assessments = db.query(VacanteAssessment).filter_by(vacante_id=candidato.vacante_id).all()

    resultado = []
    for va in vacante_assessments:
        preguntas = db.query(AssessmentPregunta).filter_by(assessment_id=va.assessment_id).order_by(AssessmentPregunta.numero).all()
        resultado.append({
            "assessment_id": va.assessment_id,
            "nombre": va.assessment.nombre,
            "categoria": va.assessment.categoria,
            "preguntas": [{"id": p.id, "numero": p.numero, "escenario": p.escenario} for p in preguntas],
        })

    return {"candidato_id": candidato_id, "assessments": resultado}


class AssessmentRespuestaPayload(BaseModel):
    respuesta_texto: str


@router.post("/{candidato_id}/assessments/preguntas/{pregunta_id}/respuesta")
def guardar_respuesta_assessment(
    candidato_id: str,
    pregunta_id: int,
    payload: AssessmentRespuestaPayload,
    db: Session = Depends(get_db),
):
    candidato = db.query(Candidato).filter_by(id=candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail=f"Candidato '{candidato_id}' no encontrado")

    pregunta = db.query(AssessmentPregunta).filter_by(id=pregunta_id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta de assessment no encontrada")

    if not payload.respuesta_texto or not payload.respuesta_texto.strip():
        raise HTTPException(status_code=400, detail="La respuesta no puede estar vacía")

    existente = db.query(AssessmentRespuesta).filter_by(
        candidato_id=candidato_id, assessment_pregunta_id=pregunta_id
    ).first()

    if existente:
        existente.respuesta_texto = payload.respuesta_texto
    else:
        db.add(AssessmentRespuesta(
            candidato_id=candidato_id,
            assessment_pregunta_id=pregunta_id,
            respuesta_texto=payload.respuesta_texto,
        ))

    db.commit()
    return {"status": "success"}
