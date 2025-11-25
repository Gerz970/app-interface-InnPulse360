# dao/servicio_transporte_dao.py
from sqlalchemy.orm import Session, joinedload
from models.reserva.servicios_transporte_model import ServicioTransporte
from schemas.reserva.servicios_transporte_schema import ServicioTransporteCreate, ServicioTransporteUpdate

class ServicioTransporteDAO:

    def get_all(self, db: Session):
        return db.query(ServicioTransporte).options(
            joinedload(ServicioTransporte.empleado)
        ).all()

    def get_by_id(self, db: Session, id_servicio: int):
        return db.query(ServicioTransporte).options(
            joinedload(ServicioTransporte.empleado)
        ).filter(ServicioTransporte.id_servicio_transporte == id_servicio).first()

    def create(self, db: Session, data: ServicioTransporteCreate):
        nuevo_servicio = ServicioTransporte(**data.dict())
        db.add(nuevo_servicio)
        db.commit()
        db.refresh(nuevo_servicio)
        # Recargar con la relación empleado para la respuesta
        return self.get_by_id(db, nuevo_servicio.id_servicio_transporte)

    def update(self, db: Session, id_servicio: int, data: ServicioTransporteUpdate):
        servicio = self.get_by_id(db, id_servicio)
        if not servicio:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(servicio, key, value)
        db.commit()
        db.refresh(servicio)
        # Recargar con la relación empleado para la respuesta
        return self.get_by_id(db, id_servicio)

    def delete(self, db: Session, id_servicio: int):
        servicio = self.get_by_id(db, id_servicio)
        if not servicio:
            return None
        db.delete(servicio)
        db.commit()
        return servicio
