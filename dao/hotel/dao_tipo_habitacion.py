"""
DAO (Data Access Object) para operaciones CRUD de TipoHabitacion
Maneja todas las interacciones con la base de datos para la entidad TipoHabitacion
"""

from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from models.hotel.tipo_habitacion_model import TipoHabitacion
from schemas.hotel.tipo_habitacion_schemas import TipoHabitacionCreate, TipoHabitacionUpdate


class TipoHabitacionDAO:
    __status_active__ = 1
    __status_inactive__ = 0
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create(self, tipo_habitacion_data: TipoHabitacionCreate) -> TipoHabitacion:
        try:
            db_tipo_habitacion = TipoHabitacion(
                clave=tipo_habitacion_data.clave,
                tipo_habitacion=tipo_habitacion_data.tipo_habitacion,
                estatus_id=tipo_habitacion_data.estatus_id or self.__status_active__,
                precio_unitario=Decimal(tipo_habitacion_data.precio_unitario),
                periodicidad_id=tipo_habitacion_data.periodicidad_id
            )
            self.db.add(db_tipo_habitacion)
            self.db.commit()
            self.db.refresh(db_tipo_habitacion)
            return db_tipo_habitacion
        except SQLAlchemyError as e:
            self.db.rollback()
            # Levanta error con detalle para debug
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear tipo de habitación: {str(e)}"
            )
    
    def get_by_id(self, id_tipoHabitacion: int) -> Optional[TipoHabitacion]:
        try:
            return self.db.query(TipoHabitacion).filter(
                TipoHabitacion.id_tipoHabitacion == id_tipoHabitacion
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_clave(self, clave: str) -> Optional[TipoHabitacion]:
        try:
            return self.db.query(TipoHabitacion).filter(
                TipoHabitacion.clave == clave
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_nombre(self, tipo_habitacion: str) -> Optional[TipoHabitacion]:
        try:
            return self.db.query(TipoHabitacion).filter(
                TipoHabitacion.tipo_habitacion == tipo_habitacion
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[TipoHabitacion]:
        try:
            return (
                self.db.query(TipoHabitacion)
                .order_by(TipoHabitacion.id_tipoHabitacion.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_active_tipos_habitacion(self, skip: int = 0, limit: int = 100) -> List[TipoHabitacion]:
        try:
            return (
                self.db.query(TipoHabitacion)
                .filter(TipoHabitacion.estatus_id == self.__status_active__)
                .order_by(TipoHabitacion.id_tipoHabitacion.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def update(self, id_tipoHabitacion: int, tipo_habitacion_data: TipoHabitacionUpdate) -> Optional[TipoHabitacion]:
        try:
            db_tipo_habitacion = self.get_by_id(id_tipoHabitacion)
            if not db_tipo_habitacion:
                return None
            
            update_data = tipo_habitacion_data.dict(exclude_unset=True)
            # Convertir precio_unitario a Decimal si existe
            if "precio_unitario" in update_data:
                update_data["precio_unitario"] = Decimal(update_data["precio_unitario"])
            
            for field, value in update_data.items():
                setattr(db_tipo_habitacion, field, value)
            
            self.db.commit()
            self.db.refresh(db_tipo_habitacion)
            return db_tipo_habitacion
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete_logical(self, id_tipoHabitacion: int) -> bool:
        try:
            db_tipo_habitacion = self.get_by_id(id_tipoHabitacion)
            if not db_tipo_habitacion:
                return False
            db_tipo_habitacion.estatus_id = self.__status_inactive__
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def reactivate(self, id_tipoHabitacion: int) -> bool:
        try:
            db_tipo_habitacion = self.get_by_id(id_tipoHabitacion)
            if not db_tipo_habitacion:
                return False
            db_tipo_habitacion.estatus_id = self.__status_active__
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists_by_clave(self, clave: str, exclude_id: Optional[int] = None) -> bool:
        try:
            query = self.db.query(TipoHabitacion).filter(TipoHabitacion.clave == clave)
            if exclude_id:
                query = query.filter(TipoHabitacion.id_tipoHabitacion != exclude_id)
            return query.first() is not None
        except SQLAlchemyError as e:
            raise e
    
    def exists_by_nombre(self, tipo_habitacion: str, exclude_id: Optional[int] = None) -> bool:
        try:
            query = self.db.query(TipoHabitacion).filter(TipoHabitacion.tipo_habitacion == tipo_habitacion)
            if exclude_id:
                query = query.filter(TipoHabitacion.id_tipoHabitacion != exclude_id)
            return query.first() is not None
        except SQLAlchemyError as e:
            raise e
