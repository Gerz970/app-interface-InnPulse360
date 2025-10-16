"""
Schemas Pydantic para el sistema de email
Define la estructura de datos para validación y serialización
"""

from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class EmailProvider(str, Enum):
    """
    Proveedores de email soportados
    """
    SMTP = "smtp"
    SENDGRID = "sendgrid"
    AWS_SES = "aws_ses"
    MAILGUN = "mailgun"


class EmailStatus(str, Enum):
    """
    Estados posibles de un email
    """
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRY = "retry"


class EmailType(str, Enum):
    """
    Tipos de email disponibles
    """
    WELCOME_USER = "welcome_user"
    PASSWORD_RESET = "password_reset"
    ROLE_ASSIGNMENT = "role_assignment"
    HOTEL_NOTIFICATION = "hotel_notification"
    BOOKING_CONFIRMATION = "booking_confirmation"
    SYSTEM_ALERT = "system_alert"
    CUSTOM = "custom"


class EmailSend(BaseModel):
    """
    Schema para envío de email
    """
    destinatario_email: EmailStr = Field(
        ...,
        description="Email del destinatario",
        example="usuario@example.com"
    )
    
    destinatario_nombre: Optional[str] = Field(
        None,
        description="Nombre del destinatario",
        example="Juan Pérez"
    )
    
    asunto: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Asunto del email",
        example="Bienvenido a InnPulse360"
    )
    
    contenido_html: Optional[str] = Field(
        None,
        description="Contenido HTML del email"
    )
    
    contenido_texto: Optional[str] = Field(
        None,
        description="Contenido en texto plano del email"
    )
    
    tipo_email: EmailType = Field(
        EmailType.CUSTOM,
        description="Tipo de email"
    )
    
    variables: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Variables para reemplazar en la plantilla",
        example={"nombre": "Juan", "codigo": "123456"}
    )
    
    id_template: Optional[int] = Field(
        None,
        description="ID de la plantilla a utilizar"
    )
    
    prioridad: Optional[int] = Field(
        1,
        ge=1,
        le=5,
        description="Prioridad del email (1=alta, 5=baja)"
    )
    
    @validator('contenido_html', 'contenido_texto')
    def validar_contenido(cls, v, values):
        """
        Valida que al menos uno de los contenidos esté presente
        """
        if not v and not values.get('id_template'):
            if 'contenido_html' in values and not values['contenido_html']:
                raise ValueError('Debe proporcionar contenido_html, contenido_texto o id_template')
        return v


class EmailResponse(BaseModel):
    """
    Schema para respuesta de email enviado
    """
    id_log: int = Field(
        ...,
        description="ID del log de email"
    )
    
    destinatario_email: EmailStr = Field(
        ...,
        description="Email del destinatario"
    )
    
    asunto: str = Field(
        ...,
        description="Asunto del email"
    )
    
    estado_envio: EmailStatus = Field(
        ...,
        description="Estado del envío"
    )
    
    fecha_envio: Optional[datetime] = Field(
        None,
        description="Fecha y hora de envío"
    )
    
    tipo_email: EmailType = Field(
        ...,
        description="Tipo de email"
    )
    
    intentos_envio: int = Field(
        ...,
        description="Número de intentos de envío"
    )
    
    error_mensaje: Optional[str] = Field(
        None,
        description="Mensaje de error si falló"
    )
    
    class Config:
        from_attributes = True


class EmailTemplateCreate(BaseModel):
    """
    Schema para crear plantilla de email
    """
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre único de la plantilla",
        example="bienvenida_usuario"
    )
    
    descripcion: Optional[str] = Field(
        None,
        max_length=255,
        description="Descripción de la plantilla"
    )
    
    tipo_template: EmailType = Field(
        ...,
        description="Tipo de plantilla"
    )
    
    asunto: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Asunto del email (puede contener variables)",
        example="Bienvenido {nombre} a InnPulse360"
    )
    
    contenido_html: str = Field(
        ...,
        min_length=1,
        description="Contenido HTML de la plantilla"
    )
    
    contenido_texto: Optional[str] = Field(
        None,
        description="Contenido en texto plano"
    )
    
    variables_disponibles: Optional[str] = Field(
        None,
        description="JSON con variables disponibles",
        example='["nombre", "email", "codigo"]'
    )
    
    idioma: str = Field(
        "es",
        min_length=2,
        max_length=5,
        description="Código de idioma",
        example="es"
    )
    
    es_default: bool = Field(
        False,
        description="Si es la plantilla por defecto para este tipo"
    )


class EmailTemplateUpdate(BaseModel):
    """
    Schema para actualizar plantilla de email
    """
    nombre: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Nombre único de la plantilla"
    )
    
    descripcion: Optional[str] = Field(
        None,
        max_length=255,
        description="Descripción de la plantilla"
    )
    
    asunto: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Asunto del email"
    )
    
    contenido_html: Optional[str] = Field(
        None,
        min_length=1,
        description="Contenido HTML de la plantilla"
    )
    
    contenido_texto: Optional[str] = Field(
        None,
        description="Contenido en texto plano"
    )
    
    variables_disponibles: Optional[str] = Field(
        None,
        description="JSON con variables disponibles"
    )
    
    activo: Optional[bool] = Field(
        None,
        description="Si la plantilla está activa"
    )
    
    es_default: Optional[bool] = Field(
        None,
        description="Si es la plantilla por defecto para este tipo"
    )


class EmailTemplateResponse(BaseModel):
    """
    Schema para respuesta de plantilla de email
    """
    id_template: int = Field(
        ...,
        description="ID de la plantilla"
    )
    
    nombre: str = Field(
        ...,
        description="Nombre de la plantilla"
    )
    
    descripcion: Optional[str] = Field(
        None,
        description="Descripción de la plantilla"
    )
    
    tipo_template: EmailType = Field(
        ...,
        description="Tipo de plantilla"
    )
    
    asunto: str = Field(
        ...,
        description="Asunto del email"
    )
    
    idioma: str = Field(
        ...,
        description="Código de idioma"
    )
    
    activo: bool = Field(
        ...,
        description="Si la plantilla está activa"
    )
    
    es_default: bool = Field(
        ...,
        description="Si es la plantilla por defecto"
    )
    
    fecha_creacion: datetime = Field(
        ...,
        description="Fecha de creación"
    )
    
    fecha_actualizacion: Optional[datetime] = Field(
        None,
        description="Fecha de última actualización"
    )
    
    class Config:
        from_attributes = True


class EmailLogResponse(BaseModel):
    """
    Schema para respuesta de log de email
    """
    id_log: int
    destinatario_email: EmailStr
    destinatario_nombre: Optional[str]
    asunto: str
    tipo_email: EmailType
    estado_envio: EmailStatus
    fecha_envio: Optional[datetime]
    fecha_entrega: Optional[datetime]
    intentos_envio: int
    error_mensaje: Optional[str]
    proveedor_email: str
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True


class EmailStats(BaseModel):
    """
    Schema para estadísticas de email
    """
    total_enviados: int = Field(
        ...,
        description="Total de emails enviados"
    )
    
    total_entregados: int = Field(
        ...,
        description="Total de emails entregados"
    )
    
    total_fallidos: int = Field(
        ...,
        description="Total de emails fallidos"
    )
    
    tasa_entrega: float = Field(
        ...,
        description="Tasa de entrega (porcentaje)"
    )
    
    por_tipo: Dict[str, int] = Field(
        ...,
        description="Emails por tipo"
    )
    
    por_estado: Dict[str, int] = Field(
        ...,
        description="Emails por estado"
    )
