"""
Email Sender - Enviar reportes por email automáticamente
"""
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import os


class EnviadorEmail:
    """Enviar emails con PDF adjunto"""
    
    # Configuración SMTP (cambiar en producción)
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    
    REMITENTE_NAME = "CENERH Consulting"
    REMITENTE_EMAIL = "reportes@cenerhconsulting.com"
    
    @staticmethod
    def enviar_ficha_candidato(
        email_destinatario: str,
        nombre_candidato: str,
        pdf_bytes: bytes,
        vacante_id: str = None,
    ) -> dict:
        """
        Enviar ficha PDF por email
        
        Args:
            email_destinatario: Email del candidato
            nombre_candidato: Nombre del candidato
            pdf_bytes: Bytes del PDF
            vacante_id: ID de la vacante (opcional)
        
        Returns:
            {"status": "success" | "error", "mensaje": "..."}
        """
        
        try:
            # Crear mensaje
            mensaje = MIMEMultipart()
            mensaje["From"] = f"{EnviadorEmail.REMITENTE_NAME} <{EnviadorEmail.REMITENTE_EMAIL}>"
            mensaje["To"] = email_destinatario
            mensaje["Subject"] = f"Evaluación Completada - {nombre_candidato}"
            
            # Body del email
            cuerpo = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                
                <div style="max-width: 600px; margin: 0 auto;">
                    
                    <div style="background-color: #0050A0; color: white; padding: 20px; text-align: center; border-radius: 5px;">
                        <h1 style="margin: 0; font-size: 24px;">CENERH CONSULTING</h1>
                        <p style="margin: 5px 0 0 0; font-size: 12px;">Consultoría Estratégica de Gestión Humana</p>
                    </div>
                    
                    <div style="padding: 30px; background-color: #f9f9f9; margin-top: 0;">
                        
                        <h2 style="color: #D62828; font-size: 18px;">¡Hola, {nombre_candidato}!</h2>
                        
                        <p>Tu evaluación psicométrica ha sido completada exitosamente.</p>
                        
                        <p>Adjunto encontrarás tu <strong>Ficha Técnica de Evaluación</strong> con:</p>
                        <ul>
                            <li>Scores por cada test completado</li>
                            <li>Análisis de competencias</li>
                            <li>Evaluación psicométrica integral</li>
                            <li>Score final ponderado</li>
                            <li>Clasificación profesional</li>
                        </ul>
                        
                        <p style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd;">
                            <strong>Próximos pasos:</strong><br>
                            Nuestro equipo de consultoría analizará tus resultados y se comunicará contigo en los próximos 3 días hábiles con feedback personalizado y recomendaciones.
                        </p>
                        
                        <p style="margin-top: 20px; color: #666; font-size: 12px;">
                            <strong>CENERH Consulting</strong><br>
                            Teléfono: +1-809-557-9632<br>
                            Email: servicios@cenerhconsulting.com<br>
                            Web: www.cenerhconsulting.com<br>
                            <br>
                            <em>Este documento es confidencial y está dirigido únicamente al destinatario.</em>
                        </p>
                        
                    </div>
                    
                    <div style="padding: 15px; text-align: center; font-size: 11px; color: #999; margin-top: 20px;">
                        <p>© {datetime.now().year} CENERH Consulting. Todos los derechos reservados.</p>
                    </div>
                    
                </div>
                
            </body>
            </html>
            """
            
            # Agregar body
            mensaje.attach(MIMEText(cuerpo, "html"))
            
            # Agregar PDF
            pdf_attachment = MIMEApplication(pdf_bytes, Name="Evaluacion_Candidato.pdf")
            pdf_attachment["Content-Disposition"] = "attachment; filename=Evaluacion_Candidato.pdf"
            mensaje.attach(pdf_attachment)
            
            if not EnviadorEmail.SMTP_USER or not EnviadorEmail.SMTP_PASSWORD:
                # Sin credenciales SMTP configuradas: modo simulado (no bloquea el flujo local)
                print(f"📧 EMAIL SIMULADO (MOCK MODE - falta SMTP_USER/SMTP_PASSWORD en .env):")
                print(f"   Para: {email_destinatario}")
                print(f"   Asunto: Evaluación Completada - {nombre_candidato}")
                print(f"   Adjunto: PDF ({len(pdf_bytes)} bytes)")
                return {
                    "status": "success",
                    "mensaje": f"Email simulado para {email_destinatario} (configura SMTP_USER/SMTP_PASSWORD para envío real)",
                    "modo": "simulado (mock)",
                }

            server = smtplib.SMTP(EnviadorEmail.SMTP_SERVER, EnviadorEmail.SMTP_PORT)
            try:
                server.starttls()
                server.login(EnviadorEmail.SMTP_USER, EnviadorEmail.SMTP_PASSWORD)
                server.send_message(mensaje)
            finally:
                server.quit()

            return {
                "status": "success",
                "mensaje": f"Email enviado a {email_destinatario}",
                "modo": "real",
            }

        except Exception as e:
            return {
                "status": "error",
                "mensaje": str(e),
            }

    @staticmethod
    def enviar_solicitud_referencia(
        email_destinatario: str,
        nombre_referencia: str,
        nombre_candidato: str,
        link_formulario: str,
    ) -> dict:
        """Envía a una referencia laboral el link a un formulario corto para
        opinar sobre un candidato. El link ya incluye el token -- no requiere
        que la referencia tenga cuenta ni inicie sesión."""
        try:
            mensaje = MIMEMultipart()
            mensaje["From"] = f"{EnviadorEmail.REMITENTE_NAME} <{EnviadorEmail.REMITENTE_EMAIL}>"
            mensaje["To"] = email_destinatario
            mensaje["Subject"] = f"Verificación de referencia laboral - {nombre_candidato}"

            cuerpo = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <div style="background-color: #0D0D0D; color: white; padding: 20px; text-align: center;">
                        <h1 style="margin: 0; font-size: 24px;">CENERH CONSULTING</h1>
                        <p style="margin: 5px 0 0 0; font-size: 12px; color: #C9A14A;">CONSULTING</p>
                    </div>
                    <div style="padding: 30px; background-color: #f9f9f9;">
                        <h2 style="color: #D62828; font-size: 18px;">Hola, {nombre_referencia}</h2>
                        <p><strong>{nombre_candidato}</strong> te incluyó como referencia laboral en un proceso de
                        selección con CENERH Consulting.</p>
                        <p>¿Puedes tomarte 2 minutos para responder unas preguntas cortas sobre tu experiencia
                        trabajando con esta persona?</p>
                        <p style="text-align: center; margin: 30px 0;">
                            <a href="{link_formulario}" style="background-color: #D62828; color: white; padding: 14px 28px; text-decoration: none; font-weight: bold;">
                                RESPONDER
                            </a>
                        </p>
                        <p style="margin-top: 20px; color: #666; font-size: 12px;">
                            Tu respuesta es confidencial y se comparte únicamente con el reclutador a cargo de este
                            proceso. Si no reconoces a esta persona o no deseas responder, puedes ignorar este correo.
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """

            mensaje.attach(MIMEText(cuerpo, "html"))

            if not EnviadorEmail.SMTP_USER or not EnviadorEmail.SMTP_PASSWORD:
                print(f"📧 EMAIL SIMULADO (MOCK MODE - falta SMTP_USER/SMTP_PASSWORD en .env):")
                print(f"   Para: {email_destinatario}")
                print(f"   Asunto: Verificación de referencia laboral - {nombre_candidato}")
                print(f"   Link: {link_formulario}")
                return {
                    "status": "success",
                    "mensaje": f"Email simulado para {email_destinatario} (configura SMTP_USER/SMTP_PASSWORD para envío real)",
                    "modo": "simulado (mock)",
                }

            server = smtplib.SMTP(EnviadorEmail.SMTP_SERVER, EnviadorEmail.SMTP_PORT)
            try:
                server.starttls()
                server.login(EnviadorEmail.SMTP_USER, EnviadorEmail.SMTP_PASSWORD)
                server.send_message(mensaje)
            finally:
                server.quit()

            return {"status": "success", "mensaje": f"Email enviado a {email_destinatario}", "modo": "real"}

        except Exception as e:
            return {"status": "error", "mensaje": str(e)}


# Test
if __name__ == "__main__":
    print("✅ Email Sender listo para usar")
    print("   Usar: EnviadorEmail.enviar_ficha_candidato(...)")
