"""
Configuración para el sistema de correo electrónico
Maneja la configuración SMTP y plantillas de email
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Cargar variables de entorno
if os.path.exists(".development.env"):
    load_dotenv(".development.env")
else:
    load_dotenv(".production.env")


class EmailSettings:
    """
    Configuración para el servicio de email
    Soporta múltiples proveedores SMTP
    """
    
    # Configuración SMTP
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: str = os.getenv("SMTP_USERNAME", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    use_tls: bool = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    use_ssl: bool = os.getenv("SMTP_USE_SSL", "false").lower() == "true"
    
    # Configuración del remitente
    from_email: str = os.getenv("FROM_EMAIL", "noreply@innpulse360.com")
    from_name: str = os.getenv("FROM_NAME", "InnPulse360")
    
    # Configuración de plantillas
    template_dir: str = os.getenv("EMAIL_TEMPLATE_DIR", "app/core/email_templates")
    default_language: str = os.getenv("DEFAULT_LANGUAGE", "es")
    
    # Configuración de cola de emails (para procesamiento asíncrono)
    use_queue: bool = os.getenv("EMAIL_USE_QUEUE", "false").lower() == "true"
    max_retries: int = int(os.getenv("EMAIL_MAX_RETRIES", "3"))
    retry_delay: int = int(os.getenv("EMAIL_RETRY_DELAY", "60"))  # segundos
    
    # Configuración de logging
    log_emails: bool = os.getenv("EMAIL_LOG_ENABLED", "true").lower() == "true"
    log_level: str = os.getenv("EMAIL_LOG_LEVEL", "INFO")
    
    # Configuración de desarrollo
    debug_mode: bool = os.getenv("EMAIL_DEBUG", "false").lower() == "true"
    test_mode: bool = os.getenv("EMAIL_TEST_MODE", "false").lower() == "true"
    test_recipient: Optional[str] = os.getenv("EMAIL_TEST_RECIPIENT")
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Valida que la configuración de email esté completa
        
        Returns:
            bool: True si la configuración es válida
        """
        required_fields = [
            cls.smtp_server,
            cls.smtp_username,
            cls.smtp_password,
            cls.from_email
        ]
        
        return all(field for field in required_fields)
    
    @classmethod
    def get_smtp_config(cls) -> dict:
        """
        Obtiene la configuración SMTP como diccionario
        
        Returns:
            dict: Configuración SMTP
        """
        return {
            "server": cls.smtp_server,
            "port": cls.smtp_port,
            "username": cls.smtp_username,
            "password": cls.smtp_password,
            "use_tls": cls.use_tls,
            "use_ssl": cls.use_ssl,
            "from_email": cls.from_email,
            "from_name": cls.from_name
        }


class EmailTemplateConfig:
    """
    Configuración para plantillas de email
    """
    
    # Tipos de plantillas disponibles
    WELCOME_USER = "welcome_user"
    PASSWORD_RESET = "password_reset"
    ROLE_ASSIGNMENT = "role_assignment"
    HOTEL_NOTIFICATION = "hotel_notification"
    BOOKING_CONFIRMATION = "booking_confirmation"
    SYSTEM_ALERT = "system_alert"
    
    # Configuración de estilos
    PRIMARY_COLOR = os.getenv("EMAIL_PRIMARY_COLOR", "#2563eb")
    SECONDARY_COLOR = os.getenv("EMAIL_SECONDARY_COLOR", "#64748b")
    SUCCESS_COLOR = os.getenv("EMAIL_SUCCESS_COLOR", "#059669")
    WARNING_COLOR = os.getenv("EMAIL_WARNING_COLOR", "#d97706")
    ERROR_COLOR = os.getenv("EMAIL_ERROR_COLOR", "#dc2626")
    
    # Configuración de branding
    COMPANY_NAME = os.getenv("COMPANY_NAME", "InnPulse360")
    COMPANY_LOGO_URL = os.getenv("COMPANY_LOGO_URL", "")
    COMPANY_WEBSITE = os.getenv("COMPANY_WEBSITE", "https://innpulse360.com")
    SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "support@innpulse360.com")
    
    @classmethod
    def get_template_variables(cls) -> dict:
        """
        Obtiene las variables globales para plantillas
        
        Returns:
            dict: Variables globales
        """
        return {
            "company_name": cls.COMPANY_NAME,
            "company_logo_url": cls.COMPANY_LOGO_URL,
            "company_website": cls.COMPANY_WEBSITE,
            "support_email": cls.SUPPORT_EMAIL,
            "primary_color": cls.PRIMARY_COLOR,
            "secondary_color": cls.SECONDARY_COLOR,
            "success_color": cls.SUCCESS_COLOR,
            "warning_color": cls.WARNING_COLOR,
            "error_color": cls.ERROR_COLOR
        }
