"""
Schemas básicos para envío de emails
Define estructuras simples para testing de envío
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class EmailSendBasic(BaseModel):
    """
    Schema básico para envío de email
    """
    destinatario_email: EmailStr = Field(
        ...,
        description="Email del destinatario",
        example="usuario@ejemplo.com"
    )
    
    asunto: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Asunto del email",
        example="Prueba de Email"
    )
    
    contenido_html: str = Field(
        ...,
        min_length=1,
        description="Contenido HTML del email",
        example="<h1>Hola</h1><p>Este es un email de prueba.</p>"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "destinatario_email": "usuario@ejemplo.com",
                "asunto": "Prueba de Email",
                "contenido_html": "<h1>Hola</h1><p>Este es un email de prueba desde InnPulse360.</p>"
            }
        }


class EmailResponseBasic(BaseModel):
    """
    Schema básico para respuesta de envío
    """
    success: bool = Field(
        ...,
        description="Si el email se envió exitosamente"
    )
    
    message: str = Field(
        ...,
        description="Mensaje descriptivo del resultado"
    )
    
    fecha_envio: Optional[datetime] = Field(
        None,
        description="Fecha y hora de envío"
    )
    
    error: Optional[str] = Field(
        None,
        description="Mensaje de error si falló"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Email enviado exitosamente",
                "fecha_envio": "2024-01-15T10:30:00Z",
                "error": None
            }
        }
