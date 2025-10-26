from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

# Schema para el Servicio de Transporte
class ServicioTransporteBase(BaseModel):
    destino: str
    fecha_servicio: date
    hora_servicio: time
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
    empleado_id: Optional[int] = None
    observaciones_cliente: Optional[str] = None
    observaciones_empleado: Optional[str] = None
    calificacion_viaje: Optional[int] = None
    id_estatus: Optional[int] = None

class ServicioTransporteResponse(ServicioTransporteBase):
    id_servicio_transporte: int
    id_estatus: int

    class Config:
        from_attributes = True

# Schema para la relación Cargo - ServicioTransporte
class CargoServicioTransporteBase(BaseModel):
    cargo_id: int
    servicio_transporte_id: int

class CargoServicioTransporteCreate(CargoServicioTransporteBase):
    pass

class CargoServicioTransporteResponse(CargoServicioTransporteBase):
    class Config:
        from_attributes = True
