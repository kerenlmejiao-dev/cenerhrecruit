"""
pagos_router.py - Endpoints de pago (dLocal): suscripción de reclutadores
(renovación manual mensual), desbloqueo de candidatos (Portal Empresa), y
compras del propio candidato sobre sí mismo (estatus del proceso, resultados,
análisis de CV).

Incluye el webhook de dLocal y un endpoint de verificación manual de estado
(útil en desarrollo local, donde dLocal no puede alcanzar un webhook en
localhost sin un túnel público).
"""

import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

import cv_parser_service
import dlocal_service
import reporte_candidato_service
from auth_users import require_role
from database import get_db
from models import (
    AssessmentScore,
    Candidato,
    CandidatoAcceso,
    CandidatoCompra,
    CandidatoPerfil,
    ScoreCandidata,
    Suscripcion,
    Transaccion,
    Usuario,
    Vacante,
)
from scoring import SistemaScoring

router = APIRouter(prefix="/api", tags=["Pagos"])


@router.get("/planes")
def listar_planes_publico():
    """Planes de membresía, públicos (sin login) -- para la página de
    comparación que se enlaza desde el registro de reclutador.

    No incluye la duración del ciclo de membresía (dato interno, ver
    dlocal_service.DURACION_MEMBRESIA_DIAS) -- eso no se comunica en
    ninguna página pública."""
    return {
        "planes": [
            {
                "id": pid,
                "nombre": p["nombre"],
                "precio_mensual": p["precio_mensual"],
                "para": p.get("para"),
                "caracteristicas": p.get("caracteristicas", []),
            }
            for pid, p in dlocal_service.PLANES_SUSCRIPCION.items()
        ],
    }


def _requiere_dlocal():
    if not dlocal_service.dlocal_configurado():
        raise HTTPException(
            status_code=503,
            detail="dLocal no está configurado (faltan DLOCALGO_API_KEY/DLOCALGO_SECRET_KEY en .env). Los pagos están deshabilitados.",
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
                suscripcion.fecha_renovacion = base + timedelta(days=dlocal_service.DURACION_MEMBRESIA_DIAS)

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

        elif transaccion.tipo in ("estatus_candidato", "resultados_candidato", "analisis_cv_candidato"):
            tipo_compra = transaccion.tipo.removesuffix("_candidato")
            existente = db.query(CandidatoCompra).filter_by(
                candidato_id=transaccion.candidato_id, tipo=tipo_compra
            ).first()
            if not existente:
                db.add(CandidatoCompra(
                    candidato_id=transaccion.candidato_id,
                    tipo=tipo_compra,
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
        {
            "id": pid,
            "nombre": p["nombre"],
            "precio_mensual": p["precio_mensual"],
            "para": p.get("para"),
            "caracteristicas": p.get("caracteristicas", []),
        }
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
# PAGOS DE CANDIDATOS (estatus del proceso / resultados / análisis de CV)
#
# A diferencia de la suscripción y el desbloqueo (donde paga el reclutador o
# la empresa), aquí el candidato paga por desbloquear algo sobre sí mismo.
# Requiere que el candidato tenga sesión iniciada (rol "candidato") y que la
# aplicación le pertenezca -- ver crear_candidato en api.py, que ya le da
# sesión automáticamente al aplicar.
# ============================================================================
def _validar_propietario_candidato(db: Session, candidato_id: str, usuario: Usuario) -> Candidato:
    candidato = db.query(Candidato).filter_by(id=candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    if candidato.email != usuario.email:
        raise HTTPException(status_code=403, detail="Esta aplicación no te pertenece")
    return candidato


@router.get("/candidatos/{candidato_id}/compras")
def obtener_compras_candidato(
    candidato_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("candidato")),
):
    _validar_propietario_candidato(db, candidato_id, usuario)
    tipos_desbloqueados = {
        c.tipo for c in db.query(CandidatoCompra).filter_by(candidato_id=candidato_id).all()
    }
    return {
        "estatus": "estatus" in tipos_desbloqueados,
        "resultados": "resultados" in tipos_desbloqueados,
        "analisis_cv": "analisis_cv" in tipos_desbloqueados,
        "precios": {tipo: p["precio"] for tipo, p in dlocal_service.PRODUCTOS_CANDIDATO.items()},
    }


class CheckoutCandidatoPayload(BaseModel):
    tipo: str  # "estatus" | "resultados" | "analisis_cv"
    documento: str | None = None


@router.post("/candidatos/{candidato_id}/pagos/checkout")
def crear_checkout_candidato(
    candidato_id: str,
    payload: CheckoutCandidatoPayload,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("candidato")),
):
    _requiere_dlocal()
    candidato = _validar_propietario_candidato(db, candidato_id, usuario)

    if payload.tipo not in dlocal_service.PRODUCTOS_CANDIDATO:
        raise HTTPException(status_code=400, detail="Producto inválido")

    if payload.tipo == "estatus" and not candidato.vacante_id:
        raise HTTPException(status_code=400, detail="Tu perfil de bolsa de talento no tiene un proceso de reclutamiento en curso")

    if payload.tipo == "resultados" and not db.query(ScoreCandidata).filter_by(candidato_id=candidato_id).first():
        raise HTTPException(status_code=400, detail="Todavía no has completado tus pruebas")

    perfil = candidato.perfil
    if payload.tipo == "analisis_cv" and not (perfil and perfil.cv_texto_extraido):
        raise HTTPException(status_code=400, detail="Sube tu CV antes de pagar por el análisis")

    ya_desbloqueado = db.query(CandidatoCompra).filter_by(candidato_id=candidato_id, tipo=payload.tipo).first()
    if ya_desbloqueado:
        return {"status": "ya_desbloqueado"}

    if payload.documento:
        if not perfil:
            perfil = CandidatoPerfil(candidato_id=candidato_id)
            db.add(perfil)
        perfil.cedula = payload.documento
        db.commit()
    documento = perfil.cedula if perfil else None
    if not documento:
        raise HTTPException(status_code=400, detail="Falta la cédula para procesar el pago")

    order_id = f"cand-{payload.tipo}-{candidato_id}-{uuid.uuid4().hex[:10]}"
    transaccion = Transaccion(
        tipo=f"{payload.tipo}_candidato", candidato_id=candidato_id,
        monto=dlocal_service.PRODUCTOS_CANDIDATO[payload.tipo]["precio"],
        order_id=order_id,
    )
    db.add(transaccion)
    db.commit()

    try:
        resultado = dlocal_service.crear_checkout_candidato(candidato.nombre, candidato.email, documento, payload.tipo, order_id)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    transaccion.dlocal_payment_id = resultado.get("id")
    db.commit()

    return {"checkout_url": resultado.get("redirect_url"), "order_id": order_id}


@router.get("/candidatos/{candidato_id}/reporte-resultados")
def obtener_reporte_resultados(
    candidato_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("candidato")),
):
    candidato = _validar_propietario_candidato(db, candidato_id, usuario)

    if not db.query(CandidatoCompra).filter_by(candidato_id=candidato_id, tipo="resultados").first():
        raise HTTPException(status_code=402, detail="Todavía no has pagado por ver tus resultados")

    if candidato.reporte_resultados:
        return {"reporte": candidato.reporte_resultados}

    scores = db.query(ScoreCandidata).filter_by(candidato_id=candidato_id).all()
    categorias = {"competencias": [], "psicometricos": [], "cognitivos": []}
    for score in scores:
        categoria = SistemaScoring.CATEGORIA_TEST.get(score.test_id)
        if categoria in categorias:
            categorias[categoria].append(score.score_normalizado)
    promedios = {cat: round(sum(v) / len(v), 1) for cat, v in categorias.items() if v}

    assessment_scores = db.query(AssessmentScore).filter_by(candidato_id=candidato_id).all()
    feedbacks = [a.feedback_llm for a in assessment_scores if a.feedback_llm]

    reporte = reporte_candidato_service.generar_reporte_candidato(candidato.nombre, promedios, feedbacks)
    if not reporte:
        raise HTTPException(status_code=503, detail="No pudimos generar tu reporte todavía. Intenta de nuevo en unos minutos.")

    candidato.reporte_resultados = reporte
    db.commit()

    return {"reporte": reporte}


@router.get("/candidatos/{candidato_id}/analisis-cv")
def obtener_analisis_cv(
    candidato_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("candidato")),
):
    """Solo consulta el estado -- no genera nada. Si ya pagó pero todavía no
    respondió el cuestionario (ver POST de abajo), "analisis" viene en null y
    el frontend muestra el cuestionario."""
    candidato = _validar_propietario_candidato(db, candidato_id, usuario)

    if not db.query(CandidatoCompra).filter_by(candidato_id=candidato_id, tipo="analisis_cv").first():
        raise HTTPException(status_code=402, detail="Todavía no has pagado por el análisis de tu CV")

    perfil = candidato.perfil
    return {"analisis": perfil.analisis_cv if perfil else None}


class CuestionarioAnalisisCVPayload(BaseModel):
    cargo_aspira: str | None = None
    mayor_fortaleza: str | None = None
    que_mejorar: str | None = None


@router.post("/candidatos/{candidato_id}/analisis-cv")
def generar_analisis_cv(
    candidato_id: str,
    payload: CuestionarioAnalisisCVPayload,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("candidato")),
):
    """Genera (o regenera) el análisis de CV a partir del cuestionario que el
    candidato responde después de pagar -- se contextualiza con la posición
    específica a la que aplicó (candidato.vacante) además del CV y sus
    respuestas."""
    candidato = _validar_propietario_candidato(db, candidato_id, usuario)

    if not db.query(CandidatoCompra).filter_by(candidato_id=candidato_id, tipo="analisis_cv").first():
        raise HTTPException(status_code=402, detail="Todavía no has pagado por el análisis de tu CV")

    perfil = candidato.perfil
    if not perfil or not perfil.cv_texto_extraido:
        raise HTTPException(status_code=400, detail="No encontramos tu CV. Súbelo de nuevo desde tu perfil")

    vacante_contexto = None
    if candidato.vacante:
        vacante_contexto = {
            "nombre": candidato.vacante.nombre,
            "descripcion": candidato.vacante.descripcion,
            "requisitos": candidato.vacante.requisitos,
        }

    analisis = cv_parser_service.analizar_cv(perfil.cv_texto_extraido, vacante_contexto, payload.model_dump())
    if not analisis:
        raise HTTPException(status_code=503, detail="No pudimos generar tu análisis todavía. Intenta de nuevo en unos minutos.")

    perfil.analisis_cv = analisis
    db.commit()

    return {"analisis": analisis}


# ============================================================================
# ESTADO DE UNA TRANSACCIÓN (usado por la página de resultado + respaldo sin webhook)
# ============================================================================
@router.get("/pagos/estado/{order_id}")
def estado_transaccion(
    order_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("owner", "reclutador", "empresa", "candidato")),
):
    transaccion = db.query(Transaccion).filter_by(order_id=order_id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    if usuario.rol == "candidato":
        candidato = db.query(Candidato).filter_by(id=transaccion.candidato_id).first()
        if not candidato or candidato.email != usuario.email:
            raise HTTPException(status_code=403, detail="Esta transacción no te pertenece")

    if transaccion.estado == "pendiente" and transaccion.dlocal_payment_id and dlocal_service.dlocal_configurado():
        try:
            info = dlocal_service.consultar_pago(transaccion.dlocal_payment_id)
            _procesar_resultado_pago(db, transaccion, info.get("status", ""))
        except Exception:
            pass  # Si dLocal no responde, se deja pendiente; el webhook lo resolverá después

    return {"order_id": order_id, "tipo": transaccion.tipo, "estado": transaccion.estado, "monto": transaccion.monto}


# ============================================================================
# WEBHOOK DE DLOCAL GO
#
# dLocal Go solo envía {"payment_id": "..."} en la notificación -- sin
# order_id ni status -- así que hay que consultar el pago aparte para saber
# qué pasó, y hacer el match contra nuestra Transaccion por dlocal_payment_id
# (guardado al crear el checkout), no por order_id.
# ============================================================================
@router.post("/webhooks/dlocal")
async def webhook_dlocal(request: Request, db: Session = Depends(get_db)):
    raw_body = (await request.body()).decode("utf-8")
    authorization = request.headers.get("authorization", "")

    if not dlocal_service.verificar_notificacion(raw_body, authorization):
        raise HTTPException(status_code=400, detail="Firma de notificación inválida")

    data = await request.json()
    payment_id = data.get("payment_id")
    if not payment_id:
        return {"status": "ok"}

    transaccion = db.query(Transaccion).filter_by(dlocal_payment_id=payment_id).first()
    if not transaccion:
        return {"status": "ok"}  # Notificación de un pago que no reconocemos; se ignora

    try:
        info = dlocal_service.consultar_pago(payment_id)
    except Exception:
        return {"status": "ok"}  # dLocal reintenta la notificación cada 10 min

    _procesar_resultado_pago(db, transaccion, info.get("status", ""))

    return {"status": "ok"}
