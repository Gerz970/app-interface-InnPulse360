from sqlalchemy.orm import Session
from dao.reserva.dao_cargo_servicio_transporte import CargoServicioTransporteDao
from models.reserva.cargo_servicio_transporte_model import CargoServicioTransporte
from schemas.reserva.cargo_servicio_transporte_schema import CargoServicioTransporteCreate
from typing import List

class CargoServicioTransporteService:
    def __init__(self):
        self.dao = CargoServicioTransporteDao()

    def listar_relaciones(self, db: Session) -> List[CargoServicioTransporte]:
        return self.dao.get_all(db)

    def obtener_por_cargo(self, db: Session, cargo_id: int) -> List[CargoServicioTransporte]:
        return self.dao.get_by_cargo(db, cargo_id)

    def obtener_por_servicio(self, db: Session, servicio_id: int) -> List[CargoServicioTransporte]:
        return self.dao.get_by_servicio(db, servicio_id)

    def crear_relacion(self, db: Session, data: CargoServicioTransporteCreate) -> CargoServicioTransporte:
        relacion = CargoServicioTransporte(**data.dict())
        return self.dao.create(db, relacion)

    def eliminar_relacion(self, db: Session, cargo_id: int, servicio_id: int) -> CargoServicioTransporte:
        return self.dao.delete(db, cargo_id, servicio_id)
