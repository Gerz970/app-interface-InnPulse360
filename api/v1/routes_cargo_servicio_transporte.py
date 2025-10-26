from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.database_connection import get_database_session
from services.reserva.cargo_servicio_transporte_service import CargoServicioTransporteService
from schemas.reserva.cargo_servicio_transporte_schema import CargoServicioTransporteCreate, CargoServicioTransporteResponse

router = APIRouter(prefix="/cargo-servicio-transporte", tags=["Cargo-Servicio Transporte"])
service = CargoServicioTransporteService()
security = HTTPBearer()

@router.get("/", response_model=List[CargoServicioTransporteResponse])
def listar_relaciones(db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.listar_relaciones(db)

@router.get("/cargo/{cargo_id}", response_model=List[CargoServicioTransporteResponse])
def obtener_por_cargo(cargo_id: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_por_cargo(db, cargo_id)

@router.get("/servicio/{servicio_id}", response_model=List[CargoServicioTransporteResponse])
def obtener_por_servicio(servicio_id: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_por_servicio(db, servicio_id)

# @router.post("/", response_model=CargoServicioTransporteResponse)
#def crear_relacion(data: CargoServicioTransporteCreate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
#    return service.crear_relacion(db, data)

@router.delete("/", response_model=CargoServicioTransporteResponse)
def eliminar_relacion(cargo_id: int, servicio_id: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    relacion_eliminada = service.eliminar_relacion(db, cargo_id, servicio_id)
    if not relacion_eliminada:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return relacion_eliminada
