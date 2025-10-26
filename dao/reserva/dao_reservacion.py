from sqlalchemy.orm import Session
from models.reserva.reservaciones_model import Reservacion

class ReservacionDao:
    def get_all(self, db: Session):
        """Obtiene todas las reservaciones"""
        return db.query(Reservacion).all()

    def get_by_id(self, db: Session, id_reservacion: int):
        """Obtiene una reservación por ID"""
        return db.query(Reservacion).filter(Reservacion.id_reservacion == id_reservacion).first()

    def create(self, db: Session, reservacion: Reservacion):
        """Crea una nueva reservación"""
        db.add(reservacion)
        db.commit()
        db.refresh(reservacion)
        return reservacion

    def update(self, db: Session, reservacion: Reservacion):
        """Actualiza una reservación existente"""
        db.commit()
        db.refresh(reservacion)
        return reservacion

    def delete(self, db: Session, id_reservacion: int):
        """Eliminación lógica de una reservación"""
        reservacion = db.query(Reservacion).filter(Reservacion.id_reservacion == id_reservacion).first()
        if not reservacion:
            return None

        # eliminación lógica → cambia el estatus
        reservacion.id_estatus = 0  
        db.commit()
        db.refresh(reservacion)
        return reservacion
