from pydantic import BaseModel, field_serializer
from datetime import datetime
from typing import Optional
from .tipos_limpieza_schema import TipoLimpiezaResponse
from ..hotel.habitacion_area_schema import HabitacionAreaBase
from ..empleado.empleado_base import EmpleadoBase

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
    tipo_limpieza: TipoLimpiezaResponse
    habitacion_area: HabitacionAreaBase
    empleado_id: Optional[int] = None  # Sobrescribe el campo de LimpiezaBase para permitir None
    empleado: Optional[EmpleadoBase] = None

    @field_serializer('empleado')
    def serialize_empleado(self, empleado: Optional[EmpleadoBase], _info):
        """Serializa el campo empleado: si es None, retorna un objeto vacío {}"""
        if empleado is None:
            return {}
        return empleado

    class Config:
        from_attributes = True
