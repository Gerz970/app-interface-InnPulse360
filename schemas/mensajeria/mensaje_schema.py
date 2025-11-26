from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .mensaje_adjunto_schema import MensajeAdjuntoResponse


class MensajeCreate(BaseModel):
    """Schema para crear un mensaje"""
    conversacion_id: int = Field(..., description="ID de la conversación")
    contenido: str = Field(..., min_length=1, description="Contenido del mensaje")


class MensajeResponse(BaseModel):
    """Schema de respuesta para un mensaje"""
    id_mensaje: int
    conversacion_id: int
    remitente_id: int
    contenido: str
    fecha_envio: datetime
    fecha_leido: Optional[datetime] = None
    id_estatus: int
    adjuntos: Optional[List['MensajeAdjuntoResponse']] = []
    
    class Config:
        from_attributes = True


class MensajeLeidoUpdate(BaseModel):
    """Schema para marcar mensaje como leído"""
    mensaje_id: int = Field(..., description="ID del mensaje a marcar como leído")

