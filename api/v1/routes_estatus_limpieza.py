from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database_connection import get_database_session
from schemas.camarista.estatus_limpieza_schema import (
    EstatusLimpiezaCreate,
    EstatusLimpiezaUpdate,
    EstatusLimpiezaResponse
)
from services.camarista.estatus_limpieza_service import EstatusLimpiezaService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(
    prefix="/estatus-limpieza",
    tags=["Estatus de limpieza"]
)
security = HTTPBearer()
service = EstatusLimpiezaService()

@router.get("/", response_model=list[EstatusLimpiezaResponse])
def obtener_todos(db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.obtener_todos(db)


@router.get("/{id_estatus_limpieza}", response_model=EstatusLimpiezaResponse)
def obtener_por_id(id_estatus_limpieza: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    estatus = service.obtener_por_id(db, id_estatus_limpieza)
    if not estatus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estatus no encontrado")
    return estatus


@router.post("/", response_model=EstatusLimpiezaResponse, status_code=status.HTTP_201_CREATED)
def crear_este(data: EstatusLimpiezaCreate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    return service.crear(db, data)


@router.put("/{id_estatus_limpieza}", response_model=EstatusLimpiezaResponse)
def actualizar_este(id_estatus_limpieza: int, data: EstatusLimpiezaUpdate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    actualizado = service.actualizar(db, id_estatus_limpieza, data)
    if not actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estatus no encontrado")
    return actualizado


@router.delete("/{id_estatus_limpieza}", status_code=status.HTTP_200_OK)
def eliminar_este(id_estatus_limpieza: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    eliminado = service.eliminar(db, id_estatus_limpieza)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estatus no encontrado")
    return {"mensaje": "Estatus marcado como inactivo correctamente"}
