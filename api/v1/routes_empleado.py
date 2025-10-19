from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.database_connection import get_database_session
from schemas.empleado import EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse
from services.empleado.empleado_service import EmpleadoService
from schemas.empleado.domicilio_base import DomicilioUpdate

# Seguridad con token tipo Bearer
security = HTTPBearer()

# Router principal para empleados
api_router = APIRouter(prefix="/empleado", tags=["Empleado"])


def get_empleado_service(db: Session = Depends(get_database_session)) -> EmpleadoService:
    """
    Dependency para obtener la instancia del servicio de Empleado
    """
    try:
        return EmpleadoService(db)
    finally:
        db.close()


@api_router.post("/", response_model=EmpleadoResponse, status_code=status.HTTP_201_CREATED)
def crear_empleado(
    empleado_data: EmpleadoCreate,
    service: EmpleadoService = Depends(get_empleado_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Crea un nuevo empleado en la base de datos.
    Requiere autenticación Bearer.
    """
    try:
        empleado = service.crear_empleado(empleado_data)
        return empleado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.get("/empleado-hotel/{hotel_id}", response_model=List[EmpleadoResponse])
def obtener_todos_los_empleados_por_hotel(
    hotel_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    service: EmpleadoService = Depends(get_empleado_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtiene todos los empleados registrados por hotel.
    Requiere autenticación Bearer.
    """
    try:
        empleados= service.obtener_todos_los_empleados_por_hotel(hotel_id, skip, limit)
        return empleados
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.get("/{empleado_id}", response_model=EmpleadoResponse)
def obtener_empleado_por_id(
    empleado_id: int,
    service: EmpleadoService = Depends(get_empleado_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtiene un empleado por su ID.
    Requiere autenticación Bearer.
    """
    empleado = service.obtener_empleado_por_id(empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@api_router.put("/{empleado_id}", response_model=EmpleadoResponse)
def actualizar_empleado(
    empleado_id: int,
    empleado_update: EmpleadoUpdate,
    service: EmpleadoService = Depends(get_empleado_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Actualiza los datos de un empleado existente.
    Requiere autenticación Bearer.
    """
    empleado = service.actualizar_empleado(empleado_id, empleado_update)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado para actualizar")
    return empleado


@api_router.delete("/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_empleado(
    empleado_id: int,
    service: EmpleadoService = Depends(get_empleado_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Elimina físicamente un empleado de la base de datos.
    Requiere autenticación Bearer.
    """
    eliminado = service.eliminar_empleado(empleado_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado para eliminar")
    return None

@api_router.put("/editar-direccion/{direccion_id}", response_model=DomicilioUpdate)
def actualizar_empleado(
    direccion_id: int,
    direccion_update: DomicilioUpdate,
    service: EmpleadoService = Depends(get_empleado_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Actualiza los datos de un empleado existente.
    Requiere autenticación Bearer.
    """
    empleado = service.actualizar_direccion(direccion_id, direccion_update)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado para actualizar")
    return empleado
