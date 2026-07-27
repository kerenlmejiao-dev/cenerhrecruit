"""
Email Sender - Enviar reportes por email automáticamente
"""
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
    SMTP_USER = os.getenv("SMTP_USER", "demo@cenerhconsulting.com")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "demo_password")
    
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
            
            # Enviar (modo MOCK - no envía realmente)
            print(f"📧 EMAIL SIMULADO (MOCK MODE):")
            print(f"   De: {EnviadorEmail.REMITENTE_EMAIL}")
            print(f"   Para: {email_destinatario}")
            print(f"   Asunto: Evaluación Completada - {nombre_candidato}")
            print(f"   Adjunto: PDF ({len(pdf_bytes)} bytes)")
            print(f"   Status: SIMULADO (En producción, usar SMTP real)")
            
            # En producción, descomentar para envío real:
            """
            try:
                server = smtplib.SMTP(EnviadorEmail.SMTP_SERVER, EnviadorEmail.SMTP_PORT)
                server.starttls()
                server.login(EnviadorEmail.SMTP_USER, EnviadorEmail.SMTP_PASSWORD)
                server.send_message(mensaje)
                server.quit()
                print(f"✅ Email enviado a {email_destinatario}")
            except smtplib.SMTPException as e:
                print(f"❌ Error SMTP: {e}")
                raise
            """
            
            return {
                "status": "success",
                "mensaje": f"Email enviado a {email_destinatario}",
                "modo": "simulado (mock)",
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": str(e),
            }


# Test
if __name__ == "__main__":
    print("✅ Email Sender listo para usar")
    print("   Usar: EnviadorEmail.enviar_ficha_candidato(...)")
