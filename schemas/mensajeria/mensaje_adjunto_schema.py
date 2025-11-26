from pydantic import BaseModel, Field
from datetime import datetime


class MensajeAdjuntoResponse(BaseModel):
    """Schema de respuesta para un adjunto de mensaje"""
    id_adjunto: int
    mensaje_id: int
    nombre_archivo: str
    tipo_archivo: str
    ruta_archivo: str
    tamanio_bytes: int
    fecha_subida: datetime
    
    class Config:
        from_attributes = True

