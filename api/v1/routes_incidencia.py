from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.mantenimiento.incidencia_service import IncidenciaService
from schemas.mantenimiento.incidencia_schema import IncidenciaCreate, IncidenciaUpdate, IncidenciaResponse
from typing import List
from core.database_connection import get_database_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime

router = APIRouter(prefix="/incidencias", tags=["Incidencias"])
service = IncidenciaService()
security = HTTPBearer()

@router.get("/", response_model=List[IncidenciaResponse])
def listar_incidencias(db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_todos(db)

@router.get("/{id_incidencia}", response_model=IncidenciaResponse)
def obtener_incidencia(id_incidencia: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    incidencia = service.obtener_por_id(db, id_incidencia)
    if not incidencia:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    return incidencia

@router.post("/", response_model=IncidenciaResponse)
def crear_incidencia(data: IncidenciaCreate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.crear(db, data)

@router.put("/{id_incidencia}", response_model=IncidenciaResponse)
def actualizar_incidencia(id_incidencia: int, data: IncidenciaUpdate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    incidencia = service.actualizar(db, id_incidencia, data)
    if not incidencia:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    return incidencia

@router.delete("/{id_incidencia}", response_model=IncidenciaResponse)
def eliminar_incidencia(id_incidencia: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    incidencia = service.eliminar(db, id_incidencia)
    if not incidencia:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    return incidencia

@router.get("/estatus/{id_estatus}", response_model=List[IncidenciaResponse])
def listar_por_estatus(id_estatus: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Obtiene todas las incidencias con un estatus específico.
    """
    incidencias = service.obtener_por_estatus(db, id_estatus)
    if not incidencias:
        raise HTTPException(status_code=404, detail="No se encontraron incidencias con ese estatus")
    return incidencias

@router.get("/habitacion/{habitacion_area_id}", response_model=List[IncidenciaResponse])
def listar_por_habitacion(habitacion_area_id: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Obtiene las incidencias por habitación o área, ordenadas por estatus.
    """
    incidencias = service.obtener_por_habitacion(db, habitacion_area_id)
    if not incidencias:
        raise HTTPException(status_code=404, detail="No se encontraron incidencias para esa habitación o área")
    return incidencias

@router.get("/fecha/{fecha_inicio}", response_model=List[IncidenciaResponse])
def listar_por_fecha(fecha_inicio: datetime, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Obtiene las incidencias con fecha mayor o igual a la indicada, ordenadas por estatus.
    """
    incidencias = service.obtener_por_fecha(db, fecha_inicio)
    if not incidencias:
        raise HTTPException(status_code=404, detail="No se encontraron incidencias a partir de esa fecha")
    return incidencias