from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .mensaje_schema import MensajeResponse


class ConversacionCreate(BaseModel):
    """Schema base para crear una conversación"""
    tipo_conversacion: str = Field(..., description="Tipo de conversación: 'cliente_admin' o 'empleado_empleado'")
    usuario1_id: int = Field(..., description="ID del usuario que inicia la conversación")
    usuario2_id: int = Field(..., description="ID del usuario destinatario")
    cliente_id: Optional[int] = Field(None, description="ID del cliente (si aplica)")
    empleado1_id: Optional[int] = Field(None, description="ID del primer empleado (si aplica)")
    empleado2_id: Optional[int] = Field(None, description="ID del segundo empleado (si aplica)")


class ConversacionCreateClienteAdmin(BaseModel):
    """Schema para crear conversación cliente-admin"""
    cliente_id: int = Field(..., description="ID del cliente")
    admin_id: int = Field(..., description="ID del administrador")


class ConversacionCreateEmpleadoEmpleado(BaseModel):
    """Schema para crear conversación empleado-empleado"""
    empleado1_id: int = Field(..., description="ID del primer empleado")
    empleado2_id: int = Field(..., description="ID del segundo empleado")


class ConversacionUpdate(BaseModel):
    """Schema para actualizar una conversación"""
    id_estatus: Optional[int] = Field(None, description="Estatus de la conversación (1=Activa, 0=Archivada)")


class ConversacionResponse(BaseModel):
    """Schema de respuesta para una conversación"""
    id_conversacion: int
    tipo_conversacion: str
    usuario1_id: int
    usuario2_id: int
    cliente_id: Optional[int] = None
    empleado1_id: Optional[int] = None
    empleado2_id: Optional[int] = None
    fecha_creacion: datetime
    fecha_ultimo_mensaje: Optional[datetime] = None
    id_estatus: int
    
    class Config:
        from_attributes = True


class ConversacionListResponse(BaseModel):
    """Schema de respuesta para lista de conversaciones con información adicional"""
    id_conversacion: int
    tipo_conversacion: str
    usuario1_id: int
    usuario2_id: int
    cliente_id: Optional[int] = None
    empleado1_id: Optional[int] = None
    empleado2_id: Optional[int] = None
    fecha_creacion: datetime
    fecha_ultimo_mensaje: Optional[datetime] = None
    id_estatus: int
    ultimo_mensaje: Optional[MensajeResponse] = None
    contador_no_leidos: int = 0
    otro_usuario_id: Optional[int] = None
    otro_usuario_nombre: Optional[str] = None
    otro_usuario_foto: Optional[str] = None
    
    class Config:
        from_attributes = True


class UsuarioDisponibleResponse(BaseModel):
    """Schema de respuesta para usuarios disponibles para iniciar conversación"""
    id_usuario: int = Field(..., description="ID del usuario")
    login: str = Field(..., description="Login del usuario")
    nombre: str = Field(..., description="Nombre completo del usuario")
    url_foto_perfil: Optional[str] = Field(None, description="URL completa de la foto de perfil")
    tipo_usuario: str = Field(..., description="Tipo de usuario: 'Administrador' o 'Empleado'")
    empleado_id: Optional[int] = Field(None, description="ID del empleado (solo si es empleado)")
    
    class Config:
        from_attributes = True
