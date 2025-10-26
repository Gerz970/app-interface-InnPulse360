from sqlalchemy.orm import Session
from dao.reserva.dao_reservacion import ReservacionDao
from models.reserva.reservaciones_model import Reservacion
from schemas.reserva.reservacion_schema import ReservacionCreate, ReservacionUpdate
from datetime import datetime
from typing import List

class ReservacionService:
    def __init__(self):
        self.dao = ReservacionDao()

    def listar_reservaciones(self, db: Session):
        return self.dao.get_all(db)

    def obtener_reservacion(self, db: Session, id_reservacion: int):
        return self.dao.get_by_id(db, id_reservacion)

    def obtener_por_cliente(self, db: Session, id_cliente: int) -> List[Reservacion]:
        return self.dao.get_by_cliente(db, id_cliente)

    def obtener_por_habitacion(self, db: Session, habitacion_area_id: int) -> List[Reservacion]:
        return self.dao.get_by_habitacion(db, habitacion_area_id)

    def obtener_por_fechas(self, db: Session, fecha_inicio: datetime, fecha_fin: datetime) -> List[Reservacion]:
        return self.dao.get_by_fechas(db, fecha_inicio, fecha_fin)

    def crear_reservacion(self, db: Session, reservacion_data: ReservacionCreate):
        nueva_reservacion = Reservacion(**reservacion_data.dict())
        return self.dao.create(db, nueva_reservacion)

    def actualizar_reservacion(self, db: Session, id_reservacion: int, reservacion_data: ReservacionUpdate):
        reservacion = self.dao.get_by_id(db, id_reservacion)
        if not reservacion:
            return None
        for key, value in reservacion_data.dict(exclude_unset=True).items():
            setattr(reservacion, key, value)
        return self.dao.update(db, reservacion)

    def eliminar_reservacion(self, db: Session, id_reservacion: int):
        return self.dao.delete(db, id_reservacion)
