from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from core.database_connection import get_database_session
from services.reserva.reservacion_service import ReservacionService
from schemas.reserva.reservacion_schema import ReservacionCreate, ReservacionUpdate, ReservacionResponse, HabitacionReservadaResponse
from schemas.reserva.tipo_habitacion_disponible_schema import TipoHabitacionDisponibleResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from datetime import datetime, date
from schemas.hotel.habitacion_area_schema import HabitacionAreaResponse

router = APIRouter(prefix="/reservaciones", tags=["Reservaciones"])
service = ReservacionService()
security = HTTPBearer()

@router.get("/", response_model=list[ReservacionResponse])
def listar_reservaciones(db: Session = Depends(get_database_session),credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.listar_reservaciones(db)

@router.get("/todas/", response_model=List[ReservacionResponse])
def listar_todas_reservaciones(
    incluir_todos_estatus: bool = Query(False, description="Incluir todas las reservaciones sin importar su estatus"),
    id_hotel: Optional[int] = Query(None, description="ID del hotel para filtrar. Si no se proporciona, trae reservaciones de todos los hoteles"),
    db: Session = Depends(get_database_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtiene todas las reservaciones con filtros opcionales.
    
    - **incluir_todos_estatus**: Si es True, incluye todas las reservaciones sin importar su estatus
    - **id_hotel**: ID del hotel para filtrar. Si no se proporciona, trae reservaciones de todos los hoteles
    
    Ejemplos:
    - Todas las reservaciones de todos los estatus y hoteles: `/reservaciones/todas/?incluir_todos_estatus=true`
    - Todas las reservaciones activas de un hotel específico: `/reservaciones/todas/?id_hotel=1`
    - Todas las reservaciones de un hotel sin importar estatus: `/reservaciones/todas/?id_hotel=1&incluir_todos_estatus=true`
    """
    return service.listar_reservaciones_filtradas(db, incluir_todos_estatus, id_hotel)

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

@router.get("/estatus/{estatus}", response_model=List[ReservacionResponse])
def obtener_por_estatus(estatus: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_por_estatus(db, estatus)

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

@router.post("/checkout/{id_reservacion}/{monto_pagado}")
def checkout(id_reservacion: int, monto_pagado: float, db: Session = Depends(get_database_session),credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.checkout(db, id_reservacion, monto_pagado)

@router.post("/check-in/{id_reservacion}/{monto_pagado}")
def checkin(id_reservacion: int, monto_pagado: float, db: Session = Depends(get_database_session),credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.checkin(db, id_reservacion, monto_pagado)

@router.get("/tipos-disponibles/{fecha_inicio_reservacion}/{fecha_salida}", 
            response_model=List[TipoHabitacionDisponibleResponse])
def obtener_tipos_habitacion_disponibles(
    fecha_inicio_reservacion: date = Path(..., example="2025-01-10"), 
    fecha_salida: date = Path(..., example="2025-01-15"),
    id_hotel: Optional[int] = Query(None, description="ID del hotel para filtrar"),
    db: Session = Depends(get_database_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtiene tipos de habitación disponibles agrupados por tipo con cantidad disponible
    
    - **fecha_inicio_reservacion**: Fecha de inicio de la reservación
    - **fecha_salida**: Fecha de salida
    - **id_hotel**: ID del hotel para filtrar (opcional)
    """
    tipos = service.obtener_tipos_habitacion_disponibles(
        db,
        fecha_inicio_reservacion, 
        fecha_salida, 
        id_hotel
    )
    return tipos

@router.get("/{fecha_inicio_reservacion}/{fecha_salida}", response_model=List[HabitacionAreaResponse])
def obtener_habitaciones_disponibles(
        limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
        fecha_inicio_reservacion: date =  Path(..., example="2025-01-10"), fecha_salida: date =  Path(..., example="2025-01-15"), credentials: HTTPAuthorizationCredentials = Depends(security)):
    habitaciones = service.obtener_habitaciones_disponibles(fecha_inicio_reservacion, fecha_salida, limit)
    return habitaciones
