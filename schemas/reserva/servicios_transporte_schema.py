# schemas/servicio_transporte_schema.py
from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from ..empleado.empleado_response import EmpleadoResponse

class ServicioTransporteBase(BaseModel):
    destino: str
    fecha_servicio: date
    hora_servicio: time
    id_estatus: Optional[int] = 1
    empleado_id: int
    observaciones_cliente: Optional[str] = None
    observaciones_empleado: Optional[str] = None
    calificacion_viaje: Optional[int] = None


class ServicioTransporteCreate(ServicioTransporteBase):
    pass


class ServicioTransporteUpdate(BaseModel):
    destino: Optional[str] = None
    fecha_servicio: Optional[date] = None
    hora_servicio: Optional[time] = None
    id_estatus: Optional[int] = None
    empleado_id: Optional[int] = None
    observaciones_cliente: Optional[str] = None
    observaciones_empleado: Optional[str] = None
    calificacion_viaje: Optional[int] = None


class ServicioTransporteResponse(ServicioTransporteBase):
    id_servicio_transporte: int
    empleado: EmpleadoResponse

    class Config:
        from_attributes = True
