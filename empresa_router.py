"""
empresa_router.py - Portal Empresa (vistas de solo lectura, filtradas por empresa_id del JWT)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import dlocal_service
from auth_users import require_role
from database import get_db
from models import Candidato, CandidatoAcceso, Usuario, Vacante

router = APIRouter(
    prefix="/api/empresa",
    tags=["Portal Empresa"],
    dependencies=[Depends(require_role("owner", "empresa"))],
)


@router.get("/vacantes")
def listar_vacantes_empresa(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "empresa")),
):
    query = db.query(Vacante)
    if usuario.rol == "empresa":
        query = query.filter_by(empresa_id=usuario.empresa_id)

    vacantes = query.order_by(Vacante.creado_en.desc()).all()
    return {
        "vacantes": [
            {
                "id": v.id,
                "nombre": v.nombre,
                "cliente": v.cliente,
                "total_candidatos": len(v.candidatos),
            }
            for v in vacantes
        ]
    }


@router.get("/vacantes/{vacante_id}/candidatos")
def listar_candidatos_vacante_empresa(
    vacante_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "empresa")),
):
    vacante = db.query(Vacante).filter_by(id=vacante_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    if usuario.rol == "empresa" and vacante.empresa_id != usuario.empresa_id:
        raise HTTPException(status_code=403, detail="No autorizado para ver esta vacante")

    candidatos = db.query(Candidato).filter_by(vacante_id=vacante_id).order_by(Candidato.fecha_inicio.desc()).all()

    empresa_id = vacante.empresa_id
    accesos = set()
    if usuario.rol == "empresa" and empresa_id:
        accesos = {
            a.candidato_id
            for a in db.query(CandidatoAcceso).filter_by(empresa_id=empresa_id).all()
        }

    resultado = []
    for c in candidatos:
        desbloqueado = usuario.rol == "owner" or c.id in accesos

        if desbloqueado:
            resultado.append({
                "id": c.id,
                "nombre": c.nombre,
                "email": c.email,
                "estado": c.estado,
                "score_final": c.score_final,
                "clasificacion": c.clasificacion,
                "desbloqueado": True,
            })
        else:
            # Vista bloqueada: solo un perfil resumido, sin datos de contacto
            resultado.append({
                "id": c.id,
                "nombre": c.nombre[:1] + ".",  # inicial únicamente
                "estado": c.estado,
                "score_final": c.score_final,
                "clasificacion": c.clasificacion,
                "desbloqueado": False,
                "precio_desbloqueo": dlocal_service.PRECIO_DESBLOQUEO_CANDIDATO,
            })

    return {"candidatos": resultado}
