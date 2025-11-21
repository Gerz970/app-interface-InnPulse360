from sqlalchemy.orm import Session
from models.reserva.reservaciones_model import Reservacion
from models.hotel.habitacionArea_model import HabitacionArea
from datetime import datetime
from typing import List
from sqlalchemy import cast, Date
from models.camarista.limpieza_model import Limpieza
from dao.camarista.dao_limpieza import LimpiezaDao

class ReservacionDao:
    def get_all(self, db: Session):
        """Obtiene todas las reservaciones"""
        return db.query(Reservacion).filter(Reservacion.id_estatus == 1).all()

    def get_by_id(self, db: Session, id_reservacion: int):
        """Obtiene una reservación por ID"""
        return db.query(Reservacion).filter(Reservacion.id_reservacion == id_reservacion).first()
    
    def get_by_cliente(self, db: Session, id_cliente: int)-> List[Reservacion]:
        return db.query(Reservacion).filter(
            Reservacion.cliente_id == id_cliente,
            Reservacion.id_estatus == 1
        ).all()

    def get_by_habitacion(self, db: Session, habitacion_area_id: int) -> List[Reservacion]:
        return db.query(Reservacion).filter(
            Reservacion.habitacion_area_id == habitacion_area_id,
            Reservacion.id_estatus == 1
        ).all()

    def get_by_fechas(self, db: Session, fecha_inicio: datetime, fecha_fin: datetime):
        return db.query(Reservacion).filter(
            cast(Reservacion.fecha_reserva, Date) >= fecha_inicio.date(),
            cast(Reservacion.fecha_salida, Date) <= fecha_fin.date(),
            Reservacion.id_estatus == 1
        ).all()
    
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

    def get_habitaciones_reservadas_por_cliente(self, db: Session, id_cliente: int) -> List[tuple]:
        """Obtiene las habitaciones que alguna vez fueron reservadas por un cliente (id_estatus <> 2)"""
        resultado = db.query(
            HabitacionArea.id_habitacion_area,
            HabitacionArea.nombre_clave
        ).join(
            Reservacion, HabitacionArea.id_habitacion_area == Reservacion.habitacion_area_id
        ).filter(
            Reservacion.id_estatus != 2,
            Reservacion.cliente_id == id_cliente
        ).distinct().all()

        return resultado
    
    def checkout(self, db: Session, id_reservacion):
        reserva = db.query(Reservacion).filter(
            Reservacion.id_reservacion == id_reservacion,
            Reservacion.id_estatus == 1 # ACTIVA 
        ).first()

        if not reserva:
            return False
        
        # Le cambia el estatus a 2: FINALIZADA
        reserva.id_estatus = 2
        reserva.fecha_salida = datetime.now()  

        db.commit()
        db.refresh(reserva)

        # se crea en automático una limpieza
        limpieza = Limpieza(
            habitacion_area_id = reserva.habitacion_area_id,
            descripcion = "La habitación ha sido desocupada. Favor de realizar limpieza.",
            fecha_programada = datetime.now(),
            tipo_limpieza_id = 1,
            estatus_limpieza_id = 1
        )
        dao_limpieza = LimpiezaDao()
        dao_limpieza.create(db, limpieza)
        db.add(limpieza)
        db.commit()
        db.refresh(limpieza)

        return True


