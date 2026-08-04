"""
dlocal_service.py - Integración con dLocal Go

Suscripciones de reclutadores (renovación manual mensual, sin auto-cobro)
y pago por candidato desbloqueado (Portal Empresa), usando el Checkout de
dLocal Go: https://docs.dlocalgo.com/integration-api/welcome-to-dlocal-go-api/

IMPORTANTE: dLocal Go es un producto distinto de la API "Payins" clásica de
dLocal (docs.dlocal.com) -- credenciales, autenticación y payloads son
diferentes. No confundir ni mezclar credenciales de uno con el otro.

Autenticación saliente: header "Authorization: Bearer <API_KEY>:<SECRET_KEY>",
sin firma por request (a diferencia de la API clásica).

Verificación de webhooks entrantes: HMAC-SHA256 sobre (API_KEY + cuerpo JSON
crudo), firmado con el Secret Key -- ver sección "Notifications" de la
documentación. El webhook solo trae el payment_id; el estado real hay que
consultarlo aparte con GET /v1/payments/{id}.
"""

import hashlib
import hmac
import os

import requests

DLOCALGO_API_KEY = os.getenv("DLOCALGO_API_KEY", "")
DLOCALGO_SECRET_KEY = os.getenv("DLOCALGO_SECRET_KEY", "")
# Sandbox: https://api-sbx.dlocalgo.com -- Producción: https://api.dlocalgo.com
API_BASE_URL = os.getenv("DLOCALGO_API_BASE_URL", "https://api.dlocalgo.com")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
# URL pública donde dLocal Go puede alcanzar nuestro webhook (requiere túnel/hosting;
# en localhost puro las notificaciones no llegarán - usar el endpoint de
# verificación manual de estado como respaldo mientras tanto).
NOTIFICATION_BASE_URL = os.getenv("DLOCAL_NOTIFICATION_URL", "")

PAIS = "DO"
MONEDA = "DOP"

# Precios y características de negocio (definidos por la dueña de la
# plataforma). "para" indica a quién está dirigido el plan -- Básico/Pro son
# para reclutadores, Enterprise es para empresas.
PLANES_SUSCRIPCION = {
    "basico": {
        "nombre": "Básico",
        "precio_mensual": 1000.0,
        "para": "reclutador",
        "caracteristicas": [
            "Vacantes activas sin límite",
            "Link de aplicación para que tus candidatos completen el proceso",
            "Ficha general del candidato (aplica / no aplica)",
            "Pruebas psicométricas para cada vacante",
        ],
    },
    "pro": {
        "nombre": "Pro",
        "precio_mensual": 1500.0,
        "para": "reclutador",
        "caracteristicas": [
            "Vacantes activas sin límite",
            "Link de aplicación para que tus candidatos completen el proceso",
            "Ficha general del candidato (aplica / no aplica)",
            "Pruebas psicométricas para cada vacante",
            "Acceso a los candidatos de la Bolsa de Talento",
        ],
    },
    "enterprise": {
        "nombre": "Enterprise",
        "precio_mensual": 5000.0,
        "para": "empresa",
        "caracteristicas": [
            "Vacantes activas sin límite",
            "Link de aplicación para que tus candidatos completen el proceso",
            "Ficha general del candidato (aplica / no aplica)",
            "Pruebas psicométricas para cada vacante",
            "Acceso a los candidatos de la Bolsa de Talento",
            "Guion de entrevistas por competencias",
            "Perfil más detallado del candidato",
        ],
    },
}

# Duración de cada ciclo de membresía. Al vencer, el reclutador pierde acceso
# al panel hasta que se registre un nuevo pago (ver require_membresia_activa
# en auth_users.py y POST /api/admin/activar-membresia).
DURACION_MEMBRESIA_DIAS = 27

PRECIO_DESBLOQUEO_CANDIDATO = 200.0

# Compras del propio candidato sobre sí mismo (distinto del desbloqueo de
# arriba, que paga la EMPRESA para ver a un candidato). Ver CandidatoCompra
# en models.py y la sección "PAGOS DE CANDIDATOS" en pagos_router.py.
PRODUCTOS_CANDIDATO = {
    "estatus": {
        "precio": 200.0,
        "descripcion": "Ver estatus completo del proceso de reclutamiento",
    },
    "resultados": {
        "precio": 500.0,
        "descripcion": "Recibir resultados del proceso",
    },
    "analisis_cv": {
        "precio": 500.0,
        "descripcion": "Análisis de CV con IA",
    },
}


def dlocal_configurado() -> bool:
    return bool(DLOCALGO_API_KEY and DLOCALGO_SECRET_KEY)


def _headers() -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DLOCALGO_API_KEY}:{DLOCALGO_SECRET_KEY}",
    }


def obtener_info_cuenta() -> dict:
    """GET /v1/me -- endpoint de dLocal Go para verificar credenciales y ver
    el estado de la cuenta (país, moneda habilitada, etc.). Útil para
    diagnosticar rechazos de pago que no dicen qué campo específico falló."""
    respuesta = requests.get(f"{API_BASE_URL}/v1/me", headers=_headers(), timeout=15)
    try:
        cuerpo = respuesta.json()
    except Exception:
        cuerpo = respuesta.text
    return {"status_code": respuesta.status_code, "body": cuerpo}


def _probar_payload(body: dict) -> dict:
    respuesta = requests.post(f"{API_BASE_URL}/v1/payments", json=body, headers=_headers(), timeout=15)
    try:
        cuerpo = respuesta.json()
    except Exception:
        cuerpo = respuesta.text
    return {"status_code": respuesta.status_code, "body": cuerpo, "enviado": body}


def crear_pago_prueba_diagnostico() -> dict:
    """Prueba varias variantes del payload de pago, agregando UN elemento a
    la vez sobre la base mínima que ya sabemos que funciona, para aislar
    exactamente qué combinación dispara "Invalid values". Usa RD$100 (por
    encima del mínimo que rechazó RD$1) y no cobra nada hasta que alguien
    complete el checkout -- solo registra la intención de pago."""
    base = {
        "amount": 100.0,
        "currency": MONEDA,
        "country": PAIS,
        "order_id": f"diagnostico-{os.urandom(4).hex()}",
        "description": "CENERH diagnostico",
        "success_url": f"{FRONTEND_URL}/pagos/resultado",
        "back_url": f"{FRONTEND_URL}/pagos/resultado",
    }

    resultados = {}
    resultados["1_minimo_sin_payer"] = _probar_payload(dict(base, order_id=f"{base['order_id']}-a"))

    con_query = dict(base, order_id=f"{base['order_id']}-b")
    con_query["success_url"] = f"{FRONTEND_URL}/pagos/resultado?order_id={con_query['order_id']}"
    con_query["back_url"] = con_query["success_url"]
    resultados["2_con_query_string_en_url"] = _probar_payload(con_query)

    con_payer = dict(base, order_id=f"{base['order_id']}-c")
    con_payer["payer"] = {"name": "Keren Mejia", "email": "diagnostico@cenerhconsulting.com", "document": "00115605545"}
    resultados["3_con_payer"] = _probar_payload(con_payer)

    con_payer_sin_document = dict(base, order_id=f"{base['order_id']}-d")
    con_payer_sin_document["payer"] = {"name": "Keren Mejia", "email": "diagnostico@cenerhconsulting.com"}
    resultados["4_con_payer_sin_document"] = _probar_payload(con_payer_sin_document)

    con_document_country = dict(base, order_id=f"{base['order_id']}-e")
    con_document_country["payer"] = {
        "name": "Keren Mejia",
        "email": "diagnostico@cenerhconsulting.com",
        "document": "00115605545",
        "document_country": "DO",
    }
    resultados["5_con_document_y_document_country"] = _probar_payload(con_document_country)

    con_nombre_separado = dict(base, order_id=f"{base['order_id']}-f")
    con_nombre_separado["payer"] = {
        "first_name": "Keren",
        "last_name": "Mejia",
        "email": "diagnostico@cenerhconsulting.com",
        "document": "00115605545",
        "document_country": "DO",
    }
    resultados["6_nombre_separado_con_document"] = _probar_payload(con_nombre_separado)

    solo_document_sin_nombre = dict(base, order_id=f"{base['order_id']}-g")
    solo_document_sin_nombre["payer"] = {
        "email": "diagnostico@cenerhconsulting.com",
        "document": "00115605545",
        "document_country": "DO",
    }
    resultados["7_document_sin_name"] = _probar_payload(solo_document_sin_nombre)

    return resultados


def _crear_pago_redirect(
    monto: float,
    order_id: str,
    descripcion: str,
    payer_nombre: str,
    payer_email: str,
    payer_documento: str,
) -> dict:
    """Crea un pago vía el Checkout de dLocal Go. Retorna el JSON de respuesta
    (incluye 'id' y 'redirect_url' si la solicitud fue aceptada)."""
    body = {
        "amount": round(monto, 2),
        "currency": MONEDA,
        "country": PAIS,
        "order_id": order_id,
        "description": descripcion[:100],
        "success_url": f"{FRONTEND_URL}/pagos/resultado?order_id={order_id}",
        "back_url": f"{FRONTEND_URL}/pagos/resultado?order_id={order_id}",
        "payer": {
            "name": payer_nombre,
            "email": payer_email,
        },
    }
    # payer_documento (la cédula/RNC) NO se envía a dLocal Go: diagnosticado
    # a mano (2026-08-04) que incluir "document" en el payer hace que dLocal
    # Go rechace la solicitud completa con "Invalid values" -- probado con y
    # sin "document_country", con nombre junto o separado en first_name/
    # last_name, siempre falla igual apenas aparece "document". Sin él, el
    # pago se crea sin problema (dLocal Go no lo exige; su propio checkout
    # hospedado puede pedirlo directamente si lo necesita). Es probable que
    # esté ligado a que la cuenta todavía tiene kyc_level_status="PENDING"
    # (ver GET /api/admin/dlocal-diagnostico) -- si dLocal confirma que el
    # KYC es la causa, esto se puede volver a intentar una vez esté
    # aprobado. payer_documento queda sin usar aquí a propósito; se sigue
    # guardando en nuestra base desde el checkout (ver pagos_router.py) por
    # si se necesita para facturación o para reintentar esto más adelante.
    if NOTIFICATION_BASE_URL:
        body["notification_url"] = f"{NOTIFICATION_BASE_URL}/api/webhooks/dlocal"

    respuesta = requests.post(
        f"{API_BASE_URL}/v1/payments",
        json=body,
        headers=_headers(),
        timeout=15,
    )
    data = respuesta.json()
    if respuesta.status_code >= 400:
        # dLocal Go no dice qué campo específico fue inválido en su mensaje
        # de error -- se incluye aquí un resumen de lo que se envió (nombre/
        # email/documento no son datos sensibles de pago, son los mismos
        # datos que ya están en nuestra base) para poder diagnosticar sin
        # necesitar acceso a los logs del servidor.
        resumen_enviado = {
            "amount": body["amount"],
            "currency": body["currency"],
            "country": body["country"],
            "order_id": body["order_id"],
            "description": body["description"],
            "success_url": body["success_url"],
            "payer_name": body["payer"]["name"],
            "payer_email": body["payer"]["email"],
            "payer_document": body["payer"].get("document"),
            "payer_document_country": body["payer"].get("document_country"),
        }
        raise RuntimeError(f"dLocal Go rechazó la solicitud: {data}. Enviado: {resumen_enviado}")
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


def crear_checkout_candidato(candidato_nombre: str, candidato_email: str, candidato_documento: str, tipo: str, order_id: str) -> dict:
    producto = PRODUCTOS_CANDIDATO[tipo]
    return _crear_pago_redirect(
        monto=producto["precio"],
        order_id=order_id,
        descripcion=f"CENERH RECRUIT OS - {producto['descripcion']}",
        payer_nombre=candidato_nombre,
        payer_email=candidato_email,
        payer_documento=candidato_documento,
    )


def consultar_pago(dlocal_payment_id: str) -> dict:
    """GET /v1/payments/{id} -- respaldo para verificación manual, y también
    necesario tras cada webhook: la notificación de dLocal Go solo trae el
    payment_id, hay que consultar aquí el estado real (PENDING/PAID/
    REJECTED/CANCELLED/EXPIRED)."""
    respuesta = requests.get(
        f"{API_BASE_URL}/v1/payments/{dlocal_payment_id}",
        headers=_headers(),
        timeout=15,
    )
    return respuesta.json()


def verificar_notificacion(raw_body: str, authorization_header: str) -> bool:
    """Verifica la firma HMAC-SHA256 de una notificación entrante de dLocal Go.
    Firma = HMAC-SHA256(key=SecretKey, msg=ApiKey + cuerpo_json_crudo)."""
    if not authorization_header or "Signature:" not in authorization_header:
        return False
    firma_recibida = authorization_header.split("Signature:")[-1].strip()
    mensaje = f"{DLOCALGO_API_KEY}{raw_body}".encode("utf-8")
    firma_esperada = hmac.new(DLOCALGO_SECRET_KEY.encode("utf-8"), mensaje, hashlib.sha256).hexdigest()
    return hmac.compare_digest(firma_esperada, firma_recibida)
