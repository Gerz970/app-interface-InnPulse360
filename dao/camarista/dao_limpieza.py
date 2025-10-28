from sqlalchemy.orm import Session
from models.camarista.limpieza_model import Limpieza

class LimpiezaDao:

    def get_all(self, db: Session):
        """Obtiene todas las limpiezas activas (estatus distinto de 'eliminada')"""
        return db.query(Limpieza).filter(Limpieza.estatus_limpieza_id != 4).all()

    def get_by_id(self, db: Session, id_limpieza: int):
        """Obtiene una limpieza por su ID si no está eliminada"""
        return db.query(Limpieza).filter(Limpieza.id_limpieza == id_limpieza, Limpieza.estatus_limpieza_id != 4).first()

    def create(self, db: Session, limpieza: Limpieza):
        """Crea una nueva limpieza"""
        db.add(limpieza)
        db.commit()
        db.refresh(limpieza)
        return limpieza

    def update(self, db: Session, id_limpieza: int, data: dict):
        """Actualiza los datos de una limpieza"""
        limpieza = db.query(Limpieza).filter(Limpieza.id_limpieza == id_limpieza, Limpieza.estatus_limpieza_id != 4).first()
        if not limpieza:
            return None
        for key, value in data.items():
            setattr(limpieza, key, value)
        db.commit()
        db.refresh(limpieza)
        return limpieza

    def delete(self, db: Session, id_limpieza: int):
        """Eliminación lógica: cambia estatus_limpieza_id a 4 (eliminada)"""
        limpieza = db.query(Limpieza).filter(Limpieza.id_limpieza == id_limpieza).first()
        if not limpieza:
            return None
        limpieza.estatus_limpieza_id = 4  # Marcamos como eliminada
        db.commit()
        return limpieza
