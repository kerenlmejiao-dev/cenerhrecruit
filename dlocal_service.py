"""
dlocal_service.py - Integración con dLocal (Payins API v2.1)

Suscripciones de reclutadores (renovación manual mensual, sin auto-cobro)
y pago por candidato desbloqueado (Portal Empresa), usando el flujo de
Checkout Redirect de dLocal: https://docs.dlocal.com/docs/integrate-checkout

Autenticación: firma HMAC-SHA256 sobre (X-Login + X-Date + RequestBody),
igual para requests salientes y para verificar notificaciones entrantes.
Ver: https://docs.dlocal.com/docs/generate-signature
"""

import hashlib
import hmac
import json
import os
from datetime import datetime, timezone

import requests

X_LOGIN = os.getenv("DLOCAL_X_LOGIN", "")
X_TRANS_KEY = os.getenv("DLOCAL_X_TRANS_KEY", "")
DLOCAL_SECRET_KEY = os.getenv("DLOCAL_SECRET_KEY", "")
API_BASE_URL = os.getenv("DLOCAL_API_BASE_URL", "https://api.sandbox.dlocal.com")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
# URL pública donde dLocal puede alcanzar nuestro webhook (requiere túnel/hosting;
# en localhost puro las notificaciones no llegarán - usar el endpoint de
# verificación manual de estado como respaldo mientras tanto).
NOTIFICATION_BASE_URL = os.getenv("DLOCAL_NOTIFICATION_URL", "")

PAIS = "DO"
MONEDA = "DOP"

# Precios de negocio (definidos por la dueña de la plataforma)
PLANES_SUSCRIPCION = {
    "basico": {"nombre": "Básico", "precio_mensual": 500.0},
    "pro": {"nombre": "Pro", "precio_mensual": 1500.0},
    "enterprise": {"nombre": "Enterprise", "precio_mensual": 3000.0},
}

PRECIO_DESBLOQUEO_CANDIDATO = 200.0


def dlocal_configurado() -> bool:
    return bool(X_LOGIN and X_TRANS_KEY and DLOCAL_SECRET_KEY)


def _x_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _firmar(x_date: str, body_str: str) -> str:
    data = f"{X_LOGIN}{x_date}{body_str}".encode("utf-8")
    return hmac.new(DLOCAL_SECRET_KEY.encode("utf-8"), data, hashlib.sha256).hexdigest()


def _headers(body_str: str) -> dict:
    x_date = _x_date()
    firma = _firmar(x_date, body_str)
    return {
        "X-Date": x_date,
        "X-Login": X_LOGIN,
        "X-Trans-Key": X_TRANS_KEY,
        "Content-Type": "application/json",
        "X-Version": "2.1",
        "User-Agent": "CenerhRecruitOS/1.0",
        "Authorization": f"V2-HMAC-SHA256, Signature: {firma}",
    }


def _crear_pago_redirect(
    monto: float,
    order_id: str,
    descripcion: str,
    payer_nombre: str,
    payer_email: str,
    payer_documento: str,
) -> dict:
    """Crea un pago vía Checkout Redirect. Retorna el JSON de respuesta de dLocal
    (incluye 'id' y 'redirect_url' si la solicitud fue aceptada)."""
    body = {
        "amount": round(monto, 2),
        "currency": MONEDA,
        "country": PAIS,
        "payment_method_flow": "REDIRECT",
        "payer": {
            "name": payer_nombre,
            "email": payer_email,
            "document": payer_documento,
        },
        "order_id": order_id,
        "description": descripcion[:200],
        "callback_url": f"{FRONTEND_URL}/pagos/resultado?order_id={order_id}",
    }
    if NOTIFICATION_BASE_URL:
        body["notification_url"] = f"{NOTIFICATION_BASE_URL}/api/webhooks/dlocal"

    body_str = json.dumps(body, separators=(",", ":"))
    respuesta = requests.post(
        f"{API_BASE_URL}/payments",
        data=body_str,
        headers=_headers(body_str),
        timeout=15,
    )
    data = respuesta.json()
    if respuesta.status_code >= 400:
        raise RuntimeError(f"dLocal rechazó la solicitud: {data}")
    return data


def crear_checkout_suscripcion(usuario_nombre: str, usuario_email: str, usuario_documento: str, plan: str, order_id: str) -> dict:
    config = PLANES_SUSCRIPCION[plan]
    return _crear_pago_redirect(
        monto=config["precio_mensual"],
        order_id=order_id,
        descripcion=f"CENERH RECRUIT OS - Plan {config['nombre']} (mensual)",
        payer_nombre=usuario_nombre,
        payer_email=usuario_email,
        payer_documento=usuario_documento,
    )


def crear_checkout_desbloqueo(empresa_nombre: str, empresa_email: str, empresa_documento: str, candidato_nombre: str, order_id: str) -> dict:
    return _crear_pago_redirect(
        monto=PRECIO_DESBLOQUEO_CANDIDATO,
        order_id=order_id,
        descripcion=f"Desbloquear perfil: {candidato_nombre}",
        payer_nombre=empresa_nombre,
        payer_email=empresa_email,
        payer_documento=empresa_documento,
    )


def consultar_pago(dlocal_payment_id: str) -> dict:
    """GET /payments/{id} - útil como respaldo cuando el webhook no puede
    alcanzarnos (ej. desarrollo local sin túnel público)."""
    respuesta = requests.get(
        f"{API_BASE_URL}/payments/{dlocal_payment_id}",
        headers=_headers(""),
        timeout=15,
    )
    return respuesta.json()


def verificar_notificacion(x_date: str, authorization_header: str, raw_body: str) -> bool:
    """Verifica la firma HMAC de una notificación entrante de dLocal."""
    if not authorization_header:
        return False
    firma_esperada = _firmar(x_date, raw_body)
    firma_recibida = authorization_header.replace("V2-HMAC-SHA256, Signature:", "").strip()
    return hmac.compare_digest(firma_esperada, firma_recibida)
