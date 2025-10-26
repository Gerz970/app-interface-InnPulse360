from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.reserva.tipo_cargo_schema import TipoCargoCreate, TipoCargoUpdate, TipoCargoResponse
from services.reserva.tipo_cargo_service import TipoCargoService
from core.database_connection import get_database_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/tipos-cargo", tags=["Tipos de Cargo"])
service = TipoCargoService()
security = HTTPBearer()

@router.get("/", response_model=list[TipoCargoResponse])
def listar_tipos(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    return service.listar_todos(db)


@router.get("/{id_tipo}", response_model=TipoCargoResponse)
def obtener_tipo(id_tipo: int, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    tipo = service.obtener_por_id(db, id_tipo)
    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de cargo no encontrado")
    return tipo


@router.post("/", response_model=TipoCargoResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo(tipo_data: TipoCargoCreate,credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    return service.crear(db, tipo_data)


@router.put("/{id_tipo}", response_model=TipoCargoResponse)
def actualizar_tipo(id_tipo: int, tipo_data: TipoCargoUpdate, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    tipo_actualizado = service.actualizar(db, id_tipo, tipo_data)
    if not tipo_actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de cargo no encontrado")
    return tipo_actualizado


@router.delete("/{id_tipo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tipo(id_tipo: int, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    eliminado = service.eliminar(db, id_tipo)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de cargo no encontrado")
    return None
