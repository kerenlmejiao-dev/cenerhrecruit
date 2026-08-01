"""
whatsapp_service.py - Notificaciones por WhatsApp (Twilio WhatsApp API)

Dos eventos disparan un mensaje:
1. Nueva aplicación a una vacante -> notifica al reclutador dueño.
2. Cambio de status de reclutamiento -> notifica al candidato.

Sin credenciales de Twilio configuradas (TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN/
TWILIO_WHATSAPP_FROM), funciona en modo simulado: registra en el log qué se
habría enviado y a quién, sin bloquear el flujo real (crear candidato,
cambiar status) que disparó la notificación. Igual que dlocal_service.py y
email_sender.py con sus integraciones externas.

Requiere que el número de WhatsApp de origen (TWILIO_WHATSAPP_FROM) esté
aprobado por Meta a través de Twilio -- eso lo gestiona la dueña de la
plataforma directamente en su cuenta de Twilio, no algo que este código
pueda activar por su cuenta.
"""

import os
import re

import requests

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "")  # formato: "whatsapp:+14155238886"

API_URL_TEMPLATE = "https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"


def whatsapp_configurado() -> bool:
    return bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_WHATSAPP_FROM)


def _normalizar_telefono(telefono: str) -> str:
    """Deja solo dígitos y el + inicial. Asume República Dominicana (+1) si
    el número viene sin código de país (10 dígitos empezando en 8 ó 9)."""
    limpio = re.sub(r"[^\d+]", "", telefono or "")
    if limpio.startswith("+"):
        return limpio
    if len(limpio) == 10:
        return f"+1{limpio}"
    return f"+{limpio}" if limpio else ""


def enviar_whatsapp(telefono_destino: str, mensaje: str) -> dict:
    """Envía un mensaje de WhatsApp vía Twilio. Retorna
    {"status": "success"|"error"|"simulado", "mensaje": "..."} -- nunca
    lanza excepción, para que el flujo que dispara la notificación no se
    rompa si WhatsApp falla."""
    numero = _normalizar_telefono(telefono_destino)
    if not numero:
        return {"status": "error", "mensaje": "Número de teléfono vacío o inválido"}

    if not whatsapp_configurado():
        print("📱 WHATSAPP SIMULADO (MOCK MODE - falta TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN/TWILIO_WHATSAPP_FROM):")
        print(f"   Para: {numero}")
        print(f"   Mensaje: {mensaje}")
        return {
            "status": "simulado",
            "mensaje": f"WhatsApp simulado para {numero} (configura las credenciales de Twilio para envío real)",
        }

    try:
        respuesta = requests.post(
            API_URL_TEMPLATE.format(sid=TWILIO_ACCOUNT_SID),
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            data={
                "From": TWILIO_WHATSAPP_FROM,
                "To": f"whatsapp:{numero}",
                "Body": mensaje,
            },
            timeout=10,
        )
        if respuesta.status_code >= 400:
            return {"status": "error", "mensaje": f"Twilio respondió {respuesta.status_code}: {respuesta.text[:200]}"}
        return {"status": "success", "mensaje": f"WhatsApp enviado a {numero}"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


def notificar_nueva_aplicacion(telefono_reclutador: str, nombre_candidato: str, nombre_vacante: str) -> dict:
    mensaje = (
        f"CENERH Recruit OS: {nombre_candidato} acaba de aplicar a la vacante "
        f"\"{nombre_vacante}\". Revisa el candidato en tu panel de reclutador."
    )
    return enviar_whatsapp(telefono_reclutador, mensaje)


def notificar_cambio_status(telefono_candidato: str, nombre_candidato: str, nuevo_status: str, nombre_vacante: str) -> dict:
    mensaje = (
        f"Hola {nombre_candidato}, tu proceso para \"{nombre_vacante}\" con CENERH Consulting "
        f"avanzó a: {nuevo_status}. Puedes ver el detalle iniciando sesión en tu cuenta."
    )
    return enviar_whatsapp(telefono_candidato, mensaje)
