from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.reserva.cargos_schema import CargoCreate, CargoResponse
from services.reserva.cargo_service import CargoService
from core.database_connection import get_database_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/cargos", tags=["Cargos"])
service = CargoService()
security = HTTPBearer()


@router.get("/", response_model=list[CargoResponse])
def listar_cargos(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    return service.listar_todos(db)


@router.get("/{id_cargo}", response_model=CargoResponse)
def obtener_cargo(id_cargo: int, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    cargo = service.obtener_por_id(db, id_cargo)
    if not cargo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo no encontrado"
        )
    return cargo

@router.get("/get-by-reserva/{id_reserva}", response_model=list[CargoResponse])
def listar_cargos(id_reserva: int, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    return service.obtener_por_id_reserva(db, id_reserva)

@router.post("/", response_model=CargoResponse, status_code=status.HTTP_201_CREATED)
def crear_cargo(cargo_data: CargoCreate, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    return service.crear(db, cargo_data)

@router.post("/create-cargo-servicio-transporte", response_model=CargoResponse, status_code=status.HTTP_201_CREATED)
def crear_cargo_con_servicio(cargo_data: CargoCreate, servicio_transporte_id:int, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    try:
        nuevo_cargo = service.crearCargoConServicio(db, cargo_data, servicio_transporte_id)
        return nuevo_cargo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id_cargo}", response_model=CargoResponse)
def actualizar_cargo(id_cargo: int, cargo_data: CargoCreate, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    cargo_actualizado = service.actualizar(db, id_cargo, cargo_data)
    if not cargo_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo no encontrado"
        )
    return cargo_actualizado


@router.delete("/{id_cargo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cargo(id_cargo: int, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    eliminado = service.eliminar(db, id_cargo)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo no encontrado"
        )
    return None

@router.get("/cargos/totales/{reservacion_id}")
def get_totales(reservacion_id: int, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_database_session)):
    return service.obtener_totales_por_reservacion(db, reservacion_id)

