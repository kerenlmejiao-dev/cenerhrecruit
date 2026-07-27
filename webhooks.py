"""
CENERH RECRUIT OS - Sistema de Webhooks
Eventos automáticos cuando ocurren cambios en candidatos
"""

import json
from datetime import datetime
from typing import Callable, List, Dict, Any
from enum import Enum


class EventoCandidato(str, Enum):
    """Eventos que pueden ocurrir con candidatos"""
    CANDIDATO_CREADO = "candidato.creado"
    CANDIDATO_EVALUACION_INICIADA = "candidato.evaluacion_iniciada"
    CANDIDATO_EVALUACION_COMPLETADA = "candidato.evaluacion_completada"
    CANDIDATO_PRIORITARIO = "candidato.prioritario"
    CANDIDATO_VIABLE = "candidato.viable"
    CANDIDATO_CONSIDERAR = "candidato.considerar"
    CANDIDATO_NO_RECOMENDADO = "candidato.no_recomendado"
    CANDIDATO_CONTRATADO = "candidato.contratado"
    CANDIDATO_RECHAZADO = "candidato.rechazado"


class WebhookManager:
    """Gestor de webhooks y eventos"""

    def __init__(self):
        self.listeners: Dict[EventoCandidato, List[Callable]] = {
            evento: [] for evento in EventoCandidato
        }

    def registrar(self, evento: EventoCandidato, callback: Callable):
        """Registrar listener para un evento"""
        self.listeners[evento].append(callback)
        print(f"✅ Webhook registrado: {evento}")

    async def disparar(self, evento: EventoCandidato, datos: Dict[str, Any]):
        """Disparar evento y ejecutar listeners"""
        print(f"\n🔔 EVENTO: {evento}")
        print(f"   Datos: {json.dumps(datos, indent=2, default=str)}\n")

        for callback in self.listeners[evento]:
            try:
                # Ejecutar callback (puede ser sync o async)
                if hasattr(callback, "__await__"):
                    await callback(datos)
                else:
                    callback(datos)
            except Exception as e:
                print(f"❌ Error en webhook: {e}")


# Instancia global
webhook_manager = WebhookManager()


# ============================================================================
# HANDLERS DE WEBHOOKS (Acciones automáticas)
# ============================================================================


async def sync_a_crm_nuevo_candidato(datos: Dict[str, Any]):
    """Sincronizar nuevo candidato a HubSpot/Pipedrive"""
    from crm_service import hubspot_service

    candidato_id = datos.get("candidato_id")
    nombre = datos.get("nombre")
    email = datos.get("email")
    telefono = datos.get("telefono", "")
    vacante_id = datos.get("vacante_id", "")

    print(f"📤 Sincronizando candidato a CRM: {nombre}")

    resultado = await hubspot_service.crear_contacto(
        nombre=nombre,
        email=email,
        telefono=telefono,
        vacante_id=vacante_id,
        candidato_id=candidato_id,
    )

    if resultado:
        print(f"   ✅ Candidato creado en HubSpot: {resultado}")
    else:
        print(f"   ⚠️  No se pudo sincronizar a HubSpot")


async def crear_deal_en_crm(datos: Dict[str, Any]):
    """Crear oportunidad (deal) en CRM cuando se completa evaluación"""
    from crm_service import hubspot_service, EstadoCRM

    candidato_id = datos.get("candidato_id")
    nombre = datos.get("nombre")
    vacante_id = datos.get("vacante_id", "")
    score = datos.get("score_final", 0)

    print(f"🤝 Creando oportunidad en CRM para: {nombre}")

    # Buscar contacto existente
    email = datos.get("email")
    contacto_id = await hubspot_service.buscar_contacto_por_email(email)

    if contacto_id:
        # Crear deal
        resultado = await hubspot_service.crear_deal(
            nombre=nombre,
            contacto_id=contacto_id,
            vacante_id=vacante_id,
            monto=float(score),  # Usar score como valor del deal
            estado=EstadoCRM.EVALUACION,
        )

        if resultado:
            print(f"   ✅ Deal creado: {resultado}")
        else:
            print(f"   ⚠️  No se pudo crear deal")
    else:
        print(f"   ⚠️  Contacto no encontrado")


async def actualizar_estado_crm_prioritario(datos: Dict[str, Any]):
    """Actualizar estado en CRM cuando candidato es PRIORITARIO"""
    from crm_service import hubspot_service

    nombre = datos.get("nombre")
    email = datos.get("email")

    print(f"⭐ Actualizando estado PRIORITARIO en CRM: {nombre}")

    contacto_id = await hubspot_service.buscar_contacto_por_email(email)

    if contacto_id:
        # Agregar nota
        nota = f"""
        CANDIDATO PRIORITARIO ⭐⭐⭐
        Score: {datos.get('score_final', 0)}/100
        Fecha de evaluación: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        Vacante: {datos.get('vacante_id', '')}
        """

        await hubspot_service.agregar_nota(contacto_id, nota, "Candidato Prioritario")
        print(f"   ✅ Estado actualizado y nota agregada")


async def crear_tarea_seguimiento(datos: Dict[str, Any]):
    """Crear tarea de seguimiento en CRM"""
    from crm_service import hubspot_service
    from datetime import datetime, timedelta

    nombre = datos.get("nombre")
    email = datos.get("email")

    print(f"✅ Creando tarea de seguimiento para: {nombre}")

    contacto_id = await hubspot_service.buscar_contacto_por_email(email)

    if contacto_id:
        fecha_vencimiento = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

        await hubspot_service.crear_tarea(
            contacto_id=contacto_id,
            titulo="Seguimiento: Evaluación de candidato",
            descripcion=f"Hacer seguimiento con {nombre} sobre resultados de evaluación",
            fecha_vencimiento=fecha_vencimiento,
        )
        print(f"   ✅ Tarea creada")


async def enviar_email_automatico(datos: Dict[str, Any]):
    """Enviar email automático con resultados"""
    from email_sender import EnviadorEmail

    nombre = datos.get("nombre")
    email = datos.get("email")
    score = datos.get("score_final", 0)
    candidato_id = datos.get("candidato_id")

    print(f"📧 Enviando email automático a: {email}")

    # Generar PDF
    from pdf_generator import GeneradorPDF
    from database import SessionLocal

    db = SessionLocal()
    try:
        pdf_bytes = GeneradorPDF().generar_ficha_candidato(db, candidato_id)

        # Enviar email
        enviador = EnviadorEmail()
        resultado = enviador.enviar_ficha_candidato(
            email=email,
            nombre=nombre,
            pdf_bytes=pdf_bytes,
            vacante_id=datos.get("vacante_id", ""),
        )

        if resultado.get("enviado"):
            print(f"   ✅ Email enviado")
        else:
            print(f"   ⚠️  Error enviando email")

    finally:
        db.close()


async def registrar_en_log_auditoria(datos: Dict[str, Any]):
    """Registrar evento en log de auditoría"""
    from database import SessionLocal
    from models import AuditLog

    db = SessionLocal()
    try:
        log = AuditLog(
            evento="candidato_evaluado",
            candidato_id=datos.get("candidato_id"),
            detalles=json.dumps(datos, default=str),
        )
        db.add(log)
        db.commit()
        print(f"   ✅ Evento registrado en auditoría")
    finally:
        db.close()


# ============================================================================
# REGISTRAR WEBHOOKS (Conectar handlers a eventos)
# ============================================================================


def registrar_todos_los_webhooks():
    """Registrar todos los webhooks al inicio"""

    # Cuando se crea un candidato
    webhook_manager.registrar(
        EventoCandidato.CANDIDATO_CREADO,
        sync_a_crm_nuevo_candidato,
    )

    # Cuando se completa la evaluación
    webhook_manager.registrar(
        EventoCandidato.CANDIDATO_EVALUACION_COMPLETADA,
        crear_deal_en_crm,
    )

    webhook_manager.registrar(
        EventoCandidato.CANDIDATO_EVALUACION_COMPLETADA,
        registrar_en_log_auditoria,
    )

    webhook_manager.registrar(
        EventoCandidato.CANDIDATO_EVALUACION_COMPLETADA,
        enviar_email_automatico,
    )

    # Cuando es prioritario
    webhook_manager.registrar(
        EventoCandidato.CANDIDATO_PRIORITARIO,
        actualizar_estado_crm_prioritario,
    )

    webhook_manager.registrar(
        EventoCandidato.CANDIDATO_PRIORITARIO,
        crear_tarea_seguimiento,
    )

    print("""
    ✅ WEBHOOKS REGISTRADOS:
       • Nuevo candidato → Sincronizar a HubSpot
       • Evaluación completada → Crear deal + Email + Auditoría
       • Candidato prioritario → Actualizar estado + Tarea
    """)
