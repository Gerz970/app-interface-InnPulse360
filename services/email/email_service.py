"""
Servicio para envío de emails con logging completo
Implementa funcionalidad de envío vía SMTP con guardado de logs
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import Optional
import logging

from core.config import EmailSettings
from core.database_connection import get_database_session
from schemas.email.email_basic_schemas import EmailSendBasic, EmailResponseBasic
from schemas.email.email_schemas import EmailSend, EmailStatus, EmailType
from dao.email.dao_email_log import EmailLogDAO
from services.email.template_service import EmailTemplateService
from utils.pdf_generator import generate_quotation_pdf

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar Resend solo si está disponible
try:
    from services.email.resend_service import ResendEmailService
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    logger.warning("Resend no está disponible. Solo se usará SMTP.")


class EmailService:
    """
    Servicio básico para envío de emails usando SMTP o Resend según configuración
    """
    
    def __init__(self):
        """
        Inicializa el servicio con la configuración de email
        Detecta automáticamente qué proveedor usar (Resend o SMTP)
        """
        # Crear instancia de EmailSettings para acceder a la propiedad email_provider
        email_settings = EmailSettings()
        self.email_provider = email_settings.email_provider
        
        # Inicializar Resend si está configurado
        self.resend_service = None
        if self.email_provider == "resend" and RESEND_AVAILABLE:
            try:
                self.resend_service = ResendEmailService()
                logger.info("✅ Usando Resend como proveedor de email (REST API)")
            except Exception as e:
                # Si Resend está configurado pero falla, NO usar SMTP automáticamente
                logger.error(f"❌ Error crítico: Resend está configurado (USE_RESEND=true) pero falló al inicializar: {str(e)}")
                logger.error("❌ Verifica que RESEND_API_KEY esté correctamente configurada")
                # NO cambiar a SMTP automáticamente - esto es un error de configuración
                self.resend_service = None
                # Mantener email_provider como "resend" para que falle claramente
        elif self.email_provider == "resend" and not RESEND_AVAILABLE:
            logger.error("❌ Resend está configurado pero la librería no está disponible. Instala: pip install resend")
            self.resend_service = None
            # Mantener email_provider como "resend" para que falle claramente
        else:
            logger.info("📧 Usando SMTP como proveedor de email")
            self.resend_service = None
        
        # Configuración SMTP (para fallback o desarrollo local)
        self.smtp_server = EmailSettings.smtp_server
        self.smtp_port = EmailSettings.smtp_port
        self.username = EmailSettings.smtp_username
        self.password = EmailSettings.smtp_password
        self.use_tls = EmailSettings.use_tls
        self.from_email = EmailSettings.from_email
        self.from_name = EmailSettings.from_name
        
        # Logging para depuración
        logger.info(f"📧 [EmailService] Configuración de remitente:")
        logger.info(f"   From Email: {self.from_email}")
        logger.info(f"   From Name: {self.from_name}")
        logger.info(f"   Email Provider: {self.email_provider}")
        
        # Logging detallado para diagnóstico
        logger.info(f"📧 [EmailService] EmailService inicializado")
        logger.info(f"   Provider detectado: {self.email_provider}")
        logger.info(f"   Resend disponible: {RESEND_AVAILABLE}")
        logger.info(f"   Resend service inicializado: {'Sí' if self.resend_service else 'No'}")
        logger.info(f"   SMTP Server: {self.smtp_server}:{self.smtp_port}")
        logger.info(f"   From Email: {self.from_email}")
        
        # Validar configuración SMTP solo si se va a usar
        if self.email_provider == "smtp":
            if not self.smtp_server or self.smtp_server == "smtp.gmail.com":
                logger.warning("⚠️ Usando servidor SMTP por defecto. Verifica las variables de entorno.")
            if not self.username or not self.password:
                logger.error("❌ Credenciales SMTP no configuradas correctamente. Verifica FromEmail y FromPassword.")
        
        # Inicializar servicio de plantillas
        self.template_service = EmailTemplateService()
    
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
            # Usar Resend si está configurado
            if self.email_provider == "resend" and self.resend_service:
                try:
                    logger.info(f"📧 [EmailService] Usando Resend para enviar email a {email_data.destinatario_email}")
                    logger.info(f"📧 [EmailService] Debug - from_email: '{self.from_email}' (type: {type(self.from_email)})")
                    logger.info(f"📧 [EmailService] Debug - from_name: '{self.from_name}' (type: {type(self.from_name)})")
                    
                    # Obtener valores de EmailSettings directamente como fallback
                    from_email_value = self.from_email or EmailSettings.from_email
                    from_name_value = self.from_name or EmailSettings.from_name
                    
                    logger.info(f"📧 [EmailService] Valores después de fallback - from_email: '{from_email_value}', from_name: '{from_name_value}'")
                    
                    # Validar que from_email esté configurado
                    if not from_email_value or not str(from_email_value).strip():
                        error_msg = f"FromEmail no está configurado para Resend. Valor actual: '{from_email_value}'"
                        logger.error(f"❌ {error_msg}")
                        if log_id:
                            self._update_log_status(log_id, EmailStatus.FAILED, error_msg)
                        return EmailResponseBasic(
                            success=False,
                            message=error_msg,
                            fecha_envio=None,
                            error=error_msg
                        )
                    
                    import resend
                    
                    # Asegurar que resend.api_key esté configurado (usar el servicio inicializado si está disponible)
                    if self.resend_service and hasattr(self.resend_service, 'api_key'):
                        resend.api_key = self.resend_service.api_key
                        logger.info(f"📧 [EmailService] Usando api_key del resend_service")
                    elif not hasattr(resend, 'api_key') or not resend.api_key:
                        resend.api_key = EmailSettings.resend_api_key
                        logger.info(f"📧 [EmailService] Configurando resend.api_key desde EmailSettings")
                    
                    logger.info(f"📧 [EmailService] resend.api_key configurado: {'Sí' if hasattr(resend, 'api_key') and resend.api_key else 'No'}")
                    
                    # Formatear el remitente
                    from_email_str = str(from_email_value).strip()
                    if from_name_value and str(from_name_value).strip():
                        from_value = f"{from_name_value} <{from_email_str}>"
                    else:
                        from_value = from_email_str
                    
                    logger.info(f"📧 [EmailService] From value final: '{from_value}'")
                    
                    # Crear parámetros usando el mismo formato que resend_service.py
                    params = resend.Emails.SendParams(
                        from_=from_value,
                        to=[email_data.destinatario_email],
                        subject=email_data.asunto,
                        html=email_data.contenido_html,
                    )
                    
                    # Logging adicional para depuración
                    logger.info(f"📧 [EmailService] Params tipo: {type(params)}")
                    if isinstance(params, dict):
                        logger.info(f"📧 [EmailService] Params keys antes: {list(params.keys())}")
                        # Verificar si tiene 'from' o 'from_'
                        if 'from' not in params:
                            if 'from_' in params:
                                # Convertir 'from_' a 'from'
                                params['from'] = params.pop('from_')
                                logger.info(f"📧 [EmailService] Convertido 'from_' a 'from' manualmente")
                            else:
                                # Si no tiene ninguno, agregarlo directamente
                                params['from'] = from_value
                                logger.info(f"📧 [EmailService] Agregado 'from' directamente: '{from_value}'")
                        logger.info(f"📧 [EmailService] Params keys después: {list(params.keys())}")
                        logger.info(f"📧 [EmailService] Params 'from' value: {params.get('from', 'NO_ENCONTRADO')}")
                    else:
                        logger.info(f"📧 [EmailService] Params dict: {params.__dict__ if hasattr(params, '__dict__') else 'No __dict__'}")
                    
                    email = resend.Emails.send(params)
                    logger.info(f"✅ [Resend] Email enviado exitosamente. ID: {email.id}")
                    
                    # Actualizar log como exitoso
                    if log_id:
                        self._update_log_status(log_id, EmailStatus.SENT)
                    
                    return EmailResponseBasic(
                        success=True,
                        message="Email enviado exitosamente",
                        fecha_envio=datetime.utcnow(),
                        error=None
                    )
                except Exception as e:
                    error_msg = f"Error al enviar email con Resend: {str(e)}"
                    logger.error(f"❌ {error_msg}")
                    import traceback
                    logger.error(f"❌ Traceback: {traceback.format_exc()}")
                    if log_id:
                        self._update_log_status(log_id, EmailStatus.FAILED, error_msg)
                    return EmailResponseBasic(
                        success=False,
                        message="Error al enviar email",
                        fecha_envio=None,
                        error=error_msg
                    )
            
            # Usar SMTP si Resend no está configurado
            if self.email_provider == "smtp":
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
            else:
                # Error de configuración
                error_msg = f"Proveedor de email no disponible: {self.email_provider}"
                if log_id:
                    self._update_log_status(log_id, EmailStatus.FAILED, error_msg)
                return EmailResponseBasic(
                    success=False,
                    message=error_msg,
                    fecha_envio=None,
                    error=error_msg
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
    
    async def send_welcome_email(self, destinatario_email: str, destinatario_nombre: str, 
                                usuario_email: str, codigo_activacion: Optional[str] = None) -> EmailResponseBasic:
        """
        Envía email de bienvenida usando plantilla específica
        
        Args:
            destinatario_email (str): Email del destinatario
            destinatario_nombre (str): Nombre del destinatario
            usuario_email (str): Email del usuario
            codigo_activacion (Optional[str]): Código de activación si aplica
            
        Returns:
            EmailResponseBasic: Resultado del envío
        """
        try:
            # Generar HTML usando la plantilla de bienvenida
            html_content = self.template_service.create_welcome_email(
                destinatario_nombre, usuario_email, codigo_activacion
            )
            
            # Crear datos del email
            email_data = EmailSendBasic(
                destinatario_email=destinatario_email,
                asunto="Bienvenido a InnPulse 360",
                contenido_html=html_content
            )
            
            return await self.send_email(email_data)
            
        except Exception as e:
            logger.error(f"Error al enviar email de bienvenida: {str(e)}")
            return EmailResponseBasic(
                success=False,
                message="Error al procesar email de bienvenida",
                fecha_envio=None,
                error=str(e)
            )
    
    async def send_client_credentials_email(self, destinatario_email: str, destinatario_nombre: str,
                                           login: str, password_temporal: str, 
                                           fecha_expiracion: str) -> EmailResponseBasic:
        """
        Envía email con credenciales de acceso para nuevo cliente (ASYNC)
        
        Args:
            destinatario_email (str): Email del destinatario
            destinatario_nombre (str): Nombre del destinatario
            login (str): Login/usuario del cliente
            password_temporal (str): Contraseña temporal generada
            fecha_expiracion (str): Fecha de expiración formateada
            
        Returns:
            EmailResponseBasic: Resultado del envío
        """
        try:
            # Generar HTML usando la plantilla de credenciales
            html_content = self.template_service.create_client_credentials_email(
                destinatario_nombre, login, password_temporal, fecha_expiracion
            )
            
            # Crear datos del email
            email_data = EmailSendBasic(
                destinatario_email=destinatario_email,
                asunto="Bienvenido a InnPulse 360 - Tus Credenciales de Acceso",
                contenido_html=html_content
            )
            
            return await self.send_email(email_data)
            
        except Exception as e:
            logger.error(f"Error al enviar email de credenciales: {str(e)}")
            return EmailResponseBasic(
                success=False,
                message="Error al procesar email de credenciales",
                fecha_envio=None,
                error=str(e)
            )
    
    def send_client_credentials_email_sync(self, destinatario_email: str, destinatario_nombre: str,
                                           login: str, password_temporal: str, 
                                           fecha_expiracion: str) -> EmailResponseBasic:
        """
        Envía email con credenciales de acceso para nuevo cliente (MÉTODO SÍNCRONO)
        
        Este método es completamente síncrono y puede ser llamado desde cualquier parte
        del código sin preocuparse por event loops o async/await.
        
        Args:
            destinatario_email: Email del destinatario
            destinatario_nombre: Nombre del destinatario  
            login: Usuario para acceder al sistema
            password_temporal: Contraseña temporal generada
            fecha_expiracion: Fecha de expiración (formato: "DD/MM/YYYY a las HH:MM")
            
        Returns:
            EmailResponseBasic con el resultado del envío
        """
        try:
            # 1. Generar contenido HTML del email
            html_content = self._generar_html_credenciales(
                destinatario_nombre, login, password_temporal, fecha_expiracion
            )
            
            # 2. Crear y enviar el mensaje SMTP
            return self._enviar_email_smtp(
                destinatario_email=destinatario_email,
                asunto="Bienvenido a InnPulse 360 - Tus Credenciales de Acceso",
                contenido_html=html_content
            )
            
        except Exception as e:
            logger.error(f"Error al enviar credenciales: {str(e)}")
            return EmailResponseBasic(
                success=False,
                message="Error al enviar email",
                fecha_envio=None,
                error=str(e)
            )
    
    def send_password_recovery_email_sync(self, destinatario_email: str, destinatario_nombre: str,
                                         login: str, password_temporal: str, 
                                         fecha_expiracion: str) -> EmailResponseBasic:
        """
        Envía email con contraseña temporal para recuperación de contraseña (MÉTODO SÍNCRONO)
        
        Este método es completamente síncrono y puede ser llamado desde cualquier parte
        del código sin preocuparse por event loops o async/await.
        
        Args:
            destinatario_email: Email del destinatario
            destinatario_nombre: Nombre del destinatario  
            login: Usuario para acceder al sistema
            password_temporal: Contraseña temporal generada
            fecha_expiracion: Fecha de expiración (formato: "DD/MM/YYYY a las HH:MM")
            
        Returns:
            EmailResponseBasic con el resultado del envío
        """
        try:
            # 1. Generar contenido HTML del email
            html_content = self._generar_html_recuperacion(
                destinatario_nombre, login, password_temporal, fecha_expiracion
            )
            
            # 2. Crear y enviar el mensaje SMTP
            return self._enviar_email_smtp(
                destinatario_email=destinatario_email,
                asunto="Recuperación de Contraseña - InnPulse 360",
                contenido_html=html_content
            )
            
        except Exception as e:
            logger.error(f"Error al enviar email de recuperación: {str(e)}")
            return EmailResponseBasic(
                success=False,
                message="Error al enviar email",
                fecha_envio=None,
                error=str(e)
            )
    
    def _generar_html_credenciales(self, destinatario_nombre: str, login: str,
                                   password_temporal: str, fecha_expiracion: str) -> str:
        """
        Genera el contenido HTML para email de credenciales
        
        Args:
            destinatario_nombre: Nombre del destinatario
            login: Usuario del sistema
            password_temporal: Contraseña temporal
            fecha_expiracion: Fecha de expiración formateada
            
        Returns:
            HTML del email
        """
        return self.template_service.create_client_credentials_email(
            destinatario_nombre, login, password_temporal, fecha_expiracion
        )
    
    def _generar_html_recuperacion(self, destinatario_nombre: str, login: str,
                                   password_temporal: str, fecha_expiracion: str) -> str:
        """
        Genera el contenido HTML para email de recuperación de contraseña
        
        Args:
            destinatario_nombre: Nombre del destinatario
            login: Usuario del sistema
            password_temporal: Contraseña temporal
            fecha_expiracion: Fecha de expiración formateada
            
        Returns:
            HTML del email
        """
        return self.template_service.create_password_recovery_email(
            destinatario_nombre, login, password_temporal, fecha_expiracion
        )
    
    def _enviar_email_smtp(self, destinatario_email: str, asunto: str, 
                          contenido_html: str) -> EmailResponseBasic:
        """
        Envía un email usando Resend o SMTP según configuración
        Método genérico que detecta automáticamente el proveedor configurado
        
        Args:
            destinatario_email: Email del destinatario
            asunto: Asunto del email
            contenido_html: Contenido HTML del mensaje
        
        Returns:
            EmailResponseBasic con el resultado
        """
        # Usar Resend si está configurado
        if self.email_provider == "resend" and self.resend_service:
            try:
                logger.info(f"📧 [EmailService] Usando Resend para enviar email a {destinatario_email}")
                logger.info(f"📧 [EmailService] Debug - from_email: '{self.from_email}' (type: {type(self.from_email)})")
                logger.info(f"📧 [EmailService] Debug - from_name: '{self.from_name}' (type: {type(self.from_name)})")
                
                # Obtener valores de EmailSettings directamente como fallback
                from_email_value = self.from_email or EmailSettings.from_email
                from_name_value = self.from_name or EmailSettings.from_name
                
                logger.info(f"📧 [EmailService] Valores después de fallback - from_email: '{from_email_value}', from_name: '{from_name_value}'")
                
                # Validar que from_email esté configurado
                if not from_email_value or not str(from_email_value).strip():
                    error_msg = f"FromEmail no está configurado para Resend. Valor actual: '{from_email_value}'"
                    logger.error(f"❌ {error_msg}")
                    return EmailResponseBasic(
                        success=False,
                        message=error_msg,
                        fecha_envio=None,
                        error=error_msg
                    )
                
                import resend
                
                # Asegurar que resend.api_key esté configurado (usar el servicio inicializado si está disponible)
                if self.resend_service and hasattr(self.resend_service, 'api_key'):
                    resend.api_key = self.resend_service.api_key
                    logger.info(f"📧 [EmailService] Usando api_key del resend_service")
                elif not hasattr(resend, 'api_key') or not resend.api_key:
                    resend.api_key = EmailSettings.resend_api_key
                    logger.info(f"📧 [EmailService] Configurando resend.api_key desde EmailSettings")
                
                logger.info(f"📧 [EmailService] resend.api_key configurado: {'Sí' if hasattr(resend, 'api_key') and resend.api_key else 'No'}")
                
                # Formatear el remitente
                from_email_str = str(from_email_value).strip()
                if from_name_value and str(from_name_value).strip():
                    from_value = f"{from_name_value} <{from_email_str}>"
                else:
                    from_value = from_email_str
                
                logger.info(f"📧 [EmailService] From value final: '{from_value}'")
                
                # Crear parámetros usando el mismo formato que resend_service.py
                params = resend.Emails.SendParams(
                    from_=from_value,
                    to=[destinatario_email],
                    subject=asunto,
                    html=contenido_html,
                )
                
                # Logging adicional para depuración
                logger.info(f"📧 [EmailService] Params tipo: {type(params)}")
                if isinstance(params, dict):
                    logger.info(f"📧 [EmailService] Params keys antes: {list(params.keys())}")
                    # Verificar si tiene 'from' o 'from_'
                    if 'from' not in params:
                        if 'from_' in params:
                            # Convertir 'from_' a 'from'
                            params['from'] = params.pop('from_')
                            logger.info(f"📧 [EmailService] Convertido 'from_' a 'from' manualmente")
                        else:
                            # Si no tiene ninguno, agregarlo directamente
                            params['from'] = from_value
                            logger.info(f"📧 [EmailService] Agregado 'from' directamente: '{from_value}'")
                    logger.info(f"📧 [EmailService] Params keys después: {list(params.keys())}")
                    logger.info(f"📧 [EmailService] Params 'from' value: {params.get('from', 'NO_ENCONTRADO')}")
                else:
                    logger.info(f"📧 [EmailService] Params dict: {params.__dict__ if hasattr(params, '__dict__') else 'No __dict__'}")
                
                email = resend.Emails.send(params)
                logger.info(f"✅ [Resend] Email enviado exitosamente. ID: {email.id}")
                
                return EmailResponseBasic(
                    success=True,
                    message="Email enviado exitosamente",
                    fecha_envio=datetime.utcnow(),
                    error=None
                )
            except Exception as e:
                error_msg = f"Error al enviar email con Resend: {str(e)}"
                logger.error(f"❌ {error_msg}")
                import traceback
                logger.error(f"❌ Traceback: {traceback.format_exc()}")
                return EmailResponseBasic(
                    success=False,
                    message="Error al enviar email",
                    fecha_envio=None,
                    error=error_msg
                )
        
        # Usar SMTP si Resend no está configurado
        if self.email_provider == "smtp":
            try:
                # 1. Validar configuración SMTP
                if not self._validate_config():
                    return EmailResponseBasic(
                        success=False,
                        message="Configuración de email incompleta",
                        fecha_envio=None,
                        error="Faltan credenciales SMTP"
                    )
                
                # 2. Crear mensaje MIME
                message = self._crear_mensaje_mime(destinatario_email, asunto, contenido_html)
                
                # 3. Enviar por SMTP
                self._send_smtp(message, destinatario_email)
                
                # 4. Retornar éxito
                logger.info(f"Email enviado exitosamente a {destinatario_email}")
                return EmailResponseBasic(
                    success=True,
                    message="Email enviado exitosamente",
                    fecha_envio=datetime.utcnow(),
                    error=None
                )
                
            except smtplib.SMTPAuthenticationError as e:
                error_msg = "Error de autenticación SMTP"
                logger.error(f"{error_msg}: {str(e)}")
                return EmailResponseBasic(
                    success=False,
                    message=error_msg,
                    fecha_envio=None,
                    error=str(e)
                )
                
            except smtplib.SMTPException as e:
                error_msg = f"Error SMTP: {str(e)}"
                logger.error(error_msg)
                return EmailResponseBasic(
                    success=False,
                    message="Error al enviar email",
                    fecha_envio=None,
                    error=error_msg
                )
                
            except Exception as e:
                error_msg = f"Error inesperado: {str(e)}"
                logger.error(error_msg)
                return EmailResponseBasic(
                    success=False,
                    message="Error al procesar email",
                    fecha_envio=None,
                    error=error_msg
                )
        else:
            # Si Resend está configurado pero no se pudo inicializar
            error_msg = f"Resend está configurado pero no está disponible. Proveedor: {self.email_provider}"
            logger.error(f"❌ {error_msg}")
            return EmailResponseBasic(
                success=False,
                message="Error de configuración de email",
                fecha_envio=None,
                error=error_msg
            )
    
    def _crear_mensaje_mime(self, destinatario_email: str, asunto: str, 
                           contenido_html: str) -> MIMEMultipart:
        """
        Crea un mensaje MIME con el contenido del email
        
        Args:
            destinatario_email: Email del destinatario
            asunto: Asunto del mensaje
            contenido_html: Contenido HTML (ya viene con la plantilla base aplicada)
            
        Returns:
            MIMEMultipart con el mensaje completo
        """
        # Crear mensaje multipart
        message = MIMEMultipart("alternative")
        message["Subject"] = asunto
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = destinatario_email
        
        # El HTML ya viene procesado con la plantilla base desde template_service
        # No necesitamos volver a aplicar la plantilla aquí
        html_part = MIMEText(contenido_html, "html", "utf-8")
        message.attach(html_part)
        
        return message
    
    async def send_password_reset_email(self, destinatario_email: str, destinatario_nombre: str,
                                      reset_token: str) -> EmailResponseBasic:
        """
        Envía email de restablecimiento de contraseña
        
        Args:
            destinatario_email (str): Email del destinatario
            destinatario_nombre (str): Nombre del destinatario
            reset_token (str): Token para restablecer contraseña
            
        Returns:
            EmailResponseBasic: Resultado del envío
        """
        try:
            # Generar HTML usando la plantilla de restablecimiento
            html_content = self.template_service.create_password_reset_email(
                destinatario_nombre, reset_token
            )
            
            # Crear datos del email
            email_data = EmailSendBasic(
                destinatario_email=destinatario_email,
                asunto="Restablecer contraseña - InnPulse 360",
                contenido_html=html_content
            )
            
            return await self.send_email(email_data)
            
        except Exception as e:
            logger.error(f"Error al enviar email de restablecimiento: {str(e)}")
            return EmailResponseBasic(
                success=False,
                message="Error al procesar email de restablecimiento",
                fecha_envio=None,
                error=str(e)
            )
    
    async def send_role_assignment_email(self, destinatario_email: str, destinatario_nombre: str,
                                       rol_asignado: str, asignado_por: str) -> EmailResponseBasic:
        """
        Envía email de asignación de rol
        
        Args:
            destinatario_email (str): Email del destinatario
            destinatario_nombre (str): Nombre del destinatario
            rol_asignado (str): Rol que se asignó
            asignado_por (str): Quién asignó el rol
            
        Returns:
            EmailResponseBasic: Resultado del envío
        """
        try:
            # Generar HTML usando la plantilla de asignación de rol
            html_content = self.template_service.create_role_assignment_email(
                destinatario_nombre, rol_asignado, asignado_por
            )
            
            # Crear datos del email
            email_data = EmailSendBasic(
                destinatario_email=destinatario_email,
                asunto=f"Nuevo rol asignado: {rol_asignado}",
                contenido_html=html_content
            )
            
            return await self.send_email(email_data)
            
        except Exception as e:
            logger.error(f"Error al enviar email de asignación de rol: {str(e)}")
            return EmailResponseBasic(
                success=False,
                message="Error al procesar email de asignación de rol",
                fecha_envio=None,
                error=str(e)
            )
    
    async def send_hotel_notification_email(self, destinatario_email: str, destinatario_nombre: str,
                                          hotel_nombre: str, tipo_notificacion: str, 
                                          mensaje: str) -> EmailResponseBasic:
        """
        Envía email de notificación de hotel
        
        Args:
            destinatario_email (str): Email del destinatario
            destinatario_nombre (str): Nombre del destinatario
            hotel_nombre (str): Nombre del hotel
            tipo_notificacion (str): Tipo de notificación
            mensaje (str): Mensaje específico
            
        Returns:
            EmailResponseBasic: Resultado del envío
        """
        try:
            # Generar HTML usando la plantilla de notificación de hotel
            html_content = self.template_service.create_hotel_notification_email(
                destinatario_nombre, hotel_nombre, tipo_notificacion, mensaje
            )
            
            # Crear datos del email
            email_data = EmailSendBasic(
                destinatario_email=destinatario_email,
                asunto=f"Notificación de hotel: {hotel_nombre}",
                contenido_html=html_content
            )
            
            return await self.send_email(email_data)
            
        except Exception as e:
            logger.error(f"Error al enviar email de notificación de hotel: {str(e)}")
            return EmailResponseBasic(
                success=False,
                message="Error al procesar email de notificación de hotel",
                fecha_envio=None,
                error=str(e)
            )
    
    async def send_booking_confirmation_email(self, destinatario_email: str, destinatario_nombre: str,
                                            hotel_nombre: str, fecha_llegada: str, 
                                            fecha_salida: str, numero_reserva: str) -> EmailResponseBasic:
        """
        Envía email de confirmación de reserva
        
        Args:
            destinatario_email (str): Email del destinatario
            destinatario_nombre (str): Nombre del destinatario
            hotel_nombre (str): Nombre del hotel
            fecha_llegada (str): Fecha de llegada
            fecha_salida (str): Fecha de salida
            numero_reserva (str): Número de reserva
            
        Returns:
            EmailResponseBasic: Resultado del envío
        """
        try:
            # Generar HTML usando la plantilla de confirmación de reserva
            html_content = self.template_service.create_booking_confirmation_email(
                destinatario_nombre, hotel_nombre, fecha_llegada, fecha_salida, numero_reserva
            )
            
            # Crear datos del email
            email_data = EmailSendBasic(
                destinatario_email=destinatario_email,
                asunto=f"Confirmación de reserva #{numero_reserva}",
                contenido_html=html_content
            )
            
            return await self.send_email(email_data)
            
        except Exception as e:
            logger.error(f"Error al enviar email de confirmación de reserva: {str(e)}")
            return EmailResponseBasic(
                success=False,
                message="Error al procesar email de confirmación de reserva",
                fecha_envio=None,
                error=str(e)
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
        Crea el mensaje de email usando la plantilla base
        
        Args:
            email_data (EmailSendBasic): Datos del email
            
        Returns:
            MIMEMultipart: Mensaje creado
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = email_data.asunto
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = email_data.destinatario_email
        
        # Procesar contenido HTML con la plantilla base
        html_content = self._process_html_content(email_data)
        
        # Crear parte HTML
        html_part = MIMEText(html_content, "html", "utf-8")
        message.attach(html_part)
        
        return message
    
    def _process_html_content(self, email_data: EmailSendBasic) -> str:
        """
        Procesa el contenido HTML usando la plantilla base
        
        Args:
            email_data (EmailSendBasic): Datos del email
            
        Returns:
            str: HTML procesado
        """
        try:
            # Usar la plantilla base para el contenido personalizado
            variables = {
                'contenido_principal': email_data.contenido_html
            }
            
            return self.template_service.render_base_template(variables)
            
        except Exception as e:
            logger.warning(f"Error al procesar plantilla, usando contenido directo: {str(e)}")
            # Fallback al contenido original si falla la plantilla
            return email_data.contenido_html
    
    def _send_smtp(self, message: MIMEMultipart, destinatario: str):
        """
        Envía el mensaje vía SMTP
        SOLO debe llamarse si email_provider == "smtp"
        """
        # Validación de seguridad: NO usar SMTP si Resend está configurado
        if self.email_provider == "resend":
            error_msg = "ERROR: Se intentó usar SMTP pero Resend está configurado (USE_RESEND=true). Esto no debería pasar."
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)
        
        try:
            logger.info(f"Intentando conectar a SMTP: {self.smtp_server}:{self.smtp_port}")
            logger.info(f"Timeout configurado: 10 segundos")
            
            # Conectar al servidor SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                logger.info("Conexión SMTP establecida")
                server.ehlo()
                
                # Iniciar TLS si está habilitado
                if self.use_tls:
                    logger.info("Iniciando TLS...")
                    server.starttls()
                    server.ehlo()
                
                logger.info("Autenticando con servidor SMTP...")
                # Autenticarse
                server.login(self.username, self.password)
                logger.info("Autenticación exitosa")
                
                # Enviar email
                logger.info(f"Enviando mensaje a {destinatario}...")
                server.send_message(message)
                
                logger.info(f"Mensaje enviado exitosamente a {destinatario}")
                
        except Exception as e:
            error_msg = f"Error al enviar SMTP: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Detalles de conexión: Server={self.smtp_server}, Port={self.smtp_port}, TLS={self.use_tls}")
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
        precio_total: float
    ) -> EmailResponseBasic:
        """
        Envía email de cotización con PDF adjunto
        
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
        
        Returns:
            EmailResponseBasic: Resultado del envío
        """
        try:
            # Validar email del destinatario
            if not destinatario_email or not destinatario_email.strip():
                error_msg = "Email del destinatario está vacío o es inválido"
                logger.error(f"❌ {error_msg}")
                return EmailResponseBasic(
                    success=False,
                    message=error_msg,
                    fecha_envio=None,
                    error=error_msg
                )
            
            # Limpiar y validar email
            destinatario_email = destinatario_email.strip()
            logger.info(f"📧 [EmailService] Preparando envío de cotización a: {destinatario_email}")
            logger.info(f"📧 [EmailService] Cliente: {destinatario_nombre}")
            logger.info(f"📧 [EmailService] Código de reservación: {codigo_reservacion}")
            logger.info(f"📧 [EmailService] Proveedor: {self.email_provider}")
            
            # Generar HTML del email usando la plantilla (común para ambos proveedores)
            logger.info(f"📧 [EmailService] Generando HTML del email...")
            # Formatear precios como strings para evitar problemas de sintaxis en Jinja2
            precio_unitario_str = f"{precio_unitario:.2f}"
            precio_total_str = f"{precio_total:.2f}"
            
            html_content = self.template_service.render_template(
                'quotation_template.html',
                {
                    'cliente_nombre': destinatario_nombre,
                    'codigo_reservacion': codigo_reservacion,
                    'fecha_entrada': fecha_entrada,
                    'fecha_salida': fecha_salida,
                    'duracion_dias': duracion_dias,
                    'hotel_nombre': hotel_nombre,
                    'hotel_direccion': hotel_direccion,
                    'hotel_telefono': hotel_telefono,
                    'hotel_email': hotel_email,
                    'habitacion_nombre': habitacion_nombre,
                    'habitacion_descripcion': habitacion_descripcion,
                    'tipo_habitacion': tipo_habitacion,
                    'precio_unitario': precio_unitario_str,
                    'periodicidad_nombre': periodicidad_nombre,
                    'precio_total': precio_total_str,
                }
            )
            
            # Usar Resend si está configurado - VALIDACIÓN ESTRICTA
            if self.email_provider == "resend":
                if self.resend_service:
                    logger.info("📧 [EmailService] Usando Resend API para enviar email")
                    logger.info(f"📧 [EmailService] Llamando a resend_service.send_quotation_email()...")
                    resultado = self.resend_service.send_quotation_email(
                        destinatario_email=destinatario_email,
                        destinatario_nombre=destinatario_nombre,
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
                        cliente_rfc=cliente_rfc,
                        cliente_identificacion=cliente_identificacion,
                        precio_unitario=precio_unitario,
                        periodicidad_nombre=periodicidad_nombre,
                        precio_total=precio_total,
                        html_content=html_content
                    )
                    logger.info(f"📧 [EmailService] Resultado de Resend: success={resultado.success}, error={resultado.error}")
                    return resultado
                else:
                    # Si Resend está configurado pero el servicio no se inicializó, es un error crítico
                    error_msg = "Resend está configurado (USE_RESEND=true) pero el servicio no se pudo inicializar. Verifica RESEND_API_KEY."
                    logger.error(f"❌ {error_msg}")
                    return EmailResponseBasic(
                        success=False,
                        message=error_msg,
                        fecha_envio=None,
                        error=error_msg
                    )
            
            # SOLO usar SMTP si Resend NO está configurado
            if self.email_provider == "smtp":
                logger.info("📧 [EmailService] Usando SMTP para enviar email")
                
                # Generar PDF usando reportlab
                logger.info(f"📧 [EmailService] Generando PDF de cotización...")
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
                
                # Crear mensaje multipart
                logger.info(f"📧 [EmailService] Creando mensaje MIME para: {destinatario_email}")
                message = MIMEMultipart("related")
                message["Subject"] = f"Cotización de Reservación - {codigo_reservacion}"
                message["From"] = f"{self.from_name} <{self.from_email}>"
                message["To"] = destinatario_email
                
                logger.info(f"📧 [EmailService] Remitente: {self.from_name} <{self.from_email}>")
                logger.info(f"📧 [EmailService] Destinatario: {destinatario_email}")
                
                # Agregar parte HTML
                html_part = MIMEText(html_content, "html", "utf-8")
                message.attach(html_part)
                
                # Adjuntar PDF
                pdf_part = MIMEBase('application', 'pdf')
                pdf_bytes.seek(0)  # Asegurar que esté en posición 0
                pdf_part.set_payload(pdf_bytes.getvalue())
                encoders.encode_base64(pdf_part)
                pdf_part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="Cotizacion_{codigo_reservacion}.pdf"'
                )
                message.attach(pdf_part)
                
                # Enviar email
                self._send_smtp(message, destinatario_email)
                
                logger.info(f"Email de cotización enviado exitosamente a {destinatario_email}")
                return EmailResponseBasic(
                    success=True,
                    message="Email de cotización enviado exitosamente",
                    fecha_envio=datetime.utcnow(),
                    error=None
                )
            else:
                # Esto no debería pasar, pero por seguridad
                error_msg = f"Proveedor de email desconocido: {self.email_provider}"
                logger.error(f"❌ {error_msg}")
                return EmailResponseBasic(
                    success=False,
                    message=error_msg,
                    fecha_envio=None,
                    error=error_msg
                )
            
        except Exception as e:
            error_msg = f"Error al enviar email de cotización: {str(e)}"
            logger.error(error_msg)
            return EmailResponseBasic(
                success=False,
                message="Error al enviar email de cotización",
                fecha_envio=None,
                error=error_msg
            )
    
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
