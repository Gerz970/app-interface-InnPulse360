"""
Servicio para envío de emails con logging completo
Implementa funcionalidad de envío vía SMTP con guardado de logs
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional
import logging

from core.config import EmailSettings
from core.database_connection import get_database_session
from schemas.email.email_basic_schemas import EmailSendBasic, EmailResponseBasic
from schemas.email.email_schemas import EmailSend, EmailStatus, EmailType
from dao.email.dao_email_log import EmailLogDAO

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailService:
    """
    Servicio básico para envío de emails usando SMTP
    """
    
    def __init__(self):
        """
        Inicializa el servicio con la configuración de email
        """
        self.smtp_server = EmailSettings.smtp_server
        self.smtp_port = EmailSettings.smtp_port
        self.username = EmailSettings.smtp_username
        self.password = EmailSettings.smtp_password
        self.use_tls = EmailSettings.use_tls
        self.from_email = EmailSettings.from_email
        self.from_name = EmailSettings.from_name
        
        logger.info(f"EmailService inicializado - Server: {self.smtp_server}:{self.smtp_port}")
    
    async def send_email(self, email_data: EmailSendBasic) -> EmailResponseBasic:
        """
        Envía un email usando SMTP con logging completo
        
        Args:
            email_data (EmailSendBasic): Datos del email a enviar
            
        Returns:
            EmailResponseBasic: Resultado del envío
        """
        # Convertir a EmailSend para el logging
        email_send = EmailSend(
            destinatario_email=email_data.destinatario_email,
            destinatario_nombre=None,
            asunto=email_data.asunto,
            contenido_html=email_data.contenido_html,
            contenido_texto=None,
            tipo_email=EmailType.CUSTOM,
            variables={},
            id_template=None
        )
        
        # Crear log inicial
        log_id = None
        try:
            db = get_database_session()
            try:
                email_dao = EmailLogDAO(db)
                email_log = email_dao.create_log(
                    email_send,
                    remitente_email=self.from_email,
                    remitente_nombre=self.from_name,
                    proveedor_email='smtp'
                )
                log_id = email_log.id_log
                logger.info(f"Log creado con ID: {log_id}")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error al crear log: {str(e)}")
            # Continuar sin log si falla la creación
        
        try:
            # Validar configuración
            if not self._validate_config():
                error_msg = "Configuración de email incompleta"
                if log_id:
                    self._update_log_status(log_id, EmailStatus.FAILED, error_msg)
                return EmailResponseBasic(
                    success=False,
                    message=error_msg,
                    fecha_envio=None,
                    error="Faltan credenciales de SMTP"
                )
            
            # Crear mensaje
            message = self._create_message(email_data)
            
            # Enviar email
            self._send_smtp(message, email_data.destinatario_email)
            
            # Actualizar log como exitoso
            if log_id:
                self._update_log_status(log_id, EmailStatus.SENT)
            
            logger.info(f"Email enviado exitosamente a {email_data.destinatario_email}")
            
            return EmailResponseBasic(
                success=True,
                message="Email enviado exitosamente",
                fecha_envio=datetime.utcnow(),
                error=None
            )
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = "Error de autenticación SMTP. Verifica las credenciales."
            logger.error(f"Error de autenticación: {str(e)}")
            if log_id:
                self._update_log_status(log_id, EmailStatus.FAILED, error_msg)
            return EmailResponseBasic(
                success=False,
                message="Error de autenticación",
                fecha_envio=None,
                error=error_msg
            )
            
        except smtplib.SMTPException as e:
            error_msg = f"Error SMTP: {str(e)}"
            logger.error(f"Error SMTP: {str(e)}")
            if log_id:
                self._update_log_status(log_id, EmailStatus.FAILED, error_msg)
            return EmailResponseBasic(
                success=False,
                message="Error al enviar email",
                fecha_envio=None,
                error=error_msg
            )
            
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            logger.error(f"Error inesperado: {str(e)}")
            if log_id:
                self._update_log_status(log_id, EmailStatus.FAILED, error_msg)
            return EmailResponseBasic(
                success=False,
                message="Error al procesar el email",
                fecha_envio=None,
                error=error_msg
            )
    
    def _validate_config(self) -> bool:
        """
        Valida que la configuración SMTP esté completa
        
        Returns:
            bool: True si la configuración es válida
        """
        return bool(
            self.smtp_server and
            self.username and
            self.password and
            self.from_email
        )
    
    def _create_message(self, email_data: EmailSendBasic) -> MIMEMultipart:
        """
        Crea el mensaje de email
        
        Args:
            email_data (EmailSendBasic): Datos del email
            
        Returns:
            MIMEMultipart: Mensaje creado
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = email_data.asunto
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = email_data.destinatario_email
        
        # Crear parte HTML
        html_part = MIMEText(email_data.contenido_html, "html", "utf-8")
        message.attach(html_part)
        
        return message
    
    def _send_smtp(self, message: MIMEMultipart, destinatario: str):
        """
        Envía el mensaje vía SMTP
        
        Args:
            message (MIMEMultipart): Mensaje a enviar
            destinatario (str): Email del destinatario
            
        Raises:
            SMTPException: Si hay error en el envío
        """
        try:
            # Conectar al servidor SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                server.ehlo()
                
                # Iniciar TLS si está habilitado
                if self.use_tls:
                    server.starttls()
                    server.ehlo()
                
                # Autenticarse
                server.login(self.username, self.password)
                
                # Enviar email
                server.send_message(message)
                
                logger.info(f"Mensaje enviado exitosamente a {destinatario}")
                
        except Exception as e:
            logger.error(f"Error al enviar SMTP: {str(e)}")
            raise
    
    def _update_log_status(self, log_id: int, estado: EmailStatus, error_mensaje: Optional[str] = None):
        """
        Actualiza el estado de un log de email
        
        Args:
            log_id (int): ID del log
            estado (EmailStatus): Nuevo estado
            error_mensaje (Optional[str]): Mensaje de error si aplica
        """
        try:
            db = get_database_session()
            try:
                email_dao = EmailLogDAO(db)
                email_dao.update_status(log_id, estado, error_mensaje)
                logger.info(f"Log {log_id} actualizado a estado: {estado}")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error al actualizar log {log_id}: {str(e)}")
    
    def test_connection(self) -> dict:
        """
        Prueba la conexión SMTP
        
        Returns:
            dict: Resultado de la prueba
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                server.ehlo()
                
                if self.use_tls:
                    server.starttls()
                    server.ehlo()
                
                server.login(self.username, self.password)
                
                return {
                    "success": True,
                    "message": "Conexión SMTP exitosa",
                    "server": self.smtp_server,
                    "port": self.smtp_port
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error de conexión: {str(e)}",
                "server": self.smtp_server,
                "port": self.smtp_port
            }
