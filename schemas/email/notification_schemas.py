"""
Schemas para notificaciones del sistema
Define estructuras para diferentes tipos de notificaciones por email
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
from .email_schemas import EmailType


class NotificationRequest(BaseModel):
    """
    Schema base para solicitudes de notificación
    """
    tipo_notificacion: EmailType = Field(
        ...,
        description="Tipo de notificación a enviar"
    )
    
    destinatario_email: EmailStr = Field(
        ...,
        description="Email del destinatario"
    )
    
    destinatario_nombre: Optional[str] = Field(
        None,
        description="Nombre del destinatario"
    )
    
    variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="Variables específicas para la notificación"
    )
    
    idioma: str = Field(
        "es",
        description="Idioma de la notificación"
    )
    
    prioridad: int = Field(
        1,
        ge=1,
        le=5,
        description="Prioridad de la notificación"
    )


class WelcomeUserNotification(BaseModel):
    """
    Notificación de bienvenida para nuevo usuario
    """
    usuario_email: EmailStr = Field(
        ...,
        description="Email del nuevo usuario"
    )
    
    usuario_nombre: str = Field(
        ...,
        description="Nombre del usuario"
    )
    
    usuario_login: str = Field(
        ...,
        description="Login del usuario"
    )
    
    password_temporal: Optional[str] = Field(
        None,
        description="Contraseña temporal si aplica"
    )
    
    url_activacion: Optional[str] = Field(
        None,
        description="URL para activar la cuenta"
    )
    
    roles_asignados: List[str] = Field(
        default_factory=list,
        description="Lista de roles asignados"
    )


class PasswordResetNotification(BaseModel):
    """
    Notificación para reset de contraseña
    """
    usuario_email: EmailStr = Field(
        ...,
        description="Email del usuario"
    )
    
    usuario_nombre: str = Field(
        ...,
        description="Nombre del usuario"
    )
    
    codigo_reset: str = Field(
        ...,
        description="Código para resetear contraseña"
    )
    
    url_reset: str = Field(
        ...,
        description="URL para resetear contraseña"
    )
    
    expiracion_minutos: int = Field(
        30,
        description="Minutos hasta que expire el código"
    )
    
    ip_solicitud: Optional[str] = Field(
        None,
        description="IP desde donde se solicitó el reset"
    )


class RoleAssignmentNotification(BaseModel):
    """
    Notificación de asignación de roles
    """
    usuario_email: EmailStr = Field(
        ...,
        description="Email del usuario"
    )
    
    usuario_nombre: str = Field(
        ...,
        description="Nombre del usuario"
    )
    
    roles_nuevos: List[str] = Field(
        ...,
        description="Nuevos roles asignados"
    )
    
    roles_removidos: List[str] = Field(
        default_factory=list,
        description="Roles removidos"
    )
    
    asignado_por: str = Field(
        ...,
        description="Usuario que realizó la asignación"
    )
    
    fecha_asignacion: datetime = Field(
        ...,
        description="Fecha de la asignación"
    )


class HotelNotification(BaseModel):
    """
    Notificación relacionada con hoteles
    """
    usuario_email: EmailStr = Field(
        ...,
        description="Email del usuario a notificar"
    )
    
    usuario_nombre: str = Field(
        ...,
        description="Nombre del usuario"
    )
    
    hotel_nombre: str = Field(
        ...,
        description="Nombre del hotel"
    )
    
    hotel_id: int = Field(
        ...,
        description="ID del hotel"
    )
    
    tipo_evento: str = Field(
        ...,
        description="Tipo de evento (creado, actualizado, eliminado)"
    )
    
    detalles_cambio: Optional[str] = Field(
        None,
        description="Detalles específicos del cambio"
    )
    
    fecha_evento: datetime = Field(
        ...,
        description="Fecha del evento"
    )


class SystemAlertNotification(BaseModel):
    """
    Notificación de alerta del sistema
    """
    destinatarios: List[EmailStr] = Field(
        ...,
        description="Lista de emails a notificar"
    )
    
    nivel_alerta: str = Field(
        ...,
        description="Nivel de alerta (info, warning, error, critical)"
    )
    
    titulo_alerta: str = Field(
        ...,
        description="Título de la alerta"
    )
    
    mensaje_alerta: str = Field(
        ...,
        description="Mensaje detallado de la alerta"
    )
    
    componente_afectado: Optional[str] = Field(
        None,
        description="Componente del sistema afectado"
    )
    
    acciones_recomendadas: Optional[str] = Field(
        None,
        description="Acciones recomendadas para resolver"
    )
    
    fecha_alerta: datetime = Field(
        ...,
        description="Fecha y hora de la alerta"
    )


class NotificationResponse(BaseModel):
    """
    Respuesta estándar para notificaciones enviadas
    """
    success: bool = Field(
        ...,
        description="Si la notificación se envió exitosamente"
    )
    
    message: str = Field(
        ...,
        description="Mensaje descriptivo del resultado"
    )
    
    email_log_id: Optional[int] = Field(
        None,
        description="ID del log de email generado"
    )
    
    destinatarios_exitosos: List[EmailStr] = Field(
        default_factory=list,
        description="Emails enviados exitosamente"
    )
    
    destinatarios_fallidos: List[EmailStr] = Field(
        default_factory=list,
        description="Emails que fallaron"
    )
    
    errores: List[str] = Field(
        default_factory=list,
        description="Lista de errores encontrados"
    )


class BulkNotificationRequest(BaseModel):
    """
    Schema para envío masivo de notificaciones
    """
    tipo_notificacion: EmailType = Field(
        ...,
        description="Tipo de notificación a enviar"
    )
    
    destinatarios: List[Dict[str, Any]] = Field(
        ...,
        description="Lista de destinatarios con sus variables específicas"
    )
    
    variables_globales: Dict[str, Any] = Field(
        default_factory=dict,
        description="Variables que aplican a todos los destinatarios"
    )
    
    idioma: str = Field(
        "es",
        description="Idioma por defecto"
    )
    
    procesar_asincrono: bool = Field(
        True,
        description="Si procesar de forma asíncrona"
    )


class NotificationTemplate(BaseModel):
    """
    Schema para configuración de plantillas de notificación
    """
    tipo_notificacion: EmailType = Field(
        ...,
        description="Tipo de notificación"
    )
    
    variables_requeridas: List[str] = Field(
        ...,
        description="Variables requeridas para esta notificación"
    )
    
    variables_opcionales: List[str] = Field(
        default_factory=list,
        description="Variables opcionales"
    )
    
    descripcion: str = Field(
        ...,
        description="Descripción del tipo de notificación"
    )
    
    ejemplo_variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="Ejemplo de variables para testing"
    )
