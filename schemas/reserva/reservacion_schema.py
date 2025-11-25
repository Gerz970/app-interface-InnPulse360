from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..hotel.habitacion_area_schema import HabitacionAreaResponse
from ..cliente.cliente_response import ClienteResponse

class ReservacionBase(BaseModel):
    cliente_id: int
    habitacion_area_id: int
    fecha_reserva: datetime
    fecha_salida: datetime
    duracion: Optional[int]
    id_estatus: int
    codigo_reservacion: Optional[str] = None

class ReservacionCreate(ReservacionBase):
    monto_reserva: float

class ReservacionUpdate(BaseModel):
    habitacion_area_id: Optional[int]
    fecha_reserva: Optional[datetime]
    fecha_salida: Optional[datetime]
    duracion: Optional[int]
    id_estatus: Optional[int]
    codigo_reservacion: Optional[str] = None

class ReservacionResponse(ReservacionBase):
    id_reservacion: int
    fecha_registro: Optional[datetime]
    habitacion: HabitacionAreaResponse
    cliente: ClienteResponse

    class Config:
        from_attributes = True

class HabitacionReservadaResponse(BaseModel):
    id_habitacion_area: int
    nombre_clave: str

    class Config:
        from_attributes = True

