"""
Servicio de TipoHabitacion
Maneja la lógica de negocio para tipos de habitación
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from dao.dao_tipo_habitacion import TipoHabitacionDAO
from models.hotel.tipo_habitacion_model import TipoHabitacion
from schemas.hotel.tipo_habitacion_schemas import TipoHabitacionCreate, TipoHabitacionUpdate, TipoHabitacionResponse


class TipoHabitacionService:
    """
    Servicio para manejar la lógica de negocio de tipos de habitación
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.dao = TipoHabitacionDAO(db_session)
    
    def create_tipo_habitacion(self, tipo_habitacion_data: TipoHabitacionCreate) -> TipoHabitacionResponse:
        """
        Crea un nuevo tipo de habitación
        
        Args:
            tipo_habitacion_data (TipoHabitacionCreate): Datos del tipo de habitación
            
        Returns:
            TipoHabitacionResponse: Tipo de habitación creado
            
        Raises:
            HTTPException: Si la clave o nombre ya existen
        """
        # Verificar si la clave ya existe (si se proporciona)
        if tipo_habitacion_data.clave and self.dao.exists_by_clave(tipo_habitacion_data.clave):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La clave del tipo de habitación ya está en uso"
            )
        
        # Verificar si el nombre ya existe
        if self.dao.exists_by_nombre(tipo_habitacion_data.tipo_habitacion):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del tipo de habitación ya está en uso"
            )
        
        # Crear el tipo de habitación
        db_tipo_habitacion = self.dao.create(tipo_habitacion_data)
        
        return TipoHabitacionResponse(
            id_tipoHabitacion=db_tipo_habitacion.id_tipoHabitacion,
            clave=db_tipo_habitacion.clave,
            tipo_habitacion=db_tipo_habitacion.tipo_habitacion,
            estatus_id=db_tipo_habitacion.estatus_id
        )
    
    def get_tipo_habitacion_by_id(self, id_tipoHabitacion: int) -> Optional[TipoHabitacionResponse]:
        """
        Obtiene un tipo de habitación por ID
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación
            
        Returns:
            Optional[TipoHabitacionResponse]: Tipo de habitación encontrado o None
        """
        db_tipo_habitacion = self.dao.get_by_id(id_tipoHabitacion)
        if not db_tipo_habitacion:
            return None
        
        return TipoHabitacionResponse(
            id_tipoHabitacion=db_tipo_habitacion.id_tipoHabitacion,
            clave=db_tipo_habitacion.clave,
            tipo_habitacion=db_tipo_habitacion.tipo_habitacion,
            estatus_id=db_tipo_habitacion.estatus_id
        )
    
    def get_tipo_habitacion_by_clave(self, clave: str) -> Optional[TipoHabitacionResponse]:
        """
        Obtiene un tipo de habitación por clave
        
        Args:
            clave (str): Clave del tipo de habitación
            
        Returns:
            Optional[TipoHabitacionResponse]: Tipo de habitación encontrado o None
        """
        db_tipo_habitacion = self.dao.get_by_clave(clave)
        if not db_tipo_habitacion:
            return None
        
        return TipoHabitacionResponse(
            id_tipoHabitacion=db_tipo_habitacion.id_tipoHabitacion,
            clave=db_tipo_habitacion.clave,
            tipo_habitacion=db_tipo_habitacion.tipo_habitacion,
            estatus_id=db_tipo_habitacion.estatus_id
        )
    
    def get_tipo_habitacion_by_nombre(self, tipo_habitacion: str) -> Optional[TipoHabitacionResponse]:
        """
        Obtiene un tipo de habitación por nombre
        
        Args:
            tipo_habitacion (str): Nombre del tipo de habitación
            
        Returns:
            Optional[TipoHabitacionResponse]: Tipo de habitación encontrado o None
        """
        db_tipo_habitacion = self.dao.get_by_nombre(tipo_habitacion)
        if not db_tipo_habitacion:
            return None
        
        return TipoHabitacionResponse(
            id_tipoHabitacion=db_tipo_habitacion.id_tipoHabitacion,
            clave=db_tipo_habitacion.clave,
            tipo_habitacion=db_tipo_habitacion.tipo_habitacion,
            estatus_id=db_tipo_habitacion.estatus_id
        )
    
    def get_all_tipos_habitacion(self, skip: int = 0, limit: int = 100) -> List[TipoHabitacionResponse]:
        """
        Obtiene una lista de tipos de habitación
        
        Args:
            skip (int): Registros a saltar
            limit (int): Límite de registros
            
        Returns:
            List[TipoHabitacionResponse]: Lista de tipos de habitación
        """
        db_tipos_habitacion = self.dao.get_active_tipos_habitacion(skip, limit)
        return [
            TipoHabitacionResponse(
                id_tipoHabitacion=tipo.id_tipoHabitacion,
                clave=tipo.clave,
                tipo_habitacion=tipo.tipo_habitacion,
                estatus_id=tipo.estatus_id
            )
            for tipo in db_tipos_habitacion
        ]
    
    def update_tipo_habitacion(self, id_tipoHabitacion: int, tipo_habitacion_data: TipoHabitacionUpdate) -> Optional[TipoHabitacionResponse]:
        """
        Actualiza un tipo de habitación existente
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación
            tipo_habitacion_data (TipoHabitacionUpdate): Datos a actualizar
            
        Returns:
            Optional[TipoHabitacionResponse]: Tipo de habitación actualizado o None
            
        Raises:
            HTTPException: Si hay conflictos de clave o nombre
        """
        # Verificar si el tipo de habitación existe
        existing_tipo = self.dao.get_by_id(id_tipoHabitacion)
        if not existing_tipo:
            return None
        
        # Verificar conflictos de clave si se está actualizando
        if tipo_habitacion_data.clave and tipo_habitacion_data.clave != existing_tipo.clave:
            if self.dao.exists_by_clave(tipo_habitacion_data.clave, exclude_id=id_tipoHabitacion):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La clave del tipo de habitación ya está en uso"
                )
        
        # Verificar conflictos de nombre si se está actualizando
        if tipo_habitacion_data.tipo_habitacion and tipo_habitacion_data.tipo_habitacion != existing_tipo.tipo_habitacion:
            if self.dao.exists_by_nombre(tipo_habitacion_data.tipo_habitacion, exclude_id=id_tipoHabitacion):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre del tipo de habitación ya está en uso"
                )
        
        # Actualizar el tipo de habitación
        db_tipo_habitacion = self.dao.update(id_tipoHabitacion, tipo_habitacion_data)
        if not db_tipo_habitacion:
            return None
        
        return TipoHabitacionResponse(
            id_tipoHabitacion=db_tipo_habitacion.id_tipoHabitacion,
            clave=db_tipo_habitacion.clave,
            tipo_habitacion=db_tipo_habitacion.tipo_habitacion,
            estatus_id=db_tipo_habitacion.estatus_id
        )
    
    def delete_tipo_habitacion(self, id_tipoHabitacion: int) -> bool:
        """
        Eliminación lógica de un tipo de habitación
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return self.dao.delete_logical(id_tipoHabitacion)
    
    def reactivate_tipo_habitacion(self, id_tipoHabitacion: int) -> bool:
        """
        Reactiva un tipo de habitación
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación
            
        Returns:
            bool: True si se reactivó correctamente
        """
        return self.dao.reactivate(id_tipoHabitacion)
