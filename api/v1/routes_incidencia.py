from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.mantenimiento.incidencia_service import IncidenciaService
from schemas.mantenimiento.incidencia_schema import IncidenciaCreate, IncidenciaUpdate, IncidenciaResponse
from typing import List
from core.database_connection import get_database_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

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
