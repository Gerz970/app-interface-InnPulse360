from sqlalchemy.orm import Session
from models.catalogos.periodicidad_model import Periodicidad

class PeriodicidadDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return (
            self.db.query(Periodicidad)
            .filter(Periodicidad.id_estatus == True)
            .order_by(Periodicidad.id_periodicidad)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, id_periodicidad: int):
        return self.db.query(Periodicidad).filter(Periodicidad.id_periodicidad == id_periodicidad).first()

    def create(self, periodicidad: Periodicidad):
        self.db.add(periodicidad)
        self.db.commit()
        self.db.refresh(periodicidad)
        return periodicidad

    def update(self, db_obj: Periodicidad, data: dict):
        for key, value in data.items():
            setattr(db_obj, key, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete_logico(self, db_obj: Periodicidad):
        db_obj.id_estatus = False
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
