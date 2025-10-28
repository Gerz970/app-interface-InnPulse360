from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LimpiezaBase(BaseModel):
    habitacion_area_id: int
    descripcion: Optional[str] = None
    fecha_programada: datetime
    fecha_termino: Optional[datetime] = None
    tipo_limpieza_id: int
    estatus_limpieza_id: int
    comentarios_observaciones: Optional[str] = None
    empleado_id: int

class LimpiezaCreate(LimpiezaBase):
    pass

class LimpiezaUpdate(BaseModel):
    descripcion: Optional[str] = None
    fecha_programada: Optional[datetime] = None
    fecha_termino: Optional[datetime] = None
    tipo_limpieza_id: Optional[int] = None
    estatus_limpieza_id: Optional[int] = None
    comentarios_observaciones: Optional[str] = None
    empleado_id: Optional[int] = None

class LimpiezaResponse(LimpiezaBase):
    id_limpieza: int

    class Config:
        from_attributes = True
