from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from ..empleado.empleado_response import EmpleadoResponse

class MantenimientoBase(BaseModel):
    descripcion: str
    fecha: datetime
    fecha_termino: Optional[date] = None
    empleado_id: int
    estatus: int

class MantenimientoCreate(MantenimientoBase):
    pass

class MantenimientoUpdate(BaseModel):
    descripcion: Optional[str] = None
    fecha: Optional[datetime] = None
    fecha_termino: Optional[date] = None
    empleado_id: Optional[int] = None

class MantenimientoResponse(MantenimientoBase):
    id_mantenimiento: int
    empleado : EmpleadoResponse
    class Config:
        from_attributes = True

class MantenimientoResponseShort(MantenimientoBase):
    id_mantenimiento: int
    class Config:
        from_attributes = True
