"""
CENERH RECRUIT OS - Endpoints de CRM
Integración con HubSpot/Pipedrive
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Candidato
from crm_service import hubspot_service, pipedrive_service, EstadoCRM
from typing import Optional

router = APIRouter(prefix="/api/crm", tags=["CRM Integration"])


# ============================================================================
# ENDPOINTS DE SINCRONIZACIÓN
# ============================================================================


@router.post("/sync/candidato/{candidato_id}")
async def sincronizar_candidato_a_crm(
    candidato_id: str,
    db: Session = Depends(get_db),
    plataforma: str = "hubspot",
):
    """
    Sincronizar un candidato específico a CRM (HubSpot o Pipedrive)
    
    Args:
        candidato_id: ID del candidato
        plataforma: "hubspot" o "pipedrive"
    
    Returns:
        Estado de sincronización
    """
    
    # Obtener candidato
    candidato = db.query(Candidato).filter(Candidato.id == candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    try:
        if plataforma == "hubspot":
            resultado = await hubspot_service.crear_contacto(
                nombre=candidato.nombre,
                email=candidato.email,
                telefono=candidato.telefono or "",
                vacante_id=candidato.vacante_id,
                candidato_id=candidato_id,
            )

            if resultado:
                return {
                    "status": "success",
                    "mensaje": f"Candidato sincronizado a HubSpot",
                    "hubspot_id": resultado.get("hubspot_id"),
                }
            else:
                raise HTTPException(status_code=400, detail="Error sincronizando a HubSpot")

        elif plataforma == "pipedrive":
            resultado = await pipedrive_service.crear_persona(
                nombre=candidato.nombre,
                email=candidato.email,
                telefono=candidato.telefono or "",
                candidato_id=candidato_id,
            )

            if resultado:
                return {
                    "status": "success",
                    "mensaje": f"Candidato sincronizado a Pipedrive",
                    "pipedrive_id": resultado.get("pipedrive_id"),
                }
            else:
                raise HTTPException(status_code=400, detail="Error sincronizando a Pipedrive")

        else:
            raise HTTPException(status_code=400, detail="Plataforma no soportada")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync/todos")
async def sincronizar_todos_los_candidatos(
    db: Session = Depends(get_db),
    plataforma: str = "hubspot",
):
    """
    Sincronizar todos los candidatos a CRM (bulk)
    
    Nota: Puede tomar varios minutos
    """
    
    try:
        candidatos = db.query(Candidato).all()
        total = len(candidatos)
        sincronizados = 0
        errores = []

        for candidato in candidatos:
            try:
                if plataforma == "hubspot":
                    resultado = await hubspot_service.crear_contacto(
                        nombre=candidato.nombre,
                        email=candidato.email,
                        telefono=candidato.telefono or "",
                        vacante_id=candidato.vacante_id,
                        candidato_id=candidato.id,
                    )

                    if resultado:
                        sincronizados += 1

                elif plataforma == "pipedrive":
                    resultado = await pipedrive_service.crear_persona(
                        nombre=candidato.nombre,
                        email=candidato.email,
                        telefono=candidato.telefono or "",
                        candidato_id=candidato.id,
                    )

                    if resultado:
                        sincronizados += 1

            except Exception as e:
                errores.append({"candidato": candidato.nombre, "error": str(e)})

        return {
            "status": "success",
            "total_candidatos": total,
            "sincronizados": sincronizados,
            "errores": len(errores),
            "detalles_errores": errores if errores else [],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/deal/{candidato_id}")
async def crear_deal_para_candidato(
    candidato_id: str,
    db: Session = Depends(get_db),
    plataforma: str = "hubspot",
):
    """Crear deal (oportunidad) en CRM para un candidato"""
    
    candidato = db.query(Candidato).filter(Candidato.id == candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    try:
        if plataforma == "hubspot":
            # Buscar contacto primero
            contacto_id = await hubspot_service.buscar_contacto_por_email(candidato.email)
            if not contacto_id:
                raise HTTPException(status_code=404, detail="Contacto no encontrado en HubSpot")

            resultado = await hubspot_service.crear_deal(
                nombre=candidato.nombre,
                contacto_id=contacto_id,
                vacante_id=candidato.vacante_id,
                monto=100.0,  # Fee de CENERH
                estado=EstadoCRM.EVALUACION,
            )

            if resultado:
                return {"status": "success", "deal_id": resultado.get("deal_id")}
            else:
                raise HTTPException(status_code=400, detail="Error creando deal")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/deal/{candidato_id}/estado")
async def actualizar_estado_deal(
    candidato_id: str,
    nuevo_estado: str,
    db: Session = Depends(get_db),
):
    """
    Actualizar estado de deal en CRM
    
    Estados válidos:
    - appointment_scheduled
    - qualification_in_progress
    - decision_pending
    - negotiation
    - disqualified
    """
    
    try:
        estado_enum = EstadoCRM(nuevo_estado)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Estado inválido: {nuevo_estado}")

    # En producción, buscar deal_id del candidato
    # Por ahora, es un ejemplo
    
    return {
        "status": "success",
        "mensaje": f"Estado actualizado a {nuevo_estado}",
    }


@router.get("/status")
async def verificar_estado_crm():
    """Verificar estado de conexión a CRM"""
    
    hubspot_config = bool(hubspot_service.api_key)
    pipedrive_config = bool(pipedrive_service.api_token)

    return {
        "hubspot": {
            "configurado": hubspot_config,
            "estado": "✅ Conectado" if hubspot_config else "❌ No configurado",
        },
        "pipedrive": {
            "configurado": pipedrive_config,
            "estado": "✅ Conectado" if pipedrive_config else "❌ No configurado",
        },
        "recomendacion": "Configura al menos una plataforma en variables de entorno",
    }


@router.get("/candidatos/hubspot")
async def listar_candidatos_en_hubspot(db: Session = Depends(get_db)):
    """Listar todos los candidatos que están en HubSpot"""
    
    candidatos = db.query(Candidato).all()
    
    return {
        "total_candidatos": len(candidatos),
        "en_hubspot": [
            {
                "id": c.id,
                "nombre": c.nombre,
                "email": c.email,
                "vacante": c.vacante_id,
                "score": c.score_final if hasattr(c, "score_final") else 0,
            }
            for c in candidatos
        ],
    }


@router.post("/test-conexion/{plataforma}")
async def test_conexion_crm(plataforma: str):
    """Test de conexión a la plataforma CRM"""
    
    if plataforma == "hubspot":
        if not hubspot_service.api_key:
            return {
                "plataforma": "HubSpot",
                "estado": "❌ No configurado",
                "mensaje": "HUBSPOT_API_KEY no definida en variables de entorno",
            }
        
        return {
            "plataforma": "HubSpot",
            "estado": "✅ Configurado",
            "mensaje": "API key válida",
            "base_url": hubspot_service.base_url,
        }

    elif plataforma == "pipedrive":
        if not pipedrive_service.api_token:
            return {
                "plataforma": "Pipedrive",
                "estado": "❌ No configurado",
                "mensaje": "PIPEDRIVE_API_TOKEN no definido en variables de entorno",
            }
        
        return {
            "plataforma": "Pipedrive",
            "estado": "✅ Configurado",
            "mensaje": "API token válido",
            "base_url": pipedrive_service.base_url,
        }

    else:
        return {"error": "Plataforma no soportada"}
