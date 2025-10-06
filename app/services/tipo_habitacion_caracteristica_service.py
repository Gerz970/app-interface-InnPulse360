"""
Servicio para gestión de asignación de características a tipos de habitación
Maneja la lógica de negocio para la relación TipoHabitacion-Caracteristica
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from dao.dao_tipo_habitacion_caracteristica import TipoHabitacionCaracteristicaDAO
from dao.dao_tipo_habitacion import TipoHabitacionDAO
from dao.dao_caracteristica import CaracteristicaDAO
from models.hotel.tipo_habitacion_model import TipoHabitacion
from models.hotel.caracteristica_model import Caracteristica
from models.hotel.tipo_habitacion_caracteristica_model import TipoHabitacionCaracteristica
from schemas.hotel.tipo_habitacion_caracteristica_schemas import (
    TipoHabitacionCaracteristicaAssign, 
    TipoHabitacionCaracteristicaBulkAssign, 
    TipoHabitacionCaracteristicaResponse
)
from schemas.hotel.tipo_habitacion_schemas import TipoHabitacionResponse
from schemas.hotel.caracteristica_schemas import CaracteristicaResponse


class TipoHabitacionCaracteristicaService:
    """
    Servicio para manejar la lógica de negocio de asignación de características
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.tipo_habitacion_caracteristica_dao = TipoHabitacionCaracteristicaDAO(db_session)
        self.tipo_habitacion_dao = TipoHabitacionDAO(db_session)
        self.caracteristica_dao = CaracteristicaDAO(db_session)
    
    def assign_caracteristica_to_tipo_habitacion(self, tipo_habitacion_id: int, caracteristica_id: int) -> bool:
        """
        Asigna una característica a un tipo de habitación
        
        Args:
            tipo_habitacion_id (int): ID del tipo de habitación
            caracteristica_id (int): ID de la característica
            
        Returns:
            bool: True si se asignó correctamente
            
        Raises:
            HTTPException: Si el tipo de habitación o característica no existen
        """
        # Verificar que el tipo de habitación existe y está activo
        tipo_habitacion = self.tipo_habitacion_dao.get_by_id(tipo_habitacion_id)
        if not tipo_habitacion or tipo_habitacion.estatus_id != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de habitación no encontrado o inactivo"
            )
        
        # Verificar que la característica existe
        caracteristica = self.caracteristica_dao.get_by_id(caracteristica_id)
        if not caracteristica:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Característica no encontrada"
            )
        
        # Asignar la característica
        success = self.tipo_habitacion_caracteristica_dao.assign_caracteristica_to_tipo_habitacion(
            tipo_habitacion_id, caracteristica_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El tipo de habitación ya tiene asignada esta característica"
            )
        
        return True
    
    def remove_caracteristica_from_tipo_habitacion(self, tipo_habitacion_id: int, caracteristica_id: int) -> bool:
        """
        Remueve una característica de un tipo de habitación
        
        Args:
            tipo_habitacion_id (int): ID del tipo de habitación
            caracteristica_id (int): ID de la característica
            
        Returns:
            bool: True si se removió correctamente
            
        Raises:
            HTTPException: Si el tipo de habitación o característica no existen
        """
        # Verificar que el tipo de habitación existe
        tipo_habitacion = self.tipo_habitacion_dao.get_by_id(tipo_habitacion_id)
        if not tipo_habitacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de habitación no encontrado"
            )
        
        # Verificar que la característica existe
        caracteristica = self.caracteristica_dao.get_by_id(caracteristica_id)
        if not caracteristica:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Característica no encontrada"
            )
        
        # Remover la característica
        success = self.tipo_habitacion_caracteristica_dao.remove_caracteristica_from_tipo_habitacion(
            tipo_habitacion_id, caracteristica_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El tipo de habitación no tiene asignada esta característica"
            )
        
        return True
    
    def get_caracteristicas_by_tipo_habitacion(self, tipo_habitacion_id: int) -> List[CaracteristicaResponse]:
        """
        Obtiene las características de un tipo de habitación
        
        Args:
            tipo_habitacion_id (int): ID del tipo de habitación
            
        Returns:
            List[CaracteristicaResponse]: Lista de características del tipo de habitación
            
        Raises:
            HTTPException: Si el tipo de habitación no existe
        """
        # Verificar que el tipo de habitación existe
        tipo_habitacion = self.tipo_habitacion_dao.get_by_id(tipo_habitacion_id)
        if not tipo_habitacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de habitación no encontrado"
            )
        
        # Obtener características
        caracteristicas = self.tipo_habitacion_caracteristica_dao.get_caracteristicas_by_tipo_habitacion(tipo_habitacion_id)
        
        return [
            CaracteristicaResponse(
                id_caracteristica=caracteristica.id_caracteristica,
                caracteristica=caracteristica.caracteristica,
                descripcion=caracteristica.descripcion
            )
            for caracteristica in caracteristicas
        ]
    
    def get_tipos_habitacion_by_caracteristica(self, caracteristica_id: int) -> List[TipoHabitacionResponse]:
        """
        Obtiene los tipos de habitación que tienen una característica específica
        
        Args:
            caracteristica_id (int): ID de la característica
            
        Returns:
            List[TipoHabitacionResponse]: Lista de tipos de habitación con la característica
            
        Raises:
            HTTPException: Si la característica no existe
        """
        # Verificar que la característica existe
        caracteristica = self.caracteristica_dao.get_by_id(caracteristica_id)
        if not caracteristica:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Característica no encontrada"
            )
        
        # Obtener tipos de habitación
        tipos_habitacion = self.tipo_habitacion_caracteristica_dao.get_tipos_habitacion_by_caracteristica(caracteristica_id)
        
        return [
            TipoHabitacionResponse(
                id_tipoHabitacion=tipo.id_tipoHabitacion,
                clave=tipo.clave,
                tipo_habitacion=tipo.tipo_habitacion,
                estatus_id=tipo.estatus_id
            )
            for tipo in tipos_habitacion
        ]
    
    def bulk_assign_caracteristicas_to_tipo_habitacion(self, tipo_habitacion_id: int, caracteristicas_ids: List[int]) -> int:
        """
        Asigna múltiples características a un tipo de habitación
        
        Args:
            tipo_habitacion_id (int): ID del tipo de habitación
            caracteristicas_ids (List[int]): Lista de IDs de características
            
        Returns:
            int: Número de características asignadas exitosamente
            
        Raises:
            HTTPException: Si el tipo de habitación no existe o alguna característica no existe
        """
        # Verificar que el tipo de habitación existe y está activo
        tipo_habitacion = self.tipo_habitacion_dao.get_by_id(tipo_habitacion_id)
        if not tipo_habitacion or tipo_habitacion.estatus_id != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de habitación no encontrado o inactivo"
            )
        
        # Verificar que todas las características existen
        for caracteristica_id in caracteristicas_ids:
            caracteristica = self.caracteristica_dao.get_by_id(caracteristica_id)
            if not caracteristica:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Característica con ID {caracteristica_id} no encontrada"
                )
        
        # Asignar características
        assigned_count = self.tipo_habitacion_caracteristica_dao.bulk_assign_caracteristicas_to_tipo_habitacion(
            tipo_habitacion_id, caracteristicas_ids
        )
        
        return assigned_count
    
    def bulk_remove_caracteristicas_from_tipo_habitacion(self, tipo_habitacion_id: int, caracteristicas_ids: List[int]) -> int:
        """
        Remueve múltiples características de un tipo de habitación
        
        Args:
            tipo_habitacion_id (int): ID del tipo de habitación
            caracteristicas_ids (List[int]): Lista de IDs de características
            
        Returns:
            int: Número de características removidas exitosamente
            
        Raises:
            HTTPException: Si el tipo de habitación no existe
        """
        # Verificar que el tipo de habitación existe
        tipo_habitacion = self.tipo_habitacion_dao.get_by_id(tipo_habitacion_id)
        if not tipo_habitacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de habitación no encontrado"
            )
        
        # Remover características
        removed_count = self.tipo_habitacion_caracteristica_dao.bulk_remove_caracteristicas_from_tipo_habitacion(
            tipo_habitacion_id, caracteristicas_ids
        )
        
        return removed_count
