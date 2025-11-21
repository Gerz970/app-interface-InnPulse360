from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.hotel.habitacion_area_schema import HabitacionAreaCreate, HabitacionAreaUpdate, HabitacionAreaResponse, HabitacionAreaConEstadoResponse
from services.hotel.habitacion_area_service import HabitacionAreaService
from dao.hotel.dao_habitacion_area import HabitacionAreaDAO
from typing import List
from core.database_connection import get_database_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import Settings

settings = Settings()
security = HTTPBearer()
router = APIRouter(prefix="/habitacion-area", tags=["Habitación Área"])

def get_habitacion_area_service(db: Session = Depends(get_database_session)) -> HabitacionAreaService:
    """
    Dependency para obtener la instancia del servicio de HabitacionArea
    """
    return HabitacionAreaService(HabitacionAreaDAO(db))

@router.get("/obtener-por-piso/{piso_id}", response_model=List[HabitacionAreaResponse])
def listar_habitaciones(piso_id:int, db: Session = Depends(get_database_session)):
    service = HabitacionAreaService(HabitacionAreaDAO(db))
    return service.listar(piso_id)

@router.get("/disponibles-por-piso/{piso_id}", response_model=List[HabitacionAreaResponse])
def obtener_habitaciones_disponibles_por_piso(
    piso_id: int,
    service: HabitacionAreaService = Depends(get_habitacion_area_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtiene habitaciones disponibles (sin reserva activa) para un piso específico.
    Una reserva activa tiene estatus = 1.
    """
    try:
        habitaciones = service.obtener_habitaciones_disponibles_por_piso(piso_id)
        return habitaciones
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id_habitacion_area}", response_model=HabitacionAreaResponse)
def obtener_habitacion(id_habitacion_area: int, db: Session = Depends(get_database_session)):
    service = HabitacionAreaService(HabitacionAreaDAO(db))
    habitacion = service.obtener_por_id(id_habitacion_area)
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    return habitacion

@router.post("/", response_model=HabitacionAreaResponse)
def crear_habitacion(data: HabitacionAreaCreate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    service = HabitacionAreaService(HabitacionAreaDAO(db))
    return service.crear(data)

@router.put("/{id_habitacion_area}", response_model=HabitacionAreaResponse)
def actualizar_habitacion(id_habitacion_area: int, data: HabitacionAreaUpdate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    service = HabitacionAreaService(HabitacionAreaDAO(db))
    habitacion = service.actualizar(id_habitacion_area, data)
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    return habitacion

@router.post("/{id_habitacion_area}")
def eliminar_habitacion(id_habitacion_area: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    service = HabitacionAreaService(HabitacionAreaDAO(db))
    habitacion = service.eliminar(id_habitacion_area)
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    return {"message": "Habitación eliminada correctamente"}

@router.get("/con-estado/{piso_id}", response_model=List[HabitacionAreaConEstadoResponse])
def obtener_habitaciones_con_estado_por_piso(
    piso_id: int,
    service: HabitacionAreaService = Depends(get_habitacion_area_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtiene habitaciones de un piso con información de estado:
    - Reservaciones activas
    - Limpiezas pendientes (estatus = 1)
    - Limpiezas en proceso (estatus = 2)
    - Si puede seleccionarse para nueva limpieza
    """
    try:
        habitaciones_con_estado = service.obtener_habitaciones_con_estado_por_piso(piso_id)
        
        # Convertir a formato de respuesta
        resultado = []
        for item in habitaciones_con_estado:
            hab = item['habitacion']
            resultado.append(HabitacionAreaConEstadoResponse(
                id_habitacion_area=hab.id_habitacion_area,
                piso_id=hab.piso_id,
                tipo_habitacion_id=hab.tipo_habitacion_id,
                nombre_clave=hab.nombre_clave,
                descripcion=hab.descripcion,
                estatus_id=hab.estatus_id,
                tiene_reservacion_activa=item['tiene_reservacion_activa'],
                tiene_limpieza_pendiente=item['tiene_limpieza_pendiente'],
                tiene_limpieza_en_proceso=item['tiene_limpieza_en_proceso'],
                puede_seleccionarse=item['puede_seleccionarse']
            ))
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
