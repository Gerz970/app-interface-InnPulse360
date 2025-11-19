from sqlalchemy.orm import Session, joinedload
from models.mantenimiento.incidencia_model import Incidencia

class IncidenciaDao:
    def obtener_todos(self, db: Session):
        return db.query(Incidencia).options(joinedload(Incidencia.habitacion_area)).all()

    def obtener_por_id(self, db: Session, id_incidencia: int):
        return db.query(Incidencia).options(joinedload(Incidencia.habitacion_area)).filter(Incidencia.id_incidencia == id_incidencia).first()

    def crear(self, db: Session, data: Incidencia):
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    def actualizar(self, db: Session, id_incidencia: int, data: dict):
        incidencia = db.query(Incidencia).filter(Incidencia.id_incidencia == id_incidencia).first()
        if incidencia:
            for key, value in data.items():
                setattr(incidencia, key, value)
            db.commit()
            db.refresh(incidencia)
        return incidencia

    def eliminar(self, db: Session, id_incidencia: int):
        incidencia = db.query(Incidencia).filter(Incidencia.id_incidencia == id_incidencia).first()
        if incidencia:
            db.delete(incidencia)
            db.commit()
        return incidencia
