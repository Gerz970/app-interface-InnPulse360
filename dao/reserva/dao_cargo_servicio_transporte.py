from sqlalchemy.orm import Session
from models.reserva.cargo_servicio_transporte_model import CargoServicioTransporte
from typing import List

class CargoServicioTransporteDao:
    def get_all(self, db: Session) -> List[CargoServicioTransporte]:
        return db.query(CargoServicioTransporte).all()

    def get_by_cargo(self, db: Session, cargo_id: int) -> List[CargoServicioTransporte]:
        return db.query(CargoServicioTransporte).filter(CargoServicioTransporte.cargo_id == cargo_id).all()

    def get_by_servicio(self, db: Session, servicio_id: int) -> List[CargoServicioTransporte]:
        return db.query(CargoServicioTransporte).filter(CargoServicioTransporte.servicio_transporte_id == servicio_id).all()

    def create(self, db: Session, relacion: CargoServicioTransporte) -> CargoServicioTransporte:
        db.add(relacion)
        db.commit()
        db.refresh(relacion)
        return relacion

    def delete(self, db: Session, cargo_id: int, servicio_id: int) -> CargoServicioTransporte:
        relacion = db.query(CargoServicioTransporte).filter(
            CargoServicioTransporte.cargo_id == cargo_id,
            CargoServicioTransporte.servicio_transporte_id == servicio_id
        ).first()
        if not relacion:
            return None
        db.delete(relacion)
        db.commit()
        return relacion
