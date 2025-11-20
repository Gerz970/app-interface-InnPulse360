from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from core.database_connection import get_database_session
from services.reserva.reservacion_service import ReservacionService
from schemas.reserva.reservacion_schema import ReservacionCreate, ReservacionUpdate, ReservacionResponse, HabitacionReservadaResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from datetime import datetime, date
from schemas.hotel.habitacion_area_schema import HabitacionAreaResponse

router = APIRouter(prefix="/reservaciones", tags=["Reservaciones"])
service = ReservacionService()
security = HTTPBearer()

@router.get("/", response_model=list[ReservacionResponse])
def listar_reservaciones(db: Session = Depends(get_database_session),credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.listar_reservaciones(db)

@router.get("/{id_reservacion}", response_model=ReservacionResponse)
def obtener_reservacion(id_reservacion: int, db: Session = Depends(get_database_session),credentials: HTTPAuthorizationCredentials = Depends(security)):
    reservacion = service.obtener_reservacion(db, id_reservacion)
    if not reservacion:
        raise HTTPException(status_code=404, detail="Reservación no encontrada")
    return reservacion

@router.get("/cliente/{id_cliente}", response_model=List[ReservacionResponse])
def obtener_por_cliente(id_cliente: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_por_cliente(db, id_cliente)

@router.get("/cliente/{id_cliente}/habitaciones", response_model=List[HabitacionReservadaResponse])
def obtener_habitaciones_reservadas_por_cliente(
    id_cliente: int,
    db: Session = Depends(get_database_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Obtiene las habitaciones que alguna vez fueron reservadas por un cliente"""
    return service.obtener_habitaciones_reservadas_por_cliente(db, id_cliente)

# Obtener por habitacion
@router.get("/habitacion/{habitacion_area_id}", response_model=List[ReservacionResponse])
def obtener_por_habitacion(habitacion_area_id: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_por_habitacion(db, habitacion_area_id)

# Obtener por fechas
@router.get("/fechas/", response_model=List[ReservacionResponse])
def obtener_por_fechas(
    fecha_inicio: datetime = Query(..., description="Fecha inicial"),
    fecha_fin: datetime = Query(..., description="Fecha final"),
    db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_por_fechas(db, fecha_inicio, fecha_fin)


@router.post("/", response_model=ReservacionResponse)
def crear_reservacion(reservacion: ReservacionCreate, db: Session = Depends(get_database_session),credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.crear_reservacion(db, reservacion)

@router.put("/{id_reservacion}", response_model=ReservacionResponse)
def actualizar_reservacion(id_reservacion: int, reservacion: ReservacionUpdate, db: Session = Depends(get_database_session),credentials: HTTPAuthorizationCredentials = Depends(security)):
    reservacion_actualizada = service.actualizar_reservacion(db, id_reservacion, reservacion)
    if not reservacion_actualizada:
        raise HTTPException(status_code=404, detail="Reservación no encontrada")
    return reservacion_actualizada

@router.delete("/{id_reservacion}", response_model=ReservacionResponse)
def eliminar_reservacion(id_reservacion: int, db: Session = Depends(get_database_session),credentials: HTTPAuthorizationCredentials = Depends(security)):
    reservacion_eliminada = service.eliminar_reservacion(db, id_reservacion)
    if not reservacion_eliminada:
        raise HTTPException(status_code=404, detail="Reservación no encontrada")
    return reservacion_eliminada

@router.get("/{fecha_inicio_reservacion}/{fecha_salida}", response_model=List[HabitacionAreaResponse])
def obtener_habitaciones_disponibles(fecha_inicio_reservacion: date =  Path(..., example="2025-01-10"), fecha_salida: date =  Path(..., example="2025-01-15"), credentials: HTTPAuthorizationCredentials = Depends(security)):
    habitaciones = service.obtener_habitaciones_disponibles(fecha_inicio_reservacion, fecha_salida)
    return habitaciones
