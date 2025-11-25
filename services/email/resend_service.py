"""
Servicio de email usando Resend API (REST)
Ideal para entornos cloud como Railway que bloquean SMTP
"""
import resend
from datetime import datetime
from typing import Optional
import logging
from io import BytesIO

from core.config import EmailSettings
from schemas.email.email_basic_schemas import EmailResponseBasic
from utils.pdf_generator import generate_quotation_pdf

logger = logging.getLogger(__name__)


class ResendEmailService:
    """
    Servicio de email usando Resend API REST
    """
    
    def __init__(self):
        self.api_key = EmailSettings.resend_api_key
        self.from_email = EmailSettings.from_email
        self.from_name = EmailSettings.from_name
        
        if not self.api_key:
            raise ValueError("RESEND_API_KEY no está configurada")
        
        resend.api_key = self.api_key
        logger.info("✅ ResendEmailService inicializado")
        logger.info(f"   From: {self.from_name} <{self.from_email}>")
    
    def send_quotation_email(
        self,
        destinatario_email: str,
        destinatario_nombre: str,
        codigo_reservacion: str,
        fecha_entrada: str,
        fecha_salida: str,
        duracion_dias: int,
        hotel_nombre: str,
        hotel_direccion: Optional[str],
        hotel_telefono: Optional[str],
        hotel_email: Optional[str],
        habitacion_nombre: str,
        habitacion_descripcion: Optional[str],
        tipo_habitacion: str,
        cliente_rfc: Optional[str],
        cliente_identificacion: Optional[str],
        precio_unitario: float,
        periodicidad_nombre: str,
        precio_total: float,
        html_content: str
    ) -> EmailResponseBasic:
        """
        Envía email de cotización con PDF adjunto usando Resend
        
        Args:
            destinatario_email: Email del destinatario
            destinatario_nombre: Nombre del cliente
            codigo_reservacion: Código de la reservación
            fecha_entrada: Fecha de entrada formateada
            fecha_salida: Fecha de salida formateada
            duracion_dias: Duración en días
            hotel_nombre: Nombre del hotel
            hotel_direccion: Dirección del hotel
            hotel_telefono: Teléfono del hotel
            hotel_email: Email del hotel
            habitacion_nombre: Nombre/clave de la habitación
            habitacion_descripcion: Descripción de la habitación
            tipo_habitacion: Tipo de habitación
            cliente_rfc: RFC del cliente
            cliente_identificacion: Documento de identificación
            precio_unitario: Precio unitario
            periodicidad_nombre: Nombre de la periodicidad
            precio_total: Precio total calculado
            html_content: Contenido HTML del email ya generado
        
        Returns:
            EmailResponseBasic: Resultado del envío
        """
        try:
            logger.info(f"📧 [Resend] Preparando envío de cotización a: {destinatario_email}")
            
            # Generar PDF
            logger.info(f"📧 [Resend] Generando PDF de cotización...")
            pdf_bytes = generate_quotation_pdf(
                codigo_reservacion=codigo_reservacion,
                fecha_entrada=fecha_entrada,
                fecha_salida=fecha_salida,
                duracion_dias=duracion_dias,
                hotel_nombre=hotel_nombre,
                hotel_direccion=hotel_direccion,
                hotel_telefono=hotel_telefono,
                hotel_email=hotel_email,
                habitacion_nombre=habitacion_nombre,
                habitacion_descripcion=habitacion_descripcion,
                tipo_habitacion=tipo_habitacion,
                cliente_nombre=destinatario_nombre,
                cliente_rfc=cliente_rfc,
                cliente_identificacion=cliente_identificacion,
                cliente_email=destinatario_email,
                precio_unitario=precio_unitario,
                periodicidad_nombre=periodicidad_nombre,
                precio_total=precio_total
            )
            
            # Convertir PDF BytesIO a bytes
            pdf_bytes.seek(0)
            pdf_content = pdf_bytes.getvalue()
            
            # Enviar email usando Resend
            logger.info(f"📧 [Resend] Enviando email a {destinatario_email}...")
            logger.info(f"📧 [Resend] From: {self.from_name} <{self.from_email}>")
            logger.info(f"📧 [Resend] Subject: Cotización de Reservación - {codigo_reservacion}")
            logger.info(f"📧 [Resend] PDF size: {len(pdf_content)} bytes")
            logger.info(f"📧 [Resend] HTML content length: {len(html_content)} characters")
            
            params = resend.Emails.SendParams(
                from_=f"{self.from_name} <{self.from_email}>",
                to=[destinatario_email],
                subject=f"Cotización de Reservación - {codigo_reservacion}",
                html=html_content,
                attachments=[
                    {
                        "filename": f"Cotizacion_{codigo_reservacion}.pdf",
                        "content": pdf_content,
                    }
                ],
            )
            
            logger.info(f"📧 [Resend] Llamando a resend.Emails.send()...")
            email = resend.Emails.send(params)
            
            logger.info(f"✅ [Resend] Email enviado exitosamente. ID: {email.id}")
            logger.info(f"✅ [Resend] Respuesta completa: {email}")
            
            return EmailResponseBasic(
                success=True,
                message="Email de cotización enviado exitosamente",
                fecha_envio=datetime.utcnow(),
                error=None
            )
            
        except Exception as e:
            error_msg = f"Error al enviar email con Resend: {str(e)}"
            logger.error(f"❌ [Resend] {error_msg}")
            import traceback
            logger.error(f"❌ [Resend] Traceback completo: {traceback.format_exc()}")
            logger.error(f"❌ [Resend] Tipo de error: {type(e).__name__}")
            return EmailResponseBasic(
                success=False,
                message="Error al enviar email de cotización",
                fecha_envio=None,
                error=error_msg
            )

