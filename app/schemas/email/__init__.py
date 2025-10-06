"""
Schemas para módulo de email
Contiene schemas Pydantic para validación de datos de email
"""

from .email_schemas import EmailSend, EmailResponse, EmailTemplateCreate, EmailTemplateResponse
from .notification_schemas import NotificationRequest, NotificationResponse

__all__ = [
    "EmailSend", 
    "EmailResponse", 
    "EmailTemplateCreate", 
    "EmailTemplateResponse",
    "NotificationRequest", 
    "NotificationResponse"
]
