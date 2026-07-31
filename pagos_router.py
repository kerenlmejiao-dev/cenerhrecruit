"""
pagos_router.py - Endpoints de pago (dLocal): suscripción de reclutadores
(renovación manual mensual) y desbloqueo de candidatos (Portal Empresa).

Incluye el webhook de dLocal y un endpoint de verificación manual de estado
(útil en desarrollo local, donde dLocal no puede alcanzar un webhook en
localhost sin un túnel público).
"""

import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

import dlocal_service
from auth_users import require_role
from database import get_db
from models import Candidato, CandidatoAcceso, Suscripcion, Transaccion, Usuario, Vacante

router = APIRouter(prefix="/api", tags=["Pagos"])


def _requiere_dlocal():
    if not dlocal_service.dlocal_configurado():
        raise HTTPException(
            status_code=503,
            detail="dLocal no está configurado (faltan DLOCAL_X_LOGIN/DLOCAL_X_TRANS_KEY/DLOCAL_SECRET_KEY en .env). Los pagos están deshabilitados.",
        )


def _procesar_resultado_pago(db: Session, transaccion: Transaccion, estado_dlocal: str) -> str:
    """Aplica el efecto de negocio (activar suscripción / desbloquear candidato)
    una sola vez, cuando el pago pasa a PAID. Idempotente: si ya estaba
    completada, no repite el efecto. Retorna el estado final aplicado."""
    if transaccion.estado == "completada":
        return transaccion.estado

    if estado_dlocal == "PAID":
        transaccion.estado = "completada"

        if transaccion.tipo == "suscripcion":
            suscripcion = db.query(Suscripcion).filter_by(usuario_id=transaccion.usuario_id).first()
            if suscripcion:
                suscripcion.estado = "activa"
                suscripcion.fecha_inicio = suscripcion.fecha_inicio or datetime.utcnow()
                base = suscripcion.fecha_renovacion if (suscripcion.fecha_renovacion and suscripcion.fecha_renovacion > datetime.utcnow()) else datetime.utcnow()
                suscripcion.fecha_renovacion = base + timedelta(days=30)

        elif transaccion.tipo == "desbloqueo_candidato":
            existente = db.query(CandidatoAcceso).filter_by(
                empresa_id=transaccion.empresa_id, candidato_id=transaccion.candidato_id
            ).first()
            if not existente:
                db.add(CandidatoAcceso(
                    empresa_id=transaccion.empresa_id,
                    candidato_id=transaccion.candidato_id,
                    transaccion_id=transaccion.id,
                ))

        db.commit()

    elif estado_dlocal in ("REJECTED", "CANCELLED", "EXPIRED"):
        transaccion.estado = "fallida"
        db.commit()

    return transaccion.estado


# ============================================================================
# SUSCRIPCIÓN DE RECLUTADORES (renovación manual)
# ============================================================================
@router.get("/reclutador/suscripcion")
def obtener_suscripcion(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    suscripcion = db.query(Suscripcion).filter_by(usuario_id=usuario.id).order_by(Suscripcion.creado_en.desc()).first()
    planes = [
        {"id": pid, "nombre": p["nombre"], "precio_mensual": p["precio_mensual"]}
        for pid, p in dlocal_service.PLANES_SUSCRIPCION.items()
    ]

    if not suscripcion:
        return {"suscripcion": None, "planes_disponibles": planes}

    # Marcar como vencida si la fecha de renovación ya pasó
    if suscripcion.estado == "activa" and suscripcion.fecha_renovacion and suscripcion.fecha_renovacion < datetime.utcnow():
        suscripcion.estado = "vencida"
        db.commit()

    return {
        "suscripcion": {
            "plan": suscripcion.plan,
            "estado": suscripcion.estado,
            "precio_mensual": suscripcion.precio_mensual,
            "fecha_renovacion": suscripcion.fecha_renovacion.isoformat() if suscripcion.fecha_renovacion else None,
            "renovacion_automatica": suscripcion.renovacion_automatica,
        },
        "planes_disponibles": planes,
    }


class RenovacionAutomaticaPayload(BaseModel):
    activar: bool


@router.post("/reclutador/suscripcion/renovacion-automatica")
def cambiar_renovacion_automatica(
    payload: RenovacionAutomaticaPayload,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    """Activa/desactiva la preferencia de renovación automática.

    NOTA: esto solo guarda la preferencia. El cobro recurrente real todavía
    no está implementado (depende de qué producto de dLocal se use para
    cargos recurrentes/tokenización); mientras tanto, toda renovación sigue
    siendo manual vía /reclutador/suscripcion/checkout, sin importar este flag.
    """
    suscripcion = db.query(Suscripcion).filter_by(usuario_id=usuario.id).order_by(Suscripcion.creado_en.desc()).first()
    if not suscripcion:
        raise HTTPException(status_code=404, detail="No tienes una suscripción todavía")

    suscripcion.renovacion_automatica = payload.activar
    db.commit()

    return {"status": "success", "renovacion_automatica": suscripcion.renovacion_automatica}


class CheckoutSuscripcionPayload(BaseModel):
    documento: str | None = None


@router.post("/reclutador/suscripcion/checkout")
def crear_checkout_suscripcion(
    plan: str,
    payload: CheckoutSuscripcionPayload,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador")),
):
    _requiere_dlocal()
    if plan not in dlocal_service.PLANES_SUSCRIPCION:
        raise HTTPException(status_code=400, detail=f"Plan '{plan}' no existe")

    if payload.documento:
        usuario.documento = payload.documento
        db.commit()
    if not usuario.documento:
        raise HTTPException(status_code=400, detail="Falta la cédula/RNC para procesar el pago")

    if not db.query(Suscripcion).filter_by(usuario_id=usuario.id).first():
        db.add(Suscripcion(usuario_id=usuario.id, plan=plan, precio_mensual=dlocal_service.PLANES_SUSCRIPCION[plan]["precio_mensual"]))
        db.commit()

    order_id = f"sub-{usuario.id}-{plan}-{uuid.uuid4().hex[:10]}"
    transaccion = Transaccion(
        tipo="suscripcion", usuario_id=usuario.id,
        monto=dlocal_service.PLANES_SUSCRIPCION[plan]["precio_mensual"],
        order_id=order_id,
    )
    db.add(transaccion)
    db.commit()

    try:
        resultado = dlocal_service.crear_checkout_suscripcion(usuario.nombre, usuario.email, usuario.documento, plan, order_id)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    transaccion.dlocal_payment_id = resultado.get("id")
    db.commit()

    return {"checkout_url": resultado.get("redirect_url"), "order_id": order_id}


# ============================================================================
# DESBLOQUEO DE CANDIDATOS (Portal Empresa)
# ============================================================================
@router.get("/empresa/candidatos/{candidato_id}/acceso")
def verificar_acceso_candidato(
    candidato_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "empresa")),
):
    if usuario.rol == "owner":
        return {"desbloqueado": True}

    acceso = db.query(CandidatoAcceso).filter_by(empresa_id=usuario.empresa_id, candidato_id=candidato_id).first()
    return {"desbloqueado": acceso is not None, "precio": dlocal_service.PRECIO_DESBLOQUEO_CANDIDATO}


class CheckoutDesbloqueoPayload(BaseModel):
    documento: str | None = None


@router.post("/empresa/candidatos/{candidato_id}/desbloquear")
def desbloquear_candidato(
    candidato_id: str,
    payload: CheckoutDesbloqueoPayload,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "empresa")),
):
    _requiere_dlocal()
    if usuario.rol != "empresa":
        raise HTTPException(status_code=400, detail="Solo cuentas de empresa pueden desbloquear candidatos")

    candidato = db.query(Candidato).filter_by(id=candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    vacante = db.query(Vacante).filter_by(id=candidato.vacante_id).first()
    if not vacante or vacante.empresa_id != usuario.empresa_id:
        raise HTTPException(status_code=403, detail="Este candidato no pertenece a una vacante de tu empresa")

    existente = db.query(CandidatoAcceso).filter_by(empresa_id=usuario.empresa_id, candidato_id=candidato_id).first()
    if existente:
        return {"status": "ya_desbloqueado"}

    if payload.documento:
        usuario.documento = payload.documento
        db.commit()
    if not usuario.documento:
        raise HTTPException(status_code=400, detail="Falta la cédula/RNC para procesar el pago")

    order_id = f"unlock-{usuario.empresa_id}-{candidato_id}-{uuid.uuid4().hex[:10]}"
    transaccion = Transaccion(
        tipo="desbloqueo_candidato", empresa_id=usuario.empresa_id, candidato_id=candidato_id,
        monto=dlocal_service.PRECIO_DESBLOQUEO_CANDIDATO,
        order_id=order_id,
    )
    db.add(transaccion)
    db.commit()

    try:
        resultado = dlocal_service.crear_checkout_desbloqueo(usuario.nombre, usuario.email, usuario.documento, candidato.nombre, order_id)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    transaccion.dlocal_payment_id = resultado.get("id")
    db.commit()

    return {"checkout_url": resultado.get("redirect_url"), "order_id": order_id}


# ============================================================================
# ESTADO DE UNA TRANSACCIÓN (usado por la página de resultado + respaldo sin webhook)
# ============================================================================
@router.get("/pagos/estado/{order_id}")
def estado_transaccion(
    order_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador", "empresa")),
):
    transaccion = db.query(Transaccion).filter_by(order_id=order_id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    if transaccion.estado == "pendiente" and transaccion.dlocal_payment_id and dlocal_service.dlocal_configurado():
        try:
            info = dlocal_service.consultar_pago(transaccion.dlocal_payment_id)
            _procesar_resultado_pago(db, transaccion, info.get("status", ""))
        except Exception:
            pass  # Si dLocal no responde, se deja pendiente; el webhook lo resolverá después

    return {"order_id": order_id, "tipo": transaccion.tipo, "estado": transaccion.estado, "monto": transaccion.monto}


# ============================================================================
# WEBHOOK DE DLOCAL
# ============================================================================
@router.post("/webhooks/dlocal")
async def webhook_dlocal(request: Request, db: Session = Depends(get_db)):
    raw_body = (await request.body()).decode("utf-8")
    x_date = request.headers.get("x-date", "")
    authorization = request.headers.get("authorization", "")

    if not dlocal_service.verificar_notificacion(x_date, authorization, raw_body):
        raise HTTPException(status_code=400, detail="Firma de notificación inválida")

    data = await request.json()
    order_id = data.get("order_id")
    estado_dlocal = data.get("status", "")

    transaccion = db.query(Transaccion).filter_by(order_id=order_id).first()
    if not transaccion:
        return {"status": "ok"}  # Notificación de un pago que no reconocemos; se ignora

    if not transaccion.dlocal_payment_id:
        transaccion.dlocal_payment_id = data.get("id")

    _procesar_resultado_pago(db, transaccion, estado_dlocal)

    return {"status": "ok"}
