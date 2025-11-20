from sqlalchemy.orm import Session, joinedload
from models.camarista.limpieza_model import Limpieza
from sqlalchemy import asc
from datetime import date, datetime, time

class LimpiezaDao:

    def get_all(self, db: Session):
        """Obtiene todas las limpiezas activas (estatus distinto de 'eliminada')"""
        return db.query(Limpieza).filter(Limpieza.estatus_limpieza_id != 4).all()

    def get_by_id(self, db: Session, id_limpieza: int):
        """Obtiene una limpieza por su ID si no está eliminada"""
        return db.query(Limpieza).options(
            joinedload(Limpieza.tipo_limpieza),
            joinedload(Limpieza.habitacion_area),
            joinedload(Limpieza.empleado)
        ).filter(Limpieza.id_limpieza == id_limpieza, Limpieza.estatus_limpieza_id != 4).first()

    def create(self, db: Session, limpieza: Limpieza):
        """Crea una nueva limpieza"""
        db.add(limpieza)
        db.commit()
        db.refresh(limpieza)
        return limpieza

    def update(self, db: Session, id_limpieza: int, data: dict):
        """Actualiza los datos de una limpieza"""
        limpieza = db.query(Limpieza).options(
            joinedload(Limpieza.tipo_limpieza),
            joinedload(Limpieza.habitacion_area),
            joinedload(Limpieza.empleado)
        ).filter(Limpieza.id_limpieza == id_limpieza, Limpieza.estatus_limpieza_id != 4).first()
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

    def get_by_empleado(self, db: Session, empleado_id: int):
        """Obtiene limpiezas de un empleado ordenadas por fecha_programada y estatus_limpieza_id"""
        return db.query(Limpieza).filter(
            Limpieza.empleado_id == empleado_id,
            Limpieza.estatus_limpieza_id != 4
        ).order_by(
            asc(Limpieza.fecha_programada),
            asc(Limpieza.estatus_limpieza_id)
        ).all()

    def get_by_habitacion_area(self, db: Session, habitacion_area_id: int):
        """Obtiene limpiezas de una habitación/área ordenadas por fecha_programada"""
        return db.query(Limpieza).filter(
            Limpieza.habitacion_area_id == habitacion_area_id,
            Limpieza.estatus_limpieza_id != 4
        ).order_by(
            asc(Limpieza.fecha_programada)
        ).all()

    def get_by_estatus(self, db: Session, estatus_limpieza_id: int):
        """Obtiene limpiezas por estatus"""
        return db.query(Limpieza).filter(
            Limpieza.estatus_limpieza_id == estatus_limpieza_id
        ).all()

    def get_by_rango_fecha(self, db: Session, inicio: datetime, fin: datetime):
        """Obtiene limpiezas entre dos datetimes, ordenadas por estatus_limpieza_id"""
        return db.query(Limpieza).filter(
            Limpieza.fecha_programada >= inicio,
            Limpieza.fecha_programada <= fin,
            Limpieza.estatus_limpieza_id != 4
        ).order_by(
            asc(Limpieza.estatus_limpieza_id)
        ).all()