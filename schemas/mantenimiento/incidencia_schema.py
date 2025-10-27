from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..hotel.habitacion_area_schema import HabitacionAreaResponse

class IncidenciaBase(BaseModel):
    habitacion_area_id: int
    incidencia: str
    descripcion: Optional[str] = None
    fecha_incidencia: datetime
    id_estatus: int

class IncidenciaCreate(IncidenciaBase):
    pass

class IncidenciaUpdate(BaseModel):
    habitacion_area_id: Optional[int] = None
    incidencia: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_incidencia: Optional[datetime] = None
    id_estatus: Optional[int] = None

class IncidenciaResponse(IncidenciaBase):
    id_incidencia: int
    habitacion_area: HabitacionAreaResponse

    class Config:
        from_attributes = True
