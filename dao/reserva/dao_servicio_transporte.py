# dao/servicio_transporte_dao.py
from sqlalchemy.orm import Session
from models.reserva.servicios_transporte_model import ServicioTransporte
from schemas.reserva.servicios_transporte_schema import ServicioTransporteCreate, ServicioTransporteUpdate

class ServicioTransporteDAO:

    def get_all(self, db: Session):
        return db.query(ServicioTransporte).all()

    def get_by_id(self, db: Session, id_servicio: int):
        return db.query(ServicioTransporte).filter(ServicioTransporte.id_servicio_transporte == id_servicio).first()

    def create(self, db: Session, data: ServicioTransporteCreate):
        nuevo_servicio = ServicioTransporte(**data.dict())
        db.add(nuevo_servicio)
        db.commit()
        db.refresh(nuevo_servicio)
        return nuevo_servicio

    def update(self, db: Session, id_servicio: int, data: ServicioTransporteUpdate):
        servicio = self.get_by_id(db, id_servicio)
        if not servicio:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(servicio, key, value)
        db.commit()
        db.refresh(servicio)
        return servicio

    def delete(self, db: Session, id_servicio: int):
        servicio = self.get_by_id(db, id_servicio)
        if not servicio:
            return None
        db.delete(servicio)
        db.commit()
        return servicio
