from sqlalchemy.orm import Session
from models.mantenimiento.mantenimiento_model import Mantenimiento

class MantenimientoDao:
    def get_all(self, db: Session):
        return db.query(Mantenimiento).all()

    def get_by_id(self, db: Session, id_mantenimiento: int):
        return db.query(Mantenimiento).filter(Mantenimiento.id_mantenimiento == id_mantenimiento).first()

    def create(self, db: Session, mantenimiento: Mantenimiento) -> Mantenimiento:
        db.add(mantenimiento)
        db.commit()
        db.refresh(mantenimiento)
        return mantenimiento

    def update(self, db: Session, id_mantenimiento: int, data: dict) -> Mantenimiento:
        db_mantenimiento = db.query(Mantenimiento).filter(Mantenimiento.id_mantenimiento == id_mantenimiento).first()
        if not db_mantenimiento:
            return None
        for key, value in data.items():
            setattr(db_mantenimiento, key, value)
        db.commit()
        db.refresh(db_mantenimiento)
        return db_mantenimiento

    def delete(self, db: Session, id_mantenimiento: int):
        db_mantenimiento = db.query(Mantenimiento).filter(Mantenimiento.id_mantenimiento == id_mantenimiento).first()
        if db_mantenimiento:
            db.delete(db_mantenimiento)
            db.commit()
        return db_mantenimiento
