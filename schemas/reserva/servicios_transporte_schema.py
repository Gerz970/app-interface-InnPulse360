# schemas/servicio_transporte_schema.py
from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from ..empleado.empleado_response import EmpleadoResponse
from decimal import Decimal

class ServicioTransporteBase(BaseModel):
    destino: str
    fecha_servicio: date
    hora_servicio: time
    id_estatus: Optional[int] = 1
    empleado_id: Optional[int] = None
    observaciones_cliente: Optional[str] = None
    observaciones_empleado: Optional[str] = None
    calificacion_viaje: Optional[int] = None
    costo_viaje : Decimal
    
    # Campos de geolocalización
    latitud_origen: Optional[Decimal] = None
    longitud_origen: Optional[Decimal] = None
    latitud_destino: Optional[Decimal] = None
    longitud_destino: Optional[Decimal] = None
    direccion_origen: Optional[str] = None
    direccion_destino: Optional[str] = None
    distancia_km: Optional[Decimal] = None


class ServicioTransporteCreate(ServicioTransporteBase):
    empleado_id: Optional[int] = None  # Opcional en create también


class ServicioTransporteUpdate(BaseModel):
    destino: Optional[str] = None
    fecha_servicio: Optional[date] = None
    hora_servicio: Optional[time] = None
    id_estatus: Optional[int] = None
    empleado_id: Optional[int] = None
    observaciones_cliente: Optional[str] = None
    observaciones_empleado: Optional[str] = None
    calificacion_viaje: Optional[int] = None
    costo_viaje: Optional[Decimal] = None
    
    # Campos de geolocalización
    latitud_origen: Optional[Decimal] = None
    longitud_origen: Optional[Decimal] = None
    latitud_destino: Optional[Decimal] = None
    longitud_destino: Optional[Decimal] = None
    direccion_origen: Optional[str] = None
    direccion_destino: Optional[str] = None
    distancia_km: Optional[Decimal] = None



class ServicioTransporteResponse(ServicioTransporteBase):
    id_servicio_transporte: int
    empleado: Optional[EmpleadoResponse] = None

    class Config:
        from_attributes = True


class ServicioTransporteOut(BaseModel):
    id_servicio_transporte: int
    destino: str
    fecha_servicio: date
    hora_servicio: time
    id_estatus: int
    observaciones_cliente: str
    observaciones_empleado: str
    calificacion_viaje: int
    costo_viaje: float
    latitud_origen: float
    longitud_origen: float
    latitud_destino: float
    longitud_destino: float
    direccion_origen: str
    direccion_destino: str
    distancia_km: float
    id_empleado: int
    clave_empleado: str
    nombre: str
    apellido_paterno: str
    apellido_materno: str