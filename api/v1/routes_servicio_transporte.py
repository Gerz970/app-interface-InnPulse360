# controllers/servicio_transporte_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database_connection import get_database_session
from schemas.reserva.servicios_transporte_schema import (
    ServicioTransporteCreate,
    ServicioTransporteUpdate,
    ServicioTransporteResponse,
)
from services.reserva.servicio_transporte_service import ServicioTransporteService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

router = APIRouter(prefix="/servicios-transporte", tags=["Servicios de Transporte"])
service = ServicioTransporteService()

@router.get("/", response_model=list[ServicioTransporteResponse])
def listar_servicios(db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.listar(db)

@router.get("/{id_servicio}", response_model=ServicioTransporteResponse)
def obtener_servicio(id_servicio: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    servicio = service.obtener(db, id_servicio)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio

@router.post("/", response_model=ServicioTransporteResponse)
def crear_servicio(data: ServicioTransporteCreate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.crear(db, data)

@router.put("/{id_servicio}", response_model=ServicioTransporteResponse)
def actualizar_servicio(id_servicio: int, data: ServicioTransporteUpdate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    servicio = service.actualizar(db, id_servicio, data)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio

@router.delete("/{id_servicio}")
def eliminar_servicio(id_servicio: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    servicio = service.eliminar(db, id_servicio)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"message": "Servicio eliminado correctamente"}
