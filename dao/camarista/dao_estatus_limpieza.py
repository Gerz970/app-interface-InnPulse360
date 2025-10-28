from sqlalchemy.orm import Session
from models.camarista.estatus_limpieza_model import EstatusLimpieza

class EstatusLimpiezaDao:
    # Obtener todos (solo activos)
    def get_all(self, db: Session):
        return db.query(EstatusLimpieza).filter(EstatusLimpieza.id_estatus == 1).all()

    # Obtener por ID
    def get_by_id(self, db: Session, id_estatus_limpieza: int):
        return db.query(EstatusLimpieza).filter(EstatusLimpieza.id_estatus_limpieza == id_estatus_limpieza).first()

    # Crear nuevo registro
    def create(self, db: Session, entidad: EstatusLimpieza):
        db.add(entidad)
        db.commit()
        db.refresh(entidad)
        return entidad

    # Actualizar registro
    def update(self, db: Session, id_estatus_limpieza: int, valores: dict):
        entidad = self.get_by_id(db, id_estatus_limpieza)
        if not entidad:
            return None
        for campo, valor in valores.items():
            setattr(entidad, campo, valor)
        db.commit()
        db.refresh(entidad)
        return entidad

    # Eliminación lógica (cambia id_estatus a 0)
    def delete(self, db: Session, id_estatus_limpieza: int):
        entidad = self.get_by_id(db, id_estatus_limpieza)
        if not entidad:
            return None
        entidad.id_estatus = 0
        db.commit()
        db.refresh(entidad)
        return entidad
