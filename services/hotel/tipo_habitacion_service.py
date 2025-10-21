from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from dao.hotel.dao_tipo_habitacion import TipoHabitacionDAO
from models.hotel.tipo_habitacion_model import TipoHabitacion
from schemas.hotel.tipo_habitacion_schemas import (
    TipoHabitacionCreate,
    TipoHabitacionUpdate,
    TipoHabitacionResponse,
    PeriodicidadResponse
)


class TipoHabitacionService:
    """
    Servicio para manejar la lógica de negocio de tipos de habitación
    """

    def __init__(self, db_session: Session):
        self.db = db_session
        self.dao = TipoHabitacionDAO(db_session)

    def create_tipo_habitacion(self, tipo_habitacion_data: TipoHabitacionCreate) -> TipoHabitacionResponse:
        # Verificar clave
        if tipo_habitacion_data.clave and self.dao.exists_by_clave(tipo_habitacion_data.clave):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="La clave del tipo de habitación ya está en uso")

        # Verificar nombre
        if self.dao.exists_by_nombre(tipo_habitacion_data.tipo_habitacion):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="El nombre del tipo de habitación ya está en uso")

        db_tipo = self.dao.create(tipo_habitacion_data)

        return TipoHabitacionResponse.from_orm(db_tipo)

    def get_tipo_habitacion_by_id(self, id_tipoHabitacion: int) -> Optional[TipoHabitacionResponse]:
        db_tipo = self.dao.get_by_id(id_tipoHabitacion)
        if not db_tipo:
            return None
        return TipoHabitacionResponse.from_orm(db_tipo)

    def get_tipo_habitacion_by_clave(self, clave: str) -> Optional[TipoHabitacionResponse]:
        db_tipo = self.dao.get_by_clave(clave)
        if not db_tipo:
            return None
        return TipoHabitacionResponse.from_orm(db_tipo)

    def get_tipo_habitacion_by_nombre(self, tipo_habitacion: str) -> Optional[TipoHabitacionResponse]:
        db_tipo = self.dao.get_by_nombre(tipo_habitacion)
        if not db_tipo:
            return None
        return TipoHabitacionResponse.from_orm(db_tipo)

    def get_all_tipos_habitacion(self, skip: int = 0, limit: int = 100) -> List[TipoHabitacionResponse]:
        db_tipos = (
            self.db.query(TipoHabitacion)
            .options(joinedload(TipoHabitacion.periodicidad))  # 👈 Cargar relación
            .filter(TipoHabitacion.estatus_id == 1)
            .order_by(TipoHabitacion.id_tipoHabitacion.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [TipoHabitacionResponse.from_orm(t) for t in db_tipos]

    def update_tipo_habitacion(self, id_tipoHabitacion: int, tipo_habitacion_data: TipoHabitacionUpdate) -> Optional[TipoHabitacionResponse]:
        existing_tipo = self.dao.get_by_id(id_tipoHabitacion)
        if not existing_tipo:
            return None

        # Validar conflictos de clave
        if tipo_habitacion_data.clave and tipo_habitacion_data.clave != existing_tipo.clave:
            if self.dao.exists_by_clave(tipo_habitacion_data.clave, exclude_id=id_tipoHabitacion):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="La clave del tipo de habitación ya está en uso")

        # Validar conflictos de nombre
        if tipo_habitacion_data.tipo_habitacion and tipo_habitacion_data.tipo_habitacion != existing_tipo.tipo_habitacion:
            if self.dao.exists_by_nombre(tipo_habitacion_data.tipo_habitacion, exclude_id=id_tipoHabitacion):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="El nombre del tipo de habitación ya está en uso")

        db_tipo = self.dao.update(id_tipoHabitacion, tipo_habitacion_data)
        if not db_tipo:
            return None

        return TipoHabitacionResponse.from_orm(db_tipo)

    def delete_tipo_habitacion(self, id_tipoHabitacion: int) -> bool:
        return self.dao.delete_logical(id_tipoHabitacion)

    def reactivate_tipo_habitacion(self, id_tipoHabitacion: int) -> bool:
        return self.dao.reactivate(id_tipoHabitacion)
